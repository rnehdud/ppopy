#!/usr/bin/env python3
"""Validator for Ppopy v3 QLoRA (SOLUTION_MODE + HOLD_MODE) synthetic dataset (Single-Owner).

Validates a single dataset JSONL (or optional multiple files) against:
1. Non-empty files, 24-row pilot gate (18 sol / 6 hold, 4 buckets x 6, distinct SLMRequest inputs)
   and 900-row Stage-1 training gate (sol >= 690, hold >= 210, hold 20-25%, HN >= 25%, EN 30-40%)
2. Outer JSONL row schema, deterministic ID format (syn-sol-0001 / syn-hold-0001), exact system prompt
3. Inner v3_contracts.SLMRequest Pydantic contract + outer/inner mode & refs alignment
4. Controlled vocabulary (kb_judgments.status, product_evidence.status) + KB v0.6.1 variable types
5. Evidence-to-input backing + computed catalog:<product_id>@<version> consistency
6. ReferenceChunk metadata; exact KB source_registry matching only in kb-anchored; probes excluded from citations & EN ratio
7. Strict citation integrity, mode headings, hold direct-instruction leak blocking, clinical guardrails
8. Mandatory v67 index loading, real source_scenario_id/source_turn_id/output.action checks,
   cross-split leakage checks, and non-empty 90/10 val_internal family/group split on new_synthetic
9. Optional --require-review + --review-file gate verifying external cross-model critic PASS
   and >= 10% human_review=='approved' on high-risk rows
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Literal

COS_AGENT_DIR = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = COS_AGENT_DIR.parents[3]
if str(COS_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(COS_AGENT_DIR))

from beauty_agent.v3_contracts import SLMRequest

ValidationProfile = Literal["rag-free", "kb-anchored"]

SYSTEM_PROMPT_SOLUTION_HOLD = (
    "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. "
    "입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, "
    "rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. "
    "allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, "
    "허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. "
    "문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, "
    "미공개 성분 농도·pH 추측은 금지합니다. "
    "확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. "
    'mode가 "hold"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. '
    "어조는 차분한 '~해요' 존댓말을 사용하세요."
)
SYSTEM_PROMPT_KB_ANCHORED = (
    "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. "
    "입력 JSON(confirmed_observations, kb_judgments, product_evidence, rag_chunks, allowed_evidence_refs)만 근거로 한국어 안내를 작성하세요. "
    "allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, distractor_refs는 무시하세요. "
    "피부 질환 진단, 임상·치료 효과 단정, 미공개 성분 농도·pH 추측은 금지합니다. "
    "확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. "
    'mode가 "hold"이면 개별 루틴이나 제품 추천 없이 보류 사유와 필요한 확인·전문가 상담 안내만 작성하세요. '
    "어조는 차분한 '~해요' 존댓말을 사용하세요."
)

ALLOWED_DOMAINS = frozenset({
    "cleansing",
    "moisturizing",
    "sun_protection",
    "cross_domain",
    "general_safety",
})
ALLOWED_SPLITS = frozenset({"train", "val_internal"})
ALLOWED_MODES = frozenset({"solution", "hold"})
ALLOWED_HARD_NEGATIVE_TYPES = frozenset({
    "rag_distractor_ignore",
    "clinical_restraint",
    "version_mismatch_or_unknown",
    "negation_or_other_subject",
})
ALLOWED_PILOT_BUCKETS = frozenset({
    "normal_guidance",
    "hold",
    "unknown_or_version",
    "distractor_or_defense",
})
ANCHORED_CHUNK_ORIGINS = frozenset({"kb_source_summary", "synthetic_defense_probe"})
RAG_FREE_CHUNK_ORIGINS = ANCHORED_CHUNK_ORIGINS | {"reference_excerpt"}
ALLOWED_SOURCE_ORIGINS = frozenset({"new_synthetic", "recycled_v67"})
ALLOWED_HUMAN_REVIEWS = frozenset({"unreviewed", "approved", "needs_revision"})
ALLOWED_CRITIC_STATUSES = frozenset({"PASS", "FAIL", "unreviewed"})

# Controlled vocabulary for structured inputs (reduces Train-Inference Skew)
ALLOWED_KB_JUDGMENT_STATUSES = frozenset({"aligned", "difference", "unknown", "hold", "exception"})
ALLOWED_PRODUCT_EVIDENCE_STATUSES = frozenset({"verified", "usage_held", "unknown"})

FORBIDDEN_SOURCE_IDS = frozenset({"F01", "F02", "S30", "S31"})
FORBIDDEN_CARD_IDS = frozenset({"B-P07"})
V67_ACTION_TO_MODE = {"request_draft": "solution", "hold": "hold"}

PILOT_TOTAL_ROWS = 24
PILOT_SOLUTION_ROWS = 18
PILOT_HOLD_ROWS = 6
PILOT_PER_BUCKET = 6

STAGE1_MIN_TOTAL_ROWS = 900
STAGE1_MIN_SOLUTION_ROWS = 690
STAGE1_MIN_HOLD_ROWS = 210

# Supports single-owner IDs (syn-sol-0001 / syn-hold-0001) and optional legacy shard prefix
ROW_ID_PATTERN = re.compile(r"^syn-(?:[abc]-)?(?P<kind>sol|hold)-(?P<num>\d{4})$")
BRACKET_CITATION_PATTERN = re.compile(
    r"\[((?:kb|catalog|alternative|ref):[^\]]+|(?:S|U|D|F)\d{2,3}|B-[A-Z]\d{2}(?:@[0-9.]+)?)\]"
)
ALLOWED_REF_PREFIXES = ("kb:", "catalog:", "alternative:", "ref:")
ENGLISH_WORD_PATTERN = re.compile(r"[A-Za-z]{3,}")

SOLUTION_REQUIRED_HEADINGS = ("### 핵심 안내", "### 근거 및 이유", "### 확인이 필요한 한계")
HOLD_REQUIRED_HEADINGS = ("### 개별 권고 보류 안내", "### 필요한 다음 단계")

FORBIDDEN_CLINICAL_PATTERNS = (
    re.compile(r"(아토피\s*피부염|접촉\s*피부염|지루성\s*피부염|여드름)\s*(입니다|으로\s*진단)"),
    re.compile(r"(진단합니다|진단할\s*수\s*있어요|처방합니다)"),
    re.compile(r"(치료됩니다|완치됩니다|확실히\s*개선됩니다|임상적으로\s*입증)"),
    re.compile(r"\d+\s*%\s*(개선됩니다|감소합니다|줄어듭니다)"),
    re.compile(r"pH\s*\d+(?:\.\d+)?\s*(?:로\s*추정|일\s*것으로\s*추정)"),
    re.compile(r"농도(?:는|가|를)?\s*\d+(?:\.\d+)?\s*%\s*(?:로\s*추정|일\s*것(?:으로\s*추정|\s*같아요))"),
)
HOLD_RECOMMENDATION_LEAK_PATTERNS = (
    re.compile(r"대체\s*후보"),
    re.compile(r"루틴을\s*(유지|추천|권해)"),
    re.compile(r"(사용해\s*보세요|사용하세요|써\s*보세요|바르는\s*것을\s*권해|권해드려요|추천해\s*드려요|추천해요)"),
    re.compile(r"(세안하세요|세안해\s*보세요|씻으세요|바르세요|발라\s*(?:보세요|주세요)|도포하세요|덧바르세요)"),
    re.compile(
        r"(클렌징폼|클렌징\s*오일|보습제|선크림|자외선차단제)(?:을|를|으로)\s*\d*\s*(?:회|번|단계)?\s*(?:사용|세안|도포|바르)"
    ),
)


@dataclass
class KBReferenceIndex:
    variable_types: dict[str, str]
    card_ids: set[str]
    source_registry: dict[str, dict[str, Any]]


@dataclass
class V67SplitIndex:
    scenario_to_split: dict[str, str] = field(default_factory=dict)
    group_to_split: dict[str, str] = field(default_factory=dict)
    turn_to_split: dict[str, str] = field(default_factory=dict)
    turn_to_scenario: dict[str, str] = field(default_factory=dict)
    turn_to_action: dict[str, str] = field(default_factory=dict)
    test_scenarios: set[str] = field(default_factory=set)
    test_groups: set[str] = field(default_factory=set)
    test_turns: set[str] = field(default_factory=set)


@dataclass
class ValidationReport:
    files: list[str]
    total_rows: int = 0
    solution_rows: int = 0
    hold_rows: int = 0
    hard_negative_rows: int = 0
    english_relevant_solution_rows: int = 0
    split_counts: dict[str, int] = field(default_factory=dict)
    pilot_bucket_counts: dict[str, int] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.errors) == 0

    def to_dict(self) -> dict[str, Any]:
        hold_ratio = (self.hold_rows / self.total_rows) if self.total_rows else 0.0
        hn_ratio = (self.hard_negative_rows / self.total_rows) if self.total_rows else 0.0
        en_ratio = (
            (self.english_relevant_solution_rows / self.solution_rows)
            if self.solution_rows
            else 0.0
        )
        return {
            "passed": self.passed,
            "files": self.files,
            "total_rows": self.total_rows,
            "solution_rows": self.solution_rows,
            "hold_rows": self.hold_rows,
            "hold_ratio": round(hold_ratio, 4),
            "hard_negative_rows": self.hard_negative_rows,
            "hard_negative_ratio": round(hn_ratio, 4),
            "english_relevant_solution_rows": self.english_relevant_solution_rows,
            "english_relevant_solution_ratio": round(en_ratio, 4),
            "split_counts": self.split_counts,
            "pilot_bucket_counts": self.pilot_bucket_counts,
            "error_count": len(self.errors),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def load_kb_index(kb_dir: pathlib.Path) -> KBReferenceIndex:
    seed_path = kb_dir / "Poppy_KB_seed_v0.6.1.json"
    if not seed_path.exists():
        raise FileNotFoundError(f"KB seed file not found: {seed_path}")
    kb = json.loads(seed_path.read_text(encoding="utf-8"))
    variable_types = {
        v["id"]: v.get("value_type", "unknown")
        for v in kb.get("variables", [])
        if isinstance(v, dict) and v.get("id")
    }
    card_ids = {
        c["id"]
        for c in kb.get("baseline_cards", [])
        if isinstance(c, dict) and c.get("id")
    }
    bi01_path = kb_dir / "sunscreen_removal_review.json"
    if bi01_path.exists():
        bi01 = json.loads(bi01_path.read_text(encoding="utf-8"))
        card_val = bi01.get("card")
        card_id = (
            card_val
            if isinstance(card_val, str)
            else card_val.get("id")
            if isinstance(card_val, dict)
            else None
        )
        if card_id:
            card_ids.add(card_id)
    source_registry = {
        s["id"]: s
        for s in kb.get("source_registry", [])
        if isinstance(s, dict) and s.get("id")
    }
    return KBReferenceIndex(
        variable_types=variable_types,
        card_ids=card_ids,
        source_registry=source_registry,
    )


def load_v67_index(v67_dir: pathlib.Path) -> V67SplitIndex:
    """Strictly load v67 split reference files; missing files fail loudly."""
    if not v67_dir.exists():
        raise FileNotFoundError(f"v67 reference directory not found: {v67_dir}")
    index = V67SplitIndex()
    split_files = (
        ("train", v67_dir / "v67-sft-train.jsonl"),
        ("val_internal", v67_dir / "v67-sft-val-internal.jsonl"),
        ("test_internal", v67_dir / "v67-sft-test-internal.jsonl"),
    )
    for split_name, path in split_files:
        if not path.exists():
            raise FileNotFoundError(f"Required v67 split file not found: {path}")
        lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if not lines:
            raise ValueError(f"Required v67 split file is empty: {path}")
        for line in lines:
            row = json.loads(line)
            sid = row.get("scenario_id")
            gid = row.get("group_id")
            tid = row.get("id")
            if sid:
                index.scenario_to_split[sid] = split_name
                if split_name == "test_internal":
                    index.test_scenarios.add(sid)
            if gid:
                index.group_to_split[gid] = split_name
                if split_name == "test_internal":
                    index.test_groups.add(gid)
            if tid:
                index.turn_to_split[tid] = split_name
                if sid:
                    index.turn_to_scenario[tid] = sid
                action = row.get("output", {}).get("action") if isinstance(row.get("output"), dict) else None
                if isinstance(action, str):
                    index.turn_to_action[tid] = action
                if split_name == "test_internal":
                    index.test_turns.add(tid)
    return index


def compute_row_content_sha256(
    req: SLMRequest,
    assistant_content: str,
    *,
    card_ids: list[str] | None = None,
    chunk_origins: dict[str, Any] | None = None,
    is_hard_negative: bool | None = None,
    hard_negative_type: str | None = None,
) -> str:
    """Canonical SHA-256 binding external Critic review to all reviewed fields."""
    canonical = json.dumps(
        {
            "user": req.model_dump(mode="json"),
            "assistant": assistant_content,
            "card_ids": sorted(card_ids or []),
            "chunk_origins": chunk_origins or {},
            "is_hard_negative": is_hard_negative,
            "hard_negative_type": hard_negative_type,
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_external_reviews(review_path: pathlib.Path) -> dict[str, dict[str, Any]]:
    """Load external Critic review JSONL keyed by row_id; rejects duplicate row_ids."""
    if not review_path.exists():
        raise FileNotFoundError(f"External critic review file not found: {review_path}")
    reviews: dict[str, dict[str, Any]] = {}
    for idx, line in enumerate(review_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        rid = obj.get("row_id")
        if not isinstance(rid, str) or not rid.strip():
            raise ValueError(f"{review_path}:{idx}: missing 'row_id'")
        if rid in reviews:
            raise ValueError(f"{review_path}:{idx}: duplicate review record for row_id {rid!r}")
        reviews[rid] = obj
    return reviews


def _is_valid_kb_value(value_type: str, value: Any) -> bool:
    if value_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if value_type == "string":
        return isinstance(value, str)
    if value_type == "array":
        return isinstance(value, list)
    if value_type == "quantity":
        return (isinstance(value, (int, float)) and not isinstance(value, bool)) or isinstance(
            value, dict
        )
    if value_type in ("categorical", "ordinal"):
        return isinstance(value, str) or (isinstance(value, int) and not isinstance(value, bool))
    if value_type == "datetime":
        return isinstance(value, str)
    return value is not None


def _is_english_text(text: str) -> bool:
    return len(ENGLISH_WORD_PATTERN.findall(text)) >= 8


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _validate_ref_id(ref_id: str, kb_index: KBReferenceIndex, *, anchored: bool) -> str | None:
    if not ref_id.startswith(ALLOWED_REF_PREFIXES):
        return f"invalid evidence_ref prefix: {ref_id!r}"
    if ref_id.startswith("ref:"):
        sid = ref_id.split(":", 1)[1]
        if sid.upper().startswith(("U", "D")) or sid.upper() in FORBIDDEN_SOURCE_IDS:
            return f"forbidden source_id in evidence_ref: {ref_id!r}"
        if anchored and sid not in kb_index.source_registry:
            return f"unknown source_id in KB v0.6.1 source_registry: {ref_id!r}"
    elif ref_id.startswith("kb:"):
        if not anchored:
            return f"KB evidence_ref requires the kb-anchored profile: {ref_id!r}"
        card_part = ref_id.split(":", 1)[1].split("@", 1)[0]
        if card_part in FORBIDDEN_CARD_IDS:
            return f"forbidden card_id in evidence_ref: {ref_id!r}"
        if card_part not in kb_index.card_ids:
            return f"unknown card_id in KB v0.6.1: {ref_id!r}"
    return None


def validate_rows(
    file_rows: list[tuple[str, int, dict[str, Any]]],
    kb_index: KBReferenceIndex,
    v67_index: V67SplitIndex,
    *,
    profile: ValidationProfile = "rag-free",
    input_files: list[str] | None = None,
    enforce_ratios: bool = False,
    enforce_stage1_min_rows: bool = False,
    pilot_mode: bool = False,
    require_review: bool = False,
    external_reviews: dict[str, dict[str, Any]] | None = None,
) -> ValidationReport:
    if profile not in ("rag-free", "kb-anchored"):
        raise ValueError(f"unknown validation profile: {profile!r}")
    anchored = profile == "kb-anchored"
    system_prompt = SYSTEM_PROMPT_KB_ANCHORED if anchored else SYSTEM_PROMPT_SOLUTION_HOLD
    allowed_chunk_origins = ANCHORED_CHUNK_ORIGINS if anchored else RAG_FREE_CHUNK_ORIGINS
    all_files = sorted(set(input_files or []) | {src for src, _, _ in file_rows})
    report = ValidationReport(files=all_files)

    if not file_rows:
        report.errors.append("dataset has 0 rows; empty input is not allowed")
        return report

    file_row_counts = Counter(src for src, _, _ in file_rows)
    for src in all_files:
        if file_row_counts[src] == 0:
            report.errors.append(f"{src}: file has 0 rows")

    seen_ids: dict[str, str] = {}
    group_splits: dict[str, set[str]] = {}
    scenario_splits: dict[str, set[str]] = {}
    family_splits: dict[str, set[str]] = {}
    source_turn_splits: dict[str, set[str]] = {}
    assistant_splits: dict[str, set[str]] = {}
    split_counter: Counter[str] = Counter()
    pilot_bucket_counter: Counter[str] = Counter()
    seen_user_inputs: set[str] = set()
    new_syn_family_splits: dict[str, set[str]] = {}
    new_syn_group_splits: dict[str, set[str]] = {}
    new_syn_split_counts: Counter[str] = Counter()

    high_risk_rows = 0
    high_risk_human_approved = 0
    total_human_approved = 0

    for src, line_no, row in file_rows:
        loc = f"{src}:{line_no}"
        report.total_rows += 1

        row_id = row.get("id")
        mode = row.get("mode")
        split = row.get("split")
        scenario_id = row.get("scenario_id")
        group_id = row.get("group_id")
        family_id = row.get("scenario_family_id")

        if not isinstance(row_id, str):
            report.errors.append(f"{loc}: missing or non-string 'id'")
        else:
            m = ROW_ID_PATTERN.match(row_id)
            if not m:
                report.errors.append(
                    f"{loc}: invalid id format {row_id!r} (expected syn-sol-0001 or syn-hold-0001)"
                )
            else:
                expected_kind = "sol" if mode == "solution" else "hold" if mode == "hold" else None
                if expected_kind and m.group("kind") != expected_kind:
                    report.errors.append(f"{loc}: id kind {m.group('kind')!r} mismatches mode {mode!r}")
            if row_id in seen_ids:
                report.errors.append(f"{loc}: duplicate id {row_id!r} (first seen at {seen_ids[row_id]})")
            else:
                seen_ids[row_id] = loc

        if mode not in ALLOWED_MODES:
            report.errors.append(f"{loc}: invalid outer mode {mode!r} (allowed: {sorted(ALLOWED_MODES)})")
        if split not in ALLOWED_SPLITS:
            report.errors.append(
                f"{loc}: invalid split {split!r} (allowed: {sorted(ALLOWED_SPLITS)}; test_internal forbidden)"
            )
        else:
            split_counter[split] += 1

        if not isinstance(scenario_id, str) or not scenario_id.strip():
            report.errors.append(f"{loc}: missing or empty 'scenario_id'")
        if not isinstance(group_id, str) or not group_id.strip():
            report.errors.append(f"{loc}: missing or empty 'group_id'")
        if not isinstance(family_id, str) or not family_id.strip():
            report.errors.append(f"{loc}: missing or empty 'scenario_family_id'")

        domains = row.get("domains")
        if not isinstance(domains, list) or not domains or not all(d in ALLOWED_DOMAINS for d in domains):
            report.errors.append(f"{loc}: invalid 'domains' {domains!r}")

        card_ids = row.get("card_ids", [])
        if not isinstance(card_ids, list) or (anchored and not card_ids):
            report.errors.append(f"{loc}: invalid 'card_ids' for profile {profile!r}")
        else:
            for cid in card_ids:
                if not isinstance(cid, str):
                    report.errors.append(f"{loc}: card_id must be a string, got {cid!r}")
                elif cid in FORBIDDEN_CARD_IDS:
                    report.errors.append(f"{loc}: forbidden card_id {cid!r}")
                elif cid not in kb_index.card_ids:
                    report.errors.append(f"{loc}: unknown card_id {cid!r} in KB v0.6.1")

        is_hn = row.get("is_hard_negative")
        hn_type = row.get("hard_negative_type")
        if not isinstance(is_hn, bool):
            report.errors.append(f"{loc}: 'is_hard_negative' must be bool")
        elif is_hn:
            report.hard_negative_rows += 1
            if hn_type not in ALLOWED_HARD_NEGATIVE_TYPES:
                report.errors.append(
                    f"{loc}: invalid 'hard_negative_type' {hn_type!r} when is_hard_negative=True"
                )
        elif hn_type is not None:
            report.errors.append(f"{loc}: 'hard_negative_type' must be null when is_hard_negative=False")

        # Pilot bucket check
        pilot_bucket = row.get("pilot_bucket")
        if pilot_mode:
            if pilot_bucket not in ALLOWED_PILOT_BUCKETS:
                report.errors.append(
                    f"{loc}: pilot mode requires 'pilot_bucket' in {sorted(ALLOWED_PILOT_BUCKETS)}, got {pilot_bucket!r}"
                )
            else:
                pilot_bucket_counter[pilot_bucket] += 1
                if pilot_bucket == "hold" and mode != "hold":
                    report.errors.append(f"{loc}: pilot_bucket='hold' requires mode='hold'")
                if pilot_bucket != "hold" and mode == "hold":
                    report.errors.append(f"{loc}: mode='hold' requires pilot_bucket='hold'")
        elif pilot_bucket is not None and pilot_bucket not in ALLOWED_PILOT_BUCKETS:
            report.errors.append(f"{loc}: invalid 'pilot_bucket' {pilot_bucket!r}")

        # Provenance & review checks
        prov = row.get("provenance")
        source_scenario_id: str | None = None
        source_turn_id: str | None = None
        src_origin: str | None = None
        gen_model: str | None = None
        is_high_risk = mode == "hold" or hn_type == "version_mismatch_or_unknown"
        if is_high_risk:
            high_risk_rows += 1

        if not isinstance(prov, dict):
            report.errors.append(f"{loc}: missing or non-dict 'provenance'")
        else:
            src_origin = prov.get("source_origin")
            if src_origin not in ALLOWED_SOURCE_ORIGINS:
                report.errors.append(f"{loc}: invalid provenance.source_origin {src_origin!r}")
            source_scenario_id = prov.get("source_scenario_id")
            source_turn_id = prov.get("source_turn_id")
            if src_origin == "recycled_v67":
                if not isinstance(source_scenario_id, str) or not source_scenario_id.strip():
                    report.errors.append(f"{loc}: provenance.source_scenario_id required for recycled_v67")
                elif source_scenario_id not in v67_index.scenario_to_split:
                    report.errors.append(
                        f"{loc}: provenance.source_scenario_id {source_scenario_id!r} does not exist in v67"
                    )
                if not isinstance(source_turn_id, str) or not source_turn_id.strip():
                    report.errors.append(f"{loc}: provenance.source_turn_id required for recycled_v67")
                elif source_turn_id not in v67_index.turn_to_split:
                    report.errors.append(
                        f"{loc}: provenance.source_turn_id {source_turn_id!r} does not exist in v67"
                    )
                elif (
                    isinstance(source_scenario_id, str)
                    and v67_index.turn_to_scenario.get(source_turn_id)
                    and v67_index.turn_to_scenario[source_turn_id] != source_scenario_id
                ):
                    report.errors.append(
                        f"{loc}: provenance.source_turn_id {source_turn_id!r} does not belong to scenario {source_scenario_id!r}"
                    )
                else:
                    src_action = v67_index.turn_to_action.get(source_turn_id)
                    expected_mode = V67_ACTION_TO_MODE.get(src_action or "")
                    if expected_mode is None:
                        report.errors.append(
                            f"{loc}: v67 source_turn_id {source_turn_id!r} has action {src_action!r}, which is not eligible for QLoRA recycling (allowed: request_draft->solution, hold->hold)"
                        )
                    elif mode in ALLOWED_MODES and mode != expected_mode:
                        report.errors.append(
                            f"{loc}: v67 source_turn_id {source_turn_id!r} has action {src_action!r} requiring mode={expected_mode!r}, got {mode!r}"
                        )

            gen_model = prov.get("generator_model")
            if not isinstance(gen_model, str) or not gen_model.strip() or "/" in gen_model:
                report.errors.append(
                    f"{loc}: provenance.generator_model must be a concrete model name, got {gen_model!r}"
                )
            critic_model = prov.get("critic_model")
            if critic_model is not None:
                if not isinstance(critic_model, str) or not critic_model.strip():
                    report.errors.append(f"{loc}: provenance.critic_model must be non-empty string or null")
                elif isinstance(gen_model, str) and critic_model.strip().lower() == gen_model.strip().lower():
                    report.errors.append(
                        f"{loc}: provenance.critic_model must differ from generator_model for cross-model critique"
                    )
            elif require_review and external_reviews is None:
                report.errors.append(f"{loc}: --require-review requires non-null provenance.critic_model")

            critic_status = prov.get("critic_status", "unreviewed")
            if critic_status not in ALLOWED_CRITIC_STATUSES:
                report.errors.append(f"{loc}: invalid provenance.critic_status {critic_status!r}")
            elif require_review and external_reviews is None and critic_status != "PASS":
                report.errors.append(f"{loc}: --require-review requires provenance.critic_status == 'PASS'")

            human_review = prov.get("human_review")
            if human_review not in ALLOWED_HUMAN_REVIEWS:
                report.errors.append(f"{loc}: invalid provenance.human_review {human_review!r}")
            elif human_review == "approved":
                total_human_approved += 1
                if is_high_risk:
                    high_risk_human_approved += 1

        # External Critic review sidecar verification
        if external_reviews is not None and isinstance(row_id, str):
            ext = external_reviews.get(row_id)
            if ext is None:
                report.errors.append(f"{loc}: missing external critic review record for row_id {row_id!r}")
            else:
                if ext.get("decision") != "PASS":
                    report.errors.append(
                        f"{loc}: external critic review decision for {row_id!r} is {ext.get('decision')!r} (expected 'PASS')"
                    )
                ext_model = ext.get("critic_model")
                if not isinstance(ext_model, str) or not ext_model.strip():
                    report.errors.append(f"{loc}: external critic review missing 'critic_model' for {row_id!r}")
                elif isinstance(gen_model, str) and ext_model.strip().lower() == gen_model.strip().lower():
                    report.errors.append(
                        f"{loc}: external critic_model {ext_model!r} must differ from generator_model {gen_model!r}"
                    )

        # 2. v67 split-preservation & leakage checks
        for sid_check in (scenario_id, source_scenario_id):
            if isinstance(sid_check, str) and sid_check:
                if sid_check in v67_index.test_scenarios:
                    report.errors.append(f"{loc}: v67 test_internal scenario leakage: {sid_check!r}")
                elif sid_check in v67_index.scenario_to_split and split in ALLOWED_SPLITS:
                    expected_split = v67_index.scenario_to_split[sid_check]
                    if split != expected_split:
                        report.errors.append(
                            f"{loc}: v67 split mismatch for scenario {sid_check!r}: got {split!r}, expected {expected_split!r}"
                        )
        if isinstance(source_turn_id, str) and source_turn_id:
            if source_turn_id in v67_index.test_turns:
                report.errors.append(f"{loc}: v67 test_internal source_turn_id leakage: {source_turn_id!r}")
            elif source_turn_id in v67_index.turn_to_split and split in ALLOWED_SPLITS:
                expected_split = v67_index.turn_to_split[source_turn_id]
                if split != expected_split:
                    report.errors.append(
                        f"{loc}: v67 split mismatch for source_turn_id {source_turn_id!r}: got {split!r}, expected {expected_split!r}"
                    )
        if isinstance(group_id, str) and group_id:
            if group_id in v67_index.test_groups:
                report.errors.append(f"{loc}: v67 test_internal group_id leakage: {group_id!r}")
            elif group_id in v67_index.group_to_split and split in ALLOWED_SPLITS:
                expected_split = v67_index.group_to_split[group_id]
                if split != expected_split:
                    report.errors.append(
                        f"{loc}: v67 split mismatch for group_id {group_id!r}: got {split!r}, expected {expected_split!r}"
                    )

        # 3. Messages structure & exact system prompt
        messages = row.get("messages")
        if not isinstance(messages, list) or len(messages) != 3:
            report.errors.append(f"{loc}: 'messages' must be a list of exactly 3 items [system, user, assistant]")
            continue

        roles = [m.get("role") if isinstance(m, dict) else None for m in messages]
        if roles != ["system", "user", "assistant"]:
            report.errors.append(f"{loc}: messages roles must be ['system', 'user', 'assistant'], got {roles!r}")
            continue

        sys_content = messages[0].get("content")
        user_content = messages[1].get("content")
        asst_content = messages[2].get("content")

        if sys_content != system_prompt:
            report.errors.append(f"{loc}: messages[0].content does not match the {profile} system prompt verbatim")
        if not isinstance(user_content, str) or not user_content.strip():
            report.errors.append(f"{loc}: messages[1].content must be a non-empty JSON string")
            continue
        if not isinstance(asst_content, str) or not asst_content.strip():
            report.errors.append(f"{loc}: messages[2].content must be a non-empty string")
            continue

        # Track cross-split leakage & new_synthetic family/group split distribution
        if split in ALLOWED_SPLITS:
            if isinstance(group_id, str) and group_id:
                group_splits.setdefault(group_id, set()).add(split)
            if isinstance(scenario_id, str) and scenario_id:
                scenario_splits.setdefault(scenario_id, set()).add(split)
            if isinstance(family_id, str) and family_id:
                family_splits.setdefault(family_id, set()).add(split)
            if isinstance(source_turn_id, str) and source_turn_id:
                source_turn_splits.setdefault(source_turn_id, set()).add(split)
            assistant_splits.setdefault(_normalize_text(asst_content), set()).add(split)
            if src_origin == "new_synthetic":
                new_syn_split_counts[split] += 1
                if isinstance(family_id, str) and family_id:
                    new_syn_family_splits.setdefault(family_id, set()).add(split)
                if isinstance(group_id, str) and group_id:
                    new_syn_group_splits.setdefault(group_id, set()).add(split)

        # 4. Inner SLMRequest Pydantic validation & outer-inner consistency
        legacy_kb_judgments: list[Any] = []
        try:
            if anchored:
                raw_req = json.loads(user_content)
                if not isinstance(raw_req, dict):
                    raise ValueError("SLMRequest JSON must be an object")
                extracted_judgments = raw_req.pop("kb_judgments", [])
                if not isinstance(extracted_judgments, list):
                    raise ValueError("kb_judgments must be a list")
                legacy_kb_judgments = extracted_judgments
                req = SLMRequest.model_validate(raw_req)
            else:
                req = SLMRequest.model_validate_json(user_content)
        except Exception as exc:
            report.errors.append(f"{loc}: SLMRequest validation failed: {exc}")
            continue

        if req.mode != mode:
            report.errors.append(f"{loc}: outer mode {mode!r} != inner SLMRequest.mode {req.mode!r}")
        if row.get("allowed_evidence_refs") != req.allowed_evidence_refs:
            report.errors.append(f"{loc}: outer allowed_evidence_refs != inner SLMRequest.allowed_evidence_refs")
        if row.get("distractor_refs") != req.distractor_refs:
            report.errors.append(f"{loc}: outer distractor_refs != inner SLMRequest.distractor_refs")

        if req.mode == "solution":
            report.solution_rows += 1
        elif req.mode == "hold":
            report.hold_rows += 1

        # 5. KB variable registry & value_type validation
        for var_key, obs in req.confirmed_observations.items():
            if obs.variable_id != var_key:
                report.errors.append(f"{loc}: observation key {var_key!r} != obs.variable_id {obs.variable_id!r}")
            if var_key not in kb_index.variable_types:
                if anchored or not var_key.strip() or var_key.casefold().startswith("product."):
                    report.errors.append(f"{loc}: unknown KB v0.6.1 variable_id {var_key!r}")
            elif obs.state == "known":
                vtype = kb_index.variable_types[var_key]
                if not _is_valid_kb_value(vtype, obs.value):
                    report.errors.append(
                        f"{loc}: variable {var_key!r} expects KB value_type={vtype!r}, got {type(obs.value).__name__} ({obs.value!r})"
                    )

        # 5b. Controlled vocabulary checks for legacy kb_judgments.status and product_evidence.status
        for j in legacy_kb_judgments:
            if isinstance(j, dict):
                j_status = j.get("status")
                if j_status not in ALLOWED_KB_JUDGMENT_STATUSES:
                    report.errors.append(
                        f"{loc}: kb_judgment status {j_status!r} not in controlled vocabulary {sorted(ALLOWED_KB_JUDGMENT_STATUSES)}"
                    )
        for p in req.product_evidence:
            if isinstance(p, dict) and "status" in p and p["status"] is not None:
                if p["status"] not in ALLOWED_PRODUCT_EVIDENCE_STATUSES:
                    report.errors.append(
                        f"{loc}: product_evidence status {p['status']!r} not in controlled vocabulary {sorted(ALLOWED_PRODUCT_EVIDENCE_STATUSES)}"
                    )

        # 6. Evidence refs, input backing, computed catalog versions, chunk_origins, source_registry
        for ref_id in req.allowed_evidence_refs + req.distractor_refs:
            err = _validate_ref_id(ref_id, kb_index, anchored=anchored)
            if err:
                report.errors.append(f"{loc}: {err}")

        chunk_origins = row.get("chunk_origins")
        if not isinstance(chunk_origins, dict):
            report.errors.append(f"{loc}: missing or non-dict 'chunk_origins'")
            chunk_origins = {}

        allowed_set = set(req.allowed_evidence_refs)
        distractor_set = set(req.distractor_refs)
        chunk_refs_seen: set[str] = set()
        has_english_relevant_chunk = False

        judgment_card_ids = {
            j.get("card_id") for j in legacy_kb_judgments if isinstance(j, dict) and isinstance(j.get("card_id"), str)
        }
        product_refs: set[str] = set()
        alternative_refs: set[str] = set()
        for p in req.product_evidence:
            if not isinstance(p, dict):
                continue
            pid = p.get("product_id")
            ver = p.get("version")
            eref = p.get("evidence_ref")
            if isinstance(pid, str) and pid and isinstance(ver, str) and ver:
                computed_ref = f"catalog:{pid}@{ver}"
                product_refs.add(computed_ref)
                if isinstance(eref, str) and eref.startswith("catalog:") and eref != computed_ref:
                    report.errors.append(
                        f"{loc}: product_evidence evidence_ref {eref!r} mismatches product_id/version ({computed_ref!r})"
                    )
            elif isinstance(eref, str) and eref.startswith("catalog:"):
                report.errors.append(
                    f"{loc}: product_evidence catalog evidence_ref {eref!r} requires matching product_id and version"
                )
            if isinstance(eref, str) and eref.startswith("alternative:"):
                alternative_refs.add(eref)
        alternative_refs |= {
            j.get("alternative_ref")
            for j in legacy_kb_judgments
            if isinstance(j, dict) and isinstance(j.get("alternative_ref"), str)
        }

        for chunk in req.rag_chunks:
            cref = chunk.evidence_ref
            chunk_refs_seen.add(cref)
            if cref not in allowed_set and cref not in distractor_set:
                report.errors.append(
                    f"{loc}: rag_chunk {cref!r} is in neither allowed_evidence_refs nor distractor_refs"
                )
            origin = chunk_origins.get(cref)
            if origin not in allowed_chunk_origins:
                report.errors.append(
                    f"{loc}: chunk_origins[{cref!r}] must be in {sorted(allowed_chunk_origins)}, got {origin!r}"
                )
            elif origin == "synthetic_defense_probe" and cref in allowed_set:
                report.errors.append(
                    f"{loc}: synthetic_defense_probe chunk {cref!r} must NOT be in allowed_evidence_refs"
                )

            if anchored:
                src_meta = kb_index.source_registry.get(cref.removeprefix("ref:"))
                if src_meta is not None:
                    for chunk_field, kb_field in (
                        ("source_url", "url"),
                        ("locator", "locator"),
                        ("checked_on", "checked_on"),
                        ("limitations", "limitations"),
                    ):
                        expected_val = src_meta.get(kb_field)
                        if expected_val is not None and getattr(chunk, chunk_field) != expected_val:
                            report.errors.append(
                                f"{loc}: rag_chunk {cref!r}.{chunk_field} does not match KB source_registry.{kb_field}"
                            )
            else:
                for chunk_field in ("source_url", "locator", "checked_on", "limitations"):
                    if not getattr(chunk, chunk_field).strip():
                        report.errors.append(f"{loc}: rag_chunk {cref!r}.{chunk_field} must not be blank")

            if cref in allowed_set and origin in {"kb_source_summary", "reference_excerpt"} and _is_english_text(chunk.text):
                has_english_relevant_chunk = True

        for aref in req.allowed_evidence_refs:
            if aref.startswith("ref:") and aref not in chunk_refs_seen:
                report.errors.append(f"{loc}: allowed_evidence_ref {aref!r} not backed by any input rag_chunks")
            elif aref.startswith("kb:"):
                card_part = aref.split(":", 1)[1].split("@", 1)[0]
                if card_part not in judgment_card_ids:
                    report.errors.append(
                        f"{loc}: allowed_evidence_ref {aref!r} not backed by any input kb_judgments"
                    )
            elif aref.startswith("catalog:") and aref not in product_refs:
                report.errors.append(
                    f"{loc}: allowed_evidence_ref {aref!r} not backed by any input product_evidence"
                )
            elif aref.startswith("alternative:") and aref not in alternative_refs:
                report.errors.append(
                    f"{loc}: allowed_evidence_ref {aref!r} not backed by input product_evidence/kb_judgments"
                )

        for dref in req.distractor_refs:
            if dref.startswith("ref:") and dref not in chunk_refs_seen:
                report.errors.append(
                    f"{loc}: distractor_ref {dref!r} not backed by any input rag_chunks"
                )

        # Verify external critic content_sha256 matches all reviewed fields
        if external_reviews is not None and isinstance(row_id, str) and row_id in external_reviews:
            ext = external_reviews[row_id]
            expected_sha = compute_row_content_sha256(
                req,
                asst_content,
                card_ids=card_ids if isinstance(card_ids, list) else [],
                chunk_origins=chunk_origins,
                is_hard_negative=is_hn if isinstance(is_hn, bool) else None,
                hard_negative_type=hn_type if isinstance(hn_type, str) else None,
            )
            actual_sha = ext.get("content_sha256")
            if actual_sha != expected_sha:
                report.errors.append(
                    f"{loc}: external critic content_sha256 mismatch for {row_id!r} (content/metadata modified after review or missing hash)"
                )

        extra_origin_keys = set(chunk_origins.keys()) - chunk_refs_seen
        if extra_origin_keys:
            report.errors.append(
                f"{loc}: chunk_origins has keys not present in rag_chunks: {sorted(extra_origin_keys)}"
            )

        if req.mode == "solution" and has_english_relevant_chunk:
            report.english_relevant_solution_rows += 1

        # 7. Strict citation integrity in assistant output
        cited = set(BRACKET_CITATION_PATTERN.findall(asst_content))
        invalid_cited = cited - allowed_set
        if invalid_cited:
            report.errors.append(f"{loc}: assistant cited unallowed/malformed refs: {sorted(invalid_cited)}")
        distractor_cited = cited & distractor_set
        if distractor_cited:
            report.errors.append(f"{loc}: assistant cited distractor_refs: {sorted(distractor_cited)}")
        probe_cited = {c for c in cited if chunk_origins.get(c) == "synthetic_defense_probe"}
        if probe_cited:
            report.errors.append(f"{loc}: assistant cited synthetic_defense_probe refs: {sorted(probe_cited)}")
        if req.mode == "solution" and not cited:
            report.errors.append(f"{loc}: solution response must cite at least one allowed_evidence_ref")

        # 8. Mode structure & safety guardrails
        if req.mode == "solution":
            for heading in SOLUTION_REQUIRED_HEADINGS:
                if heading not in asst_content:
                    report.errors.append(f"{loc}: solution response missing required heading {heading!r}")
        elif req.mode == "hold":
            for heading in HOLD_REQUIRED_HEADINGS:
                if heading not in asst_content:
                    report.errors.append(f"{loc}: hold response missing required heading {heading!r}")
            for pat in HOLD_RECOMMENDATION_LEAK_PATTERNS:
                if pat.search(asst_content):
                    report.errors.append(f"{loc}: hold response leaked recommendation phrase matching {pat.pattern!r}")

        for pat in FORBIDDEN_CLINICAL_PATTERNS:
            if pat.search(asst_content):
                report.errors.append(f"{loc}: assistant response violated clinical guardrail {pat.pattern!r}")

        # 8b. Canonical SLMRequest duplicate detection (applies to ALL runs: pilot, batch, and stage1)
        canonical_payload = req.model_dump(mode="json")
        if anchored:
            canonical_payload["kb_judgments"] = legacy_kb_judgments
        canonical_user = json.dumps(canonical_payload, sort_keys=True, ensure_ascii=False)
        if canonical_user in seen_user_inputs:
            report.errors.append(f"{loc}: duplicate canonical SLMRequest payload (every row must have a distinct input)")
        else:
            seen_user_inputs.add(canonical_user)

        # 8c. Pilot real semantic bucket checks
        if pilot_mode:
            if pilot_bucket == "unknown_or_version":
                has_unknown_obs = any(obs.state == "unknown" for obs in req.confirmed_observations.values())
                has_unknown_judgment = any(
                    isinstance(j, dict) and j.get("status") == "unknown"
                    for j in legacy_kb_judgments
                )
                has_version_product = any(
                    isinstance(p, dict) and p.get("status") in ("usage_held", "unknown")
                    for p in req.product_evidence
                )
                if not (has_unknown_obs or has_unknown_judgment or has_version_product):
                    report.errors.append(
                        f"{loc}: pilot_bucket='unknown_or_version' requires actual unknown observation, kb_judgment status='unknown', or product_evidence status in ('usage_held', 'unknown')"
                    )
            elif pilot_bucket == "distractor_or_defense":
                has_probe = any(v == "synthetic_defense_probe" for v in chunk_origins.values())
                if not (req.distractor_refs or has_probe):
                    report.errors.append(
                        f"{loc}: pilot_bucket='distractor_or_defense' must include distractor_refs or synthetic_defense_probe"
                    )

    # Cross-split leakage across submitted rows
    for label, mapping in (
        ("group_id", group_splits),
        ("scenario_id", scenario_splits),
        ("scenario_family_id", family_splits),
        ("source_turn_id", source_turn_splits),
        ("normalized assistant text", assistant_splits),
    ):
        for key, splits in mapping.items():
            if len(splits) > 1:
                report.errors.append(f"cross-split leakage: {label} {key!r} appears in multiple splits {sorted(splits)}")

    report.split_counts = dict(split_counter)
    report.pilot_bucket_counts = dict(pilot_bucket_counter)

    # Human review check when --require-review is enabled
    if require_review:
        if pilot_mode:
            if total_human_approved != report.total_rows:
                report.errors.append(
                    f"review check: pilot mode requires 100% human_review=='approved' ({total_human_approved}/{report.total_rows})"
                )
        elif high_risk_rows > 0:
            min_needed = max(1, (high_risk_rows + 9) // 10)
            if high_risk_human_approved < min_needed:
                report.errors.append(
                    f"review check: high-risk human_review=='approved' count {high_risk_human_approved} < required 10% ({min_needed}/{high_risk_rows})"
                )

    # 9. Pilot & Stage-1 distribution / ratio checks
    hold_ratio = report.hold_rows / report.total_rows
    hn_ratio = report.hard_negative_rows / report.total_rows
    en_ratio = (
        report.english_relevant_solution_rows / report.solution_rows
        if report.solution_rows
        else 0.0
    )

    if pilot_mode:
        if (
            report.total_rows != PILOT_TOTAL_ROWS
            or report.solution_rows != PILOT_SOLUTION_ROWS
            or report.hold_rows != PILOT_HOLD_ROWS
        ):
            report.errors.append(
                f"pilot check: expected {PILOT_TOTAL_ROWS} rows ({PILOT_SOLUTION_ROWS} sol / {PILOT_HOLD_ROWS} hold), got total={report.total_rows}, sol={report.solution_rows}, hold={report.hold_rows}"
            )
        for bucket in sorted(ALLOWED_PILOT_BUCKETS):
            if pilot_bucket_counter[bucket] != PILOT_PER_BUCKET:
                report.errors.append(
                    f"pilot check: bucket {bucket!r} expected {PILOT_PER_BUCKET} rows, got {pilot_bucket_counter[bucket]}"
                )
        if hn_ratio < 0.25:
            report.errors.append(f"pilot check: hard_negative_ratio {hn_ratio:.3f} < 0.25")
    elif enforce_ratios:
        if enforce_stage1_min_rows:
            if report.total_rows < STAGE1_MIN_TOTAL_ROWS:
                report.errors.append(
                    f"stage1 check: expected >= {STAGE1_MIN_TOTAL_ROWS} total rows, got {report.total_rows}"
                )
            if report.solution_rows < STAGE1_MIN_SOLUTION_ROWS:
                report.errors.append(
                    f"stage1 check: expected >= {STAGE1_MIN_SOLUTION_ROWS} solution rows, got {report.solution_rows}"
                )
            if report.hold_rows < STAGE1_MIN_HOLD_ROWS:
                report.errors.append(
                    f"stage1 check: expected >= {STAGE1_MIN_HOLD_ROWS} hold rows, got {report.hold_rows}"
                )
        if split_counter["val_internal"] == 0:
            report.errors.append("split check: val_internal must not be empty in final submission")
        total_new_syn = sum(new_syn_split_counts.values())
        if total_new_syn > 0:
            if new_syn_split_counts["val_internal"] == 0:
                report.errors.append("split check: new_synthetic val_internal must not be empty")
            else:
                val_families = sum(1 for sp in new_syn_family_splits.values() if sp == {"val_internal"})
                total_families = len(new_syn_family_splits)
                if total_families >= 10:
                    val_fam_ratio = val_families / total_families
                    if not (0.07 <= val_fam_ratio <= 0.13):
                        report.errors.append(
                            f"split check: new_synthetic val_internal family ratio {val_fam_ratio:.3f} ({val_families}/{total_families}) outside [0.07, 0.13]"
                        )
                val_groups = sum(1 for sp in new_syn_group_splits.values() if sp == {"val_internal"})
                total_groups = len(new_syn_group_splits)
                if total_groups >= 10:
                    val_grp_ratio = val_groups / total_groups
                    if not (0.07 <= val_grp_ratio <= 0.13):
                        report.errors.append(
                            f"split check: new_synthetic val_internal group ratio {val_grp_ratio:.3f} ({val_groups}/{total_groups}) outside [0.07, 0.13]"
                        )
        if not (0.20 <= hold_ratio <= 0.25):
            report.errors.append(f"ratio check: hold_ratio {hold_ratio:.3f} outside [0.20, 0.25]")
        if hn_ratio < 0.25:
            report.errors.append(f"ratio check: hard_negative_ratio {hn_ratio:.3f} < 0.25")
        if not (0.30 <= en_ratio <= 0.40):
            report.errors.append(
                f"ratio check: english_relevant_solution_ratio {en_ratio:.3f} outside [0.30, 0.40]"
            )

    return report


def load_jsonl_files(paths: list[pathlib.Path]) -> tuple[list[tuple[str, int, dict[str, Any]]], list[str]]:
    rows: list[tuple[str, int, dict[str, Any]]] = []
    parse_errors: list[str] = []
    for path in paths:
        if not path.exists():
            parse_errors.append(f"{path}: file not found")
            continue
        for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                parse_errors.append(f"{path}:{idx}: invalid JSON: {exc}")
                continue
            if not isinstance(obj, dict):
                parse_errors.append(f"{path}:{idx}: row must be a JSON object")
                continue
            rows.append((str(path), idx, obj))
    return rows, parse_errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Ppopy v3 QLoRA synthetic JSONL dataset.")
    parser.add_argument("--input", nargs="+", required=True, help="Dataset JSONL path(s).")
    parser.add_argument(
        "--profile",
        choices=("rag-free", "kb-anchored"),
        default="rag-free",
        help="Use Anchor OFF with Reference RAG (default), or require legacy KB source metadata.",
    )
    parser.add_argument("--pilot", action="store_true", help="24-row pilot gate (18 sol / 6 hold, 4 buckets x 6).")
    parser.add_argument("--stage1", action="store_true", help="Stage-1 full training gate (>=900 rows + ratios + 90/10 split).")
    parser.add_argument("--enforce-ratios", action="store_true", help="Enforce hold/HN/EN/val_internal ratios.")
    parser.add_argument(
        "--require-review",
        action="store_true",
        help="Require cross-model critic PASS and >=10%% human review on high-risk rows.",
    )
    parser.add_argument(
        "--review-file",
        type=pathlib.Path,
        default=None,
        help="Optional external critic review JSONL file (row_id, critic_model, decision).",
    )
    parser.add_argument(
        "--kb-dir",
        type=pathlib.Path,
        default=REPO_ROOT / "KB" / "Poppy_KB_v0.6.1",
        help="Path to KB/Poppy_KB_v0.6.1 directory.",
    )
    parser.add_argument(
        "--v67-dir",
        type=pathlib.Path,
        default=COS_AGENT_DIR / "data" / "action_policy" / "v67",
        help="Path to data/action_policy/v67 directory.",
    )
    parser.add_argument("--report", type=pathlib.Path, default=None, help="Optional JSON report output path.")
    args = parser.parse_args(argv)

    paths = [pathlib.Path(p) for p in args.input]
    file_rows, parse_errors = load_jsonl_files(paths)
    kb_index = load_kb_index(args.kb_dir)
    v67_index = load_v67_index(args.v67_dir)
    external_reviews = load_external_reviews(args.review_file) if args.review_file else None

    report = validate_rows(
        file_rows,
        kb_index,
        v67_index,
        profile=args.profile,
        input_files=[str(p) for p in paths],
        enforce_ratios=args.enforce_ratios or args.stage1,
        enforce_stage1_min_rows=args.stage1,
        pilot_mode=args.pilot,
        require_review=args.require_review or (external_reviews is not None),
        external_reviews=external_reviews,
    )
    report.errors = parse_errors + report.errors

    payload = report.to_dict()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
