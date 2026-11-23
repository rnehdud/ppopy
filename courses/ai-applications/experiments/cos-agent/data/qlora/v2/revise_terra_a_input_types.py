"""Apply identified variable-name fixes once to archived candidate inputs."""
import hashlib,json
from pathlib import Path
H=Path(__file__).resolve().parent; P=H/'additional_100_terra_part_a_inputs.json'
D=json.loads(P.read_text(encoding='utf-8')); C={x['id']:x for x in D['cases']}
if len(C)!=34 or 'storage.refill' not in C['syn-sol-0122']['request']['confirmed_observations']: raise RuntimeError('Already revised or unexpected input')
for ident,old,new in [('syn-sol-0122','storage.refill','storage.sharing_refill'),('syn-hold-0040','device.use','adjunct.device_use'),('syn-hold-0041','device.use','adjunct.device_use')]:
 obs=C[ident]['request']['confirmed_observations']; v=obs.pop(old); v['variable_id']=new; obs[new]=v
v=C['syn-sol-0123']['request']['confirmed_observations']['storage.instance_id']; v['value']='synthetic-container-a'
for c in C.values(): c['input_sha256']=hashlib.sha256(json.dumps(c['request'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()
P.write_text(json.dumps(D,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
