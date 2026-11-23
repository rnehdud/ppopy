"""Build complete, gold-state next-action teaching traces; NO model training/scoring."""
import copy,csv,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from demo.feedback_skin import FeedbackSkinSession
from agent.live_tool_agent import ToolRegistry
from agent.symptom_state_v1 import SYMPTOMS,empty_state
from agent.decision_context_v37 import make_view,decode,legacy_context,stable
from scripts.next_action_data_v36 import MODEL,read,save,digest
DATA=ROOT/'data/processed/complete-next-action-v37';OUT=ROOT/'output/diagnostics/complete-next-action-v37';SEED=370030

SPECS=[('dryness','건조함','제 피부가 건조해요.'),('breakout','뾰루지','제 피부에 뾰루지가 있어요.'),('redness','붉어짐','제 피부가 붉어요.'),('stinging','따가움','제 피부가 따가워요.'),('itching','가려움','제 피부가 가려워요.')]
KINDS=['read_write','write_read','write_only','read_only','no_write','missing']


def cases():
    result=[]
    for f,noun,said in SPECS:
        for split,variants in [('train',range(6)),('heldout',range(6,7))]:
            for j in variants:
                for kind in KINDS:
                    initial=empty_state();other='itching' if f!='itching' else 'stinging';initial[other]='present';observations={};desired={};history=[];allowed=['record_skin_symptoms','read_skin_record']
                    if kind=='read_write':
                        text=[
                          '현재 저장된 기록을 먼저 읽어 주세요. '+said+' 읽은 뒤 이 새 상태를 저장해 주세요.',
                          '저장된 상태를 확인하는 작업부터 해 주세요. '+said+' 확인을 마친 다음 이 증상을 기록해 주세요.',
                          said+' 저장하기 전에 제 기록부터 보여 주세요. 그다음 방금 말한 증상을 기록해 주세요.',
                          '순서는 기록 확인, 그다음 새 증상 저장이에요. '+said,
                          '기록을 읽어 준 후 제 새 상태를 기록해 줘요. '+said,
                          said+' 먼저 예전 기록을 읽고, 그 일을 마친 뒤 지금 상태를 추가해 줘요.',
                          '새 내용을 넣기 전의 기록부터 확인해 주세요. '+said+' 기존 기록을 확인한 뒤 이 내용을 저장해 주세요.'][j]
                        observations={f:'present'};desired=observations.copy();plan=['show','record','none']
                    elif kind=='write_read':
                        text=[
                          said+' 이번 상태를 저장한 다음 저장된 기록을 읽어 주세요.',
                          '이번 증상을 먼저 기록해 주세요. '+said+' 기록이 바뀐 다음 그 기록을 조회해 주세요.',
                          said+' 먼저 기록에 반영하고, 그 뒤에 저장 내용을 읽어 주세요.',
                          '순서는 새 상태 저장, 그다음 기록 조회예요. '+said,
                          said+' 저장을 끝낸 후에 제 기록을 확인하는 작업을 해 주세요.',
                          '기록을 고친 뒤 그 기록을 읽어 줘요. '+said,
                          '이번에 말한 내용을 남겨 주세요. '+said+' 저장 작업을 마치면 기록을 다시 조회해 주세요.'][j]
                        observations={f:'present'};desired=observations.copy();plan=['record','show','none']
                    elif kind=='write_only':
                        text=[said+' 이 증상을 제 기록에 남겨 주세요.',
                          '그리고 '+said.replace('제 ','',1),
                          '지금 말씀드리는 상태를 저장하고 싶어요. '+said,
                          '전에 있던 '+noun+' 증상은 이제 없어요. 없음으로 기록을 정정해 주세요.',
                          '지금은 '+noun+' 증상이 있는지 확실하지 않아요. 해당 기록을 모름으로 바꿔 주세요.',
                          '현재 '+noun+' 증상은 없어요. 없다는 사실을 제 기록에 남겨 주세요.',
                          said+' 지금 설명한 증상만 제 기록에 반영해 주세요.'][j]
                        value='absent' if j in [3,5] else 'unknown' if j==4 else 'present'
                        if j in [3,4]:initial[f]='present'
                        observations={f:value};desired=observations.copy();plan=['record','none']
                        if j==1:history=['제 '+('가려움' if other=='itching' else '따가움')+'이 있어요.']
                    elif kind=='read_only':
                        initial[f]='absent' if j%2 else 'present'
                        text=[
                          '저장된 제 '+noun+' 관련 기록을 읽어 주세요.',
                          '제 피부 기록을 조회하고 싶어요. 특히 기록해 둔 '+noun+' 내용이요.',
                          '기록에 남아 있는 '+noun+' 상태를 확인해 줄래요?',
                          '새로 저장하지 말고, 지금 기록된 '+noun+' 정보만 읽어 주세요.',
                          '이미 남겨 둔 '+noun+' 기록을 다시 조회해 주세요.',
                          '예전에 저장한 '+noun+' 내용이 궁금해요. 그 기록을 읽어 줘요.',
                          '지금 기록 속 '+noun+' 항목이 어떻게 되어 있는지 조회해 주세요.'][j];plan=['show','none']
                    elif kind=='no_write':
                        text=[
                          '이건 제 증상이 아니라 친구의 '+noun+' 이야기예요.',
                          noun+'이라는 말의 일반적인 의미를 설명해 주세요.',
                          '만약 어떤 사람에게 '+noun+' 증상이 생긴다면 어떻게 표현할 수 있을까요?',
                          said+' 이 대화에서는 기록하거나 저장하지 말아 주세요.',
                          ['안녕하세요. 오늘은 인사만 하러 왔어요.','반갑습니다. 잠깐 인사드려요.','좋은 하루 보내세요. 지금은 인사만 할게요.','안녕! 오늘은 다른 요청 없이 인사할게요.','안녕하세요. 기록 요청은 없고 인사만 드려요.'][[s[0] for s in SPECS].index(f)],
                          ['도와줘서 감사합니다. 여기까지예요.','답변 고마워요. 추가로 할 일은 없어요.','고맙습니다. 더 처리할 요청은 없어요.','감사해요. 지금은 별다른 요청이 없어요.','고마워요. 새로 부탁할 일은 없어요.'][[s[0] for s in SPECS].index(f)],
                          '가족에게 '+noun+' 증상이 생겼다고 들었어요. 제 피부 상태를 말하는 것은 아니에요.'][j];plan=['none']
                        if j==3:observations={f:'present'} # A true statement is NOT permission to store.
                    else:
                        text=[
                          said+' 이 상태를 저장해 주세요.',
                          '저장해 둔 제 '+noun+' 기록을 조회해 주세요.',
                          said+' 제 기록에 남기고 싶어요.',
                          '기존 기록부터 읽은 다음 새 상태를 적어 주세요. '+said,
                          '먼저 새 증상을 저장하고 그 뒤 기록을 읽어 주세요. '+said,
                          said+' 이 내용을 기록에 반영해 주세요.',
                          '이전에 저장한 제 '+noun+' 내용을 읽어 주세요.'][j];plan=['ask']
                        allowed=['record_skin_symptoms'] if j in [1,3,6] else [] if j==2 else ['read_skin_record']
                        if j not in [1,6]:observations={f:'present'}
                    result.append({'id':split+':'+f+':'+kind+':'+str(j),'split':split,'family':kind,'field':f,'variant':j,'text':text,'initial':initial,'gold_observations':observations,
                      'expected_stored_patch':desired,'teacher_plan':plan,'available':allowed,'history':history,'label_source':'assistant_authored_not_independently_reviewed'})
    return result


class GoldTeacherSession(FeedbackSkinSession):
    """Only a data generator. Authored state labels are not model predictions."""
    def __init__(self,score,c):
        super().__init__(score);self.c=c;self.history=c['history'][:];self.shadow_events=[];self.analysis=None
        if c['initial']!=empty_state():self.record.update(c['initial'])
    def analyze(self,text):
        if text!=self.c['text']:raise ValueError('Teacher text mismatch')
        obs=copy.deepcopy(self.c['gold_observations']);before=self.record.state
        self.analysis={'base_version':self.record.version,'observations':obs,'proposed_patch':{k:v for k,v in obs.items() if before[k]!=v},
          'decisions':{k:{'choice':obs.get(k,'unchanged'),'source':'authored_label'} for k in SYMPTOMS}}
        return copy.deepcopy(self.analysis)
    def catalog(self,text):
        r=super().catalog(text)
        for d in r.definitions():
            if d['name'] not in self.c['available']:r.remove(d['name'])
        return r
    def bound_catalog(self,text,analysis):
        bound=super().bound_catalog(text,analysis);r=ToolRegistry()
        for d in bound.definitions():
            def handler(name=d['name']):
                value=bound.invoke(name,{})
                self.shadow_events.append({'tool':name,'arguments':{},'executed':True,'result':copy.deepcopy(value)})
                return value
            r.register(d,handler)
        return r


def prepare():
    if DATA.exists() or OUT.exists():raise FileExistsError('V37 protected')
    from scripts.next_action_data_v36 import verify as verify_old
    verify_old();cs=cases()
    prior=read(ROOT/'data/processed/next-action-learning-v36/cases.json');old_test={c['text'] for c in prior if c['split']!='train'}
    if any(c['text'] in old_test for c in cs):raise ValueError('Previously evaluated utterance reused')
    a={c['text'] for c in cs if c['split']=='train'};b={c['text'] for c in cs if c['split']=='heldout'}
    if a&b:raise ValueError('New training/heldout utterance overlap')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True);save(DATA/'cases.json',cs)
    files=[ROOT/p for p in ['agent/decision_context_v37.py','scripts/complete_teacher_data_v37.py','scripts/audit_complete_teacher_v37.py','tests/test_decision_context_v37.py','demo/feedback_skin.py','demo/skin_tools.py','demo/skin_tools.json','agent/live_tool_agent.py','agent/symptom_state_v1.py']]+[DATA/'cases.json']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'max_tokens':512,
      'expected_train_cases':180,'expected_heldout_cases':30,'train_cases_per_family':30,'expected_train_rows':360,
      'construction':'Gold state observations are authored separately from expected stored changes. Actual registered handlers execute a scripted teacher sequence, including every next action and final stop. No parser prediction is promoted into gold or used to replace a correct multi-operation example with ask. These are teaching traces, not model successes.',
      'preprocessing':'Same question and candidate descriptions as the frozen feedback runtime. All actual current state, observation, pending difference, event fields, history and available actions enter a structured packet. Short field mapping and optional exact repeated-state references are losslessly reversible. Choose literal or pooled encoding by tokenizer length only, never by labels or scores. Training and future inference MUST share this renderer.',
      'quality_gate':'All180 training cases and all360 steps must remain; both operation orders must each have30 complete cases. No clipping or removal of long cases. Exact decode/source equality, actual handler/state/order replay, all final stop rows present, no contradictory identical model inputs, no old42-test reuse. Gate failure blocks training; passing establishes data mechanics only, not semantic correctness or model quality.',
      'limits':'Two known turn-bound tools, five symptom fields, zero arguments, authored Korean phrasing. Gold upstream observations are not evidence that the frozen parser can produce them. No unknown-tool/domain90 claim, independent human labeling, training or model prediction. New30 heldout conversations reserved for a future run, not yet evaluated. Existing chat and old datasets untouched.'})
    print('V37 cases frozen',len(cs),'(180 train,30 heldout); no learning',flush=True)


def verify():
    cfg=read(DATA/'protocol.json')
    for rel,h in cfg['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V37 changed:'+rel)
    return cfg


def build():
    cfg=verify()
    if (DATA/'train.json').exists():raise FileExistsError('Teaching material already built')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    rows=[];reviews=[]
    for i,c in enumerate(read(DATA/'cases.json')):
        captured=[];session=None
        def teacher(role,v):
            if set(v['options'])=={'present','absent','unchanged','unknown'}:raise ValueError('No learned symptom inference belongs in a gold teaching trace')
            index=len(captured);target=c['teacher_plan'][index]
            packet={'request':c['text'],'state':session.record.state,'observations':copy.deepcopy(session.analysis['observations']),
              'pending':{k:value for k,value in session.analysis['proposed_patch'].items() if session.record.state[k]!=value},'events':copy.deepcopy(session.shadow_events),'history':session.history[-2:],'available_actions':list(v['options'])}
            if legacy_context(packet)!=v['context']:raise ValueError('Structured packet does not match the full old input')
            converted,meta=make_view(v['question'],v['options'],packet,tok)
            if target not in converted['options']:raise ValueError('Unavailable teacher action')
            keys=list(converted['options']);random.Random(SEED+i*20+index).shuffle(keys);converted['options']={k:converted['options'][k] for k in keys}
            captured.append({'id':c['id']+':step:'+str(index),'case_id':c['id'],'split':c['split'],'family':c['family'],'step':index,**converted,'target':target,
              'source_packet':packet,'encoding':meta,'provenance':'scripted_teacher_with_actual_handlers_not_model_prediction'})
            return {'raw_scores':{k:5. if k==target else 0. for k in v['options']}}
        session=GoldTeacherSession(teacher,c);trace=session.turn(c['text'])
        if len(captured)!=len(c['teacher_plan']) or [r['target'] for r in captured]!=c['teacher_plan']:raise ValueError('Teacher path incomplete')
        if trace['events']!=session.shadow_events or trace['after']!={**c['initial'],**c['expected_stored_patch']}:raise ValueError('Actual teaching operations do not match labels')
        rows+=captured;reviews.append({'case':c,'rows':[r['id'] for r in captured],'actual_trace':trace,'provenance':'authored_gold_and_scripted_choices_not_model_ability'})
    for split in ['train','heldout']:save(DATA/(split+'.json'),[r for r in rows if r['split']==split])
    save(DATA/'teaching-review.json',reviews)
    with (DATA/'teaching-review.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['id','split','family','text','gold_observations','expected_stored_patch','teacher_plan','actual_tools','final_state','max_tokens']);w.writeheader()
        for x in reviews:
            c=x['case'];rs=[r for r in rows if r['case_id']==c['id']];w.writerow({'id':c['id'],'split':c['split'],'family':c['family'],'text':c['text'],'gold_observations':stable(c['gold_observations']),'expected_stored_patch':stable(c['expected_stored_patch']),'teacher_plan':' -> '.join(c['teacher_plan']),'actual_tools':' -> '.join(e['tool'] for e in x['actual_trace']['events']),'final_state':stable(x['actual_trace']['after']),'max_tokens':max(r['encoding']['tokens'] for r in rs)})
    save(DATA/'build-manifest.json',{'files':{str(p.relative_to(ROOT)):digest(p) for p in DATA.iterdir() if p.is_file() and p.name!='build-manifest.json'},'no_training':True,'no_model_scoring':True})
    print('V37 BUILT',len(rows),'rows; max tokens',max(r['encoding']['tokens'] for r in rows),flush=True)
if __name__=='__main__':
    if sys.argv[1]=='prepare':prepare()
    elif sys.argv[1]=='build':build()
    else:raise ValueError(sys.argv[1])
