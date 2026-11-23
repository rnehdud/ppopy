"""Unit tests for scripts/validate_qlora_dataset.py (covering all Codex P0/P1 cases)."""
from __future__ import annotations

import copy
import json
import pathlib
import sys

COS_AGENT_DIR = pathlib.Path(__file__).resolve().parents[1]
REPO_ROOT = COS_AGENT_DIR.parents[3]
SCRIPTS_DIR = COS_AGENT_DIR / "scripts"
for p in (str(COS_AGENT_DIR), str(SCRIPTS_DIR)):
    if p not in sys.path:
        sys.path.insert(0, p)

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


def make_valid_solution_row(row_id: str = "syn-a-sol-0001", split: str = "train") -> dict:
    req = {
        "mode": "solution",
        "confirmed_observations": {
            "cleansing.steps": {
                "variable_id": "cleansing.steps",
                "state": "known",
                "value": 1,
                "source": "user_report",
                "confirmed_by_user": True,
            },
            "cleansing.target_load": {
                "variable_id": "cleansing.target_load",
                "state": "known",
                "value": {"water_resistant_sunscreen": True, "method": "cleansing_water_only"},
                "source": "user_report",
                "confirmed_by_user": True,
            },
        },
        "kb_judgments": [
            {
                "card_id": "B-I01",
                "status": "difference",
                "guidance": "내수성 자외선차단제를 1단계 클렌징 워터로만 닦으면 잔여물이 남을 수 있습니다.",
            }
        ],
        "product_evidence": [
            {
                "product_id": "syn-sun-001",
                "version": "1.0",
                "synthetic_product": True,
                "label_guidance": "합성 제품 표시 예시: 폼 클렌저 1회 세안 확인",
                "evidence_ref": "catalog:syn-sun-001@1.0",
            }
        ],
        "rag_chunks": [
            _make_chunk(
                "S08",
                "In a 20-subject imaging study comparing water, facial cleanser, and cleansing oil, water alone left more sunscreen residue than cleanser or cleansing oil.",
            ),
            _make_chunk(
                "S21",
                "Apply fragrance-free hand cream or ointment immediately after hand washing to help relieve dry hands.",
            ),
        ],
        "allowed_evidence_refs": ["kb:B-I01@0.6.1", "catalog:syn-sun-001@1.0", "ref:S08"],
        "distractor_refs": ["ref:S21"],
    }
    return {
        "id": row_id,
        "scenario_id": "new-bi01-001",
        "group_id": "new-group-bi01-001",
        "scenario_family_id": "bi01-water-resistant-sunscreen",
        "split": split,
        "mode": "solution",
        "domains": ["cleansing", "sun_protection"],
        "card_ids": ["B-I01", "B-C05"],
        "is_hard_negative": True,
        "hard_negative_type": "rag_distractor_ignore",
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
                    "### 핵심 안내\n"
                    "내수성 선크림을 1단계 클렌징 워터로만 닦으면 잔여물이 남을 수 있어요. "
                    "저녁에는 합성 제품 표시 예시에서 확인된 클렌징폼 1회 세안으로 조정해 보실 수 있어요 "
                    "[kb:B-I01@0.6.1] [catalog:syn-sun-001@1.0].\n\n"
                    "### 근거 및 이유\n"
                    "20명 대상 제한된 제품 조합 영상 비교 연구에서도 물 세안만으로는 자외선차단제 잔여가 더 남고 "
                    "세정제나 클렌징 오일 사용 시 제거가 나아지는 경향이 보고됐어요 [ref:S08].\n\n"
                    "### 확인이 필요한 한계\n"
                    "위 문헌은 소규모 제한 조합 기준이며 모든 내수성 제품에 일반화되지는 않아요. "
                    "세안 후 당김이나 자극이 반복되면 세정 방식을 줄이고 확인이 필요해요."
                ),
            },
        ],
        "allowed_evidence_refs": ["kb:B-I01@0.6.1", "catalog:syn-sun-001@1.0", "ref:S08"],
        "distractor_refs": ["ref:S21"],
        "provenance": {
            "source_origin": "new_synthetic",
            "source_scenario_id": None,
            "generator_model": "gpt-5.4",
            "critic_model": "claude-sonnet-4",
            "human_review": "unreviewed",
        },
    }


def make_valid_hold_row(row_id: str = "syn-a-hold-0001", split: str = "train") -> dict:
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
                "value": "moderate",
                "source": "user_report",
                "confirmed_by_user": True,
            },
        },
        "kb_judgments": [
            {
                "card_id": "B-B01",
                "status": "hold",
                "guidance": "지속적인 불편감과 통증이 있어 개별 루틴 권고를 보류하고 전문가 확인을 우선 안내합니다.",
            }
        ],
        "product_evidence": [],
        "rag_chunks": [],
        "allowed_evidence_refs": ["kb:B-B01@0.6.1"],
        "distractor_refs": [],
    }
    return {
        "id": row_id,
        "scenario_id": "new-bb01-001",
        "group_id": "new-group-bb01-001",
        "scenario_family_id": "bb01-persistent-pain",
        "split": split,
        "mode": "hold",
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
                    "### 개별 권고 보류 안내\n"
                    "현재 지속적인 불편감과 통증이 확인되어 개별 루틴 조정이나 제품 안내는 보류해요 [kb:B-B01@0.6.1].\n\n"
                    "### 필요한 다음 단계\n"
                    "불편감이 나타난 제품 사용은 잠시 중단하시고, 증상이 이어지거나 심해지면 피부과 전문의 등 전문가의 확인을 받아 주세요. "
                    "현재 상태의 원인 진단이나 처방은 안내해 드릴 수 없어요."
                ),
            },
        ],
        "allowed_evidence_refs": ["kb:B-B01@0.6.1"],
        "distractor_refs": [],
        "provenance": {
            "source_origin": "new_synthetic",
            "source_scenario_id": None,
            "generator_model": "gpt-5.4",
            "critic_model": "claude-sonnet-4",
            "human_review": "unreviewed",
        },
    }


def test_valid_solution_and_hold_pass_pilot() -> None:
    sol = make_valid_solution_row()
    hold = make_valid_hold_row()
    report = val.validate_rows(
        [("shard_a.jsonl", 1, sol), ("shard_a.jsonl", 2, hold)],
        KB_INDEX,
        V67_INDEX,
        expected_shard="a",
        pilot_mode=True,
    )
    assert report.passed, report.errors
    assert report.solution_rows == 1
    assert report.hold_rows == 1
    assert report.english_relevant_solution_rows == 1


def test_rejects_wrong_kb_variable_type_for_cleansing_steps() -> None:
    row = make_valid_solution_row()
    req = json.loads(row["messages"][1]["content"])
    req["confirmed_observations"]["cleansing.steps"]["value"] = "water_only"
    row["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("cleansing.steps" in e and "integer" in e for e in report.errors)


def test_rejects_mismatched_source_registry_url() -> None:
    row = make_valid_solution_row()
    req = json.loads(row["messages"][1]["content"])
    req["rag_chunks"][0]["source_url"] = "https://pubmed.ncbi.nlm.nih.gov/31157512/"
    row["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("source_url" in e for e in report.errors)


def test_rejects_outer_inner_mode_mismatch_wrong_sysprompt_and_s99_citation() -> None:
    row = make_valid_solution_row()
    row["mode"] = "hold"
    row["messages"][0]["content"] = "임의의 다른 시스템 프롬프트"
    row["messages"][2]["content"] += " 근거 [S99]"
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("outer mode" in e for e in report.errors)
    assert any("SYSTEM_PROMPT_SOLUTION_HOLD" in e for e in report.errors)
    assert any("S99" in e for e in report.errors)


def test_rejects_hold_recommendation_leak() -> None:
    row = make_valid_hold_row()
    row["messages"][2]["content"] += " 대신 순한 대체 후보를 사용해 보세요."
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("leaked recommendation" in e for e in report.errors)


def test_v67_split_preservation_and_test_internal_blocking() -> None:
    # 1. test_internal scenario must be blocked
    test_row = make_valid_hold_row(row_id="syn-a-hold-0002", split="train")
    test_row["scenario_id"] = "luna-v3-train-026"
    test_row["group_id"] = "luna-v3-origin-026"
    test_row["provenance"]["source_origin"] = "recycled_v67"
    test_row["provenance"]["source_scenario_id"] = "luna-v3-train-026"
    report_test = val.validate_rows([("shard_a.jsonl", 1, test_row)], KB_INDEX, V67_INDEX)
    assert not report_test.passed
    assert any("test_internal" in e for e in report_test.errors)

    # 2. val_internal scenario placed into train must be blocked
    val_wrong = make_valid_hold_row(row_id="syn-a-hold-0003", split="train")
    val_wrong["scenario_id"] = "luna-v3-train-005"
    val_wrong["group_id"] = "luna-v3-origin-005"
    val_wrong["provenance"]["source_origin"] = "recycled_v67"
    val_wrong["provenance"]["source_scenario_id"] = "luna-v3-train-005"
    report_wrong = val.validate_rows([("shard_a.jsonl", 1, val_wrong)], KB_INDEX, V67_INDEX)
    assert not report_wrong.passed
    assert any("v67 split mismatch" in e for e in report_wrong.errors)

    # 3. val_internal scenario kept in val_internal must PASS!
    val_ok = copy.deepcopy(val_wrong)
    val_ok["split"] = "val_internal"
    report_ok = val.validate_rows([("shard_a.jsonl", 1, val_ok)], KB_INDEX, V67_INDEX)
    assert report_ok.passed, report_ok.errors


def test_merge_catches_duplicate_id_and_cross_split_leakage() -> None:
    row1 = make_valid_solution_row(row_id="syn-a-sol-0001", split="train")
    row2 = make_valid_solution_row(row_id="syn-b-sol-0001", split="val_internal")
    # Same group_id across train & val_internal must fail merge
    report = val.validate_rows(
        [("shard_a.jsonl", 1, row1), ("shard_b.jsonl", 1, row2)],
        KB_INDEX,
        V67_INDEX,
    )
    assert not report.passed
    assert any("cross-split leakage" in e for e in report.errors)


def test_guide_doc_reference_examples_pass_validator() -> None:
    """Both JSONL reference examples embedded in qlora-synthetic-dataset-guide.md must pass."""
    import re

    guide_path = COS_AGENT_DIR / "docs" / "qlora-synthetic-dataset-guide.md"
    md = guide_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", md, re.S)
    assert len(blocks) == 2, f"Expected 2 JSON reference examples (solution + hold), got {len(blocks)}"
    rows = [(str(guide_path), idx + 1, json.loads(b)) for idx, b in enumerate(blocks)]
    report = val.validate_rows(rows, KB_INDEX, V67_INDEX, expected_shard="a", pilot_mode=True)
    assert report.passed, report.errors
    assert report.solution_rows == 1
    assert report.hold_rows == 1

