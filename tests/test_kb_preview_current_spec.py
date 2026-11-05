"""57-ID current-spec trace; raw expectations are separately audited, not rewritten."""
import json
from pathlib import Path
import pytest
from skin_engine.kb_preview.audit import run
from skin_engine.kb_preview.revisions import revised_cases,manufacturer_example
ROOT=Path(__file__).resolve().parents[1]
BASE=json.loads((ROOT/'docs/launch_evidence/ledger/P3-A05-kb-ai-first-followup-20261105/original_acceptance57.json').read_text())
EXPECTED={r['id']:r for r in BASE['scenarios']}

@pytest.fixture(scope='module')
def current():return {r['id']:r for r in run()['scenarios']}
@pytest.fixture(scope='module')
def revised():return {r['revision_of']:r for r in revised_cases()}

@pytest.mark.parametrize('sid',list(EXPECTED))
def test_current_spec_trace(sid,current,revised):
    r=current[sid];old=EXPECTED[sid]
    # Compare exact IDs, facts, statuses, actions and mismatches. A new gap cannot hide in a count of five.
    for k in ['original_expectation','original_facts','statuses','actions','failures','category']:
        assert r[k]==old[k],(sid,k)
    if sid in ('T17','V06-T04','T37','T45'):
        fixed=revised[sid];assert fixed['category']=='expected_satisfied' and fixed['failures']==[]
        if sid in ('T17','V06-T04'):assert 'unknown' in r['statuses'].values() and fixed['added_synthetic_facts']
        else:assert fixed['aggregate_comparison']=='mixed_by_card' and fixed['statuses']==r['statuses'] and fixed['facts_unchanged']
    elif sid=='T20':
        m=manufacturer_example();assert m['development_result']['preferred_ids']==['SYN-A']
        assert m['production_policy_result']['preferred_ids']==[] and m['development_result']['numeric_scores'] is None
    else:assert r['category']=='expected_satisfied' and r['failures']==[]
