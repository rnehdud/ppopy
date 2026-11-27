"""검수 요청과 실제 미검수 상태를 사람이 읽기 쉬운 인계 자료로 정리해요."""

from __future__ import annotations

import csv
import hashlib
import json
import random
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
BASE = COS / "data/qlora/v2/additional_900_20261126"


def write_json(path, obj):
    path.write_text(
        json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main():
    if (BASE / "validation/remediation_18_receipt.json").exists():
        raise RuntimeError(
            "초기 생성 단계 인계 도구예요. 수정 후 인계는 RECHECK_18_HANDOFF_KO.md를 보세요."
        )
    report = json.loads((BASE / "validation/quality.json").read_text(encoding="utf-8"))
    validation = json.loads(
        (BASE / "validation/structure.json").read_text(encoding="utf-8")
    )
    rows = [
        json.loads(x)
        for x in (BASE / "qlora_solution_hold_additional_900.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    requests = {
        r["row_id"]: r
        for r in (
            json.loads(x)
            for x in (BASE / "reviews/critic_requests.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    }
    assert len(rows) == len(requests) == 900
    assert all(r["provenance"]["human_review"] == "unreviewed" for r in rows)
    assert all(r["provenance"]["critic_status"] == "unreviewed" for r in rows)
    high_risk = set(report["high_risk_rows"])
    rng = random.Random(20261126)
    # 균등한 위험 층부터 한 행씩 뽑은 뒤 남은 필요 표본을 무작위로 보충해요.
    strata = {}
    for row in rows:
        if row["id"] in high_risk:
            key = (
                row["mode"],
                row["hard_negative_type"],
                tuple(row["domains"]),
                row["split"],
            )
            strata.setdefault(key, []).append(row["id"])
    selected = {
        rng.choice(sorted(ids))
        for _, ids in sorted(strata.items(), key=lambda x: str(x[0]))
    }
    needed = report["required_human_review_minimum"]
    available = sorted(high_risk - selected)
    selected.update(rng.sample(available, max(0, needed - len(selected))))
    fields = [
        "row_id",
        "content_sha256",
        "mode",
        "split",
        "scenario_family_id",
        "request_raw",
        "assistant_raw",
        "human_review",
        "reviewer",
        "comment",
    ]
    path = BASE / "reviews/human_review_sample_unreviewed.csv"
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            if row["id"] not in selected:
                continue
            writer.writerow(
                {
                    "row_id": row["id"],
                    "content_sha256": requests[row["id"]]["content_sha256"],
                    "mode": row["mode"],
                    "split": row["split"],
                    "scenario_family_id": row["scenario_family_id"],
                    "request_raw": row["messages"][1]["content"],
                    "assistant_raw": row["messages"][2]["content"],
                    "human_review": "unreviewed",
                    "reviewer": "",
                    "comment": "",
                }
            )
    write_json(
        BASE / "reviews/human_sample_manifest.json",
        {
            "seed": 20261126,
            "sample_size": len(selected),
            "high_risk_total": len(high_risk),
            "minimum_required": needed,
            "row_ids": sorted(selected),
            "sampling": "one per risk/mode/domain/split stratum, random remainder",
            "human_review_executed": False,
            "approvals_created": False,
        },
    )
    token_path = BASE / "validation/tokens/token_report.json"
    token = (
        json.loads(token_path.read_text(encoding="utf-8"))
        if token_path.exists()
        else None
    )
    token_text = (
        f"실제 Qwen3-4B-Instruct-2507 토크나이저·chat template 기준 최대 {token['total_tokens']['max']:,}토큰, p95 {token['total_tokens']['p95']:,}토큰이에요. 길이 2,048 초과는 {token['truncation']['2048']['exceeding']}행이에요. 모델 학습·추론·GPU 메모리 시험은 하지 않았어요."
        if token
        else "토큰 길이는 아직 측정하지 않았어요."
    )
    hn = sum(report["hard_negative_types"].values())
    text = f"""# PPO-37 — 기존 자료와 별개인 추가 900턴 생성·검수 인계

**이번 단계는 생성·구조 검증까지예요. 팀원이 Cross-Model Critic을 수행할 예정이며, 사람 승인·최종 학습 승인은 아직 없어요.**

사용자 후속 지시: “cross model check은 팀원이 할거라서 안해도 돼요. 900개만 일단 만들면 되요”.
따라서 교차 모델 검수·PR·Linear 완료 보고는 이번 단계에서 수행하지 않아요.

## 기준과 원본 보존

- 기준 `origin/main`: `dbef37463a63e5c38c1f4b4737b3c7378d9b8cb0`.
- 작업 브랜치: `data/qlora-additional-900-20261126` (main 직접 수정·커밋·푸시 없음).
- 기존 승인 900턴 `../qlora_solution_hold_v2.jsonl`은 덮어쓰지 않았어요.
- 기존 SHA-256: `{report["original_dataset_sha256"]}`.
- 추가 파일: `qlora_solution_hold_additional_900.jsonl`.
- 추가 SHA-256: `{report["dataset_sha256"]}`.
- 전체 공식 풀: 151개. 세정39 / 보습38 / 보관·국내표시43 / 자외선차단31.
- 새 자료의 문헌은 공식 풀의 객체를 그대로 사용해요. 허용 문헌·방해 문헌 모두 실제 풀에 있어요.
- 기존 v67/구 KB 종속 데이터·기존 900턴 답변을 생성 재료로 재사용하지 않아요.

## 추가 900턴 분포

| 항목 | 결과 |
|---|---:|
| 전체 | {report["rows"]} |
| solution / hold | {report["modes"].get("solution", 0)} / {report["modes"].get("hold", 0)} |
| train / val_internal | {report["splits"].get("train", 0)} / {report["splits"].get("val_internal", 0)} |
| Hard Negative | {hn} / 900 |
| 영어 허용 문헌 포함 solution | {report["english_supported_solutions"]} / 690 |
| 사용한 공식 풀 문헌 | {report["used_pool_refs"]} / 151 |
| human_review=unreviewed | 900 / 900 |
| critic_status=unreviewed | 900 / 900 |

생성 모델은 런타임 지시로 확인할 수 있는 GPT-6 계열을 `gpt-6`으로 기록했어요. 정확한 호스팅 세부 모델명은 노출되지 않아 추정해 기록하지 않았어요. 생성 담당 분리는 다른 모델 계열의 외부 검수와 달라요.

## 검증과 한계

- 공식 `--profile rag-free --stage1` 구조·비율 검증: `passed={str(validation["passed"]).lower()}`, `error_count={validation["error_count"]}`.
- 원본 900턴과 추가 900턴을 두 입력 파일로 읽은 구조 검증도 오류0이에요(`validation/original_plus_additional_structure.json`). 별도 합본이나 1,800턴 학습 승인을 만든 것은 아니에요.
- `validation/quality.json`: 원본+추가 중복, 제품 식별자 제거 중복, 실제 청크 객체 일치, 안전 메타데이터 확인.
- `validation/semantic_overlap_candidates.json`: 문헌·제품 ID를 제외한 유사 입력 후보예요. 자동 유사도가 의미 정확성이나 가족 독립성을 증명하지 않아요.
- `kb_judgments` 입력·`[kb:...]` 인용 없음. HOLD의 문헌·인용 목록은 비어 있어요.
- 개발 프리뷰·생산 비활성·승인 필요·무저장 불변식을 유지해요.
- Source manifest 27건 실패0. Windows CRLF 체크아웃만 동일 Git 원본 LF 바이트로 복원했고 KB/계약/검증기/코어 내용은 바꾸지 않았어요.
- 기존 검증 주제와 겹치는 사례를 신규 train으로 잘못 배정하지 않도록 생성 중 분할을 조정했어요. `val_internal`은 개발용 분할이며 독립 최종 test라고 주장하지 않아요.
- {token_text}

## 팀원에게 넘길 자료

1. 현재 후보 데이터 `qlora_solution_hold_additional_900.jsonl`.
2. 전수 검수 요청 `reviews/critic_requests.jsonl` (900개), 소배치 `reviews/requests/batch_01.jsonl`~`batch_30.jsonl` (각30개).
3. `reviews/request_manifest.json`: 현재 입력·답변·HN·출처 메타데이터에 묶인 행별 내용 해시.
4. `reviews/CRITIC_PROMPT_KO.md`: 입력 사실, 인용 함의, 방해 청크 간접 언급, HOLD 누출, HN 분류 검수 지침.
5. `reviews/human_review_sample_unreviewed.csv`: 고위험 {len(high_risk)}개 중 {len(selected)}개 표본. 표본 목록일 뿐 사람 검수 결과가 아니에요.
6. `authoring/`: 행별 신규 사례 작성 원본·입력/주장/문헌 raw 연결 기록. 보조 발화는 실제 모델 입력을 대신하지 않아요.

팀원은 각 행을 실제로 읽고 실제 Critic 모델명·PASS/FAIL·위반 원문과 이유를 별도 JSONL로 남겨 주세요. 수정되면 기존 PASS를 재사용하지 말고 새 해시로 재검수해요.
미실시 `reviews/stage1_critic.jsonl`이나 사람 승인 결과를 대신 만들지 않았어요.

## 재현 명령 (cos-agent에서)

```powershell
python -m uv run --locked python scripts/assemble_additional_900.py --nearest
python -m uv run --locked python scripts/validate_qlora_dataset.py --profile rag-free --input data/qlora/v2/additional_900_20261126/qlora_solution_hold_additional_900.jsonl --stage1 --report data/qlora/v2/additional_900_20261126/validation/structure.json
```

현재는 `--review-file`을 붙이지 않아요. 해당 옵션은 실제 교차 검수 및 고위험 사람 승인 게이트를 함께 요구해요. 구조 검증 성공을 최종 검수 성공으로 표현하지 않아요.
기존 900턴과 추가 900턴은 이 폴더의 생성 스크립트가 자동으로 하나의 학습 파일로 합치지 않아요. 합쳐 학습하려면 전체 가족·분할·중복·검수 범위를 다시 확인해요.
"""
    (BASE / "README.md").write_text(text, encoding="utf-8", newline="\n")
    write_json(
        BASE / "validation/handoff_receipt.json",
        {
            "generated_rows": 900,
            "structural_validation_passed": validation["passed"],
            "quality_checks_passed": report["passed"],
            "dataset_sha256": report["dataset_sha256"],
            "critic_request_rows": len(requests),
            "critic_executed": False,
            "human_approved": False,
            "training_approved": False,
            "human_review_sample_rows": len(selected),
            "original_dataset_unchanged": True,
            "PR_created": False,
            "Linear_posted": False,
            "scope": "User requested generation-only handoff; teammate performs cross-model critique.",
            "human_sample_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        },
    )
    print(
        json.dumps(
            {
                "rows": 900,
                "human_review_sample": len(selected),
                "critic_executed": False,
                "readme": "README.md",
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
