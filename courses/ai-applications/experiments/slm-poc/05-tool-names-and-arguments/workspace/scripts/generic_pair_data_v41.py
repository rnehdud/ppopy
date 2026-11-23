"""Fixed family-separated paired next-action trial; labels authored, not human gold."""
import copy,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.intent_observation_data_v39 import OLD_DATA,START,PARSER,MODEL,read,save,digest,verify as verify_previous
from agent.generic_fixture_v41 import Session,World,names,tool_definitions
from agent.decision_context_v37r1 import stable,decode
DATA=ROOT/'data/processed/description-pairs-v41';OUT=ROOT/'output/diagnostics/description-pairs-v41';SEED=410041
SPLITS={'train':['note','todo','media','lamp','parcel','printer'],'dev':['climate','timer'],'test':['library','image','units','text']}
INTENTS=['a','b','c','a_b','b_a','no_tool','missing_b']


def spec(f,i):
    n=str(i+1)
    # a/b/c are handler roles ONLY; none of these role labels enter model inputs.
    table={
      'note':('메모',{'memo':'기존 문장'+n},{'text':'새 문장'+n},['메모에 저장된 내용을 읽는다. 내용을 바꾸지 않는다.','이번 요청에 연결된 새 문장을 메모 끝에 덧붙인다.','메모의 내용을 모두 지운다.'],
        [['지금 저장된 메모 내용을 보여 줘요.','메모에 뭐라고 적혀 있는지 읽어 주세요.'],['메모 끝에 새 문장'+n+'을 추가해 줘요.','새 문장'+n+'을 기존 메모 뒤에 이어 적어 주세요.'],['메모 내용을 전부 지워 줘요.','적어 둔 메모를 비워 주세요.']]),
      'todo':('할 일',{'task':'물주기'+n,'done':False,'completed':['청소']},{},['현재 할 일과 완료 여부를 조회한다.','현재 할 일을 완료 상태로 바꾼다.','완료 목록에 있는 항목들을 제거한다. 진행 중인 할 일은 보존한다.'],
        [['현재 할 일 상태를 확인해 줘요.','남아 있는 할 일과 완료 여부를 보여 주세요.'],['현재 할 일을 완료 처리해 줘요.','이 할 일은 끝냈으니 완료 표시를 해 주세요.'],['완료 목록을 비워 줘요.','이미 끝난 항목들을 목록에서 없애 주세요.']]),
      'media':('재생목록',{'queue':['노래'+n,'다른곡'],'playing':None},{'song':'노래'+n},['재생목록과 현재 재생 중인 곡을 조회한다.','이번 요청에 연결된 곡을 재생한다.','이번 요청에 연결된 곡을 재생목록에서 제거한다.'],
        [['현재 재생목록을 보여 줘요.','무슨 곡들이 있고 지금 어떤 곡이 재생되는지 알려 주세요.'],['노래'+n+'을 재생해 줘요.','노래'+n+'을 틀어 주세요.'],['노래'+n+'을 재생목록에서 빼 줘요.','목록에 있는 노래'+n+'을 삭제해 주세요.']]),
      'lamp':('조명',{'brightness':30,'color':'white'},{'brightness':70+i,'color':'blue'},['조명의 밝기와 색을 읽는다. 조명 설정을 바꾸지 않는다.','이번 요청의 값으로 조명 밝기를 바꾼다.','이번 요청의 색으로 조명 색상을 바꾼다.'],
        [['조명의 현재 설정을 확인해 줘요.','지금 불빛의 밝기와 색이 어떤지 알려 주세요.'],['밝기를 '+str(70+i)+'로 맞춰 줘요.','조명 밝기 값을 '+str(70+i)+'로 변경해 주세요.'],['조명 색을 파란색으로 바꿔 줘요.','불빛이 파랗게 나오도록 설정해 주세요.']]),
      'parcel':('배송',{'status':'preparing','place':'문앞','cancelled':False},{'place':'경비실'},['현재 배송 상태와 배송 장소를 조회한다.','이번 요청의 장소로 배송지를 바꾼다.','배송 요청을 취소한다.'],
        [['배송 상황을 보여 줘요.','배송 상태와 현재 받을 장소를 알려 주세요.'],['배송 장소를 경비실로 바꿔 줘요.','이 물건은 경비실로 받도록 수정해 주세요.'],['이 배송을 취소해 줘요.','배송 요청을 철회해 주세요.']]),
      'printer':('인쇄',{'job':'문서'+n,'paused':False},{},['현재 인쇄 작업과 일시정지 상태를 조회한다.','현재 인쇄 작업을 일시정지한다. 작업은 삭제하지 않는다.','현재 인쇄 작업을 대기열에서 삭제한다.'],
        [['현재 인쇄 작업 상태를 보여 줘요.','무슨 문서를 인쇄 중이고 멈춰 있는지 확인해 주세요.'],['이 인쇄 작업을 일시정지해 줘요.','작업은 남겨 두고 인쇄만 잠시 멈춰 주세요.'],['현재 인쇄 작업을 삭제해 줘요.','대기열에서 이 인쇄 문서를 없애 주세요.']]),
      'climate':('실내온도',{'target':24,'fan':'low'},{'target':27,'fan':'high'},['현재 목표 온도와 팬 세기를 조회한다.','이번 요청의 목표 온도로 설정한다.','팬 세기를 강하게 바꾼다.'],
        [['현재 온도 설정을 확인해 줘요.','목표 온도와 바람 세기를 읽어 주세요.'],['목표 온도를 27도로 설정해 줘요.','설정 온도가 27도가 되게 바꿔 주세요.'],['팬을 강풍으로 바꿔 줘요.','바람 세기를 강하게 올려 주세요.']]),
      'timer':('타이머',{'minutes':10,'cancelled':False},{},['타이머의 남은 시간과 취소 여부를 읽는다.','타이머의 남은 시간을 5분 늘린다.','타이머를 취소하고 남은 시간을 0으로 만든다.'],
        [['타이머가 얼마나 남았는지 보여 줘요.','남은 시간과 취소 상태를 확인해 주세요.'],['타이머를 5분 늘려 줘요.','끝나는 시간을 지금보다 5분 뒤로 미뤄 주세요.'],['타이머를 취소해 줘요.','타이머를 중단하고 남은 시간을 지워 주세요.']]),
      'library':('도서대출',{'book':'책'+n,'due_day':7,'lost':False},{},['책의 반납 예정일과 분실 여부를 조회한다.','현재 책의 대출 기간을 7일 연장한다.','현재 책을 분실했다고 신고하고 분실 상태를 남긴다.'],
        [['빌린 책의 대출 상태를 보여 줘요.','반납일과 분실로 등록됐는지 확인해 주세요.'],['이 책의 대출을 일주일 연장해 줘요.','지금 반납 예정일보다 7일 더 빌리도록 바꿔 주세요.'],['이 책을 분실했다고 신고해 줘요.','빌린 책을 잃어버렸다는 기록을 남겨 주세요.']]),
      'image':('이미지',{'width':800,'height':400},{},['이미지의 현재 가로와 세로 크기를 읽는다.','이미지를 90도 회전하여 가로와 세로 크기를 맞바꾼다.','비율을 유지하면서 이미지 가로를 512픽셀로 줄이거나 늘린다.'],
        [['이미지의 현재 크기를 확인해 줘요.','이 그림의 가로와 세로 픽셀 수를 알려 주세요.'],['이미지를 90도 돌려 줘요.','그림의 방향을 직각으로 회전해 주세요.'],['이미지 가로를 512픽셀로 맞춰 줘요.','가로 512에 맞게 비율을 유지해 크기를 조정해 주세요.']]),
      'units':('단위변환',{'celsius':20,'meters':2,'last':None},{},['마지막 변환 결과를 조회한다. 결과가 없으면 null을 반환한다.','저장된 섭씨 온도를 화씨로 환산하고 마지막 변환 결과에 남긴다.','저장된 미터 길이를 센티미터로 환산하고 마지막 변환 결과에 남긴다.'],
        [['마지막 단위변환 결과를 보여 줘요.','가장 최근에 계산해 둔 환산값을 읽어 주세요.'],['저장된 섭씨 온도를 화씨로 환산해 줘요.','현재 온도값을 화씨 단위의 수로 계산해 주세요.'],['저장된 미터 길이를 센티미터로 바꿔 줘요.','이 길이를 cm 단위로 환산해 주세요.']]),
      'text':('단어목록',{'words':['나','가','나']},{},['현재 단어 목록에 든 항목 수를 센다. 목록은 바꾸지 않는다.','단어 목록을 오름차순으로 정렬한다. 중복은 유지한다.','먼저 나온 순서를 유지하며 목록에서 중복 단어를 제거한다.'],
        [['단어 목록에 항목이 몇 개인지 세어 줘요.','현재 목록에 들어 있는 단어 수를 알려 주세요.'],['단어 목록을 오름차순 정렬해 줘요.','단어들이 작은 순서대로 놓이도록 배열해 주세요.'],['목록에서 중복 단어를 제거해 줘요.','같은 단어는 처음 것 하나만 남겨 주세요.']])}
    topic,state,binding,descs,requests=table[f]
    return {'family':f,'topic':topic,'initial':state,'binding':binding,'descriptions':descs,'requests':requests}


def cases():
    cs=[]
    for split,families in SPLITS.items():
        for family in families:
            for i in range(2 if split=='train' else 1):
                s=spec(family,i)
                for intent in INTENTS:
                    pair_id='v41:'+split+':'+family+':'+str(i)+':'+intent
                    for style in [0,1]:
                        sentences=[p[style] for p in s['requests']];a,b,c=sentences
                        if intent in ['a','b','c']:request=sentences[['a','b','c'].index(intent)];plan=[intent,'none']
                        elif intent=='a_b':
                            request=('먼저 '+a+' 그 일을 끝낸 다음 '+b) if style==0 else (a+' 확인 작업이 끝나면 그다음에 '+b);plan=['a','b','none']
                        elif intent=='b_a':
                            request=('먼저 '+b+' 그 일이 끝난 후 '+a) if style==0 else (b+' 작업을 마치면 이어서 '+a);plan=['b','a','none']
                        elif intent=='no_tool':
                            request=('도구를 실행하지 말고 '+s['topic']+'이라는 말의 뜻만 설명해 줘요.') if style==0 else (s['topic']+' 개념이 궁금해요. 실제 작업은 부탁하지 않을게요.');plan=['none']
                        else:request=b;plan=['ask']
                        ids=names(pair_id+':style:'+str(style));available=['a','c'] if intent=='missing_b' else ['a','b','c']
                        cs.append({'id':pair_id+':style:'+str(style),'pair_id':pair_id,'split':split,'family':family,'intent':intent,'style':style,'instance':i,
                          'request':request,'initial':copy.deepcopy(s['initial']),'binding':copy.deepcopy(s['binding']),'history':[], 'ids':ids,'available':available,
                          'definitions':tool_definitions(s,ids,available),'order_seed':int(__import__('hashlib').sha256((pair_id+str(style)).encode()).hexdigest()[:8],16),
                          'teacher_plan':plan,'label_source':'assistant_authored_not_independently_reviewed'})
    return cs


def semantic_keys(c,view):
    inverse={v:k for k,v in c['ids'].items()};return {k:inverse.get(k,k) for k in view['options']}


def build_rows(cs,tok):
    rows=[];reviews=[]
    for c in cs:
        captured=[];s=None
        def teacher(v):
            step=len(captured);op=c['teacher_plan'][step];target=c['ids'].get(op,op);entry=s.inputs[-1]
            if target not in v['options'] or entry['encoding']['tokens']>512:raise ValueError('Invalid/long complete teacher')
            if decode(entry['encoding']['encoded'])!=entry['packet']:raise ValueError('Lost source facts')
            captured.append({'id':c['id']+':step:'+str(step),'case_id':c['id'],'pair_id':c['pair_id']+':step:'+str(step),'step':step,'split':c['split'],'family':c['family'],
              **copy.deepcopy(v),'target':target,'semantic_target':op,'semantic_keys':semantic_keys(c,v),'source_packet':copy.deepcopy(entry['packet']),'encoding':copy.deepcopy(entry['encoding'])})
            return {'raw_scores':{k:5. if k==target else 0. for k in v['options']}}
        s=Session(c,teacher,tok);trace=s.run();w=World(c['family'],c['initial'],c['binding'])
        expected_events=[]
        for op in c['teacher_plan']:
            if op not in ['ask','none']:expected_events.append({'tool':c['ids'][op],'arguments':{},'executed':True,'result':w.invoke(op)})
        if not trace['model_stopped'] or trace['after']!=w.state or trace['events']!=expected_events or len(captured)!=len(c['teacher_plan']):raise ValueError('Teacher real-handler replay failed')
        rows+=captured;reviews.append({'case_id':c['id'],'trace':trace,'no_model_predictions':True})
    return rows,reviews


def units(rows,seed):
    pairs={};replay=[]
    for r in rows:
        if r.get('pair_id'):pairs.setdefault(r['pair_id'],[]).append(r)
        else:replay.append(r)
    random.Random(seed).shuffle(replay)
    if len(replay)%2:raise ValueError('Odd replay')
    result=[replay[i:i+2] for i in range(0,len(replay),2)]
    for pair in pairs.values():
        if len(pair)!=2 or pair[0]['semantic_target']!=pair[1]['semantic_target'] or set(pair[0]['semantic_keys'].values())!=set(pair[1]['semantic_keys'].values()):raise ValueError('Bad equivalent pair')
        result.append(pair)
    random.Random(seed+1).shuffle(result);return result


def prepare():
    verify_previous()
    if DATA.exists() or OUT.exists():raise FileExistsError('V41 protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000;cs=cases();rows,reviews=build_rows(cs,tok)
    old=read(OLD_DATA/'train.json');train=copy.deepcopy(old)+[r for r in rows if r['split']=='train']
    if len(train)!=696 or len(units(train,SEED))!=348:raise ValueError('Changed fixed data budget')
    partitions={s:{c['family'] for c in cs if c['split']==s} for s in SPLITS}
    if any(partitions[a]&partitions[b] for a,b in [('train','dev'),('train','test'),('dev','test')]):raise ValueError('Family leakage')
    # New function names are meaningless IDs; keep descriptions/schema and event IDs.
    if len({c['ids'][r] for c in cs for r in ['a','b','c']})!=len(cs)*3:raise ValueError('ID collision')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for name,value in [('cases',cs),('train',train),('dev',[r for r in rows if r['split']=='dev']),('test',[r for r in rows if r['split']=='test']),('teacher-reviews',reviews)]:save(DATA/(name+'.json'),value)
    files=[ROOT/p for p in ['agent/generic_fixture_v41.py','scripts/generic_pair_data_v41.py','scripts/generic_pair_learning_v41.py','scripts/report_generic_pair_v41.py','tests/test_generic_pair_v41.py']]+[START/'adapter_model.safetensors',START/'adapter_config.json',PARSER/'adapter_model.safetensors']+list(DATA.iterdir())
    save(OUT/'plan.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'epochs':2,'lr':3e-5,'batch':2,'units_per_epoch':348,'updates':696,'rows':696,'arms':{'regular':0.,'consistent':.2},
      'start':str(START.relative_to(ROOT)),'start_sha256':digest(START/'adapter_model.safetensors'),'parser_sha256':digest(PARSER/'adapter_model.safetensors'),
      'training':'Both arms start V38, same old360 unchanged +336 new rows, same696 rows, same grouped batch schedule, same optimizer and exposure. Only JS weight differs (0 vs.2). New equivalent pairs align anonymous IDs to semantic actions for the loss; those roles are never passed in the model view. Replay has CE only. Fixed final2 epochs, no checkpoint ranking.',
      'split':SPLITS,'source':'New Korean authored executable fixtures; UDA consistency idea and Hammer name-masking preprocessing adapted, NOT their dataset/results reproduced. Prior V8 paired EXAONE state learning failed; this is a distinct scalar next-action experiment with CE-only control.',
      'evaluation':'After both final adapters frozen: baseline/regular/consistent on heldout family dev and test, fixed teacher-prefix judgments and autonomous real local-handler episodes separately. Prior30 gold/parser and plain-read40 parser are seen retention only. No Qwen or extraction evaluation.',
      'guards':'Consistent test paired-both-judgments correct must improve over baseline AND regular. Required-tool choices, autonomous needed-tools-completed and autonomous strict success cannot fall vs baseline; unwanted local state changes cannot increase. Old30 gold/parser strict and old plain-read strict cannot fall; old plain-read unwanted writes cannot rise. No automatic live deployment even if passed.',
      'scope':'Two paraphrases per authored request, six train/two dev/four test function families. Function families excluded from THIS added training, not proved absent in base pretraining/prior unrelated experiments. Empty turn-bound arguments; arbitrary schema binding/extraction not learned. Not broad 90% unknown-domain evidence or independent human labels.',
      'preparation_note':'Before scoring or freezing, registry preflight required explicit execution_contract. Added empty requires/not_after to all fixture definitions; no hidden teacher routing or automatic action gating. No training/model predictions existed during this repair.',
      'stop':'Exactly two fixed runs and frozen evaluation, no fitting on dev/test, no subsequent prompt/cutoff/checkpoint tuning. Keep original data/weights/live chat untouched.'})
    save(OUT/'data-audit.json',{'all_passed':True,'old360_identical':train[:360]==old,'cases':len(cs),'training_cases':sum(c['split']=='train' for c in cs),'test_cases':sum(c['split']=='test' for c in cs),'training_rows':len(train),'new_training_rows':336,'test_rows':len(read(DATA/'test.json')),'max_tokens':max(r['encoding']['tokens'] for r in rows+old),'real_teacher_replays':len(reviews),'families_disjoint':True,'no_model_predictions':True})
    print('V41 FROZEN:696 rows,696 updates per arm; test4 families56 requests',flush=True)


def verify():
    verify_previous();p=read(OUT/'plan.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V41 changed:'+rel)
    return p
if __name__=='__main__':prepare()
