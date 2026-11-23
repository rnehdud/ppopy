"""Unit tests for single-owner QLoRA dataset validator & v67 seed extractor."""
from __future__ import annotations

import copy
import json
import pathlib
import re
import sys

import pytest

COS_AGENT_DIR = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = COS_AGENT_DIR.parents[3]
SCRIPTS_DIR = COS_AGENT_DIR / "scripts"
for p in (str(COS_AGENT_DIR), str(SCRIPTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

import prepare_v67_qlora_seeds as v67_seeds  # noqa: E402
import validate_qlora_dataset as val  # noqa: E402


KB_INDEX = val.load_kb_index(REPO_ROOT / "KB" / "Poppy_KB_v0.6.1")
V67_INDEX = val.load_v67_index(COS_AGENT_DIR / "data" / "action_policy" / "v67")


def _make_chunk(sid: str, text: str, scope: str = "general_skincare_practice") -> dict:
    src = KB_INDEX.source_registry[sid]
    return {
        "evidence_ref": f"ref:{sid}",
        "text": text,
        "scope": scope,
        "source_url": src["url"],
        "locator": src["locator"],
        "checked_on": src["checked_on"],
        "limitations": src["limitations"],
    }


def make_valid_solution_row(
    *,
    num: int = 1,
    split: str = "train",
    pilot_bucket: str = "distractor_or_defense",
    is_hn: bool = True,
    hn_type: str | None = "rag_distractor_ignore",
    unknown_obs: bool = False,
    english_chunk: bool = True,
) -> dict:
    obs = {
        "cleansing.steps": {
            "variable_id": "cleansing.steps",
            "state": "known",
            "value": 2 + (num % 3),
            "source": "user_report",
            "confirmed_by_user": True,
        },
        "cleansing.repeat_wash": {
            "variable_id": "cleansing.repeat_wash",
            "state": "known",
            "value": {"automatic_multi_step_for_water_resistant": True, "variant": num},
            "source": "user_report",
            "confirmed_by_user": True,
        },
    }
    if unknown_obs:
        obs["cleansing.perceived_residue"] = {
            "variable_id": "cleansing.perceived_residue",
            "state": "unknown",
            "value": None,
            "source": "user_report",
            "confirmed_by_user": True,
        }
    req = {
        "mode": "solution",
        "confirmed_observations": obs,
        "kb_judgments": [
            {
                "card_id": "B-I01",
                "status": "difference",
                "guidance": "내수성 표시만 보고 무조건 반복 세안하면 피부 부담이 커질 수 있어, 광보호를 유지하면서 제품에 맞는 세정 단계를 검토합니다.",
            }
        ],
        "product_evidence": [
            {
                "product_id": f"syn-sun-{num:03d}",
                "version": "1.0",
                "synthetic_product": True,
                "status": "verified",
                "label_guidance": "합성 제품 표시 예시: 폼 클렌저 1회 세안 가능",
                "evidence_ref": f"catalog:syn-sun-{num:03d}@1.0",
            }
        ],
        "rag_chunks": [
            _make_chunk(
                "S08",
                (
                    "In a 20-subject imaging study comparing water, facial cleanser, and cleansing oil, cleanser removal performance varied by formulation rather than requiring mandatory multi-step washing for every water-resistant product."
                    if english_chunk
                    else "20명 대상 영상 비교 연구에서 물·세정제·클렌징오일의 자외선차단제 세정 결과는 제형에 따라 달라졌으며, 모든 내수성 제품에 다단계 세안을 일률적으로 정하지 않았습니다."
                ),
            ),
            _make_chunk(
                "S21",
                "Apply fragrance-free hand cream or ointment immediately after hand washing to help relieve dry hands.",
            ),
        ],
        "allowed_evidence_refs": ["kb:B-I01@0.6.1", f"catalog:syn-sun-{num:03d}@1.0", "ref:S08"],
        "distractor_refs": ["ref:S21"],
    }
    return {
        "id": f"syn-sol-{num:04d}",
        "scenario_id": f"new-bi01-{num:03d}",
        "group_id": f"new-group-bi01-{num:03d}",
        "scenario_family_id": f"fam-bi01-{num:03d}",
        "split": split,
        "mode": "solution",
        "pilot_bucket": pilot_bucket,
        "domains": ["cleansing", "sun_protection"],
        "card_ids": ["B-I01", "B-C05"],
        "is_hard_negative": is_hn,
        "hard_negative_type": hn_type if is_hn else None,
        "chunk_origins": {
            "ref:S08": "kb_source_summary",
            "ref:S21": "synthetic_defense_probe",
        },
        "messages": [
            {"role": "system", "content": val.SYSTEM_PROMPT_SOLUTION_HOLD},
            {"role": "user", "content": json.dumps(req, ensure_ascii=False)},
            {
                "role": "assistant",
                "content": (
                    f"### 핵심 안내\n"
                    f"내수성 표시만 보고 무조건 반복 세안할 필요는 없어요 (시나리오 {num}). "
                    f"자외선차단제 도포량은 유지하면서 합성 제품 표시 예시의 클렌징폼 1회 세안으로 단계를 줄여 보실 수 있어요 "
                    f"[kb:B-I01@0.6.1] [catalog:syn-sun-{num:03d}@1.0].\n\n"
                    f"### 근거 및 이유\n"
                    f"20명 대상 제한된 제품 조합 영상 비교 연구에서도 제형에 따라 세정 결과가 달라지며 모든 내수성 제품에 이중세안을 일률적으로 확정하지는 않아요 [ref:S08].\n\n"
                    f"### 확인이 필요한 한계\n"
                    f"위 문헌은 소규모 제한 조합 기준이며 모든 내수성 제품에 일반화되지는 않아요. 세안 후 당김이나 자극이 반복되면 단계를 더 줄이고 확인이 필요해요."
                ),
            },
        ],
        "allowed_evidence_refs": ["kb:B-I01@0.6.1", f"catalog:syn-sun-{num:03d}@1.0", "ref:S08"],
        "distractor_refs": ["ref:S21"],
        "provenance": {
            "source_origin": "new_synthetic",
            "source_scenario_id": None,
            "source_turn_id": None,
            "generator_model": "gpt-5.4",
            "critic_model": "claude-sonnet-4",
            "critic_status": "PASS",
            "human_review": "unreviewed",
        },
    }


def make_valid_hold_row(
    *,
    num: int = 1,
    split: str = "train",
    human_review: str = "approved",
) -> dict:
    pain_levels = ("mild", "moderate", "severe")
    req = {
        "mode": "hold",
        "confirmed_observations": {
            "skin.current_discomfort": {
                "variable_id": "skin.current_discomfort",
                "state": "known",
                "value": "persistent",
                "source": "user_report",
                "confirmed_by_user": True,
            },
            "skin.pain": {
                "variable_id": "skin.pain",
                "state": "known",
                "value": pain_levels[(num - 1) % len(pain_levels)],
                "source": "user_report",
                "confirmed_by_user": True,
            },
        },
        "kb_judgments": [
            {
                "card_id": "B-B01",
                "status": "hold",
                "guidance": f"지속적인 불편감과 통증이 있어 개별 루틴 권고를 보류하고 전문가 확인을 우선 안내합니다 (case {num}).",
            }
        ],
        "product_evidence": [],
        "rag_chunks": [],
        "allowed_evidence_refs": ["kb:B-B01@0.6.1"],
        "distractor_refs": [],
    }
    return {
        "id": f"syn-hold-{num:04d}",
        "scenario_id": f"new-bb01-{num:03d}",
        "group_id": f"new-group-bb01-{num:03d}",
        "scenario_family_id": f"fam-bb01-{num:03d}",
        "split": split,
        "mode": "hold",
        "pilot_bucket": "hold",
        "domains": ["general_safety"],
        "card_ids": ["B-B01"],
        "is_hard_negative": False,
        "hard_negative_type": None,
        "chunk_origins": {},
        "messages": [
            {"role": "system", "content": val.SYSTEM_PROMPT_SOLUTION_HOLD},
            {"role": "user", "content": json.dumps(req, ensure_ascii=False)},
            {
                "role": "assistant",
                "content": (
                    f"### 개별 권고 보류 안내\n"
                    f"현재 지속적인 불편감과 통증이 확인되어 개별 루틴 조정이나 제품 안내는 보류해요 (사례 {num}) [kb:B-B01@0.6.1].\n\n"
                    f"### 필요한 다음 단계\n"
                    f"불편감이 나타난 제품 사용은 잠시 중단하시고, 증상이 이어지거나 심해지면 피부과 전문의 등 전문가의 확인을 받아 주세요. "
                    f"현재 상태의 원인 진단이나 처방은 안내해 드릴 수 없어요."
                ),
            },
        ],
        "allowed_evidence_refs": ["kb:B-B01@0.6.1"],
        "distractor_refs": [],
        "provenance": {
            "source_origin": "new_synthetic",
            "source_scenario_id": None,
            "source_turn_id": None,
            "generator_model": "gpt-5.4",
            "critic_model": "claude-sonnet-4",
            "critic_status": "PASS",
            "human_review": human_review,
        },
    }


def make_24_row_pilot() -> tuple[list[tuple[str, int, dict]], dict[str, dict]]:
    fname = "pilot_24.jsonl"
    rows: list[tuple[str, int, dict]] = []
    reviews: dict[str, dict] = {}
    line = 1
    sol_num = 1
    for bucket, is_hn, hn_type in (
        ("normal_guidance", False, None),
        ("unknown_or_version", True, "version_mismatch_or_unknown"),
        ("distractor_or_defense", True, "rag_distractor_ignore"),
    ):
        for _ in range(6):
            r = make_valid_solution_row(
                num=sol_num,
                pilot_bucket=bucket,
                is_hn=is_hn,
                hn_type=hn_type,
                unknown_obs=(bucket == "unknown_or_version"),
            )
            rows.append((fname, line, r))
            reviews[r["id"]] = {"row_id": r["id"], "critic_model": "claude-sonnet-4", "decision": "PASS"}
            line += 1
            sol_num += 1
    for h_num in range(1, 7):
        r = make_valid_hold_row(num=h_num)
        rows.append((fname, line, r))
        reviews[r["id"]] = {"row_id": r["id"], "critic_model": "claude-sonnet-4", "decision": "PASS"}
        line += 1
    return rows, reviews


def test_24_row_pilot_with_external_review_passes_and_empty_fails() -> None:
    empty = val.validate_rows([], KB_INDEX, V67_INDEX, input_files=["empty.jsonl"], pilot_mode=True)
    assert not empty.passed

    rows, reviews = make_24_row_pilot()
    rep = val.validate_rows(
        rows,
        KB_INDEX,
        V67_INDEX,
        input_files=["pilot_24.jsonl"],
        pilot_mode=True,
        require_review=True,
        external_reviews=reviews,
    )
    assert rep.passed, rep.errors
    assert rep.total_rows == 24
    assert rep.solution_rows == 18
    assert rep.hold_rows == 6

    # Missing 1 row from external review file must fail
    missing_rev = dict(reviews)
    missing_rev.pop("syn-sol-0001")
    rep_missing = val.validate_rows(
        rows,
        KB_INDEX,
        V67_INDEX,
        input_files=["pilot_24.jsonl"],
        pilot_mode=True,
        require_review=True,
        external_reviews=missing_rev,
    )
    assert not rep_missing.passed
    assert any("missing external critic review" in e for e in rep_missing.errors)


def test_controlled_vocabulary_and_product_version_spoof_rejected() -> None:
    row = make_valid_solution_row(num=1)
    req = json.loads(row["messages"][1]["content"])
    req["kb_judgments"][0]["status"] = "needs_change"  # Not in controlled vocabulary
    req["product_evidence"][0]["status"] = "expired"  # Not in controlled vocabulary
    req["product_evidence"][0]["evidence_ref"] = "catalog:syn-sun-001@999"
    row["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
    rep = val.validate_rows([("ds.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not rep.passed
    assert any("kb_judgment status" in e for e in rep.errors)
    assert any("product_evidence status" in e for e in rep.errors)
    assert any("mismatches product_id/version" in e for e in rep.errors)


def test_stage1_min_rows_and_90_10_split_enforced() -> None:
    # 20 rows cannot pass --stage1 (requires >= 900)
    small = [
        ("ds.jsonl", i, make_valid_solution_row(num=i, split=("val_internal" if i == 15 else "train"), english_chunk=(i <= 5)))
        for i in range(1, 16)
    ] + [
        ("ds.jsonl", 15 + i, make_valid_hold_row(num=i, split=("val_internal" if i == 5 else "train")))
        for i in range(1, 6)
    ]
    rep_small = val.validate_rows(small, KB_INDEX, V67_INDEX, enforce_ratios=True, enforce_stage1_min_rows=True)
    assert not rep_small.passed
    assert any(">= 900" in e for e in rep_small.errors)

    # Without stage1 min rows, 20 rows with 90/10 split & 33.3% EN pass enforce_ratios
    rep_ok = val.validate_rows(small, KB_INDEX, V67_INDEX, enforce_ratios=True)
    assert rep_ok.passed, rep_ok.errors

    # Empty val_internal fails enforce_ratios
    all_train = [
        ("ds.jsonl", i, make_valid_solution_row(num=i, split="train", english_chunk=(i <= 5)))
        for i in range(1, 16)
    ] + [("ds.jsonl", 15 + i, make_valid_hold_row(num=i, split="train")) for i in range(1, 6)]
    rep_no_val = val.validate_rows(all_train, KB_INDEX, V67_INDEX, enforce_ratios=True)
    assert not rep_no_val.passed
    assert any("val_internal must not be empty" in e for e in rep_no_val.errors)


def test_v67_seed_extractor_has_zero_test_internal_and_zero_ask_user() -> None:
    seeds, stats = v67_seeds.extract_v67_seeds(COS_AGENT_DIR / "data" / "action_policy" / "v67")
    assert stats["total_extracted"] > 700
    for s in seeds:
        assert s["split"] in ("train", "val_internal")
        assert s["v67_action"] in ("request_draft", "hold")
        assert s["source_scenario_id"] not in V67_INDEX.test_scenarios
        assert s["source_turn_id"] not in V67_INDEX.test_turns
        assert "B-P07" not in s["card_ids"]


def test_rejects_unbacked_refs_probe_citation_family_leak_and_hold_leak() -> None:
    row = make_valid_solution_row(num=1)
    row["chunk_origins"]["ref:S08"] = "synthetic_defense_probe"
    rep_probe = val.validate_rows([("ds.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not rep_probe.passed
    assert rep_probe.english_relevant_solution_rows == 0

    r1 = make_valid_solution_row(num=1, split="train")
    r2 = make_valid_solution_row(num=2, split="val_internal")
    r2["scenario_family_id"] = r1["scenario_family_id"]
    rep_fam = val.validate_rows([("ds.jsonl", 1, r1), ("ds.jsonl", 2, r2)], KB_INDEX, V67_INDEX)
    assert not rep_fam.passed
    assert any("scenario_family_id" in e for e in rep_fam.errors)

    hold_leak = make_valid_hold_row(num=1)
    hold_leak["messages"][2]["content"] += " 저녁에는 클렌징폼으로 1회 세안하세요."
    rep_hold = val.validate_rows([("ds.jsonl", 1, hold_leak)], KB_INDEX, V67_INDEX)
    assert not rep_hold.passed
    assert any("leaked recommendation" in e for e in rep_hold.errors)

    with pytest.raises(FileNotFoundError):
        val.load_v67_index(COS_AGENT_DIR / "data" / "missing_v67")


def test_guide_doc_all_3_reference_examples_pass_validator() -> None:
    guide_path = COS_AGENT_DIR / "docs" / "qlora-synthetic-dataset-guide.md"
    md = guide_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", md, re.S)
    assert len(blocks) == 3, f"Expected 3 JSON reference examples (1 sol + 2 hold), got {len(blocks)}"
    rows = [(str(guide_path), idx + 1, json.loads(b)) for idx, b in enumerate(blocks)]
    report = val.validate_rows(rows, KB_INDEX, V67_INDEX)
    assert report.passed, report.errors
    assert report.solution_rows == 1
    assert report.hold_rows == 2
