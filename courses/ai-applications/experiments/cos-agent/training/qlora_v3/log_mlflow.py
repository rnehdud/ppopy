"""Import measured local QLoRA records into the repository's local MLflow only.

This imports an existing run; it does not execute training and never logs weights.
"""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;COS=HERE.parents[1];sys.path.insert(0,str(COS))
from common import read_rows,dump
from beauty_agent.afa.tracking import LocalTracker

def main():
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--report',required=True)
    p.add_argument('--store',help='Existing local outputs/afa-mlflow directory, when sharing across worktrees')
    a=p.parse_args();root=Path(a.run).resolve();report=Path(a.report).resolve()
    cfg=json.loads((root/'config.json').read_text(encoding='utf-8'))
    selection=json.loads((root/'selection.json').read_text(encoding='utf-8'))
    receipt=json.loads((root/'split_receipt.json').read_text(encoding='utf-8'))
    tracker=LocalTracker(a.store) if a.store else LocalTracker()
    params={**cfg,'train_rows':810,'val_rows':90,'dataset_sha256':receipt['dataset_sha256'],
        'code_version_at_import':subprocess.check_output(['git','rev-parse','HEAD'],cwd=COS,text=True).strip(),
        'selected_checkpoint':selection['checkpoint'],'loss_backend':selection.get('loss_backend','Transformers'),
        'generation_backend':selection.get('generation_backend','Transformers')}
    metrics={}
    for row in [selection['base'],*selection['epochs']]:
        tag=row['tag'];metrics[tag+'/val_token_loss']=row['val_token_loss']
        for key,value in row['counts'].items():metrics[tag+'/'+key]=value
    logs=read_rows(root/'training_log.jsonl')
    curves=[(row['global_step'],{'train/token_loss_so_far':row['token_loss_so_far'],
        'train/lr':row['lr'],'train/peak_allocated_mib':row['peak_allocated_mib']}) for row in logs]
    sources=[root/name for name in ['config.json','environment.json','split_receipt.json','training_log.jsonl','selection.json']]
    # Explicit report formats only; no recursive model/checkpoint artifact logging.
    sources += [p for p in report.iterdir() if p.is_file() and p.suffix in {'.json','.jsonl','.md','.png','.csv'}]
    assert all(p.suffix not in {'.safetensors','.bin','.pt','.pth'} for p in sources)
    run_id=tracker.publish('SLM-QLoRA-v3','Qwen3-4B-810train-90development',metrics=metrics,params=params,
        sources=sources,curves=curves,tags={'evaluation_scope':'development_only',
            'weights_uploaded':'false','semantic_review':'see actual review artifact; no human approval implied'})
    dump(root/'mlflow_receipt.json',{'run_id':run_id,'tracking_uri':tracker.uri,
        'record_kind':'posthoc_import_of_actual_measured_run','new_training_by_this_import':False,
        'weights_logged':False})
    print(json.dumps({'run_id':run_id,'weights_logged':False}))

if __name__=='__main__':main()
