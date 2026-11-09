"""Offline fixed-state action replay. Reference judgments never enter planner inputs."""
from __future__ import annotations

import asyncio
from collections import Counter
from copy import deepcopy
import hashlib
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import re
import subprocess
import time
from typing import Literal

from pydantic import Field, model_validator

from .actions import ActionKind, ActionProposal
from .action_planner import RuleBasedActionPlanner, planner_metadata
from .contracts import Contract, ObservationSlot, OwnedProduct, Profile, TurnRequest
from .loop import AgentSession, CandidateConfirmation
from .modules.jev_adapter import JevExtractorAdapter

EXPERIMENT = Path(__file__).resolve().parents[1]
ROOT = EXPERIMENT.parents[3]
RUBRIC = EXPERIMENT / 'docs/action-evaluation-rubric.md'
OUTCOMES = {'ask_user': 'awaiting_user', 'confirm_candidate': 'awaiting_user',
            'resolve_conflict': 'awaiting_user', 'retrieve_evidence': 'awaiting_product_evidence',
            'hold': 'held', 'request_draft': 'draft_generated'}


class Review(Contract):
    status: Literal['unreviewed', 'reviewed', 'disputed']
    reviewer: str | None
    reviewed_at: str | None
    rubric_version: Literal['action-evaluation-rubric-0.1']
    approved_reference: bool = Field(strict=True)

    @model_validator(mode='after')
    def approval(self):
        if self.status == 'reviewed' and (not self.reviewer or not self.reviewer.strip() or not self.reviewed_at):
            raise ValueError('reviewed entries need actual reviewer and date')
        if self.reviewed_at:
            from datetime import datetime
            datetime.fromisoformat(self.reviewed_at.replace('Z', '+00:00'))
        if self.approved_reference and self.status != 'reviewed':
            raise ValueError('only reviewed entries may be references')
        return self


class Pair(Contract):
    action: ActionKind
    target_id: str = Field(min_length=1, max_length=160)


class StateCheck(Contract):
    path: str = Field(min_length=1)
    equals: object


class ArgumentConstraints(Contract):
    confirmation_focus: list[Literal['all', 'subject', 'polarity', 'time']] | None = None


class Judgment(Contract):
    allowed_pairs: list[Pair] = Field(min_length=1)
    forbidden_actions: list[ActionKind]
    forbidden_pairs: list[Pair]
    required_conditions: list[str]
    argument_constraints: ArgumentConstraints
    expected_execution_statuses: list[Literal['awaiting_user', 'awaiting_product_evidence', 'held', 'draft_generated']]
    state_checks: list[StateCheck]
    state_invariants: list[str]
    reason: str = Field(min_length=1)

    @model_validator(mode='after')
    def consistent(self):
        allowed = {(p.action, p.target_id) for p in self.allowed_pairs}
        forbidden = {(p.action, p.target_id) for p in self.forbidden_pairs}
        if len(allowed) != len(self.allowed_pairs) or allowed & forbidden:
            raise ValueError('duplicate or contradictory reference pairs')
        if any(a in self.forbidden_actions for a, _ in allowed):
            raise ValueError('allowed action is forbidden')
        if set(self.expected_execution_statuses) != {OUTCOMES[a] for a, _ in allowed}:
            raise ValueError('allowed pairs and expected outcomes disagree')
        if self.argument_constraints.confirmation_focus == []:
            raise ValueError('empty focus constraint')
        return self


class Updates(Contract):
    profile: Profile | None = None
    products: list[OwnedProduct] | None = None
    observations: dict[str, ObservationSlot] = Field(default_factory=dict)
    confirmations: dict[str, CandidateConfirmation] = Field(default_factory=dict)
    resolve_conflicts: tuple[str, ...] = ()

    @model_validator(mode='after')
    def user_only(self):
        for key, slot in self.observations.items():
            if key != slot.variable_id or key.startswith('product.') or not slot.confirmed_by_user:
                raise ValueError('only explicit user observations are accepted')
        return self


class Turn(Contract):
    turn_id: str = Field(min_length=1)
    message: str = Field(max_length=2000)
    user_updates: Updates
    extraction_fixture: dict
    proposed_judgment: Judgment
    review: Review


class Case(Contract):
    scenario_id: str = Field(min_length=1)
    title: str
    group_id: str = Field(min_length=1)
    scenario_family_id: str = Field(min_length=1)
    conversation_id: str = Field(min_length=1)
    variant_of: str | None
    product_family_id: str = Field(min_length=1)
    split: Literal['development', 'holdout-candidate']
    evaluation_mode: Literal['fixed_state_replay']
    interactive_branches: None
    provenance: dict
    review: Review
    initial_request: TurnRequest
    card_ids: list[str]
    tags: list[str]
    limitations: list[str]
    turns: list[Turn] = Field(min_length=1)


class Dataset(Contract):
    schema_version: Literal['action-policy-cases-0.1']
    mode: Literal['development_preview']
    production_enabled: Literal[False]
    human_review: Literal['unreviewed', 'mixed', 'reviewed']
    approved_reference: bool
    cases: list[Case] = Field(min_length=1)

    @model_validator(mode='after')
    def review_summary(self):
        statuses = [r.status for c in self.cases for r in [c.review, *[t.review for t in c.turns]]]
        if self.human_review == 'unreviewed' and any(s != 'unreviewed' for s in statuses):
            raise ValueError('dataset review summary is stale')
        if self.human_review == 'reviewed' and any(s != 'reviewed' for s in statuses):
            raise ValueError('dataset is not fully reviewed')
        if self.approved_reference and any(not r.approved_reference for c in self.cases for r in [c.review, *[t.review for t in c.turns]]):
            raise ValueError('dataset approval is inconsistent')
        return self


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def local_file(base, relative):
    path = (base / relative).resolve()
    if not path.is_relative_to(base.resolve()) or not path.is_file():
        raise ValueError('manifest path missing or outside its scope')
    return path


def validate_collection(datasets, manifest, existing):
    """Check all peer splits, not just the requested file. Does not certify semantics."""
    cases = [c for d in datasets for c in d.cases]
    case_ids = [c.scenario_id for c in cases]
    turn_ids = [t.turn_id for c in cases for t in c.turns]
    if len(case_ids) != len(set(case_ids)) or len(turn_ids) != len(set(turn_ids)):
        raise ValueError('duplicate scenario or turn ID')
    index = {c.scenario_id: c for c in cases}
    fields = ('scenario_id', 'group_id', 'scenario_family_id', 'conversation_id', 'variant_of', 'product_family_id', 'split')
    expected = [{k: getattr(c, k) for k in fields} for c in cases]
    if sorted(expected, key=lambda r: r['scenario_id']) != sorted(manifest['groups'], key=lambda r: r['scenario_id']):
        raise ValueError('manifest groups do not match data')
    for field in ('group_id', 'scenario_family_id', 'conversation_id', 'product_family_id'):
        assignments = {}
        for c in cases:
            assignments.setdefault(getattr(c, field), set()).add(c.split)
        if any(len(splits) > 1 for splits in assignments.values()):
            raise ValueError('cross-split leakage: ' + field)
    products = {}
    for c in cases:
        owned = list(c.initial_request.products)
        owned.extend(p for t in c.turns for p in (t.user_updates.products or []))
        for p in owned:
            products.setdefault(p.product_id, set()).add(c.split)
    if any(len(splits) > 1 for splits in products.values()):
        raise ValueError('cross-split leakage: product_id')
    for c in cases:
        seen = {c.scenario_id}
        parent = c.variant_of
        while parent is not None:
            if parent in seen or parent not in index:
                raise ValueError('invalid variant ancestry')
            seen.add(parent)
            other = index[parent]
            if other.split != c.split or other.group_id != c.group_id:
                raise ValueError('variant crosses split or origin group')
            parent = other.variant_of
    messages = [t.message.strip() for c in cases for t in c.turns]
    old = {s['input']['message'].strip() for s in existing['samples']}
    if len(set(messages)) != len(messages) or old & set(messages):
        raise ValueError('exact message duplicate within cases or existing examples')
    counts = {'development_scenarios': sum(c.split == 'development' for c in cases),
              'holdout_candidate_scenarios': sum(c.split == 'holdout-candidate' for c in cases),
              'turns': len(turn_ids), 'three_or_more_turn_groups': len({c.group_id for c in cases if len(c.turns) >= 3})}
    if counts != manifest['counts']:
        raise ValueError('manifest counts do not match data')
    return {'counts': counts, 'semantic_overlap_review': manifest['semantic_overlap_review'],
            'independence_certified': False, 'near_duplicate_candidates': near_duplicates(cases)}


def near_duplicates(cases):
    """Cheap review hints, not a semantic independence test."""
    rows = [(c, t, set(re.findall(r'\w+', t.message.lower()))) for c in cases for t in c.turns]
    result = []
    for i, (c, t, words) in enumerate(rows):
        for other, u, tokens in rows[i + 1:]:
            if c.split == other.split or not words | tokens:
                continue
            similarity = len(words & tokens) / len(words | tokens)
            if similarity >= .4:
                result.append({'turn_ids': [t.turn_id, u.turn_id], 'token_jaccard': similarity})
    return result


def load_cases(path):
    path = Path(path).resolve()
    base = path.parent
    mp = base / 'split-manifest.json'
    manifest = json.loads(mp.read_text(encoding='utf-8'))
    if manifest['schema_version'] != 'action-policy-split-0.1':
        raise ValueError('unsupported split manifest')
    datasets, selected, inputs = [], None, [mp, RUBRIC]
    for relative, digest in manifest['data_files_sha256'].items():
        file = local_file(base, relative)
        if sha(file) != digest:
            raise ValueError('data hash mismatch: ' + relative)
        dataset = Dataset.model_validate_json(file.read_text(encoding='utf-8'))
        datasets.append(dataset)
        inputs.append(file)
        if file == path:
            selected = dataset
    if selected is None:
        raise ValueError('requested cases are not registered in manifest')
    if sha(RUBRIC) != manifest['rubric_sha256']:
        raise ValueError('rubric hash mismatch')
    old = local_file(EXPERIMENT, manifest['existing_examples']['path'])
    if sha(old) != manifest['existing_examples']['sha256']:
        raise ValueError('existing examples hash mismatch')
    inputs.append(old)
    validation = validate_collection(datasets, manifest, json.loads(old.read_text(encoding='utf-8')))
    # Validate actual fixtures/KB inputs without calling any planner or tools.
    from .modules.mapping_adapter import MappingReviewAdapter
    from .modules.kb_adapter import KBEngineAdapter
    mapping, kb = MappingReviewAdapter(), KBEngineAdapter()
    for dataset in datasets:
        for c in dataset.cases:
            kb.evaluate({}, c.card_ids)
            for t in c.turns:
                mapping.evaluate(t.extraction_fixture)
    return selected.cases, validation, inputs


def state_at(state, path):
    if not path:
        return state
    if isinstance(state, dict):
        for key in sorted(state, key=len, reverse=True):
            if path == key:
                return state[key]
            if path.startswith(key + '.'):
                return state_at(state[key], path[len(key) + 1:])
    raise KeyError(path)


def approved(review):
    return review.status == 'reviewed' and review.approved_reference


def classify(proposal, judgment):
    if proposal is None:
        return 'proposal_absent'
    try:
        p = ActionProposal.model_validate(proposal)
    except ValueError:
        return 'invalid_contract'
    pair = (p.action, p.target_id)
    if p.action in judgment.forbidden_actions or pair in {(x.action, x.target_id) for x in judgment.forbidden_pairs}:
        return 'explicitly_forbidden'
    if pair in {(x.action, x.target_id) for x in judgment.allowed_pairs}:
        focus = judgment.argument_constraints.confirmation_focus
        if focus and p.arguments.confirmation_focus not in focus:
            return 'argument_violation'
        return 'allowed_pair'
    return 'unjudged_alternative'


def proposal_flags(proposal, state):
    if not isinstance(proposal, dict):
        return []
    action, target = proposal.get('action'), proposal.get('target_id')
    slot = state['confirmed_observations'].get(target)
    flags = []
    if action == 'ask_user' and slot and slot['state'] in ('known', 'unknown', 'declined', 'not_applicable'):
        flags.append('answered_observation_reasked')
    if action == 'confirm_candidate' and target in state['confirmed_clarifications']:
        flags.append('answered_candidate_reasked')
    if action == 'ask_user' and isinstance(target, str) and target.startswith('product.'):
        flags.append('product_evidence_asked_of_user')
    return flags


class CapturePlanner:
    def __init__(self, planner):
        self.inner = planner
        self.metadata = planner_metadata(planner)
        self.context = None

    async def plan_action(self, context):
        self.context = context.model_copy(deep=True)
        return await self.inner.plan_action(context)


async def evaluate_cases(cases, planner_factory=RuleBasedActionPlanner):
    rows = []
    for case in cases:
        capture = CapturePlanner(planner_factory())
        fixture = {}
        extractor = JevExtractorAdapter(extractor=lambda _: deepcopy(fixture))
        session = AgentSession(case.initial_request, planner=capture, extractor=extractor, card_ids=case.card_ids)
        failed = False
        for turn in case.turns:
            eligible = approved(case.review) and approved(turn.review)
            row = {'scenario_id': case.scenario_id, 'turn_id': turn.turn_id, 'split': case.split,
                   'review_status': {'scenario': case.review.status, 'turn': turn.review.status},
                   'reference_eligible': eligible, 'evaluation_mode': 'fixed_state_replay',
                   'conversation_completion': 'unsupported_no_response_branches',
                   'manual_semantic_review': 'pending', 'state_before': session.state.model_dump(mode='json')}
            if failed:
                row.update(execution_error='not_run_after_scenario_error', elapsed_seconds=None,
                           proposal_classification=None, reference_classification=None)
                rows.append(row)
                continue
            fixture = turn.extraction_fixture
            kwargs = {k: getattr(turn.user_updates, k) for k in turn.user_updates.model_fields_set}
            start = time.perf_counter()
            try:
                result = await session.step(turn.message, **kwargs)
                row['elapsed_seconds'] = time.perf_counter() - start
                trace = result.trace.model_dump(mode='json')
                after = session.state.model_dump(mode='json')
                context = capture.context
                row.update(trace=trace, state_after=after, questions=[q.model_dump() for q in result.questions],
                           response_message=result.message,
                           draft=result.draft.model_dump(mode='json') if result.draft else None,
                           execution_error=None)
                row['proposal_classification'] = classify(trace['proposed_action'], turn.proposed_judgment)
                row['reference_classification'] = row['proposal_classification'] if eligible else None
                row['applied_action_classification'] = classify(trace['applied_action'], turn.proposed_judgment)
                row['gate_rejected'] = 'rejected' in trace['validation_results']
                if eligible and row['gate_rejected'] and row['reference_classification'] in ('allowed_pair', 'unjudged_alternative'):
                    row['reference_classification'] = 'gate_rejected'
                row['proposal_flags'] = proposal_flags(trace['proposed_action'], {
                    'confirmed_observations': {k: v.model_dump() for k, v in context.observations.items()},
                    'confirmed_clarifications': context.confirmed_candidates})
                row['available_actions'] = [o.model_dump(mode='json') for o in context.available_actions]
                enabled = {(o.action, o.target_id) for o in context.enabled()}
                row['authored_pairs_not_enabled'] = [p.model_dump() for p in turn.proposed_judgment.allowed_pairs if (p.action, p.target_id) not in enabled]
                checks = []
                for check in turn.proposed_judgment.state_checks:
                    try:
                        actual = state_at(after, check.path)
                        # JSON equality must distinguish 0 from False, including nested values.
                        matches = json.dumps(actual, sort_keys=True) == json.dumps(check.equals, sort_keys=True)
                    except KeyError:
                        actual, matches = None, False
                    checks.append({'path': check.path, 'expected': check.equals, 'actual': actual, 'matches': matches})
                row['authored_state_checks'] = checks
                row['authored_outcome_matches'] = trace['execution_status'] in turn.proposed_judgment.expected_execution_statuses
            except Exception as exc:
                row.update(elapsed_seconds=time.perf_counter() - start, execution_error=type(exc).__name__,
                           state_after=session.state.model_dump(mode='json'), proposal_classification=None,
                           reference_classification=None)
                failed = True
            rows.append(row)
    return {'rows': rows, 'summary': summarize(rows)}


def summarize(rows):
    eligible = [r for r in rows if r['reference_eligible']]
    labels = Counter(r.get('reference_classification') for r in eligible)
    judged = sum(labels[k] for k in ('allowed_pair', 'explicitly_forbidden', 'argument_violation', 'invalid_contract', 'proposal_absent', 'gate_rejected'))
    executed = [r for r in rows if 'trace' in r]
    times = sorted(r['elapsed_seconds'] for r in rows if r.get('elapsed_seconds') is not None)
    def quantile(q):
        import math
        return times[max(0, math.ceil(q * len(times)) - 1)] if times else None
    return {'requested_turns': len(rows), 'reference_eligible_turns': len(eligible),
            'review_counts': dict(Counter(r['review_status']['turn'] for r in rows)),
            'proposal_observations_unreviewed_not_accuracy': dict(Counter(r.get('proposal_classification') or 'not_available' for r in rows if not r['reference_eligible'])),
            'judged_request_denominator': judged,
            'judged_reference_coverage': judged / len(eligible) if eligible else None,
            'action_pair_accuracy': labels['allowed_pair'] / judged if judged else None,
            'unjudged_reference_alternatives': labels['unjudged_alternative'],
            'reference_execution_errors': sum(r.get('execution_error') is not None for r in eligible),
            'action_pair_accuracy_scope': 'reviewed allowed/forbidden pairs and contract/argument/gate failures; unjudged alternatives and execution errors reported separately',
            'full_semantic_quality_accuracy': None,
            'execution_errors': sum(r.get('execution_error') is not None for r in rows),
            'fallback_turns': sum(r['trace']['applied_planner']['provider'] == 'baseline' and 'deterministic_baseline_applied' in r['trace']['validation_results'] for r in executed),
            'wording_replacements': sum('unverified_question_replaced_with_reviewed_wording' in r['trace']['validation_results'] for r in executed),
            'held_turns': sum(r['trace']['execution_status'] == 'held' for r in executed),
            'draft_generated_turns': sum(r['trace']['execution_status'] == 'draft_generated' for r in executed),
            'displayed_questions': sum(len(r['questions']) for r in executed),
            'conversation_completion_rate': None,
            'latency': {'scope': 'local fixed-state software replay; attempted errors included; skipped turns excluded',
                        'attempted_count': len(times), 'mean_seconds': sum(times) / len(times) if times else None,
                        'p50_seconds': quantile(.5), 'p95_seconds': quantile(.95)}}


def execution_manifest(inputs):
    import platform
    def git(*args):
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return result.stdout.strip() if result.returncode == 0 else None
    dependencies = {}
    for name in ('pydantic', 'httpx', 'pytest', 'kiwipiepy'):
        try:
            dependencies[name] = version(name)
        except PackageNotFoundError:
            dependencies[name] = None
    implementation = [*EXPERIMENT.glob('beauty_agent/**/*.py'), *EXPERIMENT.glob('poc/jev/**/*.py'),
                      EXPERIMENT / 'scripts/evaluate_action_policy.py', EXPERIMENT / 'uv.lock',
                      ROOT / 'skin_engine/kb_preview/rules.json', ROOT / 'docs/source-manifest.json']
    return {'commit': git('rev-parse', 'HEAD'), 'working_tree': git('status', '--short'),
            'python': platform.python_version(), 'dependencies': dependencies,
            'input_sha256': {str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p): sha(p) for p in inputs},
            'implementation_sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(implementation)}}


def report_path(path, inputs=()):
    path = Path(path).resolve()
    if not path.is_relative_to((ROOT / 'outputs').resolve()) or path in {Path(p).resolve() for p in inputs}:
        raise ValueError('reports must be separate files under repository outputs/')
    return path
