"""Unit tests for scripts/validate_qlora_dataset.py (covering all Codex P0/P1 cases)."""
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
    shard: str = "a",
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
        "id": f"syn-{shard}-sol-{num:04d}",
        "scenario_id": f"new-{shard}-bi01-{num:03d}",
        "group_id": f"new-group-{shard}-bi01-{num:03d}",
        "scenario_family_id": f"fam-{shard}-bi01-{num:03d}",
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
                    f"내수성 표시만 보고 무조건 반복 세안할 필요는 없어요 (시나리오 {shard}-{num}). "
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
    shard: str = "a",
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
        "id": f"syn-{shard}-hold-{num:04d}",
        "scenario_id": f"new-{shard}-bb01-{num:03d}",
        "group_id": f"new-group-{shard}-bb01-{num:03d}",
        "scenario_family_id": f"fam-{shard}-bb01-{num:03d}",
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
                    f"현재 지속적인 불편감과 통증이 확인되어 개별 루틴 조정이나 제품 안내는 보류해요 (사례 {shard}-{num}) [kb:B-B01@0.6.1].\n\n"
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


def make_12_row_pilot_shard(shard: str) -> list[tuple[str, int, dict]]:
    fname = f"shard_{shard}.jsonl"
    rows: list[tuple[str, int, dict]] = []
    line = 1
    sol_num = 1
    for bucket, is_hn, hn_type in (
        ("normal_guidance", False, None),
        ("unknown_or_version", True, "version_mismatch_or_unknown"),
        ("distractor_or_defense", True, "rag_distractor_ignore"),
    ):
        for _ in range(3):
            rows.append(
                (
                    fname,
                    line,
                    make_valid_solution_row(
                        shard=shard,
                        num=sol_num,
                        pilot_bucket=bucket,
                        is_hn=is_hn,
                        hn_type=hn_type,
                        unknown_obs=(bucket == "unknown_or_version"),
                    ),
                )
            )
            line += 1
            sol_num += 1
    for h_num in range(1, 4):
        rows.append((fname, line, make_valid_hold_row(shard=shard, num=h_num)))
        line += 1
    return rows


def test_empty_file_and_partial_pilot_are_rejected() -> None:
    empty_report = val.validate_rows([], KB_INDEX, V67_INDEX, input_files=["empty.jsonl"], merge_mode=True, pilot_mode=True)
    assert not empty_report.passed

    partial = [
        ("shard_a.jsonl", 1, make_valid_solution_row()),
        ("shard_a.jsonl", 2, make_valid_hold_row()),
    ]
    partial_report = val.validate_rows(
        partial, KB_INDEX, V67_INDEX, input_files=["shard_a.jsonl"], merge_mode=True, pilot_mode=True
    )
    assert not partial_report.passed
    assert any("expected exactly 3 shard files" in e for e in partial_report.errors)
    assert any("expected 36 total rows" in e for e in partial_report.errors)


def test_full_36_row_pilot_merge_and_review_gate_pass() -> None:
    all_rows = (
        make_12_row_pilot_shard("a")
        + make_12_row_pilot_shard("b")
        + make_12_row_pilot_shard("c")
    )
    report = val.validate_rows(
        all_rows,
        KB_INDEX,
        V67_INDEX,
        input_files=["shard_a.jsonl", "shard_b.jsonl", "shard_c.jsonl"],
        merge_mode=True,
        pilot_mode=True,
        require_review=True,
    )
    assert report.passed, report.errors
    assert report.total_rows == 36
    assert report.solution_rows == 27
    assert report.hold_rows == 9


def test_rejects_unbacked_allowed_refs_and_probe_citation() -> None:
    row = make_valid_solution_row()
    req = json.loads(row["messages"][1]["content"])
    # Add ref:S03 and catalog:ghost@1.0 to allowed_evidence_refs WITHOUT putting them in rag_chunks / product_evidence
    req["allowed_evidence_refs"].extend(["ref:S03", "catalog:ghost@1.0"])
    row["allowed_evidence_refs"] = list(req["allowed_evidence_refs"])
    row["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
    row["messages"][2]["content"] += " [ref:S03] [catalog:ghost@1.0]"
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("not backed by any input rag_chunks" in e for e in report.errors)
    assert any("not backed by any input product_evidence" in e for e in report.errors)

    # Probe chunk placed in allowed_evidence_refs must fail AND not count toward English ratio
    row2 = make_valid_solution_row()
    row2["chunk_origins"]["ref:S08"] = "synthetic_defense_probe"
    report2 = val.validate_rows([("shard_a.jsonl", 1, row2)], KB_INDEX, V67_INDEX)
    assert not report2.passed
    assert any("synthetic_defense_probe" in e for e in report2.errors)
    assert report2.english_relevant_solution_rows == 0


def test_rejects_scenario_family_cross_split_leakage_and_fake_v67_ids() -> None:
    r1 = make_valid_solution_row(shard="a", num=1, split="train")
    r2 = make_valid_solution_row(shard="b", num=1, split="val_internal")
    r2["scenario_family_id"] = r1["scenario_family_id"]  # Different scenario_id/group_id/text, same family!
    report = val.validate_rows([("shard_a.jsonl", 1, r1), ("shard_b.jsonl", 1, r2)], KB_INDEX, V67_INDEX)
    assert not report.passed
    assert any("scenario_family_id" in e for e in report.errors)

    # Non-existent recycled_v67 source_scenario_id & source_turn_id must fail
    fake_v67 = make_valid_hold_row(shard="a", num=2)
    fake_v67["provenance"]["source_origin"] = "recycled_v67"
    fake_v67["provenance"]["source_scenario_id"] = "nonexistent-v67-999"
    fake_v67["provenance"]["source_turn_id"] = "nonexistent-turn-999"
    report_fake = val.validate_rows([("shard_a.jsonl", 1, fake_v67)], KB_INDEX, V67_INDEX)
    assert not report_fake.passed
    assert any("does not exist in v67" in e for e in report_fake.errors)

    # Missing v67 directory must raise FileNotFoundError instead of silently disabling leakage checks
    with pytest.raises(FileNotFoundError):
        val.load_v67_index(COS_AGENT_DIR / "data" / "does_not_exist_v67")


def test_rejects_direct_instruction_hold_leak_and_missing_review_fields() -> None:
    row = make_valid_hold_row(human_review="unreviewed")
    row["messages"][2]["content"] += " 저녁에는 클렌징폼으로 1회 세안하세요."
    row["provenance"]["critic_model"] = None
    report = val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX, require_review=True)
    assert not report.passed
    assert any("leaked recommendation" in e for e in report.errors)
    assert any("non-null provenance.critic_model" in e for e in report.errors)
    assert any("human_review=='approved'" in e for e in report.errors)


def test_v67_real_val_internal_recycling_allowed_while_test_internal_blocked() -> None:
    # Find a real val_internal HOLD turn & scenario from V67_INDEX
    val_turn = next(
        tid
        for tid, sp in V67_INDEX.turn_to_split.items()
        if sp == "val_internal" and V67_INDEX.turn_to_action.get(tid) == "hold"
    )
    val_scen = V67_INDEX.turn_to_scenario[val_turn]
    row = make_valid_hold_row(shard="a", num=3, split="val_internal")
    row["scenario_id"] = val_scen
    row["provenance"]["source_origin"] = "recycled_v67"
    row["provenance"]["source_scenario_id"] = val_scen
    row["provenance"]["source_turn_id"] = val_turn
    assert val.validate_rows([("shard_a.jsonl", 1, row)], KB_INDEX, V67_INDEX).passed

    # Moving it to train must fail
    wrong = copy.deepcopy(row)
    wrong["split"] = "train"
    assert not val.validate_rows([("shard_a.jsonl", 1, wrong)], KB_INDEX, V67_INDEX).passed

    # Recycling an ask_user turn into solution must fail!
    ask_turn = next(
        tid
        for tid, act in V67_INDEX.turn_to_action.items()
        if act == "ask_user" and V67_INDEX.turn_to_split.get(tid) == "train"
    )
    ask_scen = V67_INDEX.turn_to_scenario[ask_turn]
    bad_action_row = make_valid_solution_row(shard="a", num=9, split="train")
    bad_action_row["scenario_id"] = ask_scen
    bad_action_row["provenance"]["source_origin"] = "recycled_v67"
    bad_action_row["provenance"]["source_scenario_id"] = ask_scen
    bad_action_row["provenance"]["source_turn_id"] = ask_turn
    rep_ask = val.validate_rows([("shard_a.jsonl", 1, bad_action_row)], KB_INDEX, V67_INDEX)
    assert not rep_ask.passed
    assert any("ask_user" in e for e in rep_ask.errors)


def test_rejects_mixed_shard_files_4row_final_merge_and_product_version_spoof() -> None:
    # 1. Mixed A+B rows in 23/1/12 pilot files must fail 1:1 file-to-shard check
    a_rows = make_12_row_pilot_shard("a")
    b_rows = make_12_row_pilot_shard("b")
    c_rows = make_12_row_pilot_shard("c")
    mixed = (
        a_rows
        + [("shard_a.jsonl", 13 + i, r) for i, (_, _, r) in enumerate(b_rows[:11])]
        + [("shard_b.jsonl", 1, b_rows[11][2])]
        + c_rows
    )
    rep_mixed = val.validate_rows(
        mixed,
        KB_INDEX,
        V67_INDEX,
        input_files=["shard_a.jsonl", "shard_b.jsonl", "shard_c.jsonl"],
        merge_mode=True,
        pilot_mode=True,
    )
    assert not rep_mixed.passed
    assert any("exactly 1 shard" in e for e in rep_mixed.errors)

    # 2. 4-row single file cannot pass --merge --enforce-ratios --require-review
    four_rows = [
        ("shard_a.jsonl", 1, make_valid_solution_row(shard="a", num=1)),
        ("shard_a.jsonl", 2, make_valid_solution_row(shard="a", num=2)),
        ("shard_a.jsonl", 3, make_valid_solution_row(shard="a", num=3)),
        ("shard_a.jsonl", 4, make_valid_hold_row(shard="a", num=1)),
    ]
    rep_4 = val.validate_rows(
        four_rows,
        KB_INDEX,
        V67_INDEX,
        input_files=["shard_a.jsonl"],
        merge_mode=True,
        enforce_ratios=True,
        require_review=True,
    )
    assert not rep_4.passed
    assert any("expected exactly 3 shard files" in e for e in rep_4.errors)
    assert any(">= 2100" in e for e in rep_4.errors)

    # 3. Spoofed product_evidence evidence_ref @999 when version is 1.0 must fail
    spoof = make_valid_solution_row(shard="a", num=5)
    req = json.loads(spoof["messages"][1]["content"])
    req["product_evidence"][0]["evidence_ref"] = "catalog:syn-sun-001@999"
    req["allowed_evidence_refs"] = ["kb:B-I01@0.6.1", "catalog:syn-sun-001@999", "ref:S08"]
    spoof["allowed_evidence_refs"] = list(req["allowed_evidence_refs"])
    spoof["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
    spoof["messages"][2]["content"] = spoof["messages"][2]["content"].replace("@1.0", "@999")
    rep_spoof = val.validate_rows([("shard_a.jsonl", 1, spoof)], KB_INDEX, V67_INDEX)
    assert not rep_spoof.passed
    assert any("mismatches product_id/version" in e for e in rep_spoof.errors)


def test_guide_doc_reference_examples_pass_validator() -> None:
    guide_path = COS_AGENT_DIR / "docs" / "qlora-synthetic-dataset-guide.md"
    md = guide_path.read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", md, re.S)
    assert len(blocks) == 2, f"Expected 2 JSON reference examples (solution + hold), got {len(blocks)}"
    rows = [(str(guide_path), idx + 1, json.loads(b)) for idx, b in enumerate(blocks)]
    report = val.validate_rows(rows, KB_INDEX, V67_INDEX, expected_shard="a")
    assert report.passed, report.errors
    assert report.solution_rows == 1
    assert report.hold_rows == 1


def test_final_enforce_ratios_rejects_empty_val_and_off_90_10_split() -> None:
    # Build 20 distinct new_synthetic families: all in train -> must fail empty val_internal
    all_train = [
        ("shard_a.jsonl", i, make_valid_solution_row(shard="a", num=i, split="train"))
        for i in range(1, 16)
    ] + [
        ("shard_a.jsonl", 15 + i, make_valid_hold_row(shard="a", num=i, split="train"))
        for i in range(1, 6)
    ]
    rep_empty_val = val.validate_rows(all_train, KB_INDEX, V67_INDEX, enforce_ratios=True)
    assert not rep_empty_val.passed
    assert any("val_internal must not be empty" in e for e in rep_empty_val.errors)

    # Now put 2 out of 20 families (10%) into val_internal + 5/15 (33.3%) EN chunks -> passes!
    split_90_10 = [
        (
            "shard_a.jsonl",
            i,
            make_valid_solution_row(
                shard="a",
                num=i,
                split=("val_internal" if i == 15 else "train"),
                english_chunk=(i <= 5),
            ),
        )
        for i in range(1, 16)
    ] + [
        (
            "shard_a.jsonl",
            15 + i,
            make_valid_hold_row(
                shard="a", num=i, split=("val_internal" if i == 5 else "train")
            ),
        )
        for i in range(1, 6)
    ]
    rep_ok = val.validate_rows(split_90_10, KB_INDEX, V67_INDEX, enforce_ratios=True)
    assert rep_ok.passed, rep_ok.errors

    # Put 6 out of 20 families (30%) into val_internal -> outside [0.07, 0.13] must fail!
    off_split = [
        (
            "shard_a.jsonl",
            i,
            make_valid_solution_row(
                shard="a", num=i, split=("val_internal" if i <= 4 else "train")
            ),
        )
        for i in range(1, 16)
    ] + [
        (
            "shard_a.jsonl",
            15 + i,
            make_valid_hold_row(
                shard="a", num=i, split=("val_internal" if i <= 2 else "train")
            ),
        )
        for i in range(1, 6)
    ]
    rep_off = val.validate_rows(off_split, KB_INDEX, V67_INDEX, enforce_ratios=True)
    assert not rep_off.passed
    assert any("outside [0.07, 0.13]" in e for e in rep_off.errors)


def test_pilot_rejects_duplicate_inputs_and_missing_bucket_signals() -> None:
    shard_rows = make_12_row_pilot_shard("a")
    # 1. Replace row 2's user SLMRequest with row 1's identical SLMRequest payload -> duplicate rejected
    dup_rows = copy.deepcopy(shard_rows)
    dup_rows[1][2]["messages"][1]["content"] = dup_rows[0][2]["messages"][1]["content"]
    rep_dup = val.validate_rows(dup_rows, KB_INDEX, V67_INDEX, expected_shard="a", pilot_mode=True)
    assert not rep_dup.passed
    assert any("duplicate user SLMRequest payload" in e for e in rep_dup.errors)

    # 2. Remove unknown observation and version signal from an unknown_or_version pilot row -> rejected
    no_unk = copy.deepcopy(shard_rows)
    for _, _, r in no_unk:
        if r.get("pilot_bucket") == "unknown_or_version":
            r["hard_negative_type"] = "rag_distractor_ignore"
            req = json.loads(r["messages"][1]["content"])
            req["confirmed_observations"].pop("cleansing.perceived_residue", None)
            r["messages"][1]["content"] = json.dumps(req, ensure_ascii=False)
            break
    rep_no_unk = val.validate_rows(no_unk, KB_INDEX, V67_INDEX, expected_shard="a", pilot_mode=True)
    assert not rep_no_unk.passed
    assert any("pilot_bucket='unknown_or_version'" in e for e in rep_no_unk.errors)
