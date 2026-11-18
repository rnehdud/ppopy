"""Create 6000 local decision examples and a frozen exploratory conversation test.

Synthetic symptom labels are rule-generated, not human-verified. KLUE-WoS
training user turns are used only as no-symptom-update examples, never as skin
gold. Test is authored separately; no evaluation labels enter training.
"""
import hashlib,json,random,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from agent.symptom_state_v1 import SYMPTOMS,empty_state

DEST=ROOT/'data/processed/ko_symptom_6000_v2'
WOS=ROOT/'data/raw/klue_wos/train-00000-of-00001.parquet'
PREVIOUS=['unknown','present','absent']
WORDS={'dryness':'건조함','breakout':'여드름','redness':'붉어짐','stinging':'따가움','itching':'가려움'}
PHRASES={
 'dryness':{'present':['제 피부가 건조해요.','얼굴이 많이 건조합니다.','저는 건조함이 있어요.','볼이 푸석하고 건조해요.','제 얼굴에 건조함이 있어요.','피부가 메말라서 건조합니다.'],
  'absent':['제 피부는 건조하지 않아요.','저는 건조함이 없어요.','얼굴이 더 이상 건조하지 않습니다.','제 피부에 건조함은 전혀 없어요.','지금은 얼굴이 안 건조해요.','볼의 건조함이 사라졌어요.'],
  'unknown':['제 피부가 건조한지 모르겠어요.','제게 건조함이 있는지 확신이 없어요.','얼굴이 건조한지 잘 모르겠습니다.','제 피부의 건조 여부는 불확실해요.','건조함이 있는지 판단하기 어려워요.','지금 건조한지는 잘 모르겠어요.']},
 'breakout':{'present':['제 얼굴에 여드름이 있어요.','저는 뾰루지가 났어요.','제 피부에 여드름이 생겼어요.','얼굴에 트러블이 올라왔어요.','저에게 뾰루지가 있습니다.','볼에 여드름이 나 있어요.'],
  'absent':['제 얼굴에는 여드름이 없어요.','저는 뾰루지가 나지 않았어요.','제 피부에 여드름이 전혀 없어요.','얼굴에 트러블이 없어졌어요.','지금 제게 뾰루지가 없습니다.','여드름은 이제 안 나요.'],
  'unknown':['제 얼굴에 여드름이 있는지 모르겠어요.','이게 뾰루지인지 잘 모르겠어요.','저에게 여드름이 있는지 확신이 없어요.','제 트러블 여부는 불확실해요.','지금 뾰루지가 난 건지 모르겠어요.','얼굴에 여드름이 있는지는 알 수 없어요.']},
 'redness':{'present':['제 얼굴이 빨개요.','저는 피부가 붉어요.','제 볼이 붉어졌어요.','얼굴에 붉은기가 있어요.','제 피부가 빨갛게 변했어요.','저에게 홍조가 있습니다.'],
  'absent':['제 얼굴은 빨갛지 않아요.','저는 피부가 붉지 않아요.','제 볼은 붉지 않습니다.','얼굴에 붉은기가 없어요.','제 피부가 빨갛게 변하지 않았어요.','저에게 홍조가 없습니다.'],
  'unknown':['제 얼굴이 빨간지 모르겠어요.','저는 피부가 붉은지 확신이 없어요.','제 볼이 붉은지 잘 모르겠습니다.','얼굴에 붉은기가 있는지 모르겠어요.','제 피부가 빨간지는 불확실해요.','저에게 홍조가 있는지 알 수 없어요.']},
 'stinging':{'present':['제 얼굴이 따가워요.','저는 피부가 따끔거려요.','제 볼이 화끈거리며 따가워요.','피부에 따가움이 있어요.','제 피부가 따끔따끔해요.','저에게 따가운 증상이 있습니다.'],
  'absent':['제 얼굴이 따갑지 않아요.','저는 피부가 따끔거리지 않아요.','제 볼은 더 이상 따갑지 않아요.','피부에 따가움이 없어요.','제 피부는 안 따끔거려요.','저에게 따가운 증상이 없습니다.'],
  'unknown':['제 얼굴이 따가운지 모르겠어요.','저는 피부가 따끔거리는지 확신이 없어요.','제 볼이 따가운지 잘 모르겠습니다.','피부에 따가움이 있는지 모르겠어요.','제 피부가 따끔한지는 불확실해요.','저에게 따가운 증상이 있는지 알 수 없어요.']},
 'itching':{'present':['제 얼굴이 가려워요.','저는 피부가 간지러워요.','제 볼이 가렵습니다.','피부에 가려움이 있어요.','제 피부가 간질간질해요.','저에게 가려운 증상이 있습니다.'],
  'absent':['제 얼굴은 가렵지 않아요.','저는 피부가 간지럽지 않아요.','제 볼은 더 이상 가렵지 않아요.','피부에 가려움이 없어요.','제 피부는 안 간지러워요.','저에게 가려운 증상이 없습니다.'],
  'unknown':['제 얼굴이 가려운지 모르겠어요.','저는 피부가 간지러운지 확신이 없어요.','제 볼이 가려운지 잘 모르겠습니다.','피부에 가려움이 있는지 모르겠어요.','제 피부가 간지러운지는 불확실해요.','저에게 가려운 증상이 있는지 알 수 없어요.']}}
TAILS=['',' 오늘은 날씨가 맑아요.',' 내일은 집에 있을 거예요.',' 어제는 일찍 잤어요.',
 ' 요즘 피부 관리에 관심이 많아요.',' 이번 주는 바빴어요.',' 오전에 산책을 했어요.',
 ' 평소에 물을 자주 마셔요.',' 오늘은 일정이 많아요.',' 다음에 다시 이야기할게요.',
 ' 요새 실내에 오래 있어요.',' 방금 상담을 시작했어요.']

# Each item contains distinct turns; patches represent explicit, task-specific
# expectations authored before training. No participant health records.
TEST=[
 [('오늘 얼굴이 너무 푸석해요.',{'dryness':'present'}),('밖에 잠깐 다녀왔어요.',{}),('이제 건조한 느낌은 없어요.',{'dryness':'absent'})],
 [('볼이 간지러워요.',{'itching':'present'}),('오늘 일정이 많네요.',{}),('지금은 안 가려워요.',{'itching':'absent'})],
 [('뺨이 빨갛게 올라왔어요.',{'redness':'present'}),('얼굴이 따끔거려요.',{'stinging':'present'}),('붉은기는 없어졌어요.',{'redness':'absent'})],
 [('이마에 뾰루지가 났어요.',{'breakout':'present'}),('아직도 트러블이 있어요.',{'breakout':'present'}),('여드름은 이제 없어졌습니다.',{'breakout':'absent'})],
 [('오늘 얼굴이 건조하고 가려워요.',{'dryness':'present','itching':'present'}),('가려운 건 나았어요.',{'itching':'absent'})],
 [('붉은기는 없는데 볼이 따가워요.',{'redness':'absent','stinging':'present'}),('지금은 따갑지도 않아요.',{'stinging':'absent'})],
 [('여드름은 없고 얼굴이 건조해요.',{'breakout':'absent','dryness':'present'}),('다른 이야기를 해볼까요?',{})],
 [('볼이 간지럽고 빨개졌어요.',{'itching':'present','redness':'present'}),('빨간 건 그대로예요.',{'redness':'present'})],
 [('제 친구는 여드름이 심하대요.',{}),('제 얼굴에는 여드름이 없어요.',{'breakout':'absent'})],
 [('동생은 피부가 건조하지만 저는 안 건조해요.',{'dryness':'absent'}),('저는 가려움이 있어요.',{'itching':'present'})],
 [('엄마 얼굴은 빨간데 제 피부는 안 빨개요.',{'redness':'absent'}),('어제 영화를 봤어요.',{})],
 [('친구가 따갑다고 했어요. 제 피부 이야기는 아니에요.',{}),('저도 이제 얼굴이 따가워요.',{'stinging':'present'})],
 [('혹시 화장품을 바르면 뾰루지가 생길 수도 있나요?',{}),('저는 아직 여드름이 없어요.',{'breakout':'absent'})],
 [('만약 피부가 가렵다면 어떻게 해야 하나요?',{}),('실제로는 가렵지 않아요.',{'itching':'absent'})],
 [('안녕하세요. 피부 이야기를 해볼게요.',{}),('아직 증상은 말하지 않았어요.',{})],
 [('제 얼굴이 빨개요.',{'redness':'present'}),('빨간지 아닌지 지금은 잘 모르겠어요.',{'redness':'unknown'})],
 [('제 피부가 따가워요.',{'stinging':'present'}),('따가운 건지 이제는 잘 모르겠어요.',{'stinging':'unknown'})],
 [('제 얼굴에 여드름이 올라왔어요.',{'breakout':'present'}),('정정할게요. 여드름이 있는지 모르겠어요.',{'breakout':'unknown'})],
 [('얼굴이 가렵지 않아요.',{'itching':'absent'}),('아, 지금은 오히려 가려워요.',{'itching':'present'})],
 [('제 얼굴이 너무 건조한 상태예요.',{'dryness':'present'}),('아까 말한 걸 고칠게요. 지금은 건조하지 않아요.',{'dryness':'absent'}),('볼이 가렵기 시작했어요.',{'itching':'present'})],
]

def case_rows():
    cases=[]
    for i,turns in enumerate(TEST):
        state=empty_state();out=[]
        for text,patch in turns:
            state={**state,**patch};out.append({'input':text,'expected':dict(state),'gold_patch':patch})
        cases.append({'id':f'case-{i+1:02}','turns':out,'label_status':'assistant-authored, not independently reviewed'})
    return cases

def main():
    import pyarrow.parquet as pq
    if DEST.exists():raise FileExistsError('Frozen dataset already exists')
    rng=random.Random(601106);direct={k:[] for k in ['present','absent','unknown','unchanged']};special={'multi':[],'other':[]}
    cases=case_rows();testtexts={t['input'] for c in cases for t in c['turns']}
    seen=set()
    def add(pool,text,target,prior,decision,category,source):
        key=(text,target,prior)
        if key in seen or text in testtexts:return
        seen.add(key);pool.append({'text':text,'field':target,'previous':prior,'decision':decision,
                                   'category':category,'source':source})
    for f,groups in PHRASES.items():
        for decision,phrases in groups.items():
            for phrase in phrases:
                for tail in TAILS:
                    for target in SYMPTOMS:
                        for prior in PREVIOUS:
                            result=decision if target==f else 'unchanged'
                            add(direct[result],phrase+tail,target,prior,result,'single', 'synthetic')
    for i,f in enumerate(SYMPTOMS):
        for j,g in enumerate(SYMPTOMS):
            if f==g:continue
            for p in PHRASES[f]['present'][:4]:
                for q in PHRASES[g]['present'][:2]+PHRASES[g]['absent'][:2]:
                    for prior in PREVIOUS:
                        for target in [f,g]:
                            result='present' if target==f or q in PHRASES[g]['present'] else 'absent'
                            add(special['multi'],p+' '+q,target,prior,result,'multiple','synthetic')
            for p in PHRASES[g]['present']:
                text='친구에게 '+WORDS[f]+' 증상이 있어요. '+p
                for prior in PREVIOUS:
                    for target in [f,g]:
                        add(special['other'],text,target,prior,'unchanged' if target==f else 'present','other_person','synthetic')
    for name,minimum in [('present',1000),('absent',1000),('unknown',1000),('unchanged',1000)]:
        if len(direct[name])<minimum:raise ValueError((name,len(direct[name])))
    selected=[]
    for name in ['present','absent','unknown','unchanged']:
        rng.shuffle(direct[name]);selected+=direct[name][:1000]
    for name in ['multi','other']:
        rng.shuffle(special[name])
        if len(special[name])<500:raise ValueError((name,len(special[name])))
        selected+=special[name][:500]
    # WOS source has no skin annotations. Conservative no-keyword filter, followed
    # by a provisional unchanged label; audit is still required by a person.
    terms=re.compile('피부|건조|여드름|뾰루지|트러블|붉|빨갛|홍조|따갑|따가|따끔|가렵|가려|가려움|간지럽|간질')
    wos=[]
    for dialog in pq.read_table(WOS,columns=['guid','dialogue']).to_pylist():
        for turn in dialog['dialogue']:
            if turn['role']!='user':continue
            text=turn['text'].strip()
            if not text or len(text)>200 or terms.search(text):continue
            for _ in range(1):
                target=rng.choice(SYMPTOMS);prior=rng.choice(PREVIOUS)
                add(wos,text,target,prior,'unchanged','wos_no_symptom',dialog['guid'])
    rng.shuffle(wos)
    if len(wos)<1000:raise ValueError('insufficient WoS utterances')
    selected+=wos[:1000]
    rng.shuffle(selected)
    if len(selected)!=6000 or len({(x['text'],x['field'],x['previous']) for x in selected})!=6000:raise ValueError('wrong count or duplicate decision')
    if testtexts&{r['text'] for r in selected}:raise ValueError('exact evaluation text overlap')
    DEST.mkdir(parents=True)
    (DEST/'train.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in selected),encoding='utf-8')
    (DEST/'heldout_cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest={'seed':601106,'examples':len(selected),'unique_utterances':len({r['text'] for r in selected}),
      'synthetic':5000,'klue_wos':1000,'outcomes':dict(Counter(r['decision'] for r in selected)),
      'categories':dict(Counter(r['category'] for r in selected)),'heldout_scenarios':len(cases),
      'heldout_turns':sum(len(c['turns']) for c in cases),'exact_utterance_overlap':0,
      'wos_file_sha256':hashlib.sha256(WOS.read_bytes()).hexdigest(),
      'caveat':'Automatically generated labels and fixed templates; not independently human reviewed. WoS is not skin-labeled.',
      'files':{n:hashlib.sha256((DEST/n).read_bytes()).hexdigest() for n in ['train.jsonl','heldout_cases.json']}}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
