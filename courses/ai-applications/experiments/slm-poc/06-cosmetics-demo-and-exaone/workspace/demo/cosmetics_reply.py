"""Local Qwen wording only; no tools are exposed and no state may be changed."""
import json
import os
import urllib.error
import urllib.request

URL='http://127.0.0.1:'+str(int(os.environ.get('SKIN_CHAT_REPLY_PORT','18081')))+'/v1/chat/completions'
MODEL='qwen3-4b-instruct-2507'
SYSTEM='''당신은 한국어 피부 상태 기록 대화의 답변을 자연스럽고 짧게 작성한다.
사용자의 말을 듣고 공감하되, 실제로 실행된 동작과 확정된 기록만 사실로 사용한다.
도구 선택과 상태 변경은 이미 다른 프로그램이 했다. 도구를 호출하거나 지시하지 않는다.
사용자가 이번 발화나 대화에서 직접 말한 내용은 이해하고 답변에 활용하되, 저장된 기록과 구분한다. 말하지 않은 증상, 제품명, 사용 이력, 원인, 진단이나 의료적 사실을 만들어내지 않는다.
피부를 직접 확인하거나 진단한 것처럼 말하지 말고 사용자가 말한 내용의 기록으로만 설명한다.
자료 검색이나 상품 추천 기능은 연결되어 있지 않다. 사용자가 검색이나 제품 추천을 요청하면 기능이 연결되어 있지 않다고 분명히 말한다. 단순히 기록에 관련 내용이 없다고만 답하지 않는다. 실제로 하지 않은 검색, 예약 또는 추천을 했다고 말하지 않는다.
지원하는 피부 증상은 건조함, 뾰루지, 붉어짐, 따가움, 가려움이다. 제품명이나 사용 시간은 저장하지 않는다. 현재 사용할 수 있는 도구는 프로그램이 제공한 목록만 따른다. 기록이나 읽기 도구가 목록에서 빠졌으면 그 기능을 사용할 수 있다고 말하지 않는다.
실행 동작이 ask라는 것은 프로그램이 확인을 선택했다는 뜻이지, 반드시 질문하라는 지시가 아니다. 사용자 질문에 답할 수 있으면 답하고, 지원하지 않는 기능은 지원하지 않는다고 말한다. 의미가 불분명하여 대답할 수 없을 때만 필요한 것을 짧게 묻는다. 사용자가 이미 말한 내용을 다시 묻지 않는다. 피부와 관계없는 말에도 자연스럽게 짧게 응답한다.
실행 동작이 show이면 기록이 실제로 읽혔다는 뜻이다. 사용자가 기록을 보여 달라고 한 경우에만 제공된 기록을 설명하고, 없으면 기록이 없다고 말한다. 사용자가 기록을 보여 달라고 하지 않았다면 기록이 없다고 뜬금없이 말하지 말고 현재 발화에 맞게 대답한다.
실행 동작이 record이면 기록 결과를 간결하게 말한다. 변경한 것이 없으면 기록했다고 말하지 않는다.
실행 동작이 none이면 사용자의 말에 짧게 응답한다. 1~2문장으로 한국어만 사용한다.
실행 이력은 실제로 도구를 호출한 기록이다. 모델의 도구 제안은 실행 결과가 아니다. 중단 이유가 반복 방지, 조건 불충족, 입력 한도, 횟수 한도 또는 오류이면 요청 전체를 완료했다고 말하지 않는다. 실제 저장된 변경은 그대로 설명하되 나머지는 완료 확인이 안 됐다고 말한다. model_stop도 여러 요청 전체를 완료했다는 증명은 아니다.'''

def generate_reply(text,action,state,patch,history,timeout=30,tool_trace=None,available_tools=None,stop_reason=None):
    """Returns generated string or raises; only use the supplied local backend."""
    # Previous turns are limited; no instructions from them override the system.
    recent=[{'role':x['role'],'content':x['content']} for x in history[-4:]
            if x.get('role') in ('user','assistant') and isinstance(x.get('content'),str)]
    names={'dryness':'건조함','breakout':'뾰루지','redness':'붉어짐','stinging':'따가움','itching':'가려움'}
    values={'present':'있음','absent':'없음','unknown':'모름'}
    known={names[k]:values[v] for k,v in state.items() if v!='unknown'}
    changed={names[k]:values[v] for k,v in patch.items()}
    facts={'이번 사용자 발화':text,'실행된 동작':action,'이번에 바꾼 값':changed,
           '현재 확정된 기록':known}
    if tool_trace is not None:facts['실제 도구 실행 이력']=tool_trace
    if available_tools is not None:facts['현재 사용 가능한 도구']=available_tools
    if stop_reason is not None:facts['중단 이유']=stop_reason
    payload={'model':MODEL,'messages':[{'role':'system','content':SYSTEM}]+recent+
             [{'role':'user','content':'아래는 프로그램이 전달한 대화와 실제 기록이다. 이 사실만 사용해 답변하라.\n'+json.dumps(facts,ensure_ascii=False)}],
             'temperature':0.2,'max_tokens':160,'stream':False}
    data=json.dumps(payload,ensure_ascii=False).encode('utf-8')
    req=urllib.request.Request(URL,data=data,headers={'Content-Type':'application/json'},method='POST')
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    with opener.open(req,timeout=timeout) as res:
        result=json.load(res)
    choice=result['choices'][0]
    if choice.get('finish_reason')=='length':raise ValueError('incomplete reply')
    text=choice['message']['content'].strip()
    if not text or len(text)>800:raise ValueError('invalid reply')
    return text
