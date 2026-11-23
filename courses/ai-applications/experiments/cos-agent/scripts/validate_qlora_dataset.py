#!/usr/bin/env python3
"""Shared validator for Ppopy v3 QLoRA (SOLUTION_MODE + HOLD_MODE) synthetic datasets.

Validates individual team shards (--shard a|b|c) or merged datasets (--merge) against:
1. Outer JSONL row schema, deterministic ID format, and exact SYSTEM_PROMPT_SOLUTION_HOLD
2. Inner v3_contracts.SLMRequest Pydantic contract + outer/inner mode & refs alignment
3. KB v0.6.1 variable registry & value_type compatibility + baseline card registry
4. KB v0.6.1 source_registry exact metadata match (url, locator, checked_on, limitations)
5. Strict citation integrity (catches unprefixed/unknown [S99] and distractor citations)
6. Mode structure, hold recommendation-leak prevention, and clinical/diagnosis guardrails
7. v67 split-preservation & cross-split leakage prevention (test_internal strictly blocked)
8. Denominator-explicit distribution checks (hold 20-25%, hard negative >=25%, EN relevant 30-40%)
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from typing import Any

COS_AGENT_DIR = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = COS_AGENT_DIR.parents[3]
if str(COS_AGENT_DIR) not in sys.path:
    sys.path.insert(0, str(COS_AGENT_DIR))

from beauty_agent.v3_contracts import SLMRequest

SYSTEM_PROMPT_SOLUTION_HOLD = (
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
ALLOWED_CHUNK_ORIGINS = frozenset({"kb_source_summary", "synthetic_defense_probe"})
ALLOWED_SOURCE_ORIGINS = frozenset({"new_synthetic", "recycled_v67"})
ALLOWED_HUMAN_REVIEWS = frozenset({"unreviewed", "approved", "needs_revision"})

FORBIDDEN_SOURCE_IDS = frozenset({"F01", "F02", "S30", "S31"})
FORBIDDEN_CARD_IDS = frozenset({"B-P07"})

ROW_ID_PATTERN = re.compile(r"^syn-(?P<shard>[abc])-(?P<kind>sol|hold)-(?P<num>\d{4})$")
# Catches both prefixed ([ref:S08], [kb:B-I01@0.6.1]) and bare ID-like brackets ([S99], [B-C01]).
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
)
HOLD_RECOMMENDATION_LEAK_PATTERNS = (
    re.compile(r"대체\s*후보"),
    re.compile(r"루틴을\s*(유지|추천|권해)"),
    re.compile(r"(사용해\s*보세요|바르는\s*것을\s*권해|권해드려요|추천해\s*드려요|추천해요)"),
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
    test_scenarios: set[str] = field(default_factory=set)
    test_groups: set[str] = field(default_factory=set)


@dataclass
class ValidationReport:
    files: list[str]
    total_rows: int = 0
    solution_rows: int = 0
    hold_rows: int = 0
    hard_negative_rows: int = 0
    english_relevant_solution_rows: int = 0
    split_counts: dict[str, int] = field(default_factory=dict)
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
            "error_count": len(self.errors),
            "errors": self.errors,
            "warnings": self.warnings,
        }


def load_kb_index(kb_dir: pathlib.Path) -> KBReferenceIndex:
    seed_path = kb_dir / "Poppy_KB_seed_v0.6.1.json"
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


def load_v67_index(v67_dir: pathlib.Path | None) -> V67SplitIndex:
    index = V67SplitIndex()
    if v67_dir is None or not v67_dir.exists():
        return index
    split_files = (
        ("train", v67_dir / "v67-sft-train.jsonl"),
        ("val_internal", v67_dir / "v67-sft-val-internal.jsonl"),
        ("test_internal", v67_dir / "v67-sft-test-internal.jsonl"),
    )
    for split_name, path in split_files:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            sid = row.get("scenario_id")
            gid = row.get("group_id")
            if sid:
                index.scenario_to_split[sid] = split_name
                if split_name == "test_internal":
                    index.test_scenarios.add(sid)
            if gid:
                index.group_to_split[gid] = split_name
                if split_name == "test_internal":
                    index.test_groups.add(gid)
    return index


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
    # structured, latent, derived, research_only allow structured JSON values
    return value is not None


def _is_english_text(text: str) -> bool:
    words = ENGLISH_WORD_PATTERN.findall(text)
    return len(words) >= 8


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _validate_ref_id(ref_id: str, kb_index: KBReferenceIndex) -> str | None:
    if not ref_id.startswith(ALLOWED_REF_PREFIXES):
        return f"invalid evidence_ref prefix: {ref_id!r}"
    if ref_id.startswith("ref:"):
        sid = ref_id.split(":", 1)[1]
        if sid.startswith(("U", "D")) or sid in FORBIDDEN_SOURCE_IDS:
            return f"forbidden source_id in evidence_ref: {ref_id!r}"
        if sid not in kb_index.source_registry:
            return f"unknown source_id in KB v0.6.1 source_registry: {ref_id!r}"
    elif ref_id.startswith("kb:"):
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
    expected_shard: str | None = None,
    enforce_ratios: bool = False,
    pilot_mode: bool = False,
) -> ValidationReport:
    report = ValidationReport(files=sorted({src for src, _, _ in file_rows}))
    seen_ids: dict[str, str] = {}
    group_splits: dict[str, set[str]] = {}
    scenario_splits: dict[str, set[str]] = {}
    assistant_splits: dict[str, set[str]] = {}
    split_counter: Counter[str] = Counter()

    for src, line_no, row in file_rows:
        loc = f"{src}:{line_no}"
        report.total_rows += 1

        # 1. Outer row required keys & types
        row_id = row.get("id")
        mode = row.get("mode")
        split = row.get("split")
        scenario_id = row.get("scenario_id")
        group_id = row.get("group_id")

        if not isinstance(row_id, str):
            report.errors.append(f"{loc}: missing or non-string 'id'")
        else:
            m = ROW_ID_PATTERN.match(row_id)
            if not m:
                report.errors.append(f"{loc}: invalid id format {row_id!r} (expected syn-{{a|b|c}}-{{sol|hold}}-0001)")
            else:
                if expected_shard and m.group("shard") != expected_shard:
                    report.errors.append(f"{loc}: id shard {m.group('shard')!r} != expected {expected_shard!r}")
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
            report.errors.append(f"{loc}: invalid split {split!r} (allowed: {sorted(ALLOWED_SPLITS)}; test_internal forbidden)")
        else:
            split_counter[split] += 1

        if not isinstance(scenario_id, str) or not scenario_id.strip():
            report.errors.append(f"{loc}: missing or empty 'scenario_id'")
        if not isinstance(group_id, str) or not group_id.strip():
            report.errors.append(f"{loc}: missing or empty 'group_id'")

        domains = row.get("domains")
        if not isinstance(domains, list) or not domains or not all(d in ALLOWED_DOMAINS for d in domains):
            report.errors.append(f"{loc}: invalid 'domains' {domains!r}")

        card_ids = row.get("card_ids")
        if not isinstance(card_ids, list) or not card_ids:
            report.errors.append(f"{loc}: missing or empty 'card_ids'")
        else:
            for cid in card_ids:
                if cid in FORBIDDEN_CARD_IDS:
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
                report.errors.append(f"{loc}: invalid 'hard_negative_type' {hn_type!r} when is_hard_negative=True")
        elif hn_type is not None:
            report.errors.append(f"{loc}: 'hard_negative_type' must be null when is_hard_negative=False")

        # Provenance checks
        prov = row.get("provenance")
        source_scenario_id: str | None = None
        if not isinstance(prov, dict):
            report.errors.append(f"{loc}: missing or non-dict 'provenance'")
        else:
            src_origin = prov.get("source_origin")
            if src_origin not in ALLOWED_SOURCE_ORIGINS:
                report.errors.append(f"{loc}: invalid provenance.source_origin {src_origin!r}")
            source_scenario_id = prov.get("source_scenario_id")
            if src_origin == "recycled_v67" and (not isinstance(source_scenario_id, str) or not source_scenario_id.strip()):
                report.errors.append(f"{loc}: provenance.source_scenario_id required for recycled_v67")
            gen_model = prov.get("generator_model")
            if not isinstance(gen_model, str) or not gen_model.strip() or "/" in gen_model:
                report.errors.append(f"{loc}: provenance.generator_model must be a concrete model name, got {gen_model!r}")
            critic_model = prov.get("critic_model")
            if critic_model is not None:
                if not isinstance(critic_model, str) or not critic_model.strip():
                    report.errors.append(f"{loc}: provenance.critic_model must be non-empty string or null")
                elif isinstance(gen_model, str) and critic_model.strip().lower() == gen_model.strip().lower():
                    report.errors.append(f"{loc}: provenance.critic_model must differ from generator_model for cross-model critique")
            if prov.get("human_review") not in ALLOWED_HUMAN_REVIEWS:
                report.errors.append(f"{loc}: invalid provenance.human_review {prov.get('human_review')!r}")

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

        if sys_content != SYSTEM_PROMPT_SOLUTION_HOLD:
            report.errors.append(f"{loc}: messages[0].content does not match SYSTEM_PROMPT_SOLUTION_HOLD verbatim")
        if not isinstance(user_content, str) or not user_content.strip():
            report.errors.append(f"{loc}: messages[1].content must be a non-empty JSON string")
            continue
        if not isinstance(asst_content, str) or not asst_content.strip():
            report.errors.append(f"{loc}: messages[2].content must be a non-empty string")
            continue

        # Track cross-split leakage across submitted rows
        if split in ALLOWED_SPLITS:
            if isinstance(group_id, str) and group_id:
                group_splits.setdefault(group_id, set()).add(split)
            if isinstance(scenario_id, str) and scenario_id:
                scenario_splits.setdefault(scenario_id, set()).add(split)
            assistant_splits.setdefault(_normalize_text(asst_content), set()).add(split)

        # 4. Inner SLMRequest Pydantic validation & outer-inner consistency
        try:
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
                report.errors.append(f"{loc}: unknown KB v0.6.1 variable_id {var_key!r}")
            elif obs.state == "known":
                vtype = kb_index.variable_types[var_key]
                if not _is_valid_kb_value(vtype, obs.value):
                    report.errors.append(
                        f"{loc}: variable {var_key!r} expects KB value_type={vtype!r}, got {type(obs.value).__name__} ({obs.value!r})"
                    )

        # 6. Evidence refs & chunk_origins & KB source_registry exact metadata check
        for ref_id in req.allowed_evidence_refs + req.distractor_refs:
            err = _validate_ref_id(ref_id, kb_index)
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

        for chunk in req.rag_chunks:
            cref = chunk.evidence_ref
            chunk_refs_seen.add(cref)
            if cref not in allowed_set and cref not in distractor_set:
                report.errors.append(f"{loc}: rag_chunk {cref!r} is in neither allowed_evidence_refs nor distractor_refs")
            origin = chunk_origins.get(cref)
            if origin not in ALLOWED_CHUNK_ORIGINS:
                report.errors.append(f"{loc}: chunk_origins[{cref!r}] must be in {sorted(ALLOWED_CHUNK_ORIGINS)}, got {origin!r}")

            sid = cref.split(":", 1)[1] if cref.startswith("ref:") else ""
            src_meta = kb_index.source_registry.get(sid)
            if src_meta is None:
                report.errors.append(f"{loc}: rag_chunk {cref!r} not found in KB v0.6.1 source_registry")
            else:
                for chunk_field, kb_field in (
                    ("source_url", "url"),
                    ("locator", "locator"),
                    ("checked_on", "checked_on"),
                    ("limitations", "limitations"),
                ):
                    expected_val = src_meta.get(kb_field)
                    actual_val = getattr(chunk, chunk_field)
                    if expected_val is not None and actual_val != expected_val:
                        report.errors.append(
                            f"{loc}: rag_chunk {cref!r}.{chunk_field} does not match KB source_registry.{kb_field}"
                        )
            if cref in allowed_set and _is_english_text(chunk.text):
                has_english_relevant_chunk = True

        extra_origin_keys = set(chunk_origins.keys()) - chunk_refs_seen
        if extra_origin_keys:
            report.errors.append(f"{loc}: chunk_origins has keys not present in rag_chunks: {sorted(extra_origin_keys)}")

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

    # Cross-split leakage across submitted rows
    for gid, splits in group_splits.items():
        if len(splits) > 1:
            report.errors.append(f"cross-split leakage: group_id {gid!r} appears in multiple splits {sorted(splits)}")
    for sid, splits in scenario_splits.items():
        if len(splits) > 1:
            report.errors.append(f"cross-split leakage: scenario_id {sid!r} appears in multiple splits {sorted(splits)}")
    for text_key, splits in assistant_splits.items():
        if len(splits) > 1:
            report.errors.append(f"cross-split leakage: duplicate normalized assistant text across splits {sorted(splits)}")

    report.split_counts = dict(split_counter)

    # 9. Distribution / ratio checks
    if report.total_rows > 0:
        hold_ratio = report.hold_rows / report.total_rows
        hn_ratio = report.hard_negative_rows / report.total_rows
        en_ratio = (
            report.english_relevant_solution_rows / report.solution_rows
            if report.solution_rows
            else 0.0
        )
        min_hn = 0.25
        if pilot_mode:
            if report.solution_rows == 0 or report.hold_rows == 0:
                report.errors.append("pilot check: must include both solution and hold rows")
            if hn_ratio < min_hn:
                report.errors.append(f"pilot check: hard_negative_ratio {hn_ratio:.3f} < {min_hn:.2f}")
        elif enforce_ratios:
            if not (0.20 <= hold_ratio <= 0.25):
                report.errors.append(f"ratio check: hold_ratio {hold_ratio:.3f} outside [0.20, 0.25]")
            if hn_ratio < min_hn:
                report.errors.append(f"ratio check: hard_negative_ratio {hn_ratio:.3f} < {min_hn:.2f}")
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
    parser = argparse.ArgumentParser(description="Validate Ppopy v3 QLoRA synthetic JSONL shards.")
    parser.add_argument("--input", nargs="+", required=True, help="One or more JSONL shard paths.")
    parser.add_argument("--shard", choices=("a", "b", "c"), default=None, help="Enforce single-shard ID prefix.")
    parser.add_argument("--merge", action="store_true", help="Merged multi-shard validation mode.")
    parser.add_argument("--pilot", action="store_true", help="Pilot mode (12 turns/member, 36 merged).")
    parser.add_argument("--enforce-ratios", action="store_true", help="Fail if hold/HN/EN ratios are out of target.")
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

    report = validate_rows(
        file_rows,
        kb_index,
        v67_index,
        expected_shard=args.shard,
        enforce_ratios=args.enforce_ratios or (args.merge and not args.pilot),
        pilot_mode=args.pilot,
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
