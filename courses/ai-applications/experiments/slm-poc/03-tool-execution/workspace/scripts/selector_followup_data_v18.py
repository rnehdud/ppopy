"""Future confirmation and conditional learning teachers, fixed before reference analysis."""
import copy,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_interface_data_v18 import DATA,OUT,CONDITIONS,view,read,read_jsonl,save,digest

FOLLOW=DATA/'followup'
FAMILIES={
 'train':[
  ('swim','수영 강습','가상북부수영장'),('tennis','테니스 코트 이용','가상남부테니스장'),('dance','댄스 수업','가상동부댄스교실'),
  ('wood','목공 체험','가상서부공방'),('vet','반려동물 검진','가상나무동물병원'),('hair','미용실 방문','가상달빛미용실'),
  ('photo','사진관 촬영','가상구름사진관'),('study','스터디룸 이용','가상별빛스터디룸'),('camp','캠핑장 숙박','가상푸른캠핑장'),('flower','꽃꽂이 수업','가상꽃길꽃집')],
 'fresh':[
  ('astronomy','천문 관측 체험','가상작은관측소'),('paper','한지 공예 수업','가상한지공방'),('sailing','요트 조종 수업','가상요트학교'),
  ('tea','다도 체험','가상고요다원'),('tuning','악기 조율 방문','가상음악작업실'),('carwash','자동차 세차','가상맑은세차장'),
  ('perfume','수제 향수 만들기 체험','가상향기공방'),('bird','철새 관찰 안내','가상철새센터'),('roast','커피 로스팅 수업','가상볶음교실'),('waterbike','수상 자전거 대여','가상호수대여소')]
}
OPS=['create','lookup','cancel','reschedule']
ACTION={
 'create':('예약을 새로 생성합니다. 기존 예약의 조회나 취소, 날짜 변경은 수행하지 않습니다.',{'venue':{'type':'string','description':'이용할 시설 명칭'},'day':{'type':'string','description':'새로 예약할 날짜'}}),
 'lookup':('이미 있는 예약의 내용을 조회합니다. 예약을 새로 만들거나 취소하거나 변경하지 않습니다.',{'reservation_id':{'type':'string','description':'조회할 기존 예약 번호'}}),
 'cancel':('기존 예약을 취소합니다. 예약을 새로 만들거나 조회하거나 날짜만 변경하는 기능은 아닙니다.',{'reservation_id':{'type':'string','description':'취소할 기존 예약 번호'}}),
 'reschedule':('기존 예약의 날짜만 변경합니다. 기존 예약 자체는 유지하며, 조회나 신규 예약이나 취소는 하지 않습니다.',{'reservation_id':{'type':'string','description':'날짜를 변경할 기존 예약 번호'},'new_day':{'type':'string','description':'바꿀 새 날짜'}})
}


def tool(family,op):
    slug,label,venue=family;codes=[23,47,61,89];random.Random(180081+sum(map(ord,slug))).shuffle(codes)
    description,props=ACTION[op]
    return {'name':'svc_'+slug+'_'+str(codes[OPS.index(op)]),'description':label+' '+description+' 이 서비스의 예약만 담당합니다.',
        'parameters':{'type':'object','properties':copy.deepcopy(props),'required':list(props)}}


def utterance(family,op,variant,index):
    slug,label,venue=family
    verbs={'create':label+' 예약을 새로 잡아 주세요.','lookup':label+' 예약이 어떻게 되어 있는지 확인해 주세요.',
        'cancel':label+' 예약을 취소해 주세요.','reschedule':label+' 예약 날짜를 바꿔 주세요.'}
    code='DEMO'+str(7300+index);day='12월 '+str(10+index%15)+'일'
    if variant==0:return verbs[op]
    if variant==1:return f'번호는 {code}이고 장소는 {venue}예요. {day}로 생각하고 있어요. '+verbs[op]
    if variant==2:return f'{code} 건이에요. 다시 말하면 {code}예요. '+verbs[op]
    if variant==3:return '다른 서비스 얘기는 나중에 할게요. 지금 부탁하는 것은 '+verbs[op]
    prefix={'create':'취소하는 게 아니라 새로 예약하고 싶어요. ', 'lookup':'새로 예약하지 말고 이미 있는 내용만 보여 주세요. ',
        'cancel':'날짜만 바꾸려는 게 아니라 예약 자체를 없애 주세요. ', 'reschedule':'예약 자체는 없애지 말고 날짜만 바꿔 주세요. '}
    return prefix[op]+verbs[op]


def build(split,arm='focused'):
    families=FAMILIES[split];rows=[]
    for n,family in enumerate(families):
        for op in OPS:
            for variant in range(5):
                target=tool(family,op);rng=random.Random(180081+n*100+OPS.index(op)*10+variant)
                if split=='train':
                    if arm=='control':
                        options=[target]+[tool(families[(n+j)%len(families)],rng.choice(OPS)) for j in [1,2,3]]
                    else:
                        other=[x for x in OPS if x!=op];rng.shuffle(other)
                        options=[target,tool(family,other[0]),tool(family,other[1]),tool(families[(n+3)%len(families)],op)]
                    expected=[target['name']]
                else:
                    options=[tool(family,x) for x in OPS]
                    expected=[target['name']]
                    if variant in [2,3]:
                        options += [tool(families[(n+j)%len(families)],op) for j in [1,2,3]]
                        options.append(tool(families[(n+4)%len(families)],OPS[(OPS.index(op)+1)%4]))
                    elif variant==4:
                        alias=copy.deepcopy(target);alias['name']+='_alternative'
                        options=[target,alias]+[tool(family,x) for x in OPS if x!=op][:2];expected.append(alias['name'])
                rng.shuffle(options);text=utterance(family,op,variant,n)
                rows.append({'id':f'selector-follow-v18:{split}:{family[0]}:{op}:v{variant}','cohort':'followup',
                    'group':op,'query_group':family[0]+':'+op,'messages':[{'role':'user','content':text}],
                    'tools':options,'expected':expected,'was_needed_call':True,'variant':variant,'family':family[0],
                    'label_scope':'Assistant-authored capability only. No argument completion/execution. Alternative identical-capability API explicitly accepted on fresh variant4.'})
    return rows


def verify_followup():
    p=read(FOLLOW/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Followup frozen file changed: '+rel)
    return p


def prepare():
    if FOLLOW.exists():raise FileExistsError('Followup protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(ROOT/'models/ko-decision-roberta-large',local_files_only=True)
    sets={'control_train':build('train','control'),'focused_train':build('train'),'fresh':build('fresh')}
    maxima={}
    for key,rows in sets.items():
        assert len(rows)==200;maxima[key]=0
        for r in rows:
            for c in CONDITIONS:
                v=view(r,c);enc=tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)
                maxima[key]=max(maxima[key],max(map(len,enc['input_ids'])))
    if max(maxima.values())>512:raise ValueError(('Refuse rather than truncate',maxima))
    a=sets['control_train'];b=sets['focused_train']
    assert all(x['id']==y['id'] and x['messages']==y['messages'] and x['expected']==y['expected'] for x,y in zip(a,b))
    train_names={t['name'] for r in a+b for t in r['tools']};test_names={t['name'] for r in sets['fresh'] for t in r['tools']}
    if train_names&test_names:raise ValueError('Overlapping tool identities')
    FOLLOW.mkdir(parents=True)
    for key,rows in sets.items():(FOLLOW/(key+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    paths=list(FOLLOW.glob('*.jsonl'))+[Path(__file__),ROOT/'tests/test_selector_followup_v18.py']
    save(FOLLOW/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in paths},'max_tokens':maxima,
        'timing':'Generator, teachers and final data fixed before aggregating reference outcomes. No adaptive rewriting of final examples.',
        'branch':'If a reference input format is eligible, compare that fixed format vs current_full on fresh200, no training. If none is eligible, one conditional learning comparison: both200-query arms from original selector, capability_full, lr1e-5, one epoch, logical batch4, fixed step50. No checkpoint/threshold selection. Controls random other-family negatives; focused same-family wrong-operation and same-operation wrong-family negatives.',
        'selection_guard':'Fresh format verification must strictly improve total correct vs current_full, reach>=180/200, keep each operation and candidate-count/alternative group not below current_full. No deployment; no later switch if it fails.',
        'learning_guard':'Focused final step50 must improve fresh correct vs original capability_full and control, reach>=180/200, and reference V16/FunctionChat total and V16 needed-case counts not below original capability_full. Also report original current_full. No learning after fresh test scores.',
        'scope':'10 train families and10 disjoint fresh families, four known reservation operations across all families. Shared templates and controlled authored meanings; not independent human gold, arbitrary unseen verb/task generalization or real execution. Only capability choice; every positive task has at least one correct supplied tool. No-match rejection still separate.',
        'stop':'At most this one fresh verification OR two fixed training arms followed by one test. No input/teacher/criterion changes using final outcomes. No state-role or demo changes.'})
    print('FOLLOWUP FROZEN',maxima,flush=True)

if __name__=='__main__':prepare()
