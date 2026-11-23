"""수정·고정한 A 입력에서 감사 실패 응답을 좁히거나 새로 작성합니다."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_INPUT_SHA256 = "77cc5377bc94b788895ab1db76f5714bc7433e36a8f81540ba06cc53f24785a4"


def main():
    source = HERE / "additional_100_part_a_inputs.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest() == EXPECTED_INPUT_SHA256
    fixed = json.loads(source.read_text(encoding="utf-8"))
    path = HERE / "additional_100_part_a.json"
    prior = json.loads(path.read_text(encoding="utf-8"))
    previous = {c["id"]: c for c in prior["cases"]}
    patched = {}
    for rid in ("syn-sol-0040", "syn-sol-0057", "syn-hold-0018"):
        patched[rid] = previous[rid]["answer"]
    patched["syn-sol-0051"] = previous["syn-sol-0051"]["answer"].replace("택배 이동 중", "운송 중")
    patched["syn-sol-0053"] = previous["syn-sol-0053"]["answer"].replace("여행용 소분은", "소분은")
    patched["syn-sol-0052"] = """### 핵심 안내
같은 제품의 용기 A와 B가 있어도 용기별 식별자와 개봉일은 미상이에요. 한 용기의 개봉일을 다른 용기에 그대로 적용하지 않아요 [kb:B-S02@0.6.1].

### 근거 및 이유
사용 이력은 제품명뿐 아니라 개별 용기를 구분해 검토해야 해요. 보관 자료가 모든 제품에 공통 사용기한을 정해 주지는 않아요 [kb:B-S02@0.6.1] [ref:S06].

### 확인이 필요한 한계
용기별 표시와 확인 가능한 개봉 기록을 살펴봐요. 확인되지 않는 날짜는 미상으로 두고, 구매일을 개봉일로 바꾸거나 임의의 사용 가능 기간을 계산하지 않아요."""
    patched["syn-sol-0062"] = """### 핵심 안내
보습량을 의도적으로 줄였고 현재 가벼운 건조와 재건조 경험이 있다고 했어요. 통증과 따가움은 없으므로 보유 보습제의 실제 사용과 감량 여부를 함께 검토해요 [kb:B-M02@0.6.1].

### 근거 및 이유
건조가 있는데도 무조건 감량하기보다 실제 사용 경험과 편안함을 기준으로 조정을 검토할 수 있어요. 일반 건조 피부 안내도 개인별로 동일한 사용량이나 치료 효과를 정하지 않아요 [kb:B-M02@0.6.1] [ref:S04].

### 확인이 필요한 한계
건조가 다시 나타나기까지의 시간은 미상이에요. 감량이 건조의 원인이라고 확정하지 않으며, 현재·이전 사용량과 경험이 확인되기 전 특정 증량 수치나 개선율을 제시하지 않아요."""
    patched["syn-hold-0013"] = """### 개별 권고 보류 안내
제품에 원래 없던 입자와 색 또는 냄새 변화가 보고됐고, 정상 입자라는 표시도 확인되지 않았어요. 품질 확인 전 개별 루틴과 제품 권고를 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 정상 제형 특성인지 제조·판매처에 확인할 필요가 있어요. 제품 유형과 변화의 구체적인 종류는 미확인이며, 관찰만으로 미생물 오염이나 원인을 확정하지 않아요."""
    patched["syn-hold-0017"] = """### 개별 권고 보류 안내
피부를 관통하는 기기의 개인별 깊이·반복 통과 횟수와 병용 제품을 정하는 요청은 일반 화장품 도포 안내의 범위를 벗어나요. 해당 시술 절차와 병용 조합의 개별 설계를 보류해요 [kb:B-G06@0.6.1].

### 필요한 다음 단계
관련 자격을 갖춘 전문가에게 요청한 행위의 적용 범위와 적합성을 확인해야 해요. 제품 지침과 개별 진료 계획은 미상이며, 깊이·횟수·대체 조합을 만들어 안내하지 않아요. 아직 시행하지 않은 계획을 실제 시술이나 발생한 손상으로 바꾸지 않아요."""
    result = deepcopy(fixed)
    result.update(schema_version="additional-100-part-a-revised-v1", generator_model="gpt-6.1-sol", critic_status="unreviewed", human_review="unreviewed")
    for c in result["cases"]:
        c["answer"] = patched.get(c["id"], previous[c["id"]]["answer"])
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = HERE.parents[2] / "outputs/additional_100/revision_a"
    receipt = {"input_sha256": EXPECTED_INPUT_SHA256, "output_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
               "reviewed_failure_rows": list(patched), "input_fixed_before_answer_revision": True,
               "human_review": "unreviewed", "external_cross_family_gate_satisfied": False,
               "unchanged_other_25_answers": all(c["answer"] == previous[c["id"]]["answer"] for c in result["cases"] if c["id"] not in patched)}
    (out / "answer_revision_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
