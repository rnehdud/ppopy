"""고정 기준의 합성 후보에 검토된 PPO-39 보완을 재현해요.

KB·원래 검증기·출처 원문을 변경하거나 검수 승인을 생성하지 않아요.
현재 사람 검수 기록이 있거나 기준 외 변경이 있으면 덮어쓰지 않아요.
"""
from __future__ import annotations
from pathlib import Path
import csv,io,json,hashlib,subprocess
from collections import Counter
import build_additional_24 as common

V=Path(__file__).resolve().parent
COS=V.parents[2]
ROOT=COS.parents[3]
OUT=COS/'outputs/ppo39_20261124'
BASE='179cc358fe3b1819886f2c45070b2827db0c562a'
PREFIX='courses/ai-applications/experiments/cos-agent/data/qlora/v2/'
REVISION='ppo39-quality-20261124'

def base_bytes(name):
    return subprocess.run(['git','show',BASE+':'+PREFIX+name],cwd=ROOT,capture_output=True,check=True).stdout

def save(path,data):
    old=path.read_bytes() if path.exists() else None
    if old==data:return
    if old is not None:
        dest=OUT/'superseded'/path.relative_to(V)
        dest=dest.with_name(dest.name+'.'+hashlib.sha256(old).hexdigest()+'.previous')
        dest.parent.mkdir(parents=True,exist_ok=True)
        if not dest.exists():dest.write_bytes(old)
    path.write_bytes(data)

def json_bytes(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+'\n').encode('utf-8')

def main():
    manifest=json.loads((V/'ppo39_revisions.json').read_text(encoding='utf-8'))
    patches={p['row_id']:p for p in manifest['patches']}
    assert len(patches)==manifest['target_rows']==275
    for relative,digest in manifest['protected_hashes'].items():
        assert common.sha(ROOT/relative)==digest,relative
    names=manifest['dataset_names']
    old={};new={};hashes={};changed_files=[]
    for name in names:
        raw=base_bytes(name+'.jsonl').decode('utf-8').splitlines()
        lines=[]
        for line in raw:
            r=json.loads(line);rid=r['id'];old[rid]=json.loads(line)
            if rid in patches:
                p=patches[rid]
                assert p['before_row_sha256']==hashlib.sha256(line.encode('utf-8')).hexdigest()
                r['messages'][1]['content']=json.dumps(p['request'],ensure_ascii=False)
                r['messages'][2]['content']=p['answer']
                provenance=r['provenance']
                provenance['original_generator_model']=provenance.get('original_generator_model',provenance['generator_model'])
                provenance.update(generator_model='gpt-6.1-terra',revision_model='gpt-6.1-terra',critic_model=None,critic_status='unreviewed',human_review='unreviewed')
                line=json.dumps(r,ensure_ascii=False)
            new[rid]=r;lines.append(line)
            q=common.validator.SLMRequest.model_validate_json(r['messages'][1]['content'])
            hashes[rid]=common.validator.compute_row_content_sha256(q,r['messages'][2]['content'],card_ids=r['card_ids'],chunk_origins=r['chunk_origins'],is_hard_negative=r['is_hard_negative'],hard_negative_type=r['hard_negative_type'])
        if any(json.loads(line)['id'] in patches for line in raw):
            changed_files.append(name)
            data=(''.join(line+'\n' for line in lines)).encode('utf-8')
            assert (V/(name+'.jsonl')).read_bytes() in (base_bytes(name+'.jsonl'),data), '기준 밖 데이터 변경을 덮어쓰지 않아요.'
            save(V/(name+'.jsonl'),data)
        else:
            assert (V/(name+'.jsonl')).read_bytes()==base_bytes(name+'.jsonl')
    updated_cases={}
    for path in sorted(V.glob('additional*_part_[a-f].json')):
        obj=json.loads(path.read_text(encoding='utf-8'))
        if not any(c['id'] in patches for c in obj['cases']):continue
        for c in obj['cases']:
            rid=c['id']
            if rid not in patches:continue
            p=patches[rid];original=old[rid]['provenance']
            c['request']=p['request']
            c['input_sha256']=hashlib.sha256(common.canonical(p['request']).encode('utf-8')).hexdigest()
            c['original_generator_model']=original.get('original_generator_model',original['generator_model'])
            c['generator_model']=c['revision_model']='gpt-6.1-terra'
            history=c.setdefault('revision_history',[])
            if not any(h.get('revision')==REVISION for h in history):
                history.append({'revision':REVISION,'reason':p['reason'],'human_review':'unreviewed'})
            c['ppo39_slot_evidence']=p['slot_evidence']
            c['ppo39_fact_preservation_notes']=p['fact_preservation_notes']
            updated_cases[rid]=c
        frozen=path.with_name(path.stem+'_inputs.json')
        inp=json.loads(frozen.read_text(encoding='utf-8'))
        byid={c['id']:c for c in obj['cases']}
        inp['cases']=[{k:v for k,v in byid[c['id']].items() if k!='answer'} for c in inp['cases']]
        save(frozen,json_bytes(inp))
        for c in obj['cases']:
            if c['id'] in patches:c['answer']=patches[c['id']]['answer']
        save(path,json_bytes(obj))
    assert set(updated_cases)==set(patches)
    for name in changed_files:
        planpath=V/(name+'_plan.json')
        plan=json.loads(planpath.read_text(encoding='utf-8'))
        plan['cases']=[{k:v for k,v in updated_cases[c['id']].items() if k!='answer'} if c['id'] in patches else c for c in plan['cases']]
        plan['latest_revision']=REVISION
        save(planpath,json_bytes(plan))
        human=V/(name+'_human_review.csv')
        with human.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;records=list(reader)
        assert all(r['human_review']=='unreviewed' and not any(r.get(k) for k in ('reviewer','reviewed_at','notes')) for r in records)
        for r in records:
            if r['row_id'] in patches:r['content_sha256']=hashes[r['row_id']]
        stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');writer.writeheader();writer.writerows(records)
        save(human,stream.getvalue().encode('utf-8-sig'))
        rr=[r for r in new.values() if r['id'] in {c['id'] for c in plan['cases']}]
        text=['# PPO-39 보완 — '+name,'','`development_preview`, `production_enabled=false`, 합성 개발 후보이며 공식 인수·사람 승인이 아니에요.',
              '원문 관찰을 정형 슬롯과 연결하고 사례별 설명을 보완했어요. 전체 판단과 과거 기록은 README 및 `ppo39_revisions.json`을 확인해요.',
              'KB 판정은 비교 명세에 대한 작성 기록이며 엔진 실행이나 임상 결과가 아니에요. 저장 문헌 청크는 요약이며 외부 원전의 직접 인용이 아니에요.','']
        for r in rr:
            text += ['## '+r['id'],'','- 모드·분할: `'+r['mode']+'` / `'+r['split']+'`','- 현재 내용 해시: `'+hashes[r['id']]+'`','- 사람 검수: **미검수**','',
                     '### 입력 원문','','```json',json.dumps(json.loads(r['messages'][1]['content']),ensure_ascii=False,indent=2),'```','','### 응답 초안 — 미승인','',r['messages'][2]['content'],'']
        save(V/(name+'_review.md'),('\n'.join(text).rstrip()+'\n').encode('utf-8'))
    assert len(new)==648 and Counter(r['mode'] for r in new.values())=={'solution':496,'hold':152}
    receipt={'revision':REVISION,'target_rows':len(patches),'unchanged_rows':648-len(patches),'dataset_sha256':{name:common.sha(V/(name+'.jsonl')) for name in names},
             'human_approved':0,'official_cross_model_review_of_revised_rows':False,'content_sha256':{rid:hashes[rid] for rid in patches}}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'application_receipt.json').write_bytes(json_bytes(receipt))
    print(json.dumps({'changed_rows':len(patches),'unchanged_rows':648-len(patches),'datasets':changed_files}))

if __name__=='__main__':main()
