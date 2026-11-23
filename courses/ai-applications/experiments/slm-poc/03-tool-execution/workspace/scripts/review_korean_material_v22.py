"""Mechanical guards plus recorded assistant whole-utterance review, not human gold."""
import copy,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.selector_korean_data_v22 import DATA,MODEL,view,read,read_jsonl,save,digest

MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']
def numbers(s):
    # English month names may be immediately followed by a Korean particle.
    for i,m in enumerate(MONTHS,1):s=re.sub(r'(?<![A-Za-z])'+m+r'(?![A-Za-z])',str(i),s)
    s=re.sub(r'\bone(?=\s+year\b)','1',s,flags=re.I)
    return sorted(re.findall(r'\d+(?:[.,]\d+)*',s))
def flags(s,t):
    out=[]
    if numbers(s)!=numbers(t):out.append('numeric_literal_difference')
    for literal in re.findall(r'"([^"\n]+)"',s):
        if literal not in t:out.append('double_quoted_literal_missing:'+literal)
    if re.search(r'\bif\b',s,re.I) and not any(x in t for x in ['면','경우','는지','인지','한지','했는지','되었는지']):out.append('condition_unverified')
    if re.search(r'\bnot\b|\bwithout\b|n\x27t\b',s,re.I) and not any(x in t for x in ['없','않','아니','못','아닌','안 ','말']):out.append('negation_unverified')
    if not any('\uac00'<=c<='\ud7a3' for c in t):out.append('not_Korean')
    return out

def main():
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);tok.model_max_length=1000000
    translations={}
    for f in sorted(DATA.glob('translations-??.json')):
        x=read(f)
        if set(translations)&set(x):raise ValueError('Duplicate translation ID')
        translations.update(x)
    worksheet=read_jsonl(DATA/'translation-worksheet.jsonl')
    if set(translations)!={r['id'] for r in worksheet}:raise ValueError('Translation coverage wrong')
    originals={r['id']:r for rs in read(DATA/'selection.json').values() for r in rs};findings={};lengths={}
    for w in worksheet:
        i=w['id'];t=translations[i];fs=flags(w['source'],t)
        r=copy.deepcopy(originals[i]);r['cohort']='korean_v22';r['messages'][-1]['content']=t;v=view(r,'current_full')
        n=max(map(len,tok([v['question']+' '+s for s in v['options'].values()],[v['context']]*len(v['options']),truncation=False)['input_ids']));lengths[i]=n
        if n>512:fs.append('over512:'+str(n))
        if fs:findings[i]=fs
    save(DATA/'translation-check.json',{'n':len(worksheet),'findings':findings,'max_tokens':max(lengths.values()),'lengths':lengths,'no_selector_inference':True,'not_semantic_proof':True})
    print('TRANSLATION CHECK',len(worksheet),'max',max(lengths.values()),'findings',json.dumps(findings,ensure_ascii=False),flush=True)
    if findings:raise ValueError('Review or length guards not passed; no training')
    save(DATA/'translations.json',translations)
    # Written only after the assistant has read and translated every complete
    # worksheet row and rechecked the output. This records that review, not an
    # independent automatic semantic-equivalence test.
    save(DATA/'language-review.json',{'reviewer':'assistant: same author as translation; not independent human confirmation','translation_sha256':digest(DATA/'translations.json'),
        'scope':'All160 complete source/translated utterances read. Target omitted from translation worksheet. Tools and schema descriptions remain unmodified English. No V20 translation reused.',
        'checks':'Requested work, actor, target, order, conditions, negation, relative time, units, numbers, quoted names and data checked against source. Mechanical guards supplement but do not prove semantic equivalence.',
        'corrections_before_freeze':['Engineering typo corrected to 공학','HSL hue rendered 색조, not generic 색상','Wet-road handling rendered 핸들링'],
        'rows':{w['id']:{'accepted':True,'source_sha256':__import__('hashlib').sha256(w['source'].encode()).hexdigest(),'Korean_sha256':__import__('hashlib').sha256(translations[w['id']].encode()).hexdigest(),'full_utterance_reviewed':True,'max_tokens':lengths[w['id']]} for w in worksheet}})
if __name__=='__main__':main()
