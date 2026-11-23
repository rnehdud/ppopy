"""고정 검증기에 없는 명시적 어휘·HOLD 가드를 추가 확인해요.

기존 검증기와 KB·전문가 판단을 대체하지 않아요. 원문/방해 청크를 증상 사실로
읽지 않고 confirmed_observations의 확인된 값만 검사해요.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from validate_qlora_dataset import SLMRequest, load_jsonl_files

ENUMS = {
    "skin.current_discomfort": frozenset({"none", "mild_transient", "repeated", "persistent"}),
    "skin.pain": frozenset({"none", "mild", "moderate", "severe"}),
    "skin.stinging": frozenset({"none", "mild", "moderate", "severe"}),
    "skin.dryness": frozenset({"none", "mild", "moderate", "severe"}),
}


def validate(paths):
    rows, parse_errors = load_jsonl_files([Path(p) for p in paths])
    errors = [{"code": "PARSE", "message": message} for message in parse_errors]
    exceptions = []
    for file, line, row in rows:
        rid = row.get("id")
        try:
            req = SLMRequest.model_validate_json(row["messages"][1]["content"])
        except Exception as exc:
            errors.append({"row_id": rid, "code": "SLM_REQUEST", "message": str(exc)})
            continue
        obs = req.confirmed_observations
        for key, allowed in ENUMS.items():
            slot = obs.get(key)
            if slot and slot.state == "known" and (not isinstance(slot.value, str) or slot.value not in allowed):
                errors.append({"row_id": rid, "file": file, "line": line, "code": "CONTROLLED_VOCABULARY", "variable": key, "value": slot.value, "allowed": sorted(allowed)})
        reasons = []
        current = obs.get("skin.current_discomfort")
        pain = obs.get("skin.pain")
        if current and current.state == "known" and current.value == "persistent":
            reasons.append("confirmed_persistent_discomfort")
        if pain and pain.state == "known" and pain.value in ("moderate", "severe"):
            reasons.append("confirmed_moderate_or_severe_pain")
        sensory = obs.get("storage.sensory_change")
        if sensory and sensory.state == "known" and isinstance(sensory.value, dict):
            positive = any(sensory.value.get(k) is True for k in ("color_or_odor_change", "separation"))
            instructions = obs.get("product.instructions")
            normal = instructions and instructions.state == "known" and isinstance(instructions.value, dict) and instructions.value.get("normal_two_phase") is True
            normal = normal and sensory.value.get("new_change") is False and sensory.value.get("color_or_odor_change") is False
            if positive and normal:
                exceptions.append({"row_id": rid, "rule": "confirmed_normal_two_phase_no_new_change"})
            elif positive:
                reasons.append("confirmed_quality_change_without_normal_formulation_exception")
        if reasons and (row.get("mode") != "hold" or req.mode != "hold"):
            errors.append({"row_id": rid, "file": file, "line": line, "code": "HOLD_REQUIRED", "current_mode": row.get("mode"), "reasons": reasons})
    return {"passed": not errors, "total_rows": len(rows), "error_count": len(errors), "errors": errors,
            "quality_exceptions": exceptions,
            "scope": "고정 가이드의 4개 통제 어휘와 명확한 지속 불편·통증·품질 변화만 추가 검사해요. 모든 임상 상황이나 자연어 의미를 자동 판정하지 않아요."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = validate(args.input)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("passed", "total_rows", "error_count", "quality_exceptions")}, ensure_ascii=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
