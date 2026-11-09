"""Offline evaluation regressions; synthetic approvals here are test inputs only.

Also runnable without pytest: python -X utf8 -m unittest discover -s tests -p test_action_evaluation.py
"""
import asyncio
import json
from pathlib import Path
import tempfile
import unittest

from beauty_agent.action_evaluation import (Case, Dataset, EXPERIMENT, ROOT, Review,
    classify, evaluate_cases, load_cases, proposal_flags, report_path, validate_collection)
from beauty_agent.contracts import PlannerMetadata


class EvaluationTests(unittest.TestCase):
    def setUp(self):
        self.folder = EXPERIMENT / 'evaluation/action_policy'
        self.raw = [json.loads((self.folder / name).read_text(encoding='utf-8'))
                    for name in ('cases.development.json', 'cases.holdout-candidate.json')]
        self.manifest = json.loads((self.folder / 'split-manifest.json').read_text(encoding='utf-8'))
        self.old = json.loads((EXPERIMENT / 'examples/action_sft.synthetic.json').read_text(encoding='utf-8'))

    def collection(self):
        return [Dataset.model_validate(d) for d in self.raw]

    def single(self, scenario='D12'):
        return next(c for d in self.collection() for c in d.cases if c.scenario_id == scenario)

    def sync_groups(self):
        keys = ('scenario_id', 'group_id', 'scenario_family_id', 'conversation_id', 'variant_of', 'product_family_id', 'split')
        self.manifest['groups'] = [{k: c[k] for k in keys} for d in self.raw for c in d['cases']]

    def test_load_checks_all_peer_splits_and_hashes(self):
        cases, validation, _ = load_cases(self.folder / 'cases.development.json')
        self.assertEqual(len(cases), 20)
        self.assertEqual(validation['counts']['turns'], 44)
        self.assertFalse(validation['independence_certified'])
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            for file in self.folder.glob('*.json'):
                (folder / file.name).write_bytes(file.read_bytes())
            peer = folder / 'cases.holdout-candidate.json'
            peer.write_text(peer.read_text(encoding='utf-8') + ' ', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                load_cases(folder / 'cases.development.json')

    def test_product_family_leak_is_rejected(self):
        self.raw[1]['cases'][0]['product_family_id'] = self.raw[0]['cases'][0]['product_family_id']
        self.sync_groups()
        with self.assertRaisesRegex(ValueError, 'cross-split leakage'):
            validate_collection(self.collection(), self.manifest, self.old)

    def test_variant_cannot_cross_split(self):
        self.raw[1]['cases'][0]['variant_of'] = 'D01'
        self.sync_groups()
        with self.assertRaisesRegex(ValueError, 'variant crosses'):
            validate_collection(self.collection(), self.manifest, self.old)

    def test_product_cannot_leak_under_a_different_family_label(self):
        self.raw[1]['cases'][0]['initial_request']['products'] = self.raw[0]['cases'][0]['initial_request']['products']
        with self.assertRaisesRegex(ValueError, 'product_id'):
            validate_collection(self.collection(), self.manifest, self.old)

    def test_existing_example_cannot_be_reused(self):
        self.raw[0]['cases'][0]['turns'][0]['message'] = self.old['samples'][0]['input']['message']
        with self.assertRaisesRegex(ValueError, 'exact message duplicate'):
            validate_collection(self.collection(), self.manifest, self.old)

    def test_approval_cannot_be_inferred_from_review_string(self):
        review = self.single().review.model_dump()
        for updates in ({'approved_reference': True}, {'status': 'reviewed'}, {'approved_reference': 'false'}):
            with self.assertRaises(ValueError):
                Review.model_validate({**review, **updates})

    def test_product_fact_updates_are_rejected(self):
        data = self.single().model_dump()
        data['turns'][0]['user_updates']['observations'] = {'product.ph': {
            'variable_id': 'product.ph', 'value': 5.5, 'state': 'known',
            'source': 'synthetic_fixture', 'confirmed_by_user': True}}
        with self.assertRaises(ValueError):
            Case.model_validate(data)

    def test_multiple_allowed_pairs_and_unjudged_alternative(self):
        judgment = self.single('D18').turns[0].proposed_judgment
        for pair in judgment.allowed_pairs:
            self.assertEqual(classify(pair.model_dump(), judgment), 'allowed_pair')
        self.assertEqual(classify({'action': 'retrieve_evidence', 'target_id': 'product.instructions'}, judgment), 'unjudged_alternative')
        self.assertEqual(classify({'action': 'request_draft', 'target_id': 'label_draft'}, judgment), 'explicitly_forbidden')

    def test_confirmation_focus_is_checked(self):
        j = self.single('D15').turns[0].proposed_judgment
        proposal = {**j.allowed_pairs[0].model_dump(), 'arguments': {'confirmation_focus': 'time'}}
        self.assertEqual(classify(proposal, j), 'argument_violation')

    def test_unreviewed_replay_has_no_quality_score(self):
        cases = [self.single('D04')]
        result = asyncio.run(evaluate_cases(cases))
        self.assertEqual(result['summary']['reference_eligible_turns'], 0)
        self.assertIsNone(result['summary']['action_pair_accuracy'])
        self.assertIsNone(result['summary']['conversation_completion_rate'])
        rows = result['rows']
        self.assertEqual(rows[1]['state_after']['confirmed_observations']['method.water_temperature']['state'], 'unknown')
        self.assertEqual(rows[2]['state_after']['confirmed_observations']['method.water_temperature']['value'], 'lukewarm')
        self.assertEqual(rows[0]['proposal_classification'], 'unjudged_alternative')

    def test_fallback_never_becomes_original_model_success(self):
        # Synthetic approval metadata exists only inside this regression test.
        case = self.single()
        review = Review(status='reviewed', reviewer='synthetic-test-reviewer', reviewed_at='2026-11-10',
                        rubric_version='action-evaluation-rubric-0.1', approved_reference=True)
        case.review = review
        case.turns[0].review = review
        class Invalid:
            metadata = PlannerMetadata(provider='custom', model='synthetic-invalid')
            async def plan_action(self, context):
                return {'action': 'invented_tool', 'target_id': 'anything'}
        result = asyncio.run(evaluate_cases([case], Invalid))
        row = result['rows'][0]
        self.assertEqual(row['reference_classification'], 'invalid_contract')
        self.assertEqual(row['applied_action_classification'], 'allowed_pair')
        self.assertEqual(row['trace']['requested_planner']['model'], 'synthetic-invalid')
        self.assertEqual(result['summary']['fallback_turns'], 1)
        self.assertEqual(result['summary']['action_pair_accuracy'], 0)

    def test_invalid_evidence_cannot_count_as_allowed_success(self):
        case = self.single()
        review = Review(status='reviewed', reviewer='synthetic-test-reviewer', reviewed_at='2026-11-10',
                        rubric_version='action-evaluation-rubric-0.1', approved_reference=True)
        case.review = review
        case.turns[0].review = review
        pair = case.turns[0].proposed_judgment.allowed_pairs[0].model_dump()
        class InvalidEvidence:
            async def plan_action(self, context):
                return {**pair, 'evidence_refs': ['source:invented']}
        result = asyncio.run(evaluate_cases([case], InvalidEvidence))
        self.assertEqual(result['rows'][0]['reference_classification'], 'gate_rejected')
        self.assertEqual(result['summary']['action_pair_accuracy'], 0)

    def test_declined_candidate_is_not_confirmed_by_request(self):
        result = asyncio.run(evaluate_cases([self.single('D02')]))
        second = result['rows'][1]
        self.assertEqual(second['state_after']['confirmed_clarifications']['clarify:turn1:0']['state'], 'declined')
        self.assertIsNone(second['draft'])
        self.assertTrue(all(c['matches'] for c in second['authored_state_checks']))

    def test_state_check_distinguishes_false_from_zero(self):
        case = self.single('D12')
        turn = case.turns[0]
        from beauty_agent.action_evaluation import StateCheck
        # Synthetic unsupported-slot observation is retained with its JSON type;
        # it is not claimed to be a domain-valid water-temperature observation.
        slot = next(iter(turn.user_updates.observations.values())).model_copy(update={
            'variable_id':'fixture.boolean','value':False,'state':'known'})
        turn.user_updates.observations['fixture.boolean'] = slot
        turn.proposed_judgment.state_checks.append(StateCheck(path='confirmed_observations.fixture.boolean.value', equals=0))
        result = asyncio.run(evaluate_cases([case]))
        self.assertFalse(result['rows'][0]['authored_state_checks'][-1]['matches'])

    def test_mandatory_hold_remains_held(self):
        result = asyncio.run(evaluate_cases([self.single('D10')]))
        row = result['rows'][0]
        self.assertEqual(row['trace']['applied_action']['target_id'], 'safety')
        self.assertEqual(row['trace']['execution_status'], 'held')
        self.assertEqual(row['questions'], [])
        self.assertIsNone(row['draft'])

    def test_failed_turn_is_not_forcibly_repaired(self):
        case = self.single('D02')
        case.turns[1].user_updates.confirmations = {'not-pending': CandidateConfirmationForTest()}
        result = asyncio.run(evaluate_cases([case]))
        row = result['rows'][1]
        self.assertEqual(row['execution_error'], 'ValueError')
        self.assertEqual(row['state_before'], row['state_after'])
        self.assertEqual(result['rows'][2]['execution_error'], 'not_run_after_scenario_error')

    def test_reask_flags_are_separate_from_reference_labels(self):
        state = {'confirmed_observations': {'method.water_temperature': {'state': 'declined'}},
                 'confirmed_clarifications': {'clarify:turn1:0': {'state': 'unknown'}}}
        self.assertIn('answered_observation_reasked', proposal_flags({'action':'ask_user','target_id':'method.water_temperature'}, state))
        self.assertIn('answered_candidate_reasked', proposal_flags({'action':'confirm_candidate','target_id':'clarify:turn1:0'}, state))

    def test_report_cannot_overwrite_input_or_leave_outputs(self):
        with self.assertRaises(ValueError):
            report_path(self.folder / 'cases.development.json')
        file = ROOT / 'outputs/action-test-report.json'
        with self.assertRaises(ValueError):
            report_path(file, [file])
        self.assertEqual(report_path(file), file.resolve())


def CandidateConfirmationForTest():
    from beauty_agent.loop import CandidateConfirmation
    return CandidateConfirmation(subject='self', state='affirmed', observed_at='2026-11-10T00:00:00Z')


if __name__ == '__main__':
    unittest.main()
