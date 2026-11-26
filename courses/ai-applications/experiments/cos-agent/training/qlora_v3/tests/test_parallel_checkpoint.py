"""Software-only protocol test: out-of-order completion and gapped resume.

Mock outputs live only in pytest's temporary directory; no model score is tested.
"""
import asyncio,json,sys
from pathlib import Path
import httpx
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import evaluate_vllm as evaluation
from common import dump,read_rows
from types import SimpleNamespace

def test_parallel_out_of_order_resume_preserves_every_row(tmp_path,monkeypatch):
    dataset=tmp_path/'data/qlora/v2/qlora_solution_hold_v2.jsonl';dataset.parent.mkdir(parents=True)
    rows=[{'id':f'r{i:03d}','split':'val_internal','mode':'solution' if i<60 else 'hold',
        'messages':[{'role':'system','content':'test'},{'role':'user','content':str(i)},
                    {'role':'assistant','content':'teacher test only'}]} for i in range(90)]
    dataset.write_text(''.join(json.dumps(r)+'\n' for r in rows),encoding='utf-8')
    root=tmp_path/'run';dump(root/'config.json',{'max_new_tokens':384,'selection':'test'})
    dump(root/'loss_summaries.json',{'base':{'tag':'base','val_token_loss':3.,'rows':90},
        'epochs':[{'tag':f'epoch-{i}','epoch':i,'rows':90,'val_token_loss':2./i} for i in [1,2]]})
    keys=['invalid_citation','kb_citation','distractor_id_citation','solution_missing_citation','hold_instruction_candidate','empty_response']
    metrics={**{k:False for k in keys},'guardrail_flags':[]}
    prior=[{'row_id':rows[i]['id'],'model':'ppopy-base-nf4','evaluation_concurrency':4,'text':'preserved',
        'metrics':metrics,'latency_s':.1,'finish_reason':'stop'} for i in [0,2]]
    (root/'base').mkdir();(root/'base/predictions.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in prior))
    monkeypatch.setattr(evaluation,'COS',tmp_path)
    monkeypatch.setattr(evaluation,'deterministic_metrics',lambda row,text:dict(metrics))
    active=0;peak=0;requested=[]
    async def handler(request):
        nonlocal active,peak
        if request.method=='GET':return httpx.Response(200,json={'data':[]})
        payload=json.loads(request.content);i=int(payload['messages'][1]['content'])
        assert payload['max_tokens']==384 and payload['temperature']==0 and payload['stream'] is False
        requested.append((payload['model'],i));active+=1;peak=max(peak,active)
        await asyncio.sleep(.01 if i%4==1 else .001);active-=1
        return httpx.Response(200,json={'choices':[{'message':{'content':f'test {i}'},'finish_reason':'stop'}],
            'usage':{'completion_tokens':3}})
    actual_client=httpx.AsyncClient
    monkeypatch.setattr(httpx,'AsyncClient',lambda **kwargs:actual_client(transport=httpx.MockTransport(handler),**kwargs))
    asyncio.run(evaluation.run(SimpleNamespace(run=root,base_url='http://test/v1',concurrency=4)))
    assert peak==4 and len(requested)==268
    assert ('ppopy-base-nf4',0) not in requested and ('ppopy-base-nf4',2) not in requested
    for path in [root/'base/predictions.jsonl',root/'epoch-1/evaluation/predictions.jsonl',root/'epoch-2/evaluation/predictions.jsonl']:
        actual=read_rows(path);assert [r['row_id'] for r in actual]==[r['id'] for r in rows]
        assert len({r['row_id'] for r in actual})==90
    assert read_rows(root/'base/predictions.jsonl')[2]['text']=='preserved'
    assert json.loads((root/'selection.json').read_text())['semantic_review_pending'] is True
