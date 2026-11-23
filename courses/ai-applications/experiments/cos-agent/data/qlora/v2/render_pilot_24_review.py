"""유니코드 문자열을 셸로 전달하지 않고 파일럿 확인 문서를 UTF-8로 생성합니다.

데이터 행, 입력 계획, 검수 판정과 사람의 기록은 변경하지 않습니다.
실행 명령: python path/to/render_pilot_24_review.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
COS = HERE.parents[2]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render() -> None:
    protected = [HERE / name for name in (
        "pilot_24.jsonl", "pilot_24_plan.json", "pilot_24_responses.json",
        "pilot_24_human_review.csv",
    )]
    before = {p.name: sha(p) for p in protected}
    plan = json.loads((HERE / "pilot_24_plan.json").read_text(encoding="utf-8"))
    rows = [json.loads(line) for line in
            (HERE / "pilot_24.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    cases = {case["id"]: case for case in plan["cases"]}
    assert len(rows) == 24 and len(cases) == 24
    sys.path.insert(0, str(COS))
    spec = importlib.util.spec_from_file_location(
        "pilot_review_renderer_validator", COS / "scripts/validate_qlora_dataset.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    revision = plan.get("plan_revision", 1)
    intro = [
        f"# 24턴 파일럿 — 전체 입력과 응답 확인 — 개정 {revision}", "",
        "**생성된 초안입니다. 사람의 전수 확인과 다른 모델 계열의 공식 검수는 미완료입니다.**", "",
        "`development_preview`, `production_enabled=false`인 합성 사례입니다. 입력과 KB 판정은 작성자의 설계이며 실제 사용자 기록, 엔진 실행 판정이나 임상적 정답이 아닙니다.",
        "생성 모델은 `gpt-6.1-sol`입니다. 같은 GPT 계열의 Codex 검토는 내부 검토로 별도 기록합니다.", "",
        f"기준 커밋: `{plan['base_commit']}`. 안내 18턴, 보류 6턴이며 네 유형이 각각 6턴입니다.",
        f"입력 계획 SHA256: `{sha(HERE / 'pilot_24_plan.json')}`",
        f"데이터 SHA256: `{sha(HERE / 'pilot_24.jsonl')}`", "",
        "## 사람의 검수 방법", "",
        "24턴 전체를 읽고 확정 관찰과 응답의 대응, 허용된 인용, 미확인 값과 버전 보존, 보류 응답의 개별 권고 누출, 진단·효능 단정의 부재와 문체를 확인해 주세요.",
        "`pilot_24_human_review.csv`에 실제 검수자의 이름, 날짜, 판정과 의견만 기록해 주세요. 이 자료를 생성한 것은 승인을 뜻하지 않습니다.",
        "입력이나 응답을 변경하면 내용 해시를 다시 계산하고 재검수해 주세요. 사람의 확인 상태는 CSV에 기록하며 이 확인 자료에서 승인을 설정하지 않습니다.", "",
        "입력 수정과 최초 내부 검토의 수정 필요 판정은 `outputs/`에 보존했습니다. 개정 3의 두 사례는 신규 합성 설정을 명시한 것으로 실제 사용자의 알려지지 않은 의도를 추측한 것이 아닙니다.", "",
        "## 사례 목록", "",
        "| ID | 유형 | 사례 | 사람 검수 기록 |", "|---|---|---|---|",
    ]
    for row in rows:
        intro.append(f"| {row['id']} | {row['pilot_bucket']} | {cases[row['id']]['title']} | CSV에 기록 |")

    for row in rows:
        case = cases[row["id"]]
        req = module.SLMRequest.model_validate_json(row["messages"][1]["content"])
        answer = row["messages"][2]["content"]
        assert json.loads(row["messages"][1]["content"]) == case["request"]
        digest = module.compute_row_content_sha256(
            req, answer, card_ids=row["card_ids"], chunk_origins=row["chunk_origins"],
            is_hard_negative=row["is_hard_negative"], hard_negative_type=row["hard_negative_type"])
        source_turn = row["provenance"]["source_turn_id"] or "해당 없음: 신규 합성"
        review_state = row["provenance"]["human_review"]
        review_label = "미검수" if review_state == "unreviewed" else review_state
        intro += [
            "", f"## {row['id']} — {case['title']}", "",
            f"- 유형: `{row['pilot_bucket']}` / `{row['mode']}` / `{row['split']}`",
            f"- 계보: `{row['provenance']['source_origin']}` / 원본 턴: `{source_turn}`",
            f"- 내용 해시: `{digest}`",
            f"- 데이터의 사람 검수 상태: **{review_label}** / 검수자·날짜: CSV에 기록", "",
            "### 설계상 판정 근거 — 엔진 실행 결과가 아닙니다", "",
            case["judgment_basis"]["rationale"], "", "### 고정한 입력", "", "```json",
            json.dumps(case["request"], ensure_ascii=False, indent=2), "```", "",
            "### 생성한 응답 — 미승인", "", answer,
        ]

    plan_lines = [
        f"# PPO-37 24턴 파일럿 입력 구성 — 개정 {revision}, 미검수", "",
        f"기준 커밋: `{plan['base_commit']}`. 합성 개발용이며 `production_enabled=false`입니다.", "",
        "초판에서는 관찰·판정·허용 근거를 응답 조립 전에 고정했습니다. 이후 내부 검토에 따른 입력 수정은 이전 버전, 사유와 해시를 보관한 뒤 다시 조립했습니다.",
        "판정은 KB 비교 명세에 따른 작성자의 설계이며 엔진 실행 결과, 전문가 정답이나 사람의 승인이 아닙니다.", "",
        "생성 모델: `gpt-6.1-sol`. 같은 계열의 Codex 내부 검토는 다른 모델 계열의 공식 검수와 구분합니다. 사람의 24턴 전수 검수와 팀 확인 전에 900턴으로 진행하지 않습니다.", "",
        "| ID | 유형 | 사례 | 분할 | 계보 |", "|---|---|---|---|---|",
    ]
    for case in plan["cases"]:
        plan_lines.append(f"| {case['id']} | {case['pilot_bucket']} | {case['title']} | {case['split']} | {case['source_turn_id'] or 'new_synthetic'} |")
    plan_lines += [
        "", "행별 확정 관찰·KB 판정·허용 근거·입력 해시는 `pilot_24_plan.json`에 있습니다.", "",
        "v67 재가공 3턴은 원본 관찰·분할·그룹·계보를 유지합니다. 신규 합성 21턴 중 2턴은 검증용입니다. 개발용 분할이며 독립 최종 평가가 아닙니다.", "",
        "## 입력 설계 수정 이력", "",
        "- 개정 2: `syn-sol-0014`의 정성적 시간 설명을 수치 필드에서 분리하고 분 단위 시간은 미확인으로 유지했습니다.",
        "- 개정 3: `syn-sol-0006`의 생각과 `syn-sol-0017`의 의도를 신규 합성 사례의 입력 설정에 명시했습니다. 실제 사용자의 알려지지 않은 의도를 추측한 것이 아닙니다.",
        "- 수정 전 입력·응답, 최초 수정 필요 판정, 수정 사유와 해시는 `outputs/pilot_24/` 및 최초 내부 검토 기록에 보관했습니다. 기존 응답을 다시 조립해 재검사했으며 사람의 승인을 부여하지 않았습니다.",
    ]
    documents = {"pilot_24_review.md": intro, "pilot_24_plan.md": plan_lines}
    backup = COS / "outputs/pilot_24/unicode_correction"
    backup.mkdir(parents=True, exist_ok=True)
    for name, lines in documents.items():
        path = HERE / name
        saved = backup / name
        if path.exists() and not saved.exists():
            saved.write_bytes(path.read_bytes())
        text = "\n".join(lines) + "\n"
        assert "??" not in text and "\ufffd" not in text
        path.write_text(text, encoding="utf-8")
        assert path.read_text(encoding="utf-8") == text
    assert before == {p.name: sha(p) for p in protected}
    receipt_path = COS / "outputs/pilot_24/generation_receipt.json"
    if receipt_path.exists():
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["documentation_encoding_correction"] = {
            "reason": "Shell-piped Python source replaced Japanese literal text with question marks.",
            "renderer": "data/qlora/v2/render_pilot_24_review.py",
            "dataset_plan_responses_and_human_entries_unchanged": True,
            "rendered_cases": len(rows),
        }
        receipt["files"] = {p.name: {"sha256": sha(p), "bytes": p.stat().st_size}
                            for p in HERE.iterdir() if p.is_file()}
        receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("UTF-8 확인 자료와 입력 계획을 생성했습니다. 24턴 원본 데이터는 변경하지 않았습니다.")


if __name__ == "__main__":
    render()
