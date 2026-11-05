"""Explicit local adapter; never imports the production consumer or changes it."""
from copy import deepcopy
from .engine import PreviewEngine


def catalog_observations(entry, *, reference):
    """Reuse literal catalog facts. No pH, care-role or filter inference from INCI."""
    p=entry['product']
    result={}
    for source,target in [('product_id','product.identity'),('name','product.name'),('ph','product.ph'),('manufacturer','product.manufacturer')]:
        val=p.get(source)
        result[target]={'value':deepcopy(val),'state':'known' if val is not None else 'unknown',
                        'source':'catalog_record','reference':reference,'acquisition':'existing_catalog_record_not_new_label_verification'}
    return result


def evaluate_routine(context, products, *, engine=None):
    """One product instance per comparison; no cross-product fact flattening.

    Caller supplies reviewed per-instance observations (including usage). Pair
    comparisons require a separately reviewed use-event input to PreviewEngine.
    """
    engine=engine or PreviewEngine()
    if any(k.startswith('product.') for k in context.get('facts',{})):
        raise ValueError('Product observations must belong to a product instance')
    seen=set(); outputs=[]
    for product in products:
        pid=product['product_instance_id']
        if not pid or pid in seen:raise ValueError('Unique product instance required')
        seen.add(pid)
        if product['kind'] not in ('test','actual'):raise ValueError('Explicit product kind required')
        if product['kind']=='test' and context.get('data_kind')!='synthetic':raise ValueError('Test product in real context')
        request=deepcopy(context);request['product_instance_id']=pid
        for field,obs in product.get('facts',{}).items():
            previous=request['facts'].get(field)
            if previous is not None and previous!=obs:
                request['facts'][field]={'value':None,'state':'conflicting','source':obs['source'],
                                         'reference':obs['reference'],'alternatives':[previous,obs]}
            else:request['facts'][field]=deepcopy(obs)
        outputs.append(engine.evaluate(request))
    return outputs
