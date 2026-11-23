"""Freeze source-reviewed Korean choice material; no prediction-based selection."""
import copy,collections,csv,hashlib,json,random,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_interface_data_v18 import MODEL,SELECTOR,view,read,read_jsonl,save,digest,verify as verify_previous
from scripts.build_tool_decision_mix_v1 import norm
from scripts.translate_selector_material_v20 import texts
MATERIAL=ROOT/'data/processed/selector-material-v20';DATA=ROOT/'data/processed/selector-broad-v20';OUT=ROOT/'output/diagnostics/selector-broad-v20';SEED=200081
OLD_HOLD_INDICES={0,5,10,11,13,28,32,44,53,59,62,92}

def signature(s):
    letters=[c for c in s if c.isalpha()]
    if letters and sum(c.isascii() for c in letters)/len(letters)<.8:return ''
    ignore={'retrieve','retrieves','get','gets','fetch','fetches','return','returns','provide','provides','information','data','details','detail','the','a','an','of','for','about','specific','given','current','specified'}
    words=re.findall('[a-z0-9]+',s.lower())
    return ' '.join(sorted(w for w in words if w not in ignore))

def identities(r):
    return {k for t in r['tools'] for k in [('name',norm(t['name'])),('description',norm(t['description'])),('purpose',signature(t['description']))] if k[1]}

def groups(rows):
    parent=list(range(len(rows)));seen={}
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,r in enumerate(rows):
        for key in identities(r):
            if key in seen:parent[root(i)]=root(seen[key])
            else:seen[key]=i
    out={}
    for i,r in enumerate(rows):out.setdefault(root(i),[]).append(r)
    return list(out.values())

def stripped(x):
    if isinstance(x,dict):return {k:stripped(v) for k,v in x.items() if not(k=='description' and isinstance(v,str))}
    if isinstance(x,list):return [stripped(v) for v in x]
    return x

def translation_flags(original,cache):
    flags=[]
    for s in texts(original):
        t=cache[s]
        # Conservative removal rather than silently accepting lost numeric literals.
        months=['January','February','March','April','May','June','July','August','September','October','November','December']
        numeric_source=s
        for n,month in enumerate(months,1):numeric_source=re.sub(r'\b'+month+(r'(?!\s+I\b)' if month=='May' else '')+r'\b',str(n),numeric_source)
        if sorted(re.findall(r'\d+',numeric_source))!=sorted(re.findall(r'\d+',t)):flags.append({'kind':'numeric_literal_changed','source':s,'korean':t})
        if len(t)>3*len(s)+100:flags.append({'kind':'possible_added_explanation','source':s,'korean':t})
        if len(s)>160 and len(t)<len(s)*.25:flags.append({'kind':'possible_omitted_source','source':s,'korean':t})
        if s.startswith('Role definition:') and not any(x in t for x in ['역할','질문자','응답자']):flags.append({'kind':'history_wrapper_not_translated','source':s,'korean':t})
        if re.match(r'^(네[, .!]|물론|알겠습니다)',t) and not re.match(r'^(yes|sure|okay)',s,re.I):flags.append({'kind':'possible_answer_instead_of_translation','source':s,'korean':t})
        if re.search(r'\b(?:not|without)\b|n\x27t\b',s,re.I) and not any(x in t for x in ['않','없','아니','말','안 ','제외','비활성']):flags.append({'kind':'negation_needs_review','source':s,'korean':t})
        if re.search(r'\bif\b',s,re.I) and not any(x in t for x in ['면','경우','때','여부','인지','는지','한지','일지']):flags.append({'kind':'condition_needs_review','source':s,'korean':t})
    return flags

def prepare():
    verify_previous()
    if DATA.exists() or OUT.exists():raise FileExistsError('Final material protected')
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    cache=read(MATERIAL/'translation-cache-qwen3.json');decisions=read(MATERIAL/'source-review.json')['decisions'];read(MATERIAL/'translation-qwen-manifest.json')
    translation_failed=read(MATERIAL/'translation-failed-qwen3.json')
    language_review=read(MATERIAL/'paired-language-review.json') if (MATERIAL/'paired-language-review.json').exists() else None
    language_holds={} if language_review is None else language_review.get('held_ids',{})
    previous=read_jsonl(ROOT/'data/processed/tool-split-pilot-v1/selector_train.jsonl')
    native=read_jsonl(MATERIAL/'legacy-candidates.jsonl')
    if not {r['id'] for r in native}<={r['id'] for r in previous}:raise ValueError('Native replay not in actual prior training')
    known=set()
    for r in previous:
        if r.get('tools'):known|=identities(r)
    for r in read_jsonl(ROOT/'data/processed/selector-interface-v18/reference.jsonl'):known|=identities(r)
    for r in native:known|=identities(r)
    known_queries={norm(r.get('input','')) for r in previous if r.get('input')}
    prior_ids={i for src in read(MATERIAL/'exposure-audit.json')['sources'] for i in src['source_ids']}
    raw_source=read(ROOT/'data/raw/tool-decision-mix-v1/toolace.json')
    for i in prior_ids:
        if 0<=i<len(raw_source):known_queries.update(norm(m['value']) for m in raw_source[i]['conversations'] if m['from']=='user')
    accepted=[];rejected=[];legacy=[]
    for kind,filename in [('new','new-qwen-draft.jsonl'),('legacy','legacy-qwen-draft.jsonl')]:
        for i,pair in enumerate(read_jsonl(MATERIAL/filename)):
            original=pair['original'];r=pair['korean'];reason=None;flags=translation_flags(original,cache)
            if r['id'] in language_holds:reason='paired_language_review_hold'
            if any(s in translation_failed for s in texts(original)):reason='translation_did_not_finish'
            if stripped(original['tools'])!=stripped(r['tools']):raise ValueError('API/schema literals changed')
            if original['expected']!=r['expected']:raise ValueError('Labels changed')
            if kind=='new' and identities(original)&known:reason='previous_tool_identity_or_shallow_alias'
            if kind=='new' and norm(original['messages'][-1]['content']) in known_queries:reason='previous_query_text'
            if kind=='legacy' and i in OLD_HOLD_INDICES:reason='source_review_ambiguous_or_underspecified'
            if flags:reason=reason or 'translation_check_flag'
            v=view(r,'current_full');n=max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
            if n>512:reason=reason or 'korean_full_view_over512'
            if not any('\uac00'<=c<='\ud7a3' for c in r['messages'][-1]['content']):reason=reason or 'no_korean_query'
            if reason:rejected.append({'id':r['id'],'kind':kind,'reason':reason,'flags':flags,'tokens':n});continue
            r['max_tokens']=n;r['task_kind']=decisions[r['id']]['task_kind'] if kind=='new' else 'legacy_replay'
            r['original_tools']=original['tools'];r['original_messages']=original['messages']
            (accepted if kind=='new' else legacy).append(r)
    # Already-Korean replay uses its complete original source schemas/history,
    # not translated boilerplate or the earlier shortened option descriptions.
    native_kept=[]
    for r in native:
        v=view(r,'current_full');n=max(map(len,tok([v['question']+' '+x for x in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']))
        if n>512:raise ValueError('Native replay length changed')
        r['max_tokens']=n;r['task_kind']='legacy_native_replay';r['original_tools']=copy.deepcopy(r['tools']);r['original_messages']=copy.deepcopy(r['messages'])
        r['provenance']='Previously trained native Korean positive; restored complete schema and complete source prefix, not independently verified gold.'
        native_kept.append(r)
    legacy=native_kept+legacy
    # Source English AND translated identities connect aliases. Entire connected
    # components stay on one side, including tools that are only distractors.
    components=groups([{**r,'tools':r['original_tools']+r['tools']} for r in accepted])
    byid={r['id']:r for r in accepted};components=[[byid[r['id']] for r in g] for g in components]
    components.sort(key=lambda g:hashlib.sha256(('split20'+min(r['id'] for r in g)).encode()).hexdigest())
    quota=None
    for train_n,test_n in [(160,80),(120,80),(80,60)]:
        if len(accepted)>=train_n+test_n and len(legacy)>=train_n//2:quota=(train_n,test_n);break
    if not quota:
        save(MATERIAL/'material-shortage.json',{'eligible_new':len(accepted),'eligible_legacy':len(legacy),'counts':dict(collections.Counter(x['reason'] for x in rejected)),'rejected':rejected,'training_started':False})
        raise ValueError('Insufficient checked material; do not train')
    train_n,test_n=quota;test=[];pool=[]
    for g in components:
        if len(test)+len(g)<=test_n:test+=g
        else:pool+=g
    if len(test)!=test_n or len(pool)<train_n:raise ValueError('Tool-group split cannot meet quota')
    pool.sort(key=lambda r:hashlib.sha256(('train20'+r['id']).encode()).hexdigest());train=pool[:train_n]
    # Both sides have diverse whole source tool definitions, never a generated
    # four-operation skeleton. Preserve original 2-6 candidate counts.
    if len({r['expected'][0] for r in test})<test_n*.7:raise ValueError('Too few distinct held-out targets')
    old=legacy[:train_n//2];mixed=train[:train_n//2]+old
    def shuffle_options(rows):
        for r in rows:
            random.Random(SEED+int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)).shuffle(r['tools'])
    shuffle_options(train);shuffle_options(test);shuffle_options(old)
    # Shared new rows in the two conditions keep exactly the same input order.
    fit_probe=[]
    for kind,rs in [('new_training',train[:train_n//2]),('legacy_training',old)]:
        chosen=sorted(rs,key=lambda r:hashlib.sha256(('fit20'+r['id']).encode()).hexdigest())[:24]
        for r in chosen:
            c=copy.deepcopy(r);c['fit_probe_kind']=kind;fit_probe.append(c)
    sets={'new_train':train,'mixed_train':mixed,'fresh':test,'fit_probe':fit_probe}
    if '--preview' in sys.argv:
        save(MATERIAL/'preparation-preview.json',{'eligible_new':len(accepted),'eligible_legacy':len(legacy),'native_legacy':len(native_kept),'quota':quota,
            'rejected':rejected,'proposed_ids':{k:[r['id'] for r in rs] for k,rs in sets.items()},'no_inference':True})
        print('PREVIEW',len(accepted),len(legacy),'quota',quota,'rejections',dict(collections.Counter(r['reason'] for r in rejected)),flush=True);return
    if language_review is None or language_review['cache_sha256']!=digest(MATERIAL/'translation-cache-qwen3.json'):raise ValueError('Paired language review missing/stale')
    DATA.mkdir(parents=True);OUT.mkdir(parents=True)
    for name,rows in sets.items():(DATA/(name+'.jsonl')).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf8')
    with (DATA/'review.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.writer(f);w.writerow(['split','id','kind','original_request','korean_request','source_target','original_candidate_purposes','korean_candidate_purposes'])
        for split in ['new_train','mixed_train','fresh']:
            for r in sets[split]:w.writerow([split,r['id'],r['task_kind'],r['original_messages'][-1]['content'],r['messages'][-1]['content'],r['expected'][0],json.dumps({t['name']:t['description'] for t in r['original_tools']},ensure_ascii=False),json.dumps({t['name']:t['description'] for t in r['tools']},ensure_ascii=False)])
    save(DATA/'material-review.json',{'eligible_new':len(accepted),'eligible_legacy':len(legacy),'eligible_native_legacy':len(native_kept),'rejected':rejected,
        'legacy_review':'All100 English replay source requests, purposes and target names read by assistant; flagged positions held. Native39 come from actual earlier positive training rows with complete source schemas/history. No independent human verification.',
        'source_label_scope':'Source-first-call matching plus assistant purpose review, no real execution. Ordered/dependent requests preserved completely and scored as next-tool selection, not single-purpose tasks.',
        'translation_quality':'Local Qwen draft, schema literal preservation and conservative numeric/negation/condition checks; paired language review still documented separately. No claim of certified or independent human translation.',
        'no_numeric_padding':'2-6 native candidate counts retained; no invented distractors to claim 8-candidate coverage.'})
    files=list(DATA.glob('*'))+[MATERIAL/n for n in ['exposure-audit.json','source-review.json','translation-cache-qwen3.json','translation-qwen-manifest.json']]
    files += [MATERIAL/n for n in ['legacy-candidates.jsonl','legacy-english.jsonl','new-qwen-draft.jsonl','legacy-qwen-draft.jsonl','translation-failed-qwen3.json','paired-language-review.json']]
    files += [ROOT/p for p in ['scripts/selector_broad_data_v20.py','scripts/selector_broad_v20.py','scripts/report_selector_broad_v20.py','tests/test_selector_broad_v20.py','scripts/selector_learning_v18.py','output/次のツール選択学習の判断-v19.txt']]
    files += [ROOT/p for p in ['scripts/translate_selector_qwen_v20.py','scripts/translate_selector_material_v20.py','scripts/selector_review_v20.py','scripts/selector_material_audit_v20.py','data/raw/tool-decision-mix-v1/toolace.json','data/raw/kotraj-v02/train-00000-of-00001.parquet']]
    files += [ROOT/'data/processed/tool-split-pilot-v1/selector_train.jsonl']
    files += [ROOT/'scripts/audit_selector_broad_v20.py']
    files += [ROOT/'scripts/restore_legacy_schema_v20.py']
    save(DATA/'protocol.json',{'frozen_files':{str(p.relative_to(ROOT)):digest(p) for p in files},'seed':SEED,'condition':'current_full','lr':1e-5,'logical_batch':4,'steps':train_n//4,
        'gradient_checkpointing':{'enabled':True,'use_reentrant':False,'reason':'Shared GPU with a separate user job. Same memory-saving training setup in both arms, inference unchanged.'},
        'train_n':train_n,'test_n':test_n,'mixed_new_n':train_n//2,'mixed_legacy_n':len(old),
        'adaptation':'After exposure and source/translation checks, shrink planned400+400 and200 fresh before any new inference. New-only vs half-new/half-old, fixed total and update count. Ordered first-next-tool source tasks kept intact and reported separately.',
        'summary':{name:{'n':len(rows),'kinds':dict(collections.Counter(r['task_kind'] for r in rows)),'candidate_counts':dict(collections.Counter(len(r['tools']) for r in rows))} for name,rows in sets.items()},
        'scope':'Tool-name, normalized-description and shallow-purpose-component separated from recorded prior exposures and current added training. Semantic review is assistant-only, not exhaustive; arbitrary unseen-domain or base-pretraining absence not guaranteed. Single next-tool capability only; all have a corresponding tool, no rejection/argument/execution metric.',
        'adoption':'Each final arm compared once: fresh correct strictly higher than baseline, >=90%, no loss in single/ordered/history subgroups, FunctionChat>=278/400, V16>=175/200 and V16 needed>=70/80. Final step only, no tuning using fresh results. Passing means candidate for further confirmation, not deployment.',
        'fit_probe':'24 shared new training rows +24 legacy training rows fixed by ID hash. Auxiliary fit check only, never checkpoint/threshold selection.',
        'stop':'Both final arms trained before fresh scoring. Finish once and report failures; do not add rounds after observing test. No production/state/response-model changes.'})
    print('MATERIAL FROZEN',json.dumps(read(DATA/'protocol.json')['summary'],ensure_ascii=False),flush=True)

def verify():
    verify_previous();p=read(DATA/'protocol.json')
    for rel,h in p['frozen_files'].items():
        if digest(ROOT/rel)!=h:raise ValueError('Frozen V20 material changed: '+rel)
    return p
if __name__=='__main__':prepare()
