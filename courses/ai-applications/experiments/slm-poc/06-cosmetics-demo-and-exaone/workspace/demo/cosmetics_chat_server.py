"""Local minimal Korean skincare chat using a choice model and in-memory state."""
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import traceback
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from demo.chat_models import ChatModels
from demo.skin_tools import SkinSession,DomainSkinSession
from demo.cosmetics_reply import generate_reply,URL as REPLY_URL,MODEL as REPLY_MODEL

PAGE=Path(__file__).with_name('cosmetics_chat.html')
TOKEN=secrets.token_urlsafe(32);LOCK=threading.Lock();SESSIONS={}
STATE={'status':'loading','error':None,'scorer':None,'reply_status':'loading'}
RESEARCH=os.environ.get('SKIN_CHAT_ENGINE','domain')=='research'
LOCAL_EXAONE=os.environ.get('SKIN_CHAT_ENGINE','domain')=='exaone35'
EXAONE_REPLY=LOCAL_EXAONE or os.environ.get('SKIN_CHAT_REPLY_BACKEND','qwen')=='exaone35'
LABELS={'dryness':'건조함','breakout':'뾰루지','redness':'붉어짐','stinging':'따가움','itching':'가려움'}

def engine_name():
    return 'exaone35-loop' if LOCAL_EXAONE else 'research-loop' if RESEARCH else 'domain-single-action'

def new_agent():
    if LOCAL_EXAONE:
        from demo.exaone35_cosmetics import Exaone35SkinSession
        return Exaone35SkinSession(STATE['scorer'])
    return (SkinSession if RESEARCH else DomainSkinSession)(STATE['scorer'].score)

def init_model():
    try:
        if LOCAL_EXAONE:
            from demo.exaone35_cosmetics import LocalExaone35
            models=LocalExaone35().start()
            STATE['reply_backend']=models
            STATE['reply_status']='ready'
        else:models=ChatModels(research=RESEARCH)
        STATE.update(status='ready',scorer=models)
        print('Tool models ready:',json.dumps(models.config['roles'],ensure_ascii=False),flush=True)
    except Exception as exc:
        STATE.update(status='error',error=f'{type(exc).__name__}: {exc}');traceback.print_exc()

def init_reply_model():
    """Reuse the local Qwen service, or start the existing project server."""
    if LOCAL_EXAONE:return
    if EXAONE_REPLY:
        try:
            from demo.exaone35_cosmetics import LocalExaone35
            STATE['reply_backend']=LocalExaone35().start()
            STATE['reply_status']='ready'
        except Exception as exc:
            STATE['reply_status']='unavailable'
            print('Local EXAONE reply startup failed:',type(exc).__name__,flush=True)
        return
    if os.environ.get('SKIN_CHAT_REPLY','').lower()=='off':STATE['reply_status']='unavailable';return
    parsed=urllib.parse.urlsplit(REPLY_URL)
    if parsed.scheme!='http' or parsed.hostname!='127.0.0.1':STATE['reply_status']='unavailable';return
    port=parsed.port or 80;health=urllib.parse.urlunsplit((parsed.scheme,parsed.netloc,'/v1/models','',''))
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def ready():
        try:
            with opener.open(health,timeout=2) as response:
                data=json.load(response)
            return any(m.get('id')==REPLY_MODEL for m in data.get('data',[]))
        except (OSError,ValueError,KeyError):return False
    if not ready():
        try:
            cmd=['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(ROOT/'scripts/start_qwen3.ps1'),'-Port',str(port)]
            subprocess.run(cmd,cwd=str(ROOT),capture_output=True,timeout=30,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0),check=True)
        except (OSError,subprocess.SubprocessError):
            STATE['reply_status']='unavailable';return
        for _ in range(60):
            if ready():break
            time.sleep(1)
    STATE['reply_status']='ready' if ready() else 'unavailable'

def format_state(state):
    present=[LABELS[k] for k,v in state.items() if v=='present']
    absent=[LABELS[k] for k,v in state.items() if v=='absent']
    if not present and not absent:return '아직 기록된 피부 상태가 없어요.'
    lines=[]
    if present:lines.append('지금 있다고 알려주신 증상: '+', '.join(present))
    if absent:lines.append('없다고 알려주신 증상: '+', '.join(absent))
    return '\n'.join(lines)

def reply(trace):
    action=trace['action']
    reason=trace.get('stop_reason')
    suffix='' if reason in ['model_stop','single_action','no_tool_chosen'] else '\n요청 전체의 완료는 확인하지 못했어요.'
    if action=='record':
        if not trace.get('patch'):
            return '어떤 피부 상태를 기록할지 조금 더 자세히 말씀해 주세요.'
        return '말씀하신 피부 상태를 기록했어요.\n'+format_state(trace['after'])+suffix
    if action=='show':return format_state(trace['after'])+suffix
    if action=='tool':return '도구를 실행했어요.'+suffix
    if action=='ask':return '조금 더 자세히 말씀해 주시겠어요?'
    tools={t['name'] for t in trace.get('available_tools',[])}
    names=[label for key,label in [('record_skin_symptoms','피부 증상 기록'),('read_skin_record','기록 확인')] if key in tools]
    return '이번에는 실행한 도구가 없어요. 가능한 기능: '+', '.join(names)+'.' if names else '현재 연결된 도구가 없어요.'

def debug_trace(trace,source):
    """Describe only observed choices and operations, not invented reasoning."""
    action=trace['action']
    patch=trace.get('patch',{})
    if patch:
        operation='state_update'
    elif action=='record':
        operation='no_state_update'
    elif action=='show':
        operation='state_read'
    elif trace.get('events'):
        operation='tool_call'
    else:
        operation='none'
    return {
        'selected_action':action,
        'operation':operation,
        'changes':[
            {'field':k,'before':trace['before'][k],'after':v}
            for k,v in patch.items()
        ],
        'symptom_choices':{k:v['choice'] for k,v in trace.get('symptom_decisions',{}).items()},
        'reply_source':source,
        'stop_reason':trace.get('stop_reason'),
        'model_stopped':trace.get('model_stopped',False),
        'steps':[{'proposed':s['decision']['raw_selected'],'selected':s['decision']['selected'],'reason':s['decision']['reason'],
          'tool':s['event']['tool'] if s['event'] else None,'ok':s['event']['result'].get('ok') if s['event'] else None} for s in trace.get('steps',[])],
        'available_tools':[t['name'] for t in trace.get('available_tools',[])],
        'engine':engine_name(),
        'model_roles':({'tool_choice':'EXAONE-3.5-2.4B','symptom_extraction':'EXAONE-3.5-2.4B','reply':'EXAONE-3.5-2.4B'} if LOCAL_EXAONE else {'tool_choice':'v27-selector','call_decision':'v29-control-gate','symptom_extraction':'cosmetics-step-0100','reply':'EXAONE-3.5-2.4B' if EXAONE_REPLY else 'Qwen'} if RESEARCH else {'tool_choice':'cosmetics-step-0100','symptom_extraction':'cosmetics-step-0100','reply':'EXAONE-3.5-2.4B' if EXAONE_REPLY else 'Qwen'}),
    }

class Handler(BaseHTTPRequestHandler):
    def send_data(self,status,data,content_type='application/json; charset=utf-8'):
        raw=data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode('utf-8')
        self.send_response(status);self.send_header('Content-Type',content_type);self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        if self.path=='/':
            sid=secrets.token_urlsafe(24)
            with LOCK:
                # No persistent records or cross-tab state. A new page is a new conversation.
                if len(SESSIONS)>=100:SESSIONS.pop(next(iter(SESSIONS)))
                SESSIONS[sid]=None
            html=PAGE.read_text(encoding='utf-8').replace('__CSRF__',TOKEN).replace('__SESSION__',sid)
            if EXAONE_REPLY:
                label='EXAONE 3.5 (실험)' if LOCAL_EXAONE else 'SLM + EXAONE 3.5'
                html=html.replace('<title>Skin Chat</title>','<title>Skin Chat - '+label+'</title>').replace('<header>Skin Chat</header>','<header>Skin Chat · '+label+'</header>')
                html=html.replace("debug.reply_source==='qwen'?'Qwen':'정해진 문구'", "debug.reply_source==='exaone35'?'EXAONE 3.5':debug.reply_source==='execution_status'?'실제 처리 결과':debug.reply_source==='qwen'?'Qwen':'정해진 문구'")
                html=html.replace("single_action:'1회 작업 후 종료", "model_output_error:'모델 출력 형식 오류 · 실행 중단',model_ask:'모델이 확인 또는 설명 선택',single_action:'1회 작업 후 종료")
            self.send_data(200,html.encode('utf-8'),'text/html; charset=utf-8')
        elif self.path=='/api/status':
            self.send_data(200,{'app':'skin-chat','build':'integrated-tools-v1','engine':engine_name(),'status':STATE['status'],'error':STATE['error'],'reply_status':STATE['reply_status'],'reply_backend':'local-exaone35' if EXAONE_REPLY else 'qwen','decision_backend':'local-exaone35' if LOCAL_EXAONE else 'research-split' if RESEARCH else 'cosmetics-step-0100'})
        elif self.path=='/api/tools':
            try:self.send_data(200,{'tools':SkinSession(None).catalog('').definitions()})
            except Exception:self.send_data(500,{'error':'Invalid local tool configuration'})
        else:self.send_data(404,{'error':'not found'})
    def do_POST(self):
        if self.path!='/api/chat':return self.send_data(404,{'error':'not found'})
        if not secrets.compare_digest(self.headers.get('X-Chat-Token',''),TOKEN):return self.send_data(403,{'error':'画面を再読み込みしてください。'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<=0 or n>8192:raise ValueError('入力が長すぎます。')
            body=json.loads(self.rfile.read(n));text=body.get('text');sid=body.get('session')
            if not isinstance(text,str) or not text.strip() or len(text)>400:raise ValueError('400文字以内で入力してください。')
            if not isinstance(sid,str) or sid not in SESSIONS:raise ValueError('画面を再読み込みしてください。')
            if STATE['status']!='ready':raise RuntimeError('モデルを準備中です。')
            with LOCK:
                if sid not in SESSIONS:raise ValueError('会話の期限が切れました。画面を再読み込みしてください。')
                if SESSIONS[sid] is None:
                    SESSIONS[sid]={'agent':new_agent(),'history':[]}
                session=SESSIONS[sid]
                trace=session['agent'].turn(text.strip())
                action=trace['action']
                if action=='record' and not trace.get('patch'):action='ask'
                source='exaone35' if EXAONE_REPLY else 'qwen'
                try:
                    if os.environ.get('SKIN_CHAT_REPLY','').lower()=='off':raise RuntimeError('Reply backend disabled')
                    if EXAONE_REPLY:answer,source=STATE['reply_backend'].answer(text.strip(),trace,session['history'])
                    else:
                        answer=generate_reply(text.strip(),action,trace['after'],trace.get('patch',{}),session['history'],
                          tool_trace=trace['events'],available_tools=trace['available_tools'],stop_reason=trace['stop_reason'])
                    STATE['reply_status']='ready'
                except Exception:
                    # The model may be still starting or unavailable. Preserve
                    # the already executed state change; never retry the action.
                    answer='답변 모델에 연결하지 못했어요. '+reply(trace)
                    source='fallback'
                session['history'].extend([{'role':'user','content':text.strip()},{'role':'assistant','content':answer}])
                session['history']=session['history'][-4:]
                if EXAONE_REPLY:
                    record={'session':sid,'text':text.strip(),'trace':trace,'reply':answer,'reply_source':source}
                    with (STATE['reply_backend'].log_dir/'turns.jsonl').open('a',encoding='utf-8') as stream:
                        stream.write(json.dumps(record,ensure_ascii=False)+'\n')
            self.send_data(200,{'reply':answer,'source':source,'debug':debug_trace(trace,source)})
        except (ValueError,TypeError,AttributeError) as exc:self.send_data(400,{'error':str(exc)})
        except Exception as exc:self.send_data(500,{'error':f'{type(exc).__name__}: {exc}'})
    def log_message(self,fmt,*args):pass

class Server(ThreadingHTTPServer):allow_reuse_address=False

if __name__=='__main__':
    port=int(os.environ.get('COSMETICS_CHAT_PORT','18770'))
    try:server=Server(('127.0.0.1',port),Handler)
    except OSError:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        try:
            with opener.open(f'http://127.0.0.1:{port}/api/status',timeout=2) as response:existing=json.load(response)
        except Exception:existing={}
        expected_engine=engine_name()
        if existing.get('app')=='skin-chat' and existing.get('build')=='integrated-tools-v1' and existing.get('engine')==expected_engine and existing.get('reply_backend','qwen')==('local-exaone35' if EXAONE_REPLY else 'qwen'):
            print(f'Chat already running: http://127.0.0.1:{port}/',flush=True)
            if '--open' in sys.argv:
                import webbrowser
                webbrowser.open(f'http://127.0.0.1:{port}/')
            raise SystemExit(0)
        raise SystemExit(f'Port {port} is in use. No process was stopped. Set COSMETICS_CHAT_PORT to an unused port.')
    threading.Thread(target=init_model,daemon=True).start()
    threading.Thread(target=init_reply_model,daemon=True).start()
    url=f'http://127.0.0.1:{port}/';print('Chat:',url,flush=True)
    if '--open' in sys.argv:
        import webbrowser
        chrome=Path(os.environ.get('PROGRAMFILES',r'C:\Program Files'))/'Google/Chrome/Application/chrome.exe'
        if chrome.exists():
            webbrowser.register('cosmetics-chrome',None,webbrowser.BackgroundBrowser(str(chrome)))
            webbrowser.get('cosmetics-chrome').open(url)
        else:webbrowser.open(url)
    server.serve_forever()
