from __future__ import annotations
import hashlib
import json
from pathlib import Path
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_KB = ROOT / 'KB/Poppy_KB_v0.6/Poppy_KB_seed_v0.6.json'
STATUSES = {'aligned','difference','unknown','conflicting','not_applicable','exception'}
SOURCES = {'user_report','product_label','service_default','literature','synthetic_fixture','catalog_record','automated_extraction'}
STATES = {'known','unknown','not_asked','declined','conflicting','not_applicable'}


def load_kb(path=DEFAULT_KB):
    raw = Path(path).read_bytes()
    kb = json.loads(raw)
    if kb['metadata']['version'] != '0.6.0-draft' or kb['metadata']['production_enabled'] is not False:
        raise ValueError('Only inactive v0.6 preview is supported')
    def index(rows):
        ids = [r['id'] for r in rows]
        if len(ids) != len(set(ids)): raise ValueError('Duplicate ID')
        return set(ids)
    sources = index(kb['source_registry'])
    cards = index(kb['baseline_cards'])
    index(kb['variables'])
    index(kb['acceptance_scenarios'])
    for c in kb['baseline_cards']:
        if c['active'] is not False or c['review']['production_enabled'] is not False:
            raise ValueError('Active card not allowed in this development module')
        if not set(c['evidence']['source_ids']) <= sources: raise ValueError('Dangling evidence')
        if not set(c['related_card_ids']) <= cards: raise ValueError('Dangling card')
        for name in ('aligned_when','difference_when','unknown_when','exception_when'):
            if not c['comparison_spec'].get(name): raise ValueError('Missing comparison schema')
        for name in ('on_aligned','on_known_difference','on_unknown','on_exception'):
            if not isinstance(c['recommendation'].get(name), str): raise ValueError('Missing recommendation')
    for s in kb['acceptance_scenarios']:
        if not set(s['card_ids']) <= cards: raise ValueError('Dangling scenario card')
    return kb, hashlib.sha256(raw).hexdigest()


class PreviewEngine:
    def __init__(self, path=DEFAULT_KB):
        self.kb, self.sha = load_kb(path)
        self.cards = {c['id']: c for c in self.kb['baseline_cards']}
        self.sources = {s['id']: s for s in self.kb['source_registry']}
        self.acquisition = {a['variable_id']: a for a in self.kb['acquisition_items']}
        self.variables = {v['id']: v for v in self.kb['variables']}
        self.rules = json.loads(Path(__file__).with_name('rules.json').read_text())
        if set(self.rules)!=set(self.cards):raise ValueError('Every KB card requires a development mapping')
        for cid, branches in self.rules.items():
            if cid not in self.cards: raise ValueError('Unknown mapped card')
            for b in branches:
                if not isinstance(b.get('when'),dict) or any(not isinstance(v,list) or not v for v in b['when'].values()):raise ValueError('Invalid condition predicate')
                origin=self.cards[cid]['scope'] if b['kb_clause']=='scope' else self.cards[cid]['comparison_spec'][b['kb_clause']]
                if b.get('kb_text')!=origin:raise ValueError('Compiled predicate source drift')
                if b['status'] not in STATUSES or not set(b['actions']) <= set(self.kb['comparison_contract']['action_types']):
                    raise ValueError('Invalid rule mapping')

    def evaluate(self, request):
        from .special import compare
        if request.get('mode') != 'development_preview' or request.get('project') != 'Poppy':
            raise ValueError('Poppy development preview only; AFA/production rejected')
        if request.get('data_kind') not in ('synthetic','local_review'):
            raise ValueError('Explicit data_kind required')
        facts=request.get('facts',{})
        if not isinstance(facts,dict):raise ValueError('facts must be an object')
        for key,obs in facts.items():
            if not isinstance(obs,dict) or obs.get('source') not in SOURCES or obs.get('state') not in STATES:
                raise ValueError('Observation requires source/state: '+key)
            if obs['source']=='synthetic_fixture' and request['data_kind']!='synthetic':raise ValueError('Synthetic observation in real review')
            if obs['state']=='known' and obs.get('value') is None:raise ValueError('Known null')
            if not isinstance(obs.get('reference'),str) or not obs['reference'].strip():raise ValueError('Observation reference required')
        def value(field):
            obs=facts.get(field,{})
            if obs.get('state')!='known' or obs.get('source') in ('service_default','literature'):return None
            return obs.get('value')
        def matches(condition):return all(value(f) in allowed for f,allowed in condition.items())
        stage=request.get('lifecycle_stage')
        if stage is not None and stage not in {s['id'] for s in self.kb['lifecycle_taxonomy']['stages']}:raise ValueError('Unknown lifecycle stage')
        selected=request.get('card_ids')
        if selected is None:
            selected=[cid for cid,c in self.cards.items() if (set(c['observable_inputs'])|{f for b in self.rules[cid] for f in b['when']}) & facts.keys()]
        if stage is not None and request.get('card_ids') is None:
            selected=[cid for cid in selected if stage in self.cards[cid]['lifecycle_stage_ids']]
        if not isinstance(selected,list) or any(cid not in self.cards for cid in selected):raise ValueError('Unknown card selector')
        results=[]
        for cid in dict.fromkeys(selected):
            c=self.cards[cid]; branches=self.rules[cid]
            fields=set(c['observable_inputs'])|{f for b in branches for f in b['when']}
            fields.update(['context.individual_instruction','person.clinician_plan','method.body_site','product.instructions'])
            if cid=='B-G11':fields.update(['storage.expiry','storage.pao','storage.sensory_change','commerce.authenticity_concern'])
            status,actions,reason='unknown',['ask_targeted_question','retrieve_product_evidence'],'insufficient_observations'
            matched=None
            for b in branches:
                if matches(b['when']):
                    status,actions,reason=b['status'],list(b['actions']),b['reason'];matched=b;break
            special=compare(cid,value,self.kb)
            if special:
                status,actions,reason=special['status'],special['actions'],special['reason']
                fields.update(special['fields']);matched=None
            if cid in ('B-G13','B-G14','B-G15') and status=='difference':
                fields.add('product.reviewed_role_pair')
                pair=next(p for p in self.kb['combination_policy']['pairs'] if p['card_id']==cid)
                roles=value('product.reviewed_role_pair')
                if not isinstance(roles,list) or len(roles)!=2 or set(roles)!={pair['left'],pair['right']}:
                    status,actions,reason='unknown',['retrieve_product_evidence'],'reviewed_role_pair_missing'
            # No factual conclusion can bypass contradictory observations.
            if any(facts.get(f,{}).get('state')=='conflicting' or value(f)=='conflicting' for f in fields):
                status,actions,reason='conflicting',['retrieve_product_evidence'],'conflicting_observations'
            if value('product.instructions')=='specific_instruction_overrides_general':
                status,actions,reason='exception',['review_current_label_scope','review_exception'],'specific_label_instruction'
            if value('context.individual_instruction') is True or value('person.clinician_plan') in ('individual_plan','specific_plan','confirmed_individual_plan'):
                status,actions,reason='exception',['review_exception'],'individual_instruction'
            site=value('method.body_site') or request.get('body_site')
            if request.get('population') != 'adult':
                status,actions,reason='not_applicable',['review_exception'],'outside_adult_scope'
            elif value('method.body_site') and request.get('body_site') and value('method.body_site')!=request['body_site']:
                status,actions,reason='conflicting',['review_exception'],'body_site_context_conflict'
            elif site is None:
                status,actions,reason='unknown',['ask_targeted_question'],'body_site_missing';fields.add('method.body_site')
            elif site not in ('face','hands','body','scalp') or (site!='face' and cid.startswith('B-C')):
                status,actions,reason='not_applicable',['review_exception'],'outside_card_body_site'
            elif status not in ('conflicting','exception') and cid in ('B-M04','B-L02') and site!='hands' and not any(f.startswith('hand.') or f=='skin.hand_observation' for f in facts):
                # Explicit hand observations are themselves a separate site context.
                status,actions,reason='unknown',['ask_targeted_question','inform_general_practice','defer_specific_recommendation'],'hand_context_not_present'
            if cid=='B-C03' and (value('product.regulatory_type')=='chemical_depilatory' or value('shaving.preparation')=='label_compliant'):
                status,actions,reason='not_applicable',['review_current_label_scope'],'not_ordinary_face_cleanser'
            if cid in ('B-H01','B-B01') and value('skin.pain')=='new_severe':
                status,actions,reason='exception',['refer_for_professional_review'],'individual_review_required'
            if cid in ('B-G01','B-G11','B-G17') and value('person.known_allergies') in ('confirmed_product_allergen','previous_severe_reaction'):
                status,actions,reason='exception',['defer_specific_recommendation','refer_for_professional_review'],'known_allergen_or_severe_history'
            if cid=='B-G11' and (value('storage.expiry')=='confirmed_expired' or value('storage.pao')=='confirmed_exceeded'
                or value('commerce.authenticity_concern')=='specific_concern'
                or value('storage.sensory_change') in ('new_odor_and_texture','new_separation','new_color','new_texture')):
                status,actions,reason='exception',['defer_specific_recommendation'],'quality_issue_precludes_local_trial'
            if cid=='B-H01' and (value('cycle.observation_consent') in ('declined','not_applicable') or facts.get('cycle.observation_consent',{}).get('state') in ('declined','not_applicable')):
                status,actions,reason='not_applicable',['inform_general_practice'],'cycle_consent_not_given'
            if cid=='B-H02' and facts.get('routine.change_log',{}).get('state') in ('declined','not_applicable'):
                status,actions,reason='not_applicable',['inform_general_practice'],'optional_changes_not_reported'
            if matched and reason!=matched['reason']:matched=None
            missing=[f for f in sorted(fields) if value(f) is None and f not in ('context.individual_instruction','person.clinician_plan','method.body_site')]
            if reason=='body_site_missing':missing=['method.body_site']
            if special and special['fields'] and status=='unknown':missing=[f for f in special['fields'] if value(f) is None or f=='dose.contact_time']
            if special and status=='conflicting' and 'ask_targeted_question' in actions:missing=list(special['fields'])
            if special and status=='unknown':missing=sorted(set(missing+special.get('clarify_fields',[])))
            unrecognized=[f for f in (special or {}).get('clarify_fields',[]) if value(f) is not None]
            if status=='unknown' and reason=='insufficient_observations':
                for f in fields:
                    allowed=[v for b in branches for v in b['when'].get(f,[])]
                    if allowed and value(f) is not None and value(f) not in allowed:
                        unrecognized.append(f)
                missing=sorted(set(missing+unrecognized))
            questions=[]
            if 'ask_targeted_question' in actions and status in ('unknown','conflicting'):
                for f in missing:
                    v=self.variables.get(f,{})
                    if facts.get(f,{}).get('state') in ('declined','not_applicable'):continue
                    if v.get('consumer_question_allowed') is not True or f.startswith('product.'):continue
                    if f.startswith('cycle.') and value('cycle.observation_consent')!='accepted' and f!='cycle.observation_consent':continue
                    a=self.acquisition.get(f,{})
                    questions.append({'field':f,'text':a.get('question_example') or f"{v.get('label',f)}에 대해 알려주세요.",'wording_status':'development_draft','card_ids':[cid]})
            key={'aligned':'on_aligned','difference':'on_known_difference','exception':'on_exception'}.get(status,'on_unknown')
            text=c['recommendation'][key] if status not in ('not_applicable','conflicting') else ('현재 적용 범위를 확인해 주세요.' if status=='not_applicable' else '서로 다른 정보가 있어 확인이 필요해요.')
            if 'maintain' in actions and status=='difference':text+=' 현재 편안하게 사용하는 제품은 이 선호 차이만으로 교체하지 않습니다.'
            if cid=='B-P09' and status=='unknown' and value('product.application_form') in ('nongas_spray','aerosol'):
                actions=['inform_general_practice','ask_targeted_question']
                text='얼굴에 직접 분사하지 않고 손에 덜어 바르며, 표시 사용법에 맞는 충분한 도포를 유지하세요.'
            if cid=='B-P07':text='기록된 제조업자 의견만 개발용으로 대조했습니다. 제품 순위·점수에는 적용하지 않으며 운영 정책 결정이 필요합니다.'
            results.append({'card_id':cid,'title':c['title'],'comparison_status':status,'action_types':actions,'reason':reason,
                'matched_branch_id':matched['branch_id'] if matched else None,
                'comparison_scope':'recorded_opinion_only' if cid=='B-P07' else ('filter_profile_only' if cid=='B-P05' else 'card_observations'),
                'recommendation_text':text,'missing_fields':missing,'unrecognized_fields':unrecognized,'questions':questions,
                'evidence_requests':[{'field':f,'route':'retrieve_product_evidence','card_id':cid} for f in missing if f.startswith('product.') and 'private' not in f],
                'observations':{f:deepcopy(facts[f]) for f in sorted(fields) if f in facts},
                'basis_type':c['baseline_type'],'evidence':deepcopy(c['evidence']),
                'sources':[deepcopy(self.sources[s]) for s in c['evidence']['source_ids']],
                'exceptions_considered':c['comparison_spec']['exception_when'],'follow_up':c['follow_up'],
                'policy_conflicts':['MP-01_vs_production_source_blind'] if cid=='B-P07' else [],
                'requires_production_approval':True,'requires_individual_human_review_for_preview':False,
                'automatic_product_replacement':False})
        # Apply priority to actions AND text. Suppressed advice remains traceable.
        suppressors=[r['card_id'] for r in results if any(a in r['action_types'] for a in ('pause_specific_product_pending_quality_check','pause_specific_cosmetic_due_to_discomfort','refer_for_professional_review'))]
        if suppressors:
            for r in results:
                if r['card_id'] in suppressors:continue
                if r['card_id'] in ('B-C04','B-G01','B-M03','B-P05','B-P07','B-G11','B-P06','B-M05','B-G12'):
                    r['suppressed_advice']={'actions':r['action_types'],'text':r['recommendation_text'],'by_cards':suppressors}
                    r['action_types']=['defer_specific_recommendation']
                    r['recommendation_text']='해당 제품의 불편·품질 또는 개별 지시 확인을 우선하며 유지·선호 안내는 보류합니다.'
                    r['reason']='quality_issue_precedes_trial_or_preference'
                    r['questions']=[]
        questions={}
        for r in results:
            for q in r['questions']:
                if q['field'] in questions:questions[q['field']]['card_ids'].extend(q['card_ids'])
                else:questions[q['field']]=deepcopy(q)
        context_result=None
        if not selected:
            context_result={'comparison_status':'not_applicable','action_types':['ask_targeted_question'],'reason':'no_supported_baseline_selected'}
            for f in ('skin.current_discomfort','method.current_routine'):
                if f not in facts:
                    questions[f]={'field':f,'text':self.variables[f]['label']+'에 대해 알려주세요.','card_ids':[],'wording_status':'development_draft'}
        # Only truly identical instructions are combined; distinct advice is retained.
        guidance={}
        for r in results:
            key=(tuple(r['action_types']),r['recommendation_text'])
            if key not in guidance:guidance[key]={'action_types':r['action_types'],'text':r['recommendation_text'],'card_ids':[],'source_ids':[]}
            g=guidance[key];g['card_ids'].append(r['card_id']);g['source_ids']=sorted(set(g['source_ids']+r['evidence']['source_ids']))
        return {'mode':'development_preview','production_enabled':False,'kb_version':self.kb['metadata']['version'],
            'kb_sha256':self.sha,'data_kind':request['data_kind'],'product_instance_id':request.get('product_instance_id'),
            'results':results,'questions':list(questions.values()),'context_result':context_result,'guidance':list(guidance.values()),
            'unmapped_cards':[],
            'aggregate_comparison':aggregate_comparison(results,context_result),
            'overall':'hold' if not results or suppressors or any(r['comparison_status'] in ('unknown','conflicting','exception') for r in results) else ('adjust' if any(r['comparison_status']=='difference' for r in results) else 'maintain')}

    def answer(self, request, answers, *, resolve_conflicts=()):
        """No persistence or transmission. Conflicting answers require explicit resolution."""
        self.evaluate(request)
        updated=deepcopy(request)
        updated.setdefault('facts',{})
        for field,observation in answers.items():
            previous=updated['facts'].get(field)
            if previous and previous.get('state')=='conflicting' and field not in resolve_conflicts:
                raise ValueError('Explicit conflict resolution required: '+field)
            if previous and previous.get('state')=='known' and previous.get('value')!=observation.get('value') and field not in resolve_conflicts:
                updated['facts'][field]={'state':'conflicting','value':None,'source':observation.get('source'),'reference':observation.get('reference'),'alternatives':[previous,deepcopy(observation)]}
            else:
                updated['facts'][field]=deepcopy(observation)
                if previous:updated['facts'][field]['previous_observation']=previous
        return updated,self.evaluate(updated)


def aggregate_comparison(results,context_result=None):
    """Comparison aggregation is distinct from action priority (overall hold/adjust).

    Mixed cards retain their own comparison/actions; no scenario-ID special cases.
    """
    states={r['comparison_status'] for r in results}
    if not states:return (context_result or {}).get('comparison_status','unknown')
    return next(iter(states)) if len(states)==1 else 'mixed_by_card'
