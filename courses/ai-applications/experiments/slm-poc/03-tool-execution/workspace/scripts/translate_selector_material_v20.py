"""Local draft translation, separately cached and never treated as human gold."""
import copy,hashlib,json,re,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_interface_data_v18 import view
DATA=ROOT/'data/processed/selector-material-v20';MODEL=ROOT/'models/nllb-200-distilled-600m'
REV='f8d333a098d19b4fd9a8b18f94170487ad3f821d'

def readrows(p):return [json.loads(x) for x in p.read_text(encoding='utf8').splitlines() if x]
def legacy():
    rows=readrows(ROOT/'data/processed/tool-split-pilot-v1/selector_train.jsonl');out=[]
    for r in rows:
        if not r.get('tools') or r.get('target')=='no_tool' or r['target'] not in r.get('tool_keys',{}):continue
        if len(r.get('reference_calls',[]))!=1:continue
        out.append({'id':r['id'],'source_index':r.get('source_index'),'cohort':'legacy','tools':r['tools'],'messages':r['messages'],
            'expected':[r['tool_keys'][r['target']]],'provenance':'Actually used in original selector training; translated here by the same draft translator as new examples.'})
    out.sort(key=lambda r:hashlib.sha256(('legacy20'+r['id']).encode()).hexdigest())
    return out[:200]

def texts(row):
    def schema(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k=='description' and isinstance(v,str) and v.strip():yield v
                elif isinstance(v,(list,dict)):yield from schema(v)
        elif isinstance(x,list):
            for v in x:yield from schema(v)
    for m in row['messages']:
        if isinstance(m.get('content'),str) and m['content'].strip():yield m['content']
    for t in row['tools']:
        yield t['description'];yield from schema(t['parameters'])

def convert(row,cache):
    r=copy.deepcopy(row)
    def schema(x):
        if isinstance(x,dict):
            for k,v in list(x.items()):
                if k=='description' and isinstance(v,str) and v.strip():x[k]=cache[v]
                elif isinstance(v,(list,dict)):schema(v)
        elif isinstance(x,list):
            for v in x:schema(v)
    for m in r['messages']:
        if isinstance(m.get('content'),str) and m['content'].strip():m['content']=cache[m['content']]
    for t in r['tools']:t['description']=cache[t['description']];schema(t['parameters'])
    r['translation']='NLLB600M draft, not independent human verification; API names, keys, types, enum/default/required unchanged.'
    return r

def main():
    import torch
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer,AutoModelForSeq2SeqLM
    old=legacy();(DATA/'legacy-english.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in old),encoding='utf8')
    rows=readrows(DATA/'candidates.jsonl')+old;unique=sorted({x for r in rows for x in texts(r)},key=lambda s:(len(s),s))
    cachepath=DATA/'translation-cache.json';cache=json.loads(cachepath.read_text(encoding='utf8')) if cachepath.exists() else {}
    missing=[x for x in unique if x not in cache];print('DRAFT TRANSLATION',len(rows),'rows',len(unique),'unique strings',len(missing),'missing',flush=True)
    if not all((MODEL/n).exists() for n in ['pytorch_model.bin','tokenizer.json','sentencepiece.bpe.model','config.json']):
        snapshot_download('facebook/nllb-200-distilled-600M',revision=REV,local_dir=MODEL,
            allow_patterns=['config.json','generation_config.json','pytorch_model.bin','tokenizer.json','tokenizer_config.json','special_tokens_map.json','sentencepiece.bpe.model','README.md'])
    tok=AutoTokenizer.from_pretrained(MODEL,src_lang='eng_Latn',local_files_only=True)
    model=AutoModelForSeq2SeqLM.from_pretrained(MODEL,dtype=torch.float16,local_files_only=True).to('cuda').eval();torch.set_num_threads(4)
    started=time.perf_counter();rejected=[]
    for i in range(0,len(missing),24):
        group=missing[i:i+24];lengths=[len(tok(x,truncation=False)['input_ids']) for x in group]
        if max(lengths)>512:raise ValueError(('Translator source over512; no truncation',max(lengths)))
        batch=tok(group,padding=True,truncation=False,return_tensors='pt').to('cuda')
        with torch.inference_mode():
            y=model.generate(**batch,forced_bos_token_id=tok.convert_tokens_to_ids('kor_Hang'),max_new_tokens=384,num_beams=1,do_sample=False)
        for source,tokens in zip(group,y):
            if int(tokens[-1]) not in [tok.eos_token_id,tok.pad_token_id]:raise ValueError('Translation length cap reached')
            translated=tok.decode(tokens,skip_special_tokens=True).strip()
            if not translated:raise ValueError('Empty translation')
            cache[source]=translated
        cachepath.write_text(json.dumps(cache,ensure_ascii=False,indent=2),encoding='utf8')
        if i%120==0:print('translated',min(i+24,len(missing)),'/',len(missing),'seconds',round(time.perf_counter()-started),flush=True)
    for name,rs in [('new-draft',rows[:len(rows)-len(old)]),('legacy-draft',old)]:
        (DATA/(name+'.jsonl')).write_text(''.join(json.dumps({'original':r,'korean':convert(r,cache)},ensure_ascii=False)+'\n' for r in rs),encoding='utf8')
    (DATA/'translation-manifest.json').write_text(json.dumps({'repo':'facebook/nllb-200-distilled-600M','revision':REV,'license':'CC-BY-NC-4.0; research draft translation, not commercial deployment',
        'rows':len(rows),'unique_strings':len(unique),'cache_sha256':hashlib.sha256(cachepath.read_bytes()).hexdigest(),'human_verified':False,'training_started':False},indent=2),encoding='utf8')
    print('TRANSLATION COMPLETE',flush=True)
if __name__=='__main__':main()
