"""One fixed next-action-only QLoRA run. Freeze conversations before any scoring."""
import copy,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from demo.feedback_skin import FeedbackSkinSession
from agent.symptom_state_v1 import empty_state
DATA=ROOT/'data/processed/next-action-learning-v36';OUT=ROOT/'output/diagnostics/next-action-learning-v36'
INITIAL=ROOT/'adapters/cosmetics-chat-v1/step-0100';MODEL=ROOT/'models/ko-decision-roberta-large';SEED=360061


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def cases():
    fields=[('dryness','피부가 건조해요','건조함'),('breakout','뾰루지가 있어요','뾰루지'),('redness','피부가 붉어요','붉어짐'),('stinging','피부가 따가워요','따가움'),('itching','피부가 가려워요','가려움')];out=[]
    def add(split,id_,text,kind,field=None,value='present',history=None,available=None):
        state=empty_state()
        if field:
            other='itching' if field!='itching' else 'stinging';state[other]='present'
            if kind=='correct':state[field]='present'
        desired={field:value} if field and kind in ['write','followup','read_write','write_read','correct'] else {}
        plan={'write':['record','none'],'followup':['record','none'],'correct':['record','none'],'read_write':['show','record','none'],'write_read':['record','show','none'],'read':['show','none'],'no_write':['none'],'missing':['ask']}[kind]
        out.append({'id':split+':'+id_,'split':split,'text':text,'kind':kind,'initial':state,'gold_patch':desired,'ideal_plan':plan,'history':history or [],'available':available if available is not None else ['record_skin_symptoms','read_skin_record']})
    for i,(field,phrase,noun) in enumerate(fields):
        for j in range(2):
            add('train',field+':write:'+str(j),['제 '+phrase+'. 이 상태를 기록해 주세요.','오늘 저는 '+phrase+'. 제 증상으로 저장해 줘.'][j],'write',field)
            add('train',field+':followup:'+str(j),['그리고 '+phrase+'.','또 '+phrase+'. 이것도 제 기록에 추가해 줘.'][j],'followup',field,history=['앞에서 말한 피부 증상도 기록했어요.'])
            add('train',field+':rw:'+str(j),['현재 기록을 먼저 보여 주고, 그다음 제 '+noun+'이 있다고 추가해 주세요.','저장된 상태부터 읽어 줘. 읽은 다음 제 '+noun+'을 있음으로 기록해 줘.'][j],'read_write',field)
            add('train',field+':wr:'+str(j),['제 '+noun+'이 있어요. 기록한 다음 저장된 상태를 보여 주세요.','제 '+noun+'을 먼저 있음으로 저장하고, 그 후 제 기록을 읽어 주세요.'][j],'write_read',field)
            add('train',field+':correct:'+str(j),['지금은 '+noun+'이 없어요. 제 기록을 고쳐 주세요.','제 '+noun+'은 이제 사라졌어요. 없음으로 바꿔 줘.'][j],'correct',field,'absent')
        add('train',field+':friend','제 친구는 '+phrase+'.','no_write')
        add('train',field+':deny','저는 '+phrase+'. 하지만 기록하지 마세요.','no_write')
        add('train',field+':missing-write','제 '+phrase+'. 기록해 주세요.','missing',available=['read_skin_record'])
        add('train',field+':missing-read','제 피부 기록을 보여 주세요.','missing',available=['record_skin_symptoms'])
        add('test',field+':write','제 상태를 말씀드리면 '+phrase+'. 제 기록에 남겨 주세요.','write',field)
        add('test',field+':rw','제 기록을 확인해서 보여 주세요. 그 일을 끝낸 뒤 '+noun+'이 있다는 새 내용을 적어 주세요.','read_write',field)
        add('test',field+':wr','제가 '+noun+'을 겪고 있어요. 먼저 기록하고 이어서 저장된 기록을 읽어 주세요.','write_read',field)
        add('test',field+':correct','아까 있던 제 '+noun+'은 지금은 없어요. 저장된 상태를 정정해 주세요.','correct',field,'absent')
        add('test',field+':other','동생이 자기 '+noun+'이 있다고 했어요. 제 얘기는 아니에요.','no_write')
        add('test',field+':deny','제 '+noun+'이 있는 건 맞지만 저장은 하지 말아 주세요.','no_write')
        add('test',field+':missing','제 '+noun+'을 기록에 남기고 싶어요.','missing',available=['read_skin_record'])
    for i,t in enumerate(['안녕하세요.','고마워요.','건조함이 무슨 뜻이에요?','가려움에 대해 일반적으로 질문하고 싶어요.','피부가 붉다는 말은 무슨 의미인가요?']):add('train','general:'+str(i),t,'no_write')
    for i,t in enumerate(['지금 저장된 피부 기록을 보여 주세요.','제 기록을 읽어 줘.','기록해 둔 제 상태가 궁금해요.','저장한 증상을 확인하고 싶어요.','이전의 피부 기록을 알려 주세요.']):add('train','read:'+str(i),t,'read')
    for i,t in enumerate(['제 상태를 저장해 주세요.','저장한 내용을 읽어 주세요.','제 피부 기록을 확인해 주세요.','제 증상을 기록해 줘.']):add('train','no-tools:'+str(i),t,'missing',available=[])
    for i,t in enumerate(['반가워요.','건조함에 관해 일반적인 설명을 듣고 싶어요.','피부가 따갑다는 표현이 무슨 뜻인지 궁금해요.','여드름이라는 단어를 설명해 주세요.']):add('test','general:'+str(i),t,'no_write')
    for i,t in enumerate(['지금까지 저장한 제 증상을 읽어서 알려 주세요.','제 피부에 관해 남아 있는 기록을 확인해 주세요.','제가 저장해 둔 상태를 다시 보여 줄래요?']):add('test','read:'+str(i),t,'read')
    # Previously inspected inputs: reference only, never fresh test or training.
    refs=[('question','제 피부상태는 어떤가요?','read',None,'present'),('stinging','지금 피부상태는 따가움이 있어요','write','stinging','present'),('dry-followup','그리고 건조해요','followup','dryness','present'),
      ('rw','먼저 지금 저장된 피부 기록을 보여 주고, 그다음 건조함이 있다고 추가해 주세요.','read_write','dryness','present'),('wr','가려움이 있어요. 기록한 다음 제 기록을 보여 주세요.','write_read','itching','present'),
      ('friend','제 친구가 피부가 건조하대요.','no_write',None,'present'),('deny','피부가 건조해요. 하지만 기록하지 마세요.','no_write',None,'present')]
    for id_,text,kind,field,value in refs:add('reference',id_,text,kind,field,value)
    for r in out:
        if r['id']=='reference:dry-followup':r['initial']=empty_state();r['initial']['stinging']='present';r['history']=['지금 피부상태는 따가움이 있어요']
        if r['id']=='reference:question':r['accepted_event_paths']=[[],['read_skin_record']]
    return out


class AvailableSession(FeedbackSkinSession):
    def __init__(self,score,c):
        super().__init__(score);self.allowed=c['available'];self.history=c['history'][:]
        if c['initial']!=empty_state():self.record.update(c['initial'])
    def catalog(self,text):
        r=super().catalog(text)
        for d in r.definitions():
            if d['name'] not in self.allowed:r.remove(d['name'])
        return r


def grade(c,t):
    names={'record':'record_skin_symptoms','show':'read_skin_record'};desired=[names[x] for x in c['ideal_plan'] if x in names]
    actual=[e['tool'] for e in t['events']];expected={**c['initial'],**c['gold_patch']};state_ok=t['after']==expected
    stopped=t['stop_reason']=='model_stop' if desired else t['stop_reason'] in ['model_stop','model_ask']
    allowed=c.get('accepted_event_paths',[desired]);ok=actual in allowed and state_ok and stopped and all(e['result'].get('ok') is True for e in t['events'])
    writes=sum(e['tool']=='record_skin_symptoms' and e['result'].get('ok') is True for e in t['events'])
    return {'strict':bool(ok),'state_ok':state_ok,'expected_tools':desired,'actual_tools':actual,'successful_writes':writes,'unwanted_write':bool(writes and not c['gold_patch']),
      'stop_ok':stopped,'stop_reason':t['stop_reason'],'required_write':bool(c['gold_patch']),'required_write_completed':bool(c['gold_patch'] and writes and state_ok)}


def prepare():
    if DATA.exists() or OUT.exists():raise FileExistsError('V36 protected')
    from scripts.contract_filter_data_v34 import verify
    verify();cs=cases()
    sets={split:{r['text'] for r in cs if r['split']==split} for split in ['train','test','reference']}
    if sets['train']&sets['test']:raise ValueError('Utterance leakage')
    if len({r['id'] for r in cs})!=len(cs):raise ValueError('Duplicate case id')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'cases.json',cs)
    sources=['scripts/next_action_data_v36.py','scripts/next_action_learning_v36.py','scripts/report_next_action_v36.py','tests/test_next_action_v36.py','demo/feedback_skin.py','demo/skin_tools.py','demo/skin_tools.json','agent/live_tool_agent.py','agent/symptom_state_v1.py']
    paths=[ROOT/p for p in sources]+[DATA/'cases.json',INITIAL/'adapter_model.safetensors',INITIAL/'adapter_config.json']
    save(DATA/'plan.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'seed':SEED,'epochs':6,'lr':1e-4,'effective_batch':4,'max_length':512,
      'counts':{s:sum(r['split']==s for r in cs) for s in ['train','test','reference']},
      'training':'Only next-action query/value LoRA from cosmetics-step-0100. NF4 FP16, standard categorical CE per variable candidate set, per-row backward then average4; gradient checkpointing. No symptom questions in training, no input/question/threshold search, one final checkpoint, no selection on test.',
      'teacher':'Assistant-authored Korean requests, correct action orders, stops and missing-tool examples. Correct traces made with actual registered handlers and a SCRIPTED TEACHER; those are not model achievements. Parser is the existing frozen adapter. Predictions are input evidence, not gold symptom labels. If the parser disagrees with a required correct write, train ask instead of saving the wrong patch; count it separately.',
      'evaluation':'Final weights fixed first, then before/after autonomous runs with exact same frozen FeedbackSkinSession. Parser always initial weights. Fresh utterance/conversation templates separate from training; same TWO supported tools, NOT unknown-domain/tool evaluation. Previously observed examples reference only. Grade actual writes, exact requested operation order and MODEL stop, not merely backend refusal. No Qwen evaluation or active demo changes.',
      'adoption_guard':'Fresh strict improves; required writes not lower; unwanted writes not higher; explicit read/write orders and stops reported separately. No automatic deployment even if passed.',
      'scope':'Exploratory synthetic Korean, assistant-defined labels, not independently human-reviewed. Shared symptom vocabulary and operation types; test phrasings held out but not independent tool/domain splits. No claims of arbitrary unseen-tool90.',
      'stop':'One fixed6-epoch run, no prompt/threshold/checkpoint retry on these test results. Existing live chat remains untouched.'})
    print('V36 FROZEN',read(DATA/'plan.json')['counts'],flush=True)


def verify():
    cfg=read(DATA/'plan.json')
    for rel,h in cfg['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V36 frozen changed: '+rel)
    return cfg
if __name__=='__main__':prepare()
