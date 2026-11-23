"""Contrast requests while retaining the SAME observation; reserve new wording."""
import copy,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.prepared_learning_plan_v38 import TEACH as OLD_DATA,OUT as OLD_OUT,MODEL,INITIAL as PARSER,verify as verify_old,read,save,digest
from scripts.complete_teacher_data_v37 import SPECS
from agent.symptom_state_v1 import empty_state
from demo.provided_feedback_v39 import ProvidedFeedbackSession
from agent.decision_context_v37r1 import decode,stable
DATA=ROOT/'data/processed/intent-observation-v39';OUT=ROOT/'output/diagnostics/intent-observation-v39'
START=OLD_OUT/'train/final-adapter';SEED=390039
FAMILIES=['read_only','missing_read','write_only','write_read','read_write','third_party','no_store','missing_write']


def cases():
    cs=[]
    for field,noun,_ in SPECS:
        for value in ['present','absent','unknown']:
            fact={'present':'지금 제 '+noun+' 증상이 있어요.','absent':'지금 제 '+noun+' 증상은 없어요.','unknown':'지금 제 '+noun+' 증상이 있는지 모르겠어요.'}[value]
            for split in ['train','heldout']:
                texts={
                  'read_only': ['저장된 '+noun+' 내용을 보여 주세요. 기록을 바꾸지는 마세요.','제 '+noun+' 항목은 어떤 내용으로 남아 있나요? 수정 없이 확인만 부탁해요.'],
                  'missing_read':['제 '+noun+' 기록을 읽어 주세요. 다른 작업은 요청하지 않았어요.','남겨 둔 '+noun+' 내용을 보고 싶어요. 읽는 기능이 없으면 저장으로 대신하지 마세요.'],
                  'write_only':[fact+' 이 새 상태로 기록을 고쳐 주세요.',fact+' 앞서 남긴 상태 대신 방금 말한 내용으로 수정해 줘요.'],
                  'write_read':[fact+' 기록을 바꾸고 나서 바뀐 내용을 보여 주세요.',fact+' 먼저 이 상태를 반영해 줘요. 반영이 끝나면 기록 내용을 읽어 줘요.'],
                  'read_write':[fact+' 예전 내용을 읽는 일을 먼저 하고, 그다음 새 상태로 고쳐 주세요.',fact+' 변경 전 내용을 먼저 보여 주고, 보여 준 뒤 방금 말한 상태를 남겨 줘요.'],
                  'third_party':['동생의 '+noun+' 이야기예요. 제 증상으로 저장하지 마세요.','지인의 '+noun+' 상태를 대신 이야기하는 거예요. 저의 기록은 그대로 두세요.'],
                  'no_store':[fact+' 지금은 말만 하는 거고 기록하지 말아 주세요.',fact+' 내용을 이해만 해 주세요. 이번에는 저장하거나 조회할 필요 없어요.'],
                  'missing_write':[fact+' 제 기록을 수정해 주세요. 읽기만 해서는 안 돼요.',fact+' 이 내용으로 기록을 바꾸고 싶어요. 수정 기능이 없으면 바꾸었다고 하지 마세요.']}
                initial=empty_state();initial['itching' if field!='itching' else 'stinging']='present';initial[field]='present' if value=='unknown' else 'unknown'
                available=['record_skin_symptoms','read_skin_record']
                if split=='heldout':available.reverse() # tool listing order not label.
                if split=='heldout' and field in ['breakout','stinging']:available=available[::-1]
                if split=='heldout' and value=='unknown':available.reverse()
                for family in FAMILIES:
                    allowed=available[:]
                    if family=='missing_read':allowed=['record_skin_symptoms']
                    if family=='missing_write':allowed=['read_skin_record']
                    obs={field:value};gold=obs if family not in ['read_only','missing_read','third_party'] else {}
                    expected=obs if family in ['write_only','write_read','read_write'] else {}
                    plan={'read_only':['show','none'],'missing_read':['ask'],'write_only':['record','none'],
                      'write_read':['record','show','none'],'read_write':['show','record','none'],
                      'third_party':['none'],'no_store':['none'],'missing_write':['ask']}[family]
                    cs.append({'id':'v39:'+split+':'+field+':'+value+':'+family,'split':split,'family':family,'field':field,
                      'text':texts[family][split=='heldout'],'initial':initial.copy(),'history':[], 'available':allowed,
                      'provided_observations':obs.copy(),'gold_observations':copy.deepcopy(gold),'expected_stored_patch':copy.deepcopy(expected),'teacher_plan':plan,
                      'label_source':'assistant_authored_not_independently_reviewed'})
    return cs


def prepare():
    verify_old()
    if DATA.exists() or OUT.exists():raise FileExistsError('V39 protected')
    if not read(OLD_OUT/'audit.json')['all_passed']:raise ValueError('Parent audit')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    cs=cases();old_train=read(OLD_DATA/'train.json');rows=[];reviews=[]
    old_test=read(OLD_DATA/'cases.json');reserved={c['text'] for c in old_test if c['split']=='heldout'}
    tr={c['text'] for c in cs if c['split']=='train'};te={c['text'] for c in cs if c['split']=='heldout'}
    if tr&te or tr&reserved or te&reserved:raise ValueError('Wording split overlap')
    for c in cs:
        captured=[];s=None
        def teacher(role,v):
            if role!='action':raise ValueError('No symptom inference in controlled teaching')
            j=len(captured);target=c['teacher_plan'][j]
            entry=s.scoring_inputs[-1];view=copy.deepcopy(v);keys=list(v['options']);random.Random(SEED+len(rows)+j).shuffle(keys);view['options']={k:view['options'][k] for k in keys}
            if target not in view['options'] or entry['encoding']['tokens']>512:raise ValueError('Invalid/long full teacher')
            if decode(entry['encoding']['encoded'])!=entry['packet']:raise ValueError('Lossy input')
            captured.append({'id':c['id']+':step:'+str(j),'case_id':c['id'],'split':c['split'],'family':c['family'],'step':j,
              **view,'target':target,'source_packet':copy.deepcopy(entry['packet']),'encoding':copy.deepcopy(entry['encoding'])})
            return {'raw_scores':{k:5. if k==target else 0. for k in v['options']}}
        s=ProvidedFeedbackSession(teacher,c,tok);trace=s.turn(c['text'])
        names={'record':'record_skin_symptoms','show':'read_skin_record'}
        if [r['target'] for r in captured]!=c['teacher_plan'] or trace['after']!={**c['initial'],**c['expected_stored_patch']} or not trace['model_stopped'] or [e['tool'] for e in trace['events']]!=[names[k] for k in c['teacher_plan'] if k in names]:raise ValueError('Teacher replay')
        rows+=captured;reviews.append({'case_id':c['id'],'trace':trace,'rows':[r['id'] for r in captured],'teacher_only_not_model_achievement':True})
    train=copy.deepcopy(old_train)+[r for r in rows if r['split']=='train']
    if len(train)!=570 or len(cs)!=240:raise ValueError('Changed fixed data budget')
    contradictions={}
    for r in train:
        k=stable({x:r[x] for x in ['question','options','context']})
        if k in contradictions and contradictions[k]!=r['target']:raise ValueError('Conflicting exact model inputs')
        contradictions[k]=r['target']
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for name,value in [('cases',cs),('train',train),('heldout',[r for r in rows if r['split']=='heldout']),('teacher-reviews',reviews)]:save(DATA/(name+'.json'),value)
    files=[Path(__file__),ROOT/'demo/provided_feedback_v39.py',ROOT/'scripts/intent_observation_learning_v39.py',ROOT/'scripts/report_intent_observation_v39.py',ROOT/'tests/test_intent_observation_v39.py',OLD_OUT/'plan.json',OLD_OUT/'completion-manifest.json',START/'adapter_model.safetensors',START/'adapter_config.json',PARSER/'adapter_model.safetensors']+list(DATA.iterdir())
    save(OUT/'plan.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'epochs':4,'lr':5e-5,'effective_batch':4,'rows':570,'updates':572,
      'start':str(START.relative_to(ROOT)),'start_sha256':digest(START/'adapter_model.safetensors'),'parser_sha256':digest(PARSER/'adapter_model.safetensors'),
      'data':'Existing360 rows unchanged +210 complete controlled-observation action judgments from120 new authored training requests. Both operation orders, write/read, no-write, missing tools. Same observation across differing requests; all steps and final stops kept.',
      'evaluation':'Before/after once.120 new heldout requests x gold/provided/frozen-parser, plus old30 as seen retention x gold/parser =840 autonomous episodes. Provided observations deliberately include upstream mistakes; not real parser predictions. Targets never passed to runtime. Final weights only, no threshold/prompt/epoch selection.',
      'guards':'New provided-mode unwanted writes must decrease; required correct writes and two-operation strict count cannot fall in any new mode; parser unwanted writes cannot rise; old30 gold/parser strict cannot fall. No automatic demo deployment.',
      'grading':'Order, actual state, successful tools, normal model stop, plus exact final ask/none choice. V38 allowed ask/none interchangeably on no-tool cases; report previous_metric_strict separately for historical comparability. Both new before/after use identical stricter grading.',
      'scope':'Two known tools, five symptoms, no generated arguments; assistant-authored labels. New wording within known task patterns, not unknown-domain generality, independent human gold, Qwen or voice evaluation.',
      'stop':'One fixed training run. Report failures and stop. Current chat, parser weights and earlier frozen artifacts unchanged.'})
    save(OUT/'data-audit.json',{'all_passed':True,'old360_identical':train[:360]==old_train,'train_rows':len(train),'new_training_cases':120,'new_heldout_cases':120,'new_train_rows':210,'new_heldout_rows':210,'max_tokens':max(r['encoding']['tokens'] for r in train+rows),'full_teacher_replays':len(reviews),'wording_overlap':False,'no_model_predictions':True})
    print('V39 data frozen:570 training judgments;120 new heldout requests; no learning yet',flush=True)


def verify():
    verify_old();p=read(OUT/'plan.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('V39 frozen file changed:'+rel)
    return p
if __name__=='__main__':prepare()
