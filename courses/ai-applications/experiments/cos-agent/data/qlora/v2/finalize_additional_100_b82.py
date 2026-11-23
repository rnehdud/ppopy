"""UTF-8로 다시 고정한 B82 입력에서 응답을 작성합니다."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED = "f81be12fa8a6bf7af191f5a8a144c2f4e183a7d690ea7bf401e935027ecd5a73"


def main():
    path = HERE / "additional_100_part_b_inputs.json"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED
    fixed = json.loads(path.read_text(encoding="utf-8"))
    output = HERE / "additional_100_part_b.json"
    old = json.loads(output.read_text(encoding="utf-8"))
    by_id = {c["id"]: c for c in old["cases"]}
    result = deepcopy(fixed)
    result.update(generator_model="gpt-6.1-sol", critic_status="unreviewed", human_review="unreviewed")
    for c in result["cases"]:
        c["answer"] = by_id[c["id"]]["answer"]
        if c["id"] == "syn-sol-0082":
            c["answer"] = """### 핵심 안내
집의 보습제를 운반하기 어려워 직장 세면 공간에 한 통을 따로 비치하려는 목적과 다음 출근일부터 쓸 계획이 확인됐어요. 같은 기능의 제품을 집에 갖고 있다는 사실만으로 불필요한 중복 구매라고 판정하지 않아요 [kb:B-Q01@0.6.1].

### 근거 및 이유
이 기준은 제품 수만 세기보다 별도 사용 목적·보유 재고·시작 계획과 비용을 함께 검토해요. 추가 한 통의 비용을 감당할 수 있다는 관찰도 있어요 [kb:B-Q01@0.6.1]. 브랜드 허가 판매자 목록과 실제 판매자의 일치를 확인했다는 관찰은 판매 경로 확인에 해당하지만, 제품 품질 전체를 보증하는 것은 아니에요 [ref:S36].

### 확인이 필요한 한계
실제 소진량이나 남은 제품의 사용 가능 기간은 계산할 정보가 없어요. 별도 목적이 있다는 사실을 임상 효과나 개인 적합성의 증거로 바꾸지 않으며, 이 자료로 구매 자체가 피부에 해롭다고 단정하지 않아요."""
    assert all(c == by_id[c["id"]] for c in result["cases"] if c["id"] != "syn-sol-0082")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {"row_id": "syn-sol-0082", "fixed_input_file_sha256": EXPECTED, "answer_written_after_input_freeze": True,
               "other_32_cases_unchanged": True, "output_sha256": hashlib.sha256(output.read_bytes()).hexdigest(), "human_review": "unreviewed"}
    dest = HERE.parents[2] / "outputs/additional_100/encoding_b82/fresh_answer_receipt.json"
    dest.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False))


if __name__ == "__main__":
    main()
