"""Local EXAONE 3.5 adapter for the EXISTING two-tool/five-symptom skin task.

No API, SLM, Qwen, training, product/time database, expected labels, or scripted
action correction. Tool handlers and state validation are the original ones.
"""
import atexit
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import subprocess
import threading
import time
import uuid

import requests
from demo.skin_tools import SkinSession
from agent.live_tool_agent import ToolRegistry
from agent.contract_filter_v34 import readiness
from agent.symptom_state_v1 import SYMPTOMS
from demo.cosmetics_reply import SYSTEM as REPLY_SYSTEM

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/exaone35-cosmetics-v1'
MODEL = ROOT / 'models/exaone-3.5-2.4b-instruct-q4'
CONTEXT = 8192
MAX_NEW = 512

SELECT_SYSTEM = '''한국어 피부 기록 프로그램의 다음 동작 하나를 선택하세요.
출력은 {"action":"record"}처럼 action 키 하나를 가진 JSON 객체만 사용하세요.
가능한 값은 제공된 available_actions에 있는 record, show, ask, none입니다.
record: 사용자 본인이 지금 있다고/없다고 명시하거나 정정한 다섯 피부 증상을 기록. 다른 사람, 가정, 일반 질문은 기록하지 않음.
show: 사용자가 이미 저장된 피부 기록을 보고 싶을 때 실제 기록을 조회.
ask: 기록에 필요한 의미가 불분명하거나 사용자가 지원하지 않는 실행을 요청하여 설명/확인이 필요함.
none: 실행할 도구가 없거나 이번 요청에 필요한 일을 이미 끝냄.
제품명, 사용 시각, 검색, 예약, 알람, 이메일은 이 프로그램에서 저장하거나 실행할 수 없음.
actual_events는 실제 실행 결과이며, 제안이나 계획이 아닙니다. 성공한 일을 반복하지 마세요.
읽기만 요청했으면 읽은 뒤 none. 기록만 요청했으면 기록한 뒤 none.
기록 후 조회를 요청했으면 record 다음 show. 변경 전 기록을 본 뒤 저장을 요청했으면 show 다음 record.
이번 요청의 필요한 동작을 모두 했으면 none. 없는 도구를 선택하지 마세요.
현재 상태는 지금까지 저장된 내용이지 사용자의 새 증상이 아닙니다. 새 증상은 이번 발화와 실제 최근 대화로 판단하세요.'''

SYMPTOM_SYSTEM = '''이번 한국어 발화가 사용자 본인의 현재 피부 상태에 대해 명시한 내용만 판정하세요.
dryness(건조함), breakout(뾰루지), redness(붉어짐), stinging(따가움), itching(가려움)의 다섯 키를 모두 가진 JSON 객체만 출력하세요.
각 값은 present, absent, unknown, unchanged 중 하나입니다.
present: 지금 본인에게 있다고 말함. absent: 지금 본인에게 없거나 사라졌다고 명시함.
unknown: 해당 증상이 있는지 모르겠다고 명시하여 불확실 상태로 바꿈.
unchanged: 이번 발화에서 해당 증상을 말하지 않았거나, 다른 사람/가정/일반 질문/제품 사용만 말함.
말하지 않은 증상을 absent나 unknown으로 초기화하지 마세요. 여러 증상을 말하면 각각 판단하세요.
정정은 최신 명시 내용을 따르세요. 제품명이나 사용 시각을 피부 증상으로 만들지 마세요.
출력 예시는 형식 설명이지 정답이 아닙니다. JSON의 키나 값을 추가하지 마세요.'''


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(2**20), b''):
            h.update(block)
    return h.hexdigest()


def strict_object(text):
    text = text.strip()
    fence = re.fullmatch(r'```(?:json)?[ \t]*\r?\n(.*?)\r?\n```', text, flags=re.S | re.I)
    if fence:
        text = fence.group(1)
    def pairs(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise ValueError('Duplicate JSON key')
            obj[key] = value
        return obj
    def invalid(value):
        raise ValueError('Non-JSON constant')
    value = json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)
    if not isinstance(value, dict):
        raise ValueError('JSON object required')
    return value


def render(messages):
    return ''.join('[|' + m['role'] + '|]' + m['content'] +
                   ('\n' if m['role'] == 'user' else '[|endofturn|]\n')
                   for m in messages) + '[|assistant|]'


class LocalExaone35:
    def __init__(self, log_dir=None):
        self.log_dir = Path(log_dir or OUT / 'live')
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.process = None
        self.lock = threading.Lock()
        self.config = {'structured_decoding': True, 'roles': {'tool_choice': 'EXAONE-3.5-2.4B',
                       'symptom_extraction': 'EXAONE-3.5-2.4B', 'reply': 'EXAONE-3.5-2.4B'}}

    def start(self):
        manifest = json.loads((MODEL / 'manifest.json').read_text(encoding='utf-8'))
        weight = MODEL / manifest['filename']
        if sha(weight) != manifest['sha256']:
            raise ValueError('EXAONE model hash differs')
        engines = sorted((Path(os.environ['APPDATA']) / 'Jan/data/llamacpp/backends').glob('*/win-cuda*/build/bin/llama-server.exe'))
        if not engines:
            raise RuntimeError('Local CUDA llama-server not found')
        engine = engines[-1]
        with socket.socket() as probe:
            probe.bind(('127.0.0.1', 0))
            port = probe.getsockname()[1]
        self.url = f'http://127.0.0.1:{port}'
        args = [str(engine), '-m', str(weight), '--alias', 'exaone35-cosmetics',
                '--host', '127.0.0.1', '--port', str(port), '-c', str(CONTEXT), '-np', '1',
                '-ngl', 'all', '-b', '512', '-ub', '128', '--threads', '8',
                '--cache-ram', '0', '--no-webui']
        self.stdout = (self.log_dir / 'server.stdout.log').open('a', encoding='utf-8')
        self.stderr = (self.log_dir / 'server.stderr.log').open('a', encoding='utf-8')
        self.process = subprocess.Popen(args, cwd=ROOT, stdout=self.stdout, stderr=self.stderr,
                        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        atexit.register(self.close)
        info = {'pid': self.process.pid, 'url': self.url, 'argv': args,
                'model': manifest, 'engine_sha256': sha(engine), 'training': False,
                'structured_decoding': True,
                'task': 'Existing five symptoms, two empty-argument tools; no product/time storage'}
        (self.log_dir / 'runtime.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
        for _ in range(90):
            if self.process.poll() is not None:
                raise RuntimeError('EXAONE process exited; see local server.stderr.log')
            try:
                if requests.get(self.url + '/health', timeout=2).status_code == 200:
                    return self
            except requests.RequestException:
                pass
            time.sleep(1)
        self.close()
        raise TimeoutError('EXAONE startup timed out')

    def close(self):
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)
        for stream in [getattr(self, 'stdout', None), getattr(self, 'stderr', None)]:
            if stream and not stream.closed:
                stream.close()

    def generate(self, role, system, facts, history=None):
        messages = [{'role': 'system', 'content': system}]
        if history:
            messages.extend(copy.deepcopy(history))
        messages.append({'role': 'user', 'content': json.dumps(facts, ensure_ascii=False, separators=(',', ':'))})
        prompt = render(messages)
        with self.lock:
            response = requests.post(self.url + '/tokenize', json={'content': prompt, 'add_special': True}, timeout=20)
            response.raise_for_status()
            length = len(response.json()['tokens'])
            if length + MAX_NEW > CONTEXT:
                raise ValueError('Input exceeds local context; no truncation')
            payload = {'prompt': prompt, 'temperature': 0, 'seed': 350035,
                       'n_predict': MAX_NEW, 'cache_prompt': False, 'stream': False}
            if role == 'select':
                payload['json_schema'] = {'type': 'object',
                    'properties': {'action': {'type': 'string', 'enum': facts['available_actions']}},
                    'required': ['action'], 'additionalProperties': False}
            elif role == 'symptoms':
                payload['json_schema'] = {'type': 'object', 'properties': {
                    k: {'type': 'string', 'enum': ['present', 'absent', 'unknown', 'unchanged']} for k in SYMPTOMS},
                    'required': list(SYMPTOMS), 'additionalProperties': False}
            started = time.perf_counter()
            response = requests.post(self.url + '/completion', json=payload, timeout=120)
            response.raise_for_status()
            raw = response.json()
            call = {'id': uuid.uuid4().hex, 'role': role, 'messages': messages, 'request': payload,
                    'raw_response': raw, 'input_tokens': length, 'seconds': time.perf_counter()-started}
            with (self.log_dir / 'model-calls.jsonl').open('a', encoding='utf-8') as f:
                f.write(json.dumps(call, ensure_ascii=False) + '\n')
            if raw.get('truncated') or raw.get('stop_type') not in ['eos', 'word']:
                raise ValueError('Incomplete model response; no state correction substituted')
            return raw['content']

    def reply(self, text, trace, history):
        recent = [{'role': r['role'], 'content': r['content']} for r in history[-4:]
                  if r.get('role') in ['user', 'assistant']]
        facts = {'이번 사용자 발화': text, '실행된 동작': trace['action'],
                 '이번에 바꾼 값': trace['patch'], '현재 확정된 기록': trace['after'],
                 '실제 도구 실행 이력': trace['events'], '현재 사용 가능한 도구': trace['available_tools'],
                 '중단 이유': trace['stop_reason']}
        return self.generate('reply', REPLY_SYSTEM, facts, recent).strip()

    def answer(self, text, trace, history):
        """Do not display a model's success claim after an observed execution error."""
        if trace['stop_reason'] not in ['model_stop', 'model_ask', 'single_action', 'no_tool_chosen']:
            return observed_status_reply(trace, incomplete=True), 'execution_status'
        try:
            return self.reply(text, trace, history), 'exaone35'
        except Exception:
            return observed_status_reply(trace, incomplete=False), 'execution_status'


def observed_status_reply(trace, incomplete):
    names = {'dryness': '건조함', 'breakout': '뾰루지', 'redness': '붉어짐', 'stinging': '따가움', 'itching': '가려움'}
    values = {'present': '있음', 'absent': '없음', 'unknown': '모름'}
    changes = ', '.join(names[k] + ': ' + values[v] for k, v in trace.get('patch', {}).items())
    if changes:
        result = '실제로 저장된 변경은 ' + changes + '입니다.'
    else:
        result = '새로 저장된 변경은 없습니다.'
    return ('이번 요청 전체는 완료하지 못했어요. ' if incomplete else '답변 생성은 완료하지 못했어요. ') + result


class Exaone35SkinSession(SkinSession):
    def __init__(self, client):
        super().__init__(None)
        self.client = client

    def catalog(self, text):
        original = super().catalog(text)
        registry = ToolRegistry()
        def record():
            before = self.record.state
            raw = self.client.generate('symptoms', SYMPTOM_SYSTEM,
                    {'current_state': before, 'current_user_message': text,
                     'recent_actual_turns': self.history[-2:]})
            values = strict_object(raw)
            if set(values) != set(SYMPTOMS) or any(v not in ['present', 'absent', 'unknown', 'unchanged'] for v in values.values()):
                raise ValueError('Invalid symptom decision; no state update')
            self._symptom_decisions = {k: {'choice': v} for k, v in values.items()}
            patch = {k: v for k, v in values.items() if v != 'unchanged' and v != before[k]}
            if not patch:
                return {'ok': False, 'reason': 'no_supported_change', 'state': before, 'version': self.record.version}
            result = self.record.update(patch)
            return {**result, 'done': True, 'patch': patch}
        for definition in original.definitions():
            name = definition['name']
            handler = record if name == 'record_skin_symptoms' else lambda n=name: original.invoke(n, {})
            registry.register(definition, handler)
        return registry

    def turn(self, text, max_steps=4):
        before = self.record.state
        self._symptom_decisions = {}
        registry = self.catalog(text)
        definitions = registry.definitions()
        aliases = {'record_skin_symptoms': 'record', 'read_skin_record': 'show'}
        by_action = {aliases[d['name']]: d for d in definitions}
        allowed = list(by_action) + ['ask', 'none']
        events, steps, seen = [], [], set()
        reason, stopped = 'step_limit', False
        for i in range(max_steps):
            facts = {'current_user_message': text, 'current_state': self.record.state,
                     'recent_actual_turns': self.history[-2:], 'actual_events': copy.deepcopy(events),
                     'available_actions': allowed, 'actual_tool_definitions': definitions}
            try:
                raw = self.client.generate('select', SELECT_SYSTEM, facts)
                chosen = strict_object(raw)
                if set(chosen) != {'action'} or chosen['action'] not in allowed:
                    raise ValueError('Invalid action')
                action = chosen['action']
            except Exception as exc:
                reason = 'input_limit' if 'context' in str(exc).lower() else 'model_output_error'
                steps.append({'index': i, 'decision': {'raw_selected': 'invalid', 'selected': 'no_tool',
                    'reason': reason, 'domain_decision': {'choice': 'invalid'}, 'error': type(exc).__name__}, 'event': None})
                break
            name = by_action[action]['name'] if action in by_action else 'no_tool'
            step = {'index': i, 'decision': {'raw_selected': name, 'selected': name,
                    'reason': 'model_choice', 'domain_decision': {'choice': action}, 'model_output': raw}, 'event': None}
            steps.append(step)
            if action not in by_action:
                reason = 'model_stop' if action == 'none' else 'model_ask'
                stopped = True
                break
            condition = readiness(by_action[action], events)
            step['decision']['condition'] = condition
            if not condition['eligible']:
                step['decision']['selected'] = 'no_tool'
                reason = 'condition_not_met'
                break
            key = (name, self.record.version)
            if key in seen:
                step['decision']['selected'] = 'no_tool'
                reason = 'duplicate_call'
                break
            seen.add(key)
            try:
                result = registry.invoke(name, {})
            except Exception as exc:
                result = {'ok': False, 'reason': 'handler_error', 'effects_unknown': True}
                step['decision']['handler_error'] = type(exc).__name__
            event = {'tool': name, 'arguments': {}, 'executed': True, 'result': result}
            events.append(event)
            step['event'] = copy.deepcopy(event)
            if result.get('ok') is not True:
                reason = 'tool_error'
                break
        after = self.record.state
        patch = {k: v for k, v in after.items() if v != before[k]}
        writes = any(e['tool'] == 'record_skin_symptoms' and e['result'].get('ok') for e in events)
        reads = any(e['tool'] == 'read_skin_record' and e['result'].get('ok') for e in events)
        action = 'record' if writes else 'show' if reads else 'none' if reason == 'model_stop' else 'ask'
        self.history.append({'role': 'user', 'content': text, 'actual_tools': copy.deepcopy(events)})
        self.history = self.history[-2:]
        return {'before': before, 'after': after, 'patch': patch, 'action': action, 'input': text,
                'symptom_decisions': self._symptom_decisions, 'events': events, 'steps': steps,
                'stop_reason': reason, 'model_stopped': stopped, 'complete': False,
                'engine': 'exaone35-loop', 'available_tools': [{'name': d['name'], 'description': d['description']} for d in definitions]}
