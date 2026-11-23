"""Generate isolated synthetic four-choice decision examples; never uses AI Hub."""
import hashlib
import json
import random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'data/processed/ko_decision_qlora_pilot_v1'
FIELDS={'dryness':'건조함','breakout':'여드름','redness':'붉어짐','stinging':'따가움','itching':'가려움'}
TEMPLATES={
 'train':{
 'present':['저는 {s} 증상이 있어요.','지금 제 피부에 {s}이 있어요.','제 증상은 {s}입니다.','오늘 제게는 {s}이 나타나요.'],
 'absent':['저는 {s} 증상이 없어요.','지금 제 피부에 {s}은 없어요.','제게 {s}은 전혀 없어요.','현재 제 증상 중에 {s}은 없습니다.'],
 'unknown':['저는 {s} 증상이 있는지 모르겠어요.','지금 제게 {s}이 있는지 확신이 없어요.','제 피부에 {s}이 있는지는 잘 몰라요.','현재 제 {s} 증상은 알 수 없어요.'],
 'unchanged':['안녕하세요. 오늘 상담받고 싶어요.','저는 오늘 밖에 나가지 않았어요.','피부 관리를 시작하고 싶습니다.','점심을 먹고 물을 마셨어요.']},
 'validation':{
 'present':['제 피부에는 {s} 증세가 있습니다.','오늘 제 피부에 {s}이 생겼어요.'],
 'absent':['지금 저는 {s} 증세가 없어요.','제 피부는 {s} 증상이 나타나지 않아요.'],
 'unknown':['제게 {s} 증상이 있는지 잘 모르겠습니다.','제 피부의 {s} 여부는 확실하지 않아요.'],
 'unchanged':['오늘 기분이 좋아요.','상담은 다음 주에 다시 할게요.']}}

def main():
    DEST.mkdir(parents=True,exist_ok=False)
    result={}
    for split,groups in TEMPLATES.items():
        rows=[]
        for field,symptom in FIELDS.items():
            for decision,templates in groups.items():
                for i,template in enumerate(templates):
                    for prior in ['unknown','present','absent']:
                        rows.append({'id':f'{split}-{field}-{decision}-{i}-{prior}','field':field,
                          'symptom_ko':symptom,'previous':prior,'text':template.format(s=symptom),
                          'decision':decision,'provenance':'synthetic template; not independently human reviewed'})
        random.Random(271828).shuffle(rows)
        result[split]=rows
        (DEST/f'{split}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
    train={r['text'] for r in result['train']};val={r['text'] for r in result['validation']}
    if train&val:raise ValueError('Text leakage across splits')
    manifest={'seed':271828,'splits':{k:len(v) for k,v in result.items()},'exact_train_validation_text_overlap':0,
      'data':'synthetic templates, 5 symptoms, 4 outcomes, three prior states; no human review',
      'sha256':{f'{k}.jsonl':hashlib.sha256((DEST/f'{k}.jsonl').read_bytes()).hexdigest() for k in result}}
    (DEST/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(manifest,ensure_ascii=False),flush=True)
if __name__=='__main__':main()
