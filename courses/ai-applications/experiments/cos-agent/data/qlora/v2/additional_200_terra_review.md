# 추가 개발 후보 200턴

기존 448턴을 변경하지 않고 추가한 안내 154턴·보류 46턴입니다. 합계는 648턴입니다.
`development_preview`, `production_enabled=false`이며 실제 사용자 자료나 임상 정답이 아닙니다.
작성 담당과 별도 문맥의 Codex 감사 담당을 분리합니다. 동일 GPT 계열의 감사는 다른 모델 계열의 공식 검수나 사람 승인을 대체하지 않습니다.
사람 검수는 미검수이며, 현재 감사 판정은 `reviews/additional_200_terra_codex_independent.*`에서 내용 해시와 함께 확인합니다.
합성 방어 청크는 실제 문헌 인용문이 아니며 감사용 출처 분류를 유지합니다. KB 판정 근거는 비교 명세를 대조한 작성 기록이지 엔진 실행 결과가 아닙니다.

## 사례 목록

| ID | 유형 | 사례 | 분할 |
|---|---|---|---|
| syn-sol-0346 | normal_guidance | 운동 전 세안과 운동 뒤 땀 제거 | train |
| syn-sol-0351 | normal_guidance | 얼굴에 천을 썼지만 압력 미상 | train |
| syn-sol-0352 | normal_guidance | 얼굴 세안 때 장갑 손가락의 강한 마찰 | train |
| syn-sol-0357 | normal_guidance | 일반 얼굴 세정제를 일부러 올려둠 | val_internal |
| syn-sol-0361 | normal_guidance | 사용자가 얼굴 세정제를 오래 문지름 | train |
| syn-sol-0362 | normal_guidance | 헹굼형 얼굴 세정제의 헹굼 생략 | train |
| syn-sol-0365 | normal_guidance | 얼굴 제품은 헹구고 두 번째 제품 여부 미상 | train |
| syn-sol-0366 | normal_guidance | 제거가 번거로워 선크림을 극소량으로 | train |
| syn-sol-0367 | normal_guidance | 내수성 표시와 자동 반복 의도 구분 | train |
| syn-sol-0382 | normal_guidance | 두 얼굴 제품 사전 혼합 | train |
| syn-sol-0383 | normal_guidance | 표시에 따라 두 제품을 혼합 | val_internal |
| syn-sol-0384 | normal_guidance | 얼굴 로션을 분사형으로 전환 | train |
| syn-sol-0386 | normal_guidance | 기기의 제품 병용 제한 확인 | train |
| syn-sol-0389 | normal_guidance | 기기 지시와 실제 얼굴 사용 일치 | train |
| syn-sol-0390 | normal_guidance | 표시 향료와 모두에게 금지라는 주장 | train |
| syn-sol-0391 | normal_guidance | 미표시와 성분 부재 구분 | train |
| syn-sol-0396 | normal_guidance | 손 씻은 뒤 편안한 보습 | train |
| syn-sol-0398 | normal_guidance | 건조한 손을 일부러 계속 방치 | train |
| syn-sol-0399 | normal_guidance | 특정 핸드크림의 반복 불편 | train |
| syn-sol-0400 | normal_guidance | 향 표시는 아직 미확인 | train |
| syn-sol-0402 | normal_guidance | 무향 표시와 개인 반응 | train |
| syn-sol-0410 | normal_guidance | 손 위생과 보습 유지 | train |
| syn-sol-0412 | normal_guidance | 과거 제품 반응과 현재 제품 | train |
| syn-sol-0416 | normal_guidance | 손 위생 뒤 보습과 작업 미상 | train |
| syn-sol-0417 | normal_guidance | 반복 불편과 손 위생 | train |
| syn-sol-0418 | normal_guidance | 손 건조와 전면 중단 | train |
| syn-sol-0422 | normal_guidance | 얼굴 수동 면도의 털 방향 | val_internal |
| syn-sol-0423 | normal_guidance | 목 수동 면도의 압력 | val_internal |
| syn-sol-0424 | normal_guidance | 턱 수동 면도의 반복 통과 | val_internal |
| syn-sol-0427 | normal_guidance | 얼굴 면도 불편을 무시한 강한 압력 | train |
| syn-sol-0428 | normal_guidance | 목 면도의 역방향 고수 | train |
| syn-sol-0430 | normal_guidance | 이전과 현재 수동 면도 분리 | val_internal |
| syn-sol-0431 | normal_guidance | 면도기 날 개수 미상 | val_internal |
| syn-sol-0432 | normal_guidance | 얼굴 면도 후 편안한 보습 | val_internal |
| syn-sol-0433 | normal_guidance | 목 면도 후 특정 제품의 반복 따가움 | train |
| syn-sol-0437 | normal_guidance | 목 면도 뒤 모든 보습 중단 | train |
| syn-sol-0438 | normal_guidance | 얼굴 면도 뒤 예전 제품과 현재 제품 | train |
| syn-sol-0439 | normal_guidance | 목 면도 뒤 별도 상품 미사용 | val_internal |
| syn-sol-0440 | normal_guidance | 얼굴 레티놀과 AHA 제품 동시 사용 | train |
| syn-sol-0441 | normal_guidance | 목 레티놀과 AHA 겹치는 기간 | train |
| syn-sol-0445 | normal_guidance | 서로 다른 부위의 두 제품 | train |
| syn-sol-0446 | normal_guidance | 단일 복합 완제품 | train |
| syn-sol-0449 | normal_guidance | 야외 수영 후보의 내수성 없음 | train |
| syn-sol-0455 | normal_guidance | 낮은 SPF가 명시된 새 후보 | train |
| syn-sol-0456 | normal_guidance | 노출 귀를 의도적으로 제외 | train |
| syn-sol-0458 | normal_guidance | 표시 제외 부위와 노출 | train |
| syn-sol-0459 | normal_guidance | 얼굴 일부의 의도적 누락 | train |
| syn-sol-0467 | normal_guidance | 목의 노출과 사용 범위 | train |
| syn-sol-0472 | normal_guidance | 얼굴 오른쪽 볼의 의도적 제외 | train |
| syn-sol-0473 | normal_guidance | 고온 운반 뒤 현재 보관 | train |
| syn-sol-0475 | normal_guidance | 장시간 열린 뚜껑 | train |
| syn-sol-0479 | normal_guidance | 열어 둔 가와 닫힌 나 | train |
| syn-sol-0481 | normal_guidance | 직사광선과 품질 미측정 | train |
| syn-hold-0107 | hold | 새 세정제 사용 후 지속 불편 | train |
| syn-hold-0108 | hold | 세정제 변경 전부터 지속된 불편 | train |
| syn-hold-0109 | hold | 불편한 얼굴 세정제 사용 중단 후 지속 | train |
| syn-hold-0110 | hold | 세안 횟수 변경 질문과 지속 불편 | train |
| syn-hold-0111 | hold | 세안 후 지속 불편과 원인 미상 | train |
| syn-hold-0112 | hold | 세정 방법 질문과 지속 불편 | train |
| syn-hold-0113 | hold | 타인 경험과 본인의 지속 불편 | train |
| syn-hold-0114 | hold | 지속 불편과 제품 버전 답변 거절 | train |
| syn-hold-0115 | hold | 로션 사용 후 지속된 얼굴 불편 | train |
| syn-hold-0116 | hold | 미용기기 사용 전부터 있던 지속 불편 | train |
| syn-hold-0117 | hold | 얼굴 제품 중단 뒤 지속 불편 | train |
| syn-hold-0118 | hold | 두 얼굴용 제품과 지속 불편 | train |
| syn-hold-0119 | hold | 사용량 변경 문의와 지속 불편 | train |
| syn-hold-0120 | hold | 제품 순서 문의와 지속 불편 | train |
| syn-hold-0121 | hold | 얼굴용 기기 후 지속 불편 | train |
| syn-hold-0122 | hold | 얼굴 제품과 지속 불편의 정보 거절 | train |
| syn-hold-0123 | hold | 손 보습 후 지속 불편 | train |
| syn-hold-0124 | hold | 손 씻기와 지속 불편 | train |
| syn-hold-0125 | hold | 손 보습 제품 변경 뒤 지속 불편 | train |
| syn-hold-0126 | hold | 손 작업 뒤 지속 불편 | train |
| syn-hold-0127 | hold | 손 보습 횟수 질문과 지속 불편 | train |
| syn-hold-0128 | hold | 양손의 지속 불편 | train |
| syn-hold-0129 | hold | 손 제품 반응과 지속 불편 | train |
| syn-hold-0130 | hold | 손 건조와 지속 불편 | train |
| syn-hold-0131 | hold | 얼굴 면도 부위 지속 불편 | train |
| syn-hold-0132 | hold | 목 면도 후 지속 불편 | train |
| syn-hold-0133 | hold | 면도 후 제품과 지속 불편 | train |
| syn-hold-0134 | hold | 면도 방법 질문과 지속 불편 | train |
| syn-hold-0135 | hold | 목 보습 질문과 지속 불편 | train |
| syn-hold-0136 | hold | 얼굴 관리 제품과 지속 불편 | train |
| syn-hold-0137 | hold | 면도 후 지속 불편과 원인 미상 | train |
| syn-hold-0138 | hold | 표시기한 전 새 변색 | val_internal |
| syn-hold-0139 | hold | 정상 두 층과 새 냄새 | val_internal |
| syn-hold-0140 | hold | 회수 조회와 새 냄새 | train |
| syn-hold-0141 | hold | 새 용기 누출 | train |
| syn-hold-0142 | hold | 두 용기 중 새 분리 | train |
| syn-hold-0143 | hold | 새 입자와 사용량 조절 | train |
| syn-hold-0144 | hold | 새 이물과 제조번호 | train |
| syn-hold-0145 | hold | 새 냄새와 보관 이동 | train |
| syn-hold-0146 | hold | 정상 분리와 새 냄새 | val_internal |
| syn-hold-0147 | hold | 기한 전 새 변색 | val_internal |
| syn-hold-0148 | hold | 새 균열과 누출 | train |
| syn-hold-0149 | hold | 한 용기의 새 분리 | train |
| syn-hold-0150 | hold | 새 입자 걸러 사용 | train |
| syn-hold-0151 | hold | 회수 비대상과 새 이물 | train |
| syn-hold-0152 | hold | 보관 변경과 새 악취 | train |
| syn-sol-0345 | unknown_or_version | 합성 분장 제거와 이후 잔여감 반복 | train |
| syn-sol-0347 | unknown_or_version | 횟수는 알려졌지만 제거 이유는 거절 | train |
| syn-sol-0355 | unknown_or_version | 온도계 없는 얼굴 세안 | train |
| syn-sol-0356 | unknown_or_version | 차가운 얼굴 세안수 | train |
| syn-sol-0359 | unknown_or_version | 제품 지시의 접촉시간 확인 안 됨 | train |
| syn-sol-0364 | unknown_or_version | 표시는 있지만 실제 헹굼은 미상 | train |
| syn-sol-0369 | unknown_or_version | 제거 부담이 있는 사용 선크림의 표시 미상 | train |
| syn-sol-0374 | unknown_or_version | 동일 용기 펌프의 양도 미측정 | val_internal |
| syn-sol-0379 | unknown_or_version | 알레르겐 표시와 현재 얼굴 제품 확인 | train |
| syn-sol-0380 | unknown_or_version | 두 제품의 향료 표시 구분 | train |
| syn-sol-0387 | unknown_or_version | 실제 병용과 기기 지시 미상 | train |
| syn-sol-0393 | unknown_or_version | 향 무선호와 확인된 개인 알레르기 구분 | train |
| syn-sol-0395 | unknown_or_version | 향료 표시와 개인 반응 미상 | train |
| syn-sol-0397 | unknown_or_version | 동료의 보습은 본인 기록이 아님 | val_internal |
| syn-sol-0401 | unknown_or_version | 손 보습 답변 거절 | train |
| syn-sol-0403 | unknown_or_version | 손 씻기는 유지하고 보습은 미상 | train |
| syn-sol-0404 | unknown_or_version | 가족의 크림과 본인의 미상 | val_internal |
| syn-sol-0405 | unknown_or_version | 동료의 보습 시간과 본인 | val_internal |
| syn-sol-0406 | unknown_or_version | 친구의 보습 경험과 본인 | val_internal |
| syn-sol-0407 | unknown_or_version | 동거인의 손 씻기 뒤 보습 | val_internal |
| syn-sol-0408 | unknown_or_version | 작업 뒤 손 보습의 반응 미상 | train |
| syn-sol-0409 | unknown_or_version | 무향료 표기와 오일 미상 | train |
| syn-sol-0411 | unknown_or_version | 손 작업 노출과 보습 미상 | train |
| syn-sol-0413 | unknown_or_version | 진료 지시 확인 중인 손 보습 | train |
| syn-sol-0414 | unknown_or_version | 손에 바르지 않는 얼굴 제품 | train |
| syn-sol-0415 | unknown_or_version | 핸드크림 이름과 향료 | train |
| syn-sol-0419 | unknown_or_version | 고정유와 향성 오일 구별 | train |
| syn-sol-0420 | unknown_or_version | 이전 표시와 현재 포장 | train |
| syn-sol-0421 | unknown_or_version | 손 반응의 주체 구분 | train |
| syn-sol-0425 | unknown_or_version | 동료의 목 면도와 본인의 볼 면도 | train |
| syn-sol-0426 | unknown_or_version | 목의 수동 면도 방향 미상 | train |
| syn-sol-0429 | unknown_or_version | 얼굴 면도의 압력 답변 거절 | train |
| syn-sol-0434 | unknown_or_version | 얼굴 후처리 반응 미상 | train |
| syn-sol-0435 | unknown_or_version | 목 면도 뒤 보습 거절 답변 | train |
| syn-sol-0436 | unknown_or_version | 동거인의 얼굴 후처리와 본인의 목 보습 | train |
| syn-sol-0442 | unknown_or_version | 레티놀과 AHA 접촉 부위 미상 | train |
| syn-sol-0443 | unknown_or_version | AHA 포함만 확인된 제품 | train |
| syn-sol-0444 | unknown_or_version | 관리 목적만 알려진 제품 | train |
| syn-sol-0447 | unknown_or_version | 처방 레티노이드와 AHA의 계획 | train |
| syn-sol-0448 | unknown_or_version | 접힌 사진의 광범위 표시 | train |
| syn-sol-0450 | unknown_or_version | 용기와 판매 정보의 버전 연결 | train |
| syn-sol-0451 | unknown_or_version | 두 후보의 서로 다른 누락 | train |
| syn-sol-0452 | unknown_or_version | 내수성의 가려진 부분 | train |
| syn-sol-0453 | unknown_or_version | 이전 용기와 현재 후보 | train |
| syn-sol-0454 | unknown_or_version | 수영 후보의 한 항목만 확인 | train |
| syn-sol-0457 | unknown_or_version | 전날 보습제 기록과 오늘 얼굴 차단제 | train |
| syn-sol-0460 | unknown_or_version | 예정된 도포와 실제 기록 | train |
| syn-sol-0461 | unknown_or_version | 새 용기 펌프 양 미확인 | val_internal |
| syn-sol-0462 | unknown_or_version | 땀과 도포의 순서 미상 | val_internal |
| syn-sol-0463 | unknown_or_version | 알림과 실행 구분 | val_internal |
| syn-sol-0464 | unknown_or_version | 발한 후 예정된 재도포 | val_internal |
| syn-sol-0465 | unknown_or_version | 긴소매 이외의 보호 미상 | val_internal |
| syn-sol-0466 | unknown_or_version | 야외 산책자의 기록과 친구의 말 | train |
| syn-sol-0468 | unknown_or_version | 야외 체류 중 재도포 알림 | val_internal |
| syn-sol-0469 | unknown_or_version | 모자의 사용과 선제품 양 | train |
| syn-sol-0470 | unknown_or_version | 그늘과 다른 수단 미상 | val_internal |
| syn-sol-0471 | unknown_or_version | 알림 해제와 실행 미상 | val_internal |
| syn-sol-0474 | unknown_or_version | 친구 용기와 본인 용기 | train |
| syn-sol-0476 | unknown_or_version | 배송 중 온도와 현재 위치 | train |
| syn-sol-0477 | unknown_or_version | 가려진 지침과 보관 이력 | train |
| syn-sol-0478 | unknown_or_version | 현재 서랍과 과거 노출 | train |
| syn-sol-0480 | unknown_or_version | 현재 밀봉과 열 이력 | train |
| syn-sol-0482 | unknown_or_version | 두 용기의 개봉일 | val_internal |
| syn-sol-0483 | unknown_or_version | 기한과 개봉 후 기간 | val_internal |
| syn-sol-0484 | unknown_or_version | 개봉일과 표시 가림 | train |
| syn-sol-0485 | unknown_or_version | 구매일과 개봉일 | train |
| syn-sol-0486 | unknown_or_version | 빈 용기와 새 용기 | val_internal |
| syn-sol-0487 | unknown_or_version | 개봉 전 상태 미확인 | val_internal |
| syn-sol-0488 | unknown_or_version | 타인의 개봉 기록 | train |
| syn-sol-0489 | unknown_or_version | 다른 나라 용기의 날짜 | train |
| syn-sol-0490 | unknown_or_version | 용량 다른 두 용기 | train |
| syn-sol-0491 | unknown_or_version | 이전 포장과 새 포장 | train |
| syn-sol-0492 | unknown_or_version | 실제 용기와 판매 페이지 | train |
| syn-sol-0493 | unknown_or_version | 재구매와 성분표 | train |
| syn-sol-0494 | unknown_or_version | 타 용기의 표시 복사 계획 | train |
| syn-sol-0495 | unknown_or_version | 인쇄 날짜의 일부 가림 | train |
| syn-sol-0496 | unknown_or_version | 두 용기의 구매 이력 | train |
| syn-sol-0497 | unknown_or_version | 보관 지침과 옛 사진 | train |
| syn-sol-0498 | unknown_or_version | 표시 충돌과 버전 불명 | train |
| syn-sol-0348 | distractor_or_defense | 본인의 한 번과 동거인의 두 번 | train |
| syn-sol-0349 | distractor_or_defense | 헹굼 반복과 세정제 재사용의 차이 | train |
| syn-sol-0350 | distractor_or_defense | 얼굴 수건 압력과 다른 부위의 강한 문지름 | train |
| syn-sol-0353 | distractor_or_defense | 손 씻는 물은 뜨겁지만 얼굴 물은 미온 | val_internal |
| syn-sol-0354 | distractor_or_defense | 얼굴 세안 물과 샤워 물의 차이 | train |
| syn-sol-0358 | distractor_or_defense | 대기 중 손 씻기를 얼굴 문지름으로 오인 | train |
| syn-sol-0360 | distractor_or_defense | 얼굴 세정제와 별도 팩 시간 구분 | train |
| syn-sol-0363 | distractor_or_defense | 얼굴 세정제와 바디 제품의 헹굼 | val_internal |
| syn-sol-0368 | distractor_or_defense | 얼굴 선크림 제거법을 아직 모름 | train |
| syn-sol-0370 | distractor_or_defense | 본인의 광보호 유지와 가족의 감량 | train |
| syn-sol-0371 | distractor_or_defense | 서로 다른 버전의 얼굴 팩 지시 | train |
| syn-sol-0372 | distractor_or_defense | 새 얼굴 세정제의 비공개 pH | train |
| syn-sol-0373 | distractor_or_defense | 용기 크기와 실제 사용량 분리 | train |
| syn-sol-0375 | distractor_or_defense | 세정제 양과 농도 혼동 | train |
| syn-sol-0376 | distractor_or_defense | 본인의 사용량 검토와 친구의 증량 | train |
| syn-sol-0377 | distractor_or_defense | 사용량과 성분 농도 미확인 | train |
| syn-sol-0378 | distractor_or_defense | 얼굴 로션 사용량과 비공개 농도 | train |
| syn-sol-0381 | distractor_or_defense | 다른 버전의 사용 지시 | train |
| syn-sol-0385 | distractor_or_defense | 미용기기 버전별 젤 병용 지시 | train |
| syn-sol-0388 | distractor_or_defense | 기기 병용과 제품 버전 미상 | train |
| syn-sol-0392 | distractor_or_defense | 가족의 알레르기와 본인의 선호 | val_internal |
| syn-sol-0394 | distractor_or_defense | 현재 제품과 다른 버전의 향료 표시 | train |

## syn-sol-0346 — 운동 전 세안과 운동 뒤 땀 제거

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `153f15b9ec6fd23e5a793d056ddaccfc7eeb0f23c403b5b544e275bef555e41d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

서로 다른 시점과 땀 제거 목적을 확인했어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "운동 전 얼굴을 한 번 씻고 운동하여 땀이 난 뒤 다시 얼굴을 씻었습니다. 각각 한 번씩이고 다른 연속 반복은 하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "aligned",
      "guidance": "운동 뒤 땀을 씻는 목적은 운동 전의 세안과 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
운동 뒤 땀을 씻는 목적은 운동 전의 세안과 구분해요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0351 — 얼굴에 천을 썼지만 압력 미상

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `3d187e754820e077383256bbf1732f5164516a3be0873a0e17d6e861896063e0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

도구 사용 차이와 압력 미상을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴의 일상 세안에 천을 사용했습니다. 문지르는 힘은 기억나지 않아 알려주지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "얼굴에 천을 쓴 점을 살펴보되 강한 마찰까지 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 천을 쓴 점을 살펴보되 강한 마찰까지 단정하지 않아요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0352 — 얼굴 세안 때 장갑 손가락의 강한 마찰

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `04649b02a6da1c51276b9f72674a21e28a603690b4909647552adfa5ef4f7304`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴의 실제 강한 마찰이 확인되며 증상은 추가하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "일상 얼굴 세안 때 장갑 낀 손가락으로 얼굴을 강하게 반복 문지릅니다. 증상은 보고하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "difference",
      "guidance": "얼굴에 강한 반복 마찰을 주는 현재 방법을 부드럽게 바꾸는 것을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 강한 반복 마찰을 주는 현재 방법을 부드럽게 바꾸는 것을 검토해요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0357 — 일반 얼굴 세정제를 일부러 올려둠

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `9d219b3648b167b1d123554392af6f73dbf89a5b1b291c4f12b0eee88c8d8926`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

일반 헹굼형 제품의 의도적인 긴 접촉이 확인됐어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "별도 접촉시간 지시가 없는 일반 헹굼형 얼굴 세정제를 세안 시 얼굴에 일부러 오래 올려둔 뒤 씻어냅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "별도 접촉시간 지시가 없는 이 헹굼형 세정제는 일부러 오래 올려두지 말고 부드럽게 사용한 뒤 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
별도 접촉시간 지시가 없는 이 헹굼형 세정제는 일부러 오래 올려두지 말고 부드럽게 사용한 뒤 헹궈요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0361 — 사용자가 얼굴 세정제를 오래 문지름

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `a3c80db375846aafaa96877e70846e0db243950baa3a15ec0d1bcc173986d681`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

경과 숫자가 아니라 의도된 오래 문지름이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "별도 시간 지시가 없는 일반 헹굼형 얼굴 세정제를 충분히 작용시키려 일부러 얼굴에 오래 문지른 뒤 헹굽니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "difference",
      "guidance": "일부러 오래 문지르기보다 세정제를 부드럽게 사용한 뒤 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
일부러 오래 문지르기보다 세정제를 부드럽게 사용한 뒤 헹궈요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0362 — 헹굼형 얼굴 세정제의 헹굼 생략

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `187a4fbc05f4eebabd918c57e30543364ac79b88c4edbc0be7ed9632ea8b694f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

해당 제품의 헹굼 필요와 생략이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "씻어내라고 표시된 일반 얼굴 세정제를 실제로 얼굴에 쓴 후 시간을 줄이기 위해 헹굼을 생략합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "difference",
      "guidance": "시간을 줄이려고 헹굼을 생략하지 말고 이 제품의 표시대로 사용 후 헹궈요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
시간을 줄이려고 헹굼을 생략하지 말고 이 제품의 표시대로 사용 후 헹궈요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0365 — 얼굴 제품은 헹구고 두 번째 제품 여부 미상

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `d553035d5ee363eacbb0d97b1a2ccae80b1764497390d1fcc94a21d995679919`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 한 제품의 사용에만 한정해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 쓴 헹굼형 세정제 하나는 표시대로 헹궜습니다. 그 뒤 다른 세정제를 썼는지는 기억나지 않습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "확인된 그 제품의 헹굼은 표시와 일치해요. 다른 제품 사용 여부는 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 그 제품의 헹굼은 표시와 일치해요. 다른 제품 사용 여부는 미상이에요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0366 — 제거가 번거로워 선크림을 극소량으로

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `a39b0a965bd02eb23ebd9c03b7fbd07dc71adb7ca10b27cbdd75baae4b2b1d49`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제거 부담과 도포량 변경의 연결이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 사용하는 선크림을 저녁에 지우기 번거로워서 표시 사용량보다 극소량만 바릅니다. 실제 제거 방법은 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "제거를 편하게 하려고 도포량을 극소량으로 줄이기보다 표시된 사용량 등 광보호 요건을 유지하고 해당 제품의 제거 지시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제거를 편하게 하려고 도포량을 극소량으로 줄이기보다 표시된 사용량 등 광보호 요건을 유지하고 해당 제품의 제거 지시를 확인해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합의 소규모 비교 결과는 모든 제품의 제거 방법으로 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0367 — 내수성 표시와 자동 반복 의도 구분

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `adb81133e5fb5fee01630acabcf8b8a3f36d7bbcce63405df4995fa7d0883c33`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제품 종류와 표시, 실제 반복 및 이유가 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "내수성 얼굴 선크림을 실제로 사용하고 표시만을 이유로 매번 무조건 얼굴을 연속 세 번 세안합니다. 별도의 제거 지시나 추가 오염은 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "difference",
      "guidance": "내수성 표시만으로 세 번 반복하기보다 광보호 사용을 유지하면서 해당 제품의 제거 지시와 실제 제거 필요에 맞춰 세안 단계를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
내수성 표시만으로 세 번 반복하기보다 광보호 사용을 유지하면서 해당 제품의 제거 지시와 실제 제거 필요에 맞춰 세안 단계를 검토해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합의 소규모 비교 결과는 모든 제품의 제거 방법으로 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0382 — 두 얼굴 제품 사전 혼합

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `5f35bc11c476007f5fc71ade1e3815c00a40354e9a83628f8a5d3fda456eb872`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 사전 혼합과 지시 미확인이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 로션 두 개를 같은 용기에 미리 섞어 사용합니다. 두 제품 모두 혼합 사용 지시가 확인되지 않았고 의료진 지시도 보고되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "확인되지 않은 사전 혼합을 기본 사용법으로 삼지 않도록 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인되지 않은 사전 혼합을 기본 사용법으로 삼지 않도록 검토해요. [kb:B-G04@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0383 — 표시에 따라 두 제품을 혼합

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `5059eb66484e35e14da84f822336ef7104c571df666ae7e1d286aebf92079ef6`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제조사 명시 혼합 지시와 실제 혼합을 함께 확인한 예외예요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "합성 얼굴용 제품 A의 확인된 사용 표시에는 지정된 제품 B와 사용 직전에 섞으라고 적혀 있습니다. 본인은 얼굴에 쓰기 직전 표시대로 A와 B를 섞어 사용합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "exception",
      "guidance": "확인된 해당 제품의 혼합 지시와 실제 사용을 함께 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 해당 제품의 혼합 지시와 실제 사용을 함께 살펴요. [kb:B-G04@0.6.1]

### 근거 및 이유
확인된 실제 사용과 표시·지시의 확인 여부를 분리해서 살펴요.

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0384 — 얼굴 로션을 분사형으로 전환

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `372d39fdcf673a489a016c16023c7d412b1a034c59aeefc6a0d569596e75cd64`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

바르는 제품의 실제 분사 전환과 지시 미확인이 확인됐어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 바르도록 만들어진 로션을 분사 용기에 옮겨 얼굴에 분사해 사용합니다. 해당 제품의 분사 전환 지시는 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G04",
      "status": "difference",
      "guidance": "분사 용기로 바꿔 쓰기보다 확인된 원래 제품의 도포 용법에 맞춰 사용해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
분사 용기로 바꿔 쓰기보다 확인된 원래 제품의 도포 용법에 맞춰 사용해요. [kb:B-G04@0.6.1]

### 근거 및 이유
확인된 실제 사용과 표시·지시의 확인 여부를 분리해서 살펴요.

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0386 — 기기의 제품 병용 제한 확인

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `a0be8b7f5f44d0ee216ed011e7b6418bcd8f6eaac606a56da80a0b96e525e571`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 병용과 해당 표시의 불일치가 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기와 로션을 실제로 함께 씁니다. 기기 표시에는 해당 로션을 병용하지 말라고 적혀 있으나 이를 무시하고 사용했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "difference",
      "guidance": "확인된 기기의 병용 제한을 따르도록 사용 방법을 재검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 기기의 병용 제한을 따르도록 사용 방법을 재검토해요. [kb:B-G06@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0389 — 기기 지시와 실제 얼굴 사용 일치

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `e05f23e80c390f4dea608c69c5070aa9bf2e077f38a5c93024d8e51f0fbad96e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제품별 지시와 그 범위의 사용이 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기와 합성 얼굴용 젤을 실제로 함께 사용합니다. 확인된 해당 기기의 표시에는 그 젤과 얼굴 부위의 병용이 명시되어 있고 실제 사용도 그 지시와 일치합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "aligned",
      "guidance": "확인된 해당 기기와 젤의 얼굴 사용은 표시된 지시와 일치하므로 그 지시 범위에서 유지할 수 있어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 해당 기기와 젤의 얼굴 사용은 표시된 지시와 일치하므로 그 지시 범위에서 유지할 수 있어요. [kb:B-G06@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0390 — 표시 향료와 모두에게 금지라는 주장

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `099ef60bc67786523fe145e44f53dfcaaef0af01bf88e0f42c33816d9f53a5a5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시와 개인 알레르기 여부를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품을 고르는 중 향료가 표시된 것을 보고 그 성분을 모든 사람에게 금지해야 한다고 생각합니다. 본인의 알레르기 여부는 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시에 있다는 이유만으로 모든 사람에게 금지된다고 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시에 있다는 이유만으로 모든 사람에게 금지된다고 판단하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0391 — 미표시와 성분 부재 구분

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `dfae69c5723ca8ebf26bf45f3834a31e97d1d3bd340f9df7d74eccd1ecdfbea3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시 여부와 실제 부재는 같지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품의 확인된 성분표에 특정 향료명이 보이지 않아 그 물질이 제품에 전혀 없다고 단정했습니다. 목록의 적용 범위는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "difference",
      "guidance": "표시에서 보이지 않는 사실만으로 성분이 전혀 없다고 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시에서 보이지 않는 사실만으로 성분이 전혀 없다고 확정하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0396 — 손 씻은 뒤 편안한 보습

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `61b306781427d491f27f5c6786b40922f1203d75fb83df3a7c31a6d48682534f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 견딜 수 있는 손 보습을 개별 지시와 함께 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손을 씻은 뒤 현재 쓰는 핸드크림을 바르며 이 제품을 바를 때 불편하지 않아요. 필요한 손 위생은 유지하고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견딜 수 있는 손 보습을 개별 지시와 함께 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손을 씻은 뒤 현재 쓰는 핸드크림을 바르며 이 제품을 바를 때 불편하지 않아요. 필요한 손 위생은 유지하고 있어요. 현재 견딜 수 있는 손 보습을 개별 지시와 함께 살펴요. [kb:B-M04@0.6.1]

### 근거 및 이유
현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0398 — 건조한 손을 일부러 계속 방치

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `2fbb882eaccbb52bf44db05bf275e2961a6610cb05f04a57581dd36d477010db`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손 건조를 계속 방치하는 현재 행동을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 건조한데도 손 보습을 계속 하지 않고 건조하게 두고 있어요. 손 위생은 유지해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "손 건조를 계속 방치하는 현재 행동을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손이 건조한데도 손 보습을 계속 하지 않고 건조하게 두고 있어요. 손 위생은 유지해요. 손 건조를 계속 방치하는 현재 행동을 검토해요. [kb:B-M04@0.6.1]

### 근거 및 이유
보습 전체를 중단하기보다 견딜 수 있는 손 보습을 검토해요. 필요한 손 위생은 유지해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0399 — 특정 핸드크림의 반복 불편

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `76790e5ae25f4bc0d5111a4c6cddec907c003a28c70d9c3b775148afe52c6de5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

반복 불편이 있는 해당 제품의 사용을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 같은 핸드크림을 바를 때마다 불편하지만 계속 쓰고 있어요. 다른 제품에 대한 반응은 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "반복 불편이 있는 해당 제품의 사용을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손에 같은 핸드크림을 바를 때마다 불편하지만 계속 쓰고 있어요. 다른 제품에 대한 반응은 몰라요. 반복 불편이 있는 해당 제품의 사용을 검토해요. [kb:B-M04@0.6.1]

### 근거 및 이유
반복해서 불편한 해당 제품은 사용 중단이나 대체를 검토해요. 필요한 손 위생은 유지해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0400 — 향 표시는 아직 미확인

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `65855848c705b887177f997f1502e971b68fbb0a16d4c30f827bb5aa6ff62312`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 견디는 제품의 유지와 미확인 표시를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 씻은 뒤 핸드크림을 바르지만 용기의 향료 표시를 읽지 못했어요. 이 제품을 바를 때 불편하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견디는 제품의 유지와 미확인 표시를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 씻은 뒤 핸드크림을 바르지만 용기의 향료 표시를 읽지 못했어요. 이 제품을 바를 때 불편하지 않아요. 현재 견디는 제품의 유지와 미확인 표시를 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0402 — 무향 표시와 개인 반응

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `d1c673f04b3de130025349b66b9163bce41ae3943e582e40bb8967e537882d5f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

무향료 표시와 그 제품의 반복 불편을 별도로 고려해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 쓰는 핸드크림에 무향료라고 적혀 있지만 바를 때마다 불편해요. 그래도 현재 계속 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "무향료 표시와 그 제품의 반복 불편을 별도로 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손에 쓰는 핸드크림에 무향료라고 적혀 있지만 바를 때마다 불편해요. 그래도 현재 계속 사용해요. 무향료 표시와 그 제품의 반복 불편을 별도로 고려해요. [kb:B-M04@0.6.1]

### 근거 및 이유
반복해서 불편한 해당 제품은 사용 중단이나 대체를 검토해요. 필요한 손 위생은 유지해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0410 — 손 위생과 보습 유지

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `b45aadb158338047f7806790afa6c6bbf516cee6af87995f8c898b906290287e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

견딜 수 있는 현재 손 보습과 필요한 위생을 함께 고려해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "필요한 손 씻기를 계속하고 씻은 뒤 현재 핸드크림을 발라요. 이 제품 사용에 불편은 없고 진료 지시는 없어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "견딜 수 있는 현재 손 보습과 필요한 위생을 함께 고려해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
필요한 손 씻기를 계속하고 씻은 뒤 현재 핸드크림을 발라요. 이 제품 사용에 불편은 없고 진료 지시는 없어요. 견딜 수 있는 현재 손 보습과 필요한 위생을 함께 고려해요. [kb:B-M04@0.6.1]

### 근거 및 이유
현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0412 — 과거 제품 반응과 현재 제품

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `b009ecfc8f8a29cdf406b09d1cf4971f9b7fca60c97f46c0bce18e2f2ee172dd`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 제품의 불편과 현재 제품의 관찰을 나누어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "이전 핸드크림은 손에 불편했어요. 지금 쓰는 다른 핸드크림은 편안하고 손 씻기 후 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "이전 제품의 불편과 현재 제품의 관찰을 나누어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 핸드크림은 손에 불편했어요. 지금 쓰는 다른 핸드크림은 편안하고 손 씻기 후 사용해요. 이전 제품의 불편과 현재 제품의 관찰을 나누어요. [kb:B-M04@0.6.1]

### 근거 및 이유
현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0416 — 손 위생 뒤 보습과 작업 미상

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `7ab4301d7824b5d6ce0497bfdb260f8d6bf2a5b78a7f0c821633f0f0690e09a1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 견디는 손 보습을 유지하면서 작업 정보는 미상으로 두어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 씻기 뒤 편안한 핸드크림을 쓰고 있어요. 그 밖의 젖은 작업 여부는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "exception",
      "guidance": "현재 견디는 손 보습을 유지하면서 작업 정보는 미상으로 두어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 씻기 뒤 편안한 핸드크림을 쓰고 있어요. 그 밖의 젖은 작업 여부는 확인되지 않았어요. 현재 견디는 손 보습을 유지하면서 작업 정보는 미상으로 두어요. [kb:B-M04@0.6.1]

### 근거 및 이유
현재 견딜 수 있는 제품의 사용은 개별 진료 지시와 함께 살펴요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0417 — 반복 불편과 손 위생

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `66c9e0a61767e995b92a6190cbc30854d2bf78440b5c7c57d64856e4f29e4713`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

필요한 손 위생과 특정 제품의 반복 불편을 분리해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "필요한 손 씻기를 유지하며 핸드크림을 사용해요. 해당 크림을 바를 때마다 불편한데도 계속 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "필요한 손 위생과 특정 제품의 반복 불편을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
필요한 손 씻기를 유지하며 핸드크림을 사용해요. 해당 크림을 바를 때마다 불편한데도 계속 사용해요. 필요한 손 위생과 특정 제품의 반복 불편을 분리해요. [kb:B-M04@0.6.1]

### 근거 및 이유
반복해서 불편한 해당 제품은 사용 중단이나 대체를 검토해요. 필요한 손 위생은 유지해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0418 — 손 건조와 전면 중단

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `6b40a13cd233feedbb59a5a423d25128b2e155bfec70cc0115eed40677c8a46b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손을 계속 건조하게 두는 행동을 검토하되 진단은 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 건조하다고 느끼는데 보습제를 모두 끊고 손을 계속 건조하게 두어요. 진단받은 질환은 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "difference",
      "guidance": "손을 계속 건조하게 두는 행동을 검토하되 진단은 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손이 건조하다고 느끼는데 보습제를 모두 끊고 손을 계속 건조하게 두어요. 진단받은 질환은 말하지 않았어요. 손을 계속 건조하게 두는 행동을 검토하되 진단은 만들지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
보습 전체를 중단하기보다 견딜 수 있는 손 보습을 검토해요. 필요한 손 위생은 유지해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0422 — 얼굴 수동 면도의 털 방향

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `46cbe0d0984d0915a7fe9c14c84c529ed25a848b8ee647de2cdf38ffd0038450`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 부드러운 수동 면도 방법을 유지해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 반복 통과를 줄여요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 부드러운 수동 면도 방법을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 반복 통과를 줄여요. 확인된 부드러운 수동 면도 방법을 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인된 현재 동작에 한정해 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0423 — 목 수동 면도의 압력

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `6c93d1ce11d7c1e2ec046cdaafef841d91e833d3dc8fcb12fe7beaa809dd9f69`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 압력과 방향, 반복 관리에 한정해 유지해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목을 수동 날면도로 깎으며 강하게 누르지 않고 털 방향으로 움직여요. 같은 곳을 반복하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 압력과 방향, 반복 관리에 한정해 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 수동 날면도로 깎으며 강하게 누르지 않고 털 방향으로 움직여요. 같은 곳을 반복하지 않아요. 확인된 압력과 방향, 반복 관리에 한정해 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인된 현재 동작에 한정해 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0424 — 턱 수동 면도의 반복 통과

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `3f36369d10ada3bc76351ddfb6770b5e5cd05aeb61e5b4dff962553de97cdacc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 얼굴 수동 면도 방법을 유지해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴의 턱을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 같은 곳의 반복 통과를 줄여요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 얼굴 수동 면도 방법을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴의 턱을 수동 날면도로 깎을 때 털 방향으로 가볍게 움직이고 같은 곳의 반복 통과를 줄여요. 확인된 얼굴 수동 면도 방법을 유지해요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인된 현재 동작에 한정해 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0427 — 얼굴 면도 불편을 무시한 강한 압력

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `502fad81c362be071879d12c0118fa80a2f56cd2bd6790eb01569e40ba7026ef`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

불편을 무시한 강한 압력과 반복 통과를 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강하게 누르고 여러 번 같은 곳을 지나가요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "difference",
      "guidance": "불편을 무시한 강한 압력과 반복 통과를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강하게 누르고 여러 번 같은 곳을 지나가요. 불편을 무시한 강한 압력과 반복 통과를 검토해요. [kb:B-G10@0.6.1]

### 근거 및 이유
불편을 무시하며 강하게 누르거나 반복하는 방법을 조정할 여지를 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0428 — 목 면도의 역방향 고수

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `510b6583c6cff787fe9ad5e9b013be497dca1af3a200f0051110f390811f8d76`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

불편을 무시한 강한 역방향 면도를 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강한 역방향 면도를 계속해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "difference",
      "guidance": "불편을 무시한 강한 역방향 면도를 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 수동 날면도로 깎을 때 불편해도 매끈함을 위해 강한 역방향 면도를 계속해요. 불편을 무시한 강한 역방향 면도를 검토해요. [kb:B-G10@0.6.1]

### 근거 및 이유
불편을 무시하며 강한 역방향으로 면도하는 방법을 조정할 여지를 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0430 — 이전과 현재 수동 면도 분리

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `7e60742679f618b979e9801ef2928ebaa210a06c095e9916dc67062e9cab88f4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 동작과 확인된 현재 동작을 나누어 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "예전에 얼굴 수동 날면도에서 강하게 눌렀어요. 현재는 털 방향으로 가볍게 움직이고 반복 통과를 줄여요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "이전 동작과 확인된 현재 동작을 나누어 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
예전에 얼굴 수동 날면도에서 강하게 눌렀어요. 현재는 털 방향으로 가볍게 움직이고 반복 통과를 줄여요. 이전 동작과 확인된 현재 동작을 나누어 살펴요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인된 현재 동작에 한정해 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0431 — 면도기 날 개수 미상

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `1f0af6ebeeac61fcce33e3fbe9ee9c9471df005933992377b73b01c6cf1b559a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 방법을 살피며 날 개수를 추측하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴을 수동 날면도로 깎고 털 방향으로 가볍게 움직이며 반복 통과를 줄여요. 날의 개수는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "aligned",
      "guidance": "확인된 방법을 살피며 날 개수를 추측하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "수동 날면도 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. 준비와 면도날 관리도 함께 안내해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 수동 날면도로 깎고 털 방향으로 가볍게 움직이며 반복 통과를 줄여요. 날의 개수는 확인하지 못했어요. 확인된 방법을 살피며 날 개수를 추측하지 않아요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인된 현재 동작에 한정해 살펴요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0432 — 얼굴 면도 후 편안한 보습

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `a80688b6168b6abab35091b5fbeecffabaf502d5927d1955bde57c924f7ddca9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

견딜 수 있는 면도 후 보습을 유지해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 현재 보습제를 바르고 편안해요. 별도의 애프터셰이브는 쓰지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "견딜 수 있는 면도 후 보습을 유지해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 면도 후 현재 보습제를 바르고 편안해요. 별도의 애프터셰이브는 쓰지 않아요. 견딜 수 있는 면도 후 보습을 유지해요. [kb:B-M05@0.6.1]

### 근거 및 이유
편안한 보습을 고려하며 별도 애프터셰이브 상품을 필수로 정하지 않아요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0433 — 목 면도 후 특정 제품의 반복 따가움

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `7d1ee451f5dae5bfaee70566b0cc2f9367f1ff2bcd229343120e099d30a6b915`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

반복 따가움을 흡수 효과로 해석해 계속 사용하는 행동을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 후처리 제품을 바를 때마다 따갑지만 흡수되는 느낌이라며 계속 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "difference",
      "guidance": "반복 따가움을 흡수 효과로 해석해 계속 사용하는 행동을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목 면도 후 후처리 제품을 바를 때마다 따갑지만 흡수되는 느낌이라며 계속 사용해요. 반복 따가움을 흡수 효과로 해석해 계속 사용하는 행동을 검토해요. [kb:B-M05@0.6.1]

### 근거 및 이유
불편을 유발하는 특정 후처리 제품은 중단이나 대체를 검토하고 기본 보습은 함께 고려해요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0437 — 목 면도 뒤 모든 보습 중단

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `19c11f101aa640dad9fa75ad01c744bdb9aa195be46678b013e2fb33a3be8341`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

특정 후처리 제품의 반응과 보습 전체 중단을 분리해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 보습이 필요하다고 느끼지만 따가운 후처리 제품 하나 때문에 모든 보습을 중단했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "difference",
      "guidance": "특정 후처리 제품의 반응과 보습 전체 중단을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목 면도 후 보습이 필요하다고 느끼지만 따가운 후처리 제품 하나 때문에 모든 보습을 중단했어요. 특정 후처리 제품의 반응과 보습 전체 중단을 분리해요. [kb:B-M05@0.6.1]

### 근거 및 이유
불편을 유발하는 특정 후처리 제품은 중단이나 대체를 검토하고 기본 보습은 함께 고려해요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0438 — 얼굴 면도 뒤 예전 제품과 현재 제품

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `163dfcb707e0d8cac25909cdde6854557bac01fd0f8c05c90be098143ad26e1a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

예전 후처리 제품과 현재 견디는 보습제를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 뒤 예전 후처리 제품은 따가웠어요. 다른 현재 보습제는 사용 후 편안해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "예전 후처리 제품과 현재 견디는 보습제를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 면도 뒤 예전 후처리 제품은 따가웠어요. 다른 현재 보습제는 사용 후 편안해요. 예전 후처리 제품과 현재 견디는 보습제를 구분해요. [kb:B-M05@0.6.1]

### 근거 및 이유
편안한 보습을 고려하며 별도 애프터셰이브 상품을 필수로 정하지 않아요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0439 — 목 면도 뒤 별도 상품 미사용

- 유형·분할: `normal_guidance` / `solution` / `val_internal`
- 내용 해시: `4dc77502d3459450c6c49d63d47491cca46830e73497b80557684da371652b22`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 편안한 보습을 살피며 별도 상품을 강제하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 보습제를 사용해 편안해요. 별도 애프터셰이브는 사용하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "aligned",
      "guidance": "확인된 편안한 보습을 살피며 별도 상품을 강제하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목 면도 후 보습제를 사용해 편안해요. 별도 애프터셰이브는 사용하지 않아요. 확인된 편안한 보습을 살피며 별도 상품을 강제하지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
편안한 보습을 고려하며 별도 애프터셰이브 상품을 필수로 정하지 않아요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0440 — 얼굴 레티놀과 AHA 제품 동시 사용

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `13523ece4dbd190ace5e0ae1176bd67ef3554d94d09f4a8cc23e3382e5c6028d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 부위의 별도 관리제품 중첩을 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 레티놀 관리용 화장품과 AHA 각질관리용 화장품을 별도 제품으로 같은 저녁 루틴에 함께 사용해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "같은 부위의 별도 관리제품 중첩을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 레티놀 관리용 화장품과 AHA 각질관리용 화장품을 별도 제품으로 같은 저녁 루틴에 함께 사용해요. 같은 부위의 별도 관리제품 중첩을 검토해요. [kb:B-G13@0.6.1]

### 근거 및 이유
별도 제품의 같은 부위 중첩을 줄이고 필요한 관리 한 종류를 우선 검토해요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0441 — 목 레티놀과 AHA 겹치는 기간

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `71ed065b8b27a7f9a8207b3879ead905376da7788acc247f5459c1d383ac6dcf`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 부위와 겹치는 사용기간을 확인하고 날짜 분리만으로 적합하다고 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목에 레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 사용하는 날은 달라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "difference",
      "guidance": "같은 부위와 겹치는 사용기간을 확인하고 날짜 분리만으로 적합하다고 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목에 레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 사용하는 날은 달라요. 같은 부위와 겹치는 사용기간을 확인하고 날짜 분리만으로 적합하다고 정하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
별도 제품의 같은 부위 중첩을 줄이고 필요한 관리 한 종류를 우선 검토해요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0445 — 서로 다른 부위의 두 제품

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `793c650c161319d5a01d5b73d33994b1afac96aee2717e31a9688e9f14e5e677`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 다른 부위에 동일 부위 중첩을 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "레티놀 관리용 화장품은 얼굴에, AHA 각질관리용 별도 화장품은 손에 같은 기간 사용해요. 두 제품의 실제 접촉 부위는 겹치지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "exception",
      "guidance": "확인된 다른 부위에 동일 부위 중첩을 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
레티놀 관리용 화장품은 얼굴에, AHA 각질관리용 별도 화장품은 손에 같은 기간 사용해요. 두 제품의 실제 접촉 부위는 겹치지 않아요. 확인된 다른 부위에 동일 부위 중첩을 적용하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
서로 다른 부위 또는 단일 복합 완제품이라는 확인된 조건을 별도로 살펴요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0446 — 단일 복합 완제품

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `be550e7479e093075c9ddd949ea96045bc0ea12b5827c15f6331deec1b80df6f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

단일 복합 완제품은 별도 제품 중첩과 나누어 제품별로 검토해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "레티놀과 AHA가 함께 든 단일 복합 완제품을 얼굴에 사용해요. 같은 관리 목적의 다른 제품은 사용하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "exception",
      "guidance": "단일 복합 완제품은 별도 제품 중첩과 나누어 제품별로 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
레티놀과 AHA가 함께 든 단일 복합 완제품을 얼굴에 사용해요. 같은 관리 목적의 다른 제품은 사용하지 않아요. 단일 복합 완제품은 별도 제품 중첩과 나누어 제품별로 검토해요. [kb:B-G13@0.6.1]

### 근거 및 이유
서로 다른 부위 또는 단일 복합 완제품이라는 확인된 조건을 별도로 살펴요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0449 — 야외 수영 후보의 내수성 없음

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `5fbdfe395894bd8a36f64a2bb613ac7b0be087044ffe18ed6b2649f586f2e410`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

수영용 후보의 내수성 없음 표시가 선택 기본값과 달라요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제 새 후보에 SPF 50, 광범위 보호와 내수성 없음이 표시돼 있어요. 야외 수영에 사용할 제품을 고르고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "difference",
      "guidance": "수영용 후보의 내수성 없음 표시가 선택 기본값과 달라요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
수영용 후보의 내수성 없음 표시가 선택 기본값과 달라요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0455 — 낮은 SPF가 명시된 새 후보

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `121479ef58bd4bfdd8c168cea75507ef694c827e8c9487e929d335035dd2dd84`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시된 SPF 15는 야외 후보의 SPF 30 선택 기본값보다 낮아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 달리기용 새 합성 자외선차단제의 현재 용기에는 SPF 15, 광범위 보호 및 내수성이 표시돼 있어요. 실제 사용은 아직 하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "difference",
      "guidance": "표시된 SPF 15는 야외 후보의 SPF 30 선택 기본값보다 낮아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시된 SPF 15는 야외 후보의 SPF 30 선택 기본값보다 낮아요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0456 — 노출 귀를 의도적으로 제외

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `0af9c724961e14bc5b4aab25a14ec431915a1f6963e06e6e8409116192e8b353`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시된 범위에서 노출된 귀의 누락을 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 산책에서 얼굴과 귀에 쓸 수 있다고 표시된 합성 자외선차단제를 얼굴에 바르면서 노출된 귀에는 일부러 바르지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "제품 표시 범위에 포함된 노출 귀를 빠뜨리지 않도록 표시된 용법에 맞춰 발라요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 표시 범위에 포함된 노출 귀를 빠뜨리지 않도록 표시된 용법에 맞춰 발라요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0458 — 표시 제외 부위와 노출

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `4a74b14c0a86a74fa73f78c34b5f4979ad1f4ee5c0fe1503b3181672d392faaf`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 사용 제한과 노출 부위를 함께 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 얼굴과 귀가 노출됐어요. 합성 자외선차단제의 사용 표시가 귀를 제외하므로 귀에는 바르지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "exception",
      "guidance": "확인된 사용 제한과 노출 부위를 함께 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 사용 제한과 노출 부위를 함께 살펴요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0459 — 얼굴 일부의 의도적 누락

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `923c74fd7809951912ad7f741dbf63bf27e9ae3f95d15ed9524df25a8b0e489b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

의도적으로 제외한 노출 부위를 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 얼굴에 사용할 합성 자외선차단제를 쓰면서 노출된 얼굴의 이마는 끈적임을 피하려고 일부러 빼고 발랐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "얼굴용 제품의 표시된 용법에 맞춰 노출된 이마를 빠뜨리지 않도록 발라요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품의 표시된 용법에 맞춰 노출된 이마를 빠뜨리지 않도록 발라요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0467 — 목의 노출과 사용 범위

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `62670eeb70760c0ccc0eead5d2c8ffc2d194ed29af070ae8338a79ddd9655447`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사용 범위에 포함된 노출 목의 의도적 누락을 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 합성 자외선차단제의 사용 범위에 포함되는 목이 노출됐지만 옷에 묻는 것이 싫어 일부러 목에는 바르지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "제품의 표시 사용 범위에 포함된 노출 목을 빠뜨리지 않도록 표시된 용법에 맞춰 발라요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품의 표시 사용 범위에 포함된 노출 목을 빠뜨리지 않도록 표시된 용법에 맞춰 발라요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0472 — 얼굴 오른쪽 볼의 의도적 제외

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `9238c630e990c73068c86354a381a39cc18ea8291f1897140a17cf8dbf09cb78`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴 관리 범위에서 확인된 오른쪽 볼의 의도적 누락을 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 얼굴용 합성 자외선차단제를 얼굴에 사용하면서 노출된 오른쪽 볼은 사용감 때문에 일부러 빼고 발랐어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "difference",
      "guidance": "얼굴용 제품을 바를 때 노출된 오른쪽 볼을 의도적으로 제외한 행동을 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 제품을 얼굴에 바를 때 노출된 오른쪽 볼을 빠뜨리지 않도록 표시된 용법에 맞춰 발라요. [kb:B-P02@0.6.1]

### 근거 및 이유
얼굴의 노출 부위를 의도적으로 제외한 사용을 제품의 표시 범위와 함께 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동이나 개인의 실제 보호 수준은 추정하지 않아요.

## syn-sol-0473 — 고온 운반 뒤 현재 보관

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `03998caa27952a4539bb4a9e74f283d86051e4de4adf82f4258080eca0ffeed1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

과거의 뜨거운 차 보관과 현재의 보관을 구분하고 현재 품질은 따로 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품이 뜨거운 차 안에 있었어요. 정확한 온도와 시간은 모르고 지금은 닫아서 직사광선을 피해 보관해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "과거의 뜨거운 차 보관과 현재의 보관을 구분하고 현재 품질은 따로 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
과거의 뜨거운 차 보관과 현재의 보관을 구분하고 현재 품질은 따로 확인해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0475 — 장시간 열린 뚜껑

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `1059a2765496eff3e7cda09f16842713919b38c2b9d96c7d9cf512c10cde135e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

직사광선 회피와 지속적으로 열린 용기를 분리해 살펴요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 햇빛은 피해서 보관했지만 뚜껑을 지속적으로 열어 두었어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "직사광선을 피한 보관은 유지하고 지속적으로 열어 둔 용기는 제품 보관 지침에 맞춰 닫아 보관해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
직사광선을 피한 보관은 유지하고 지속적으로 열어 둔 용기는 제품 보관 지침에 맞춰 닫아 보관해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0479 — 열어 둔 가와 닫힌 나

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `4b6c474973c9cea9dd8e82c0ca74b49958bbab4a142dcca188f43161732b545b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 열린 보관과 나의 닫힌 보관을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 가의 뚜껑은 계속 열려 있었어요. 나의 뚜껑은 닫혀 있었고 두 제품의 내용물 상태는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "열려 있던 가의 용기는 보관 지침에 맞춰 닫아 두고 이미 닫혀 있던 나와 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
열려 있던 가의 용기는 보관 지침에 맞춰 닫아 두고 이미 닫혀 있던 나와 구분해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0481 — 직사광선과 품질 미측정

- 유형·분할: `normal_guidance` / `solution` / `train`
- 내용 해시: `703d31db68e2de7c936cc7a3cab3a4e475f3ef9c5e020e4d2d1d30eed9dbd709`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

직사광선 보관은 확인됐으나 현재 안정성은 별도예요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 창가의 직사광선 아래에 계속 두었어요. 온도와 내용물의 현재 안정성은 측정하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "difference",
      "guidance": "제품 보관 지침을 확인하고 직사광선을 피해 보관해요. 현재 내용물의 안정성은 별도로 미확인 상태예요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 보관 지침을 확인하고 직사광선을 피해 보관해요. 현재 내용물의 안정성은 별도로 미확인 상태예요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-hold-0107 — 새 세정제 사용 후 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `732dc35775e35fa472b9b875973b0db33c89c965d52ff768f21bbaa64d391739`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "새 얼굴 세정제를 사용한 후 얼굴 불편감이 지속됩니다. 다른 제품의 사용 여부는 기억나지 않습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 새 세정제 사용 후 불편이 지속되지만 다른 제품의 사용은 기억나지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0108 — 세정제 변경 전부터 지속된 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `e7b6879d84b2849daa5d8327593dbe9758041fbd38ce59c3523498701643b4eb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속되는 동안 얼굴 세정제를 바꿨습니다. 불편감은 바꾸기 전부터 있었습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 불편은 세정제를 바꾸기 전부터 지속됐어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0109 — 불편한 얼굴 세정제 사용 중단 후 지속

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `4b027c58ff90ed457a7687d8e0d5f7bc8e357b87680526cfc09eb69c8f33b599`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 세정제 사용 중 불편해 그 제품을 중단했지만 얼굴 불편감이 여전히 지속됩니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 해당 세정제를 중단한 뒤에도 불편이 지속돼요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0110 — 세안 횟수 변경 질문과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `ed2e3a6a4a9b0d86846c34ad7c64ab9c554cd9a0a643d9b6f775618fe06c931a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속되는 가운데 얼굴 세안 횟수만 줄이면 되는지 묻습니다. 사용한 세정제는 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 불편이 지속되는 상황에서 세안 횟수만 줄여 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0111 — 세안 후 지속 불편과 원인 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `315b26070324004066da1ce613fc848712b5b60f7c78e7a1f48ba8330ec5287c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 세안 뒤 불편감이 지속되지만 세안 때문인지는 모릅니다. 새로운 제품 사용 여부도 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 세안 뒤 불편이 지속되지만 세안이 원인인지는 확인되지 않았어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0112 — 세정 방법 질문과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `8d7b205596964834ddd7517882cda156daa8d37ffc03a3932c504045cc53c610`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴의 불편감이 지속되고 있으며 세정 도구를 바꾸면 될지 묻습니다. 도구가 원인인지는 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 도구를 바꾸는 것만으로 지속 불편이 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0113 — 타인 경험과 본인의 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `9931810619ea28759b45dfd8b675d63b5b24bd378aca774d4ee3826c287478b3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "가족은 세안 뒤 편안했다고 합니다. 본인은 얼굴 불편감이 지속되고 있어 같은 방법을 따라도 되는지 묻습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 가족의 편안한 경험과 본인의 지속 불편을 구분해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0114 — 지속 불편과 제품 버전 답변 거절

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `5b4405a59991144c26ea8c1e4acc315c978be89d1a3edced899b83ec245b4414`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속됩니다. 사용 제품의 버전에 대한 답변은 거절했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 세안 루틴 판단을 보류해요. 제품 버전에 대한 답변을 거절하신 점을 그대로 존중해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0115 — 로션 사용 후 지속된 얼굴 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `cc69b800b176ea5d7d0d2bed19aa4f0e08aa248d55dc2f2f685535c77615ab9f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 로션을 사용한 후 얼굴 불편감이 지속됩니다. 정확한 제품 버전은 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 로션 사용 뒤 지속되었지만 정확한 제품 버전은 모르고 있어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0116 — 미용기기 사용 전부터 있던 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `65614f64be58caaaa8019c42057b864270095f04979715b38252a981485cd871`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속되는 가운데 얼굴용 미용기기를 사용했습니다. 불편감은 기기 사용 전부터 있었습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 불편은 기기를 사용하기 전부터 지속됐어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0117 — 얼굴 제품 중단 뒤 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `56a72f80745931254089c58c5c5776529cf602f6c709d75c408f87f6f8404657`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품을 쓰고 불편해 사용을 중단했지만 얼굴 불편감이 계속됩니다. 원인은 확인되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 해당 제품을 중단한 뒤에도 불편이 계속돼요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0118 — 두 얼굴용 제품과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `7e72938c7321c4a56dcfd1fbbb8d370293827cc82bb858443a6ca2665f5c14ba`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품 두 개를 같은 날 사용했고 얼굴 불편감이 지속됩니다. 어느 제품이 원인인지는 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 두 제품을 사용했지만 어느 제품이 원인인지는 알 수 없어요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0119 — 사용량 변경 문의와 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `1edf1ca59d1ba8dc9fa16db503c0e4e37fd189b4ab132d777398daf7771a11cb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품을 사용하는 동안 불편감이 지속됩니다. 양을 절반으로 줄여 계속 써도 되는지 묻습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 사용량을 절반으로 줄이는 것만으로 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0120 — 제품 순서 문의와 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `ceccdd8b8c669ea6210dfcca7a86efe7abc6f17267102c8f2c066ff423c9c742`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속되는 상태에서 얼굴용 제품 순서를 바꾸면 되는지 묻습니다. 제품 순서가 원인인지 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 제품 순서를 바꾸는 것만으로 해결된다고 판단하지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0121 — 얼굴용 기기 후 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `eb7c01b69bed63c6e4bf7700e36d09ee1c5c729e9221b063ff8a198d0b4b9bdc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기를 사용한 후 얼굴 불편감이 지속됩니다. 함께 쓴 제품은 기억하지 못합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 기기 사용 뒤 불편이 지속되지만 함께 쓴 제품은 기억나지 않아요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0122 — 얼굴 제품과 지속 불편의 정보 거절

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `7da01275cb5d0c2737520b87a7f472f8eb44ed47a938ae4e06e0d858d094805c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 불편감이 지속됩니다. 사용한 얼굴 제품의 성분표에 대한 답변은 거절했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속되는 불편에 대해 개별 루틴 판단을 보류하고 전문가 상담을 안내해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 불편이 지속되어 개별 루틴 판단을 보류해요. 성분표에 대한 답변을 거절하신 점을 그대로 존중해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
지속되는 불편을 의료 전문가에게 상담해요. 원인은 확인되지 않았어요.

## syn-hold-0123 — 손 보습 후 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `40cb2ee4f215df030da5ecf39da2db4a1523f1d8a5dda38ae04c205cb0fc40cf`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 핸드크림을 바른 뒤 불편이 지속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손에 핸드크림을 바른 뒤 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0124 — 손 씻기와 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `b12116a15011dd32e76a4d257d53c58a7d8d28fe104ab844c5b4221e97746396`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손을 씻는 일을 계속해야 하는데 손 불편이 지속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손을 씻는 일을 계속해야 하는데 손 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0125 — 손 보습 제품 변경 뒤 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `be194f5dc7bba917b57f7665b3aed3250449ad325f8c1c1ec5d9fd5ab2640d58`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습 제품을 바꾼 뒤 불편이 계속돼요. 원인은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손 보습 제품을 바꾼 뒤 불편이 계속돼요. 원인은 확인되지 않았어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0126 — 손 작업 뒤 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `9fcd830cd258e1de1cb31a56648ffeb6f8357333f93d3e7c344b6d196baa4ee8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "물에 손이 자주 닿는 작업을 한 뒤 손 불편이 지속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
물에 손이 자주 닿는 작업을 한 뒤 손 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0127 — 손 보습 횟수 질문과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `20b9b4452127551ff4cc04d8973ef42cb1da7795922ac4465708b9fc4de874c5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 불편이 지속되는 가운데 핸드크림을 몇 번 더 바를지 묻고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손 불편이 지속되는 가운데 핸드크림을 몇 번 더 바를지 묻고 있어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0128 — 양손의 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `60d9a38927e9b75d25ef88fb3f6362f90c2734cef69ed4261ac0b1a23831afd3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "양손에 불편이 계속돼요. 손에 바른 제품의 영향인지는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
양손에 불편이 계속돼요. 손에 바른 제품의 영향인지는 몰라요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0129 — 손 제품 반응과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `301520718295c395377becac4e301bcc2ff14814e5a2a2c3bd58f09865108fdc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 쓰는 제품을 바를 때 불편하고 그 불편이 지속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손에 쓰는 제품을 바를 때 불편하고 그 불편이 지속돼요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0130 — 손 건조와 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `3300e8db4f37b6acfce34e908ce67734579ecf8f890e6b2e6b2f1151eef9c095`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 건조하다고 느끼며 불편이 지속돼요. 별도 진단은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
손이 건조하다고 느끼며 불편이 지속돼요. 별도 진단은 확인되지 않았어요. 지속되는 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 단정하지 않아요.

## syn-hold-0131 — 얼굴 면도 부위 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `c595732b6d72b40e7c5492e15e18e80ebceb694769e7e4c1545d0eddd1062312`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 부위의 불편이 지속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 면도 부위의 불편이 지속돼요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0132 — 목 면도 후 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `c929610d78d59dbb44c9cd2367d7d1b962262a8b7544a38a7290a479ab968311`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 후 불편이 계속돼요. 원인은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
목 면도 후 불편이 계속돼요. 원인은 확인되지 않았어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0133 — 면도 후 제품과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `08406bc88227a81d82fd45e28ebbfd30862583a9843777e6903faff803554b8f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 제품을 바른 뒤 불편이 계속돼요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 면도 후 제품을 바른 뒤 불편이 계속돼요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0134 — 면도 방법 질문과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `61518998a4a8204d062e6d63aa063067ec25840bf7f451b589363d7bb96f57a8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "수동 날면도하는 얼굴 부위에 불편이 지속돼서 압력을 어떻게 바꿀지 묻고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
수동 날면도하는 얼굴 부위에 불편이 지속돼서 압력을 어떻게 바꿀지 묻고 있어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0135 — 목 보습 질문과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `c803fab6a85c2704c2eeeeedbcb72f53e5dcdf6ebedf5e30d3ba7490ae5e3518`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목 면도 부위에 불편이 지속되어 보습 횟수를 묻고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
목 면도 부위에 불편이 지속되어 보습 횟수를 묻고 있어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0136 — 얼굴 관리 제품과 지속 불편

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `170337443c2877e844c7c7c9670d6600982661b2c7fcf895604a9afeea58cb68`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 쓰는 두 관리 제품의 사용 기간 중 불편이 지속돼요. 어느 제품 때문인지는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴에 쓰는 두 관리 제품의 사용 기간 중 불편이 지속돼요. 어느 제품 때문인지는 몰라요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0137 — 면도 후 지속 불편과 원인 미상

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `09362317557e0caf5390d9ddc3f30e60b158458605cbdd531adafcad5b26ae67`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

지속 불편을 개별 루틴 조정으로 해결했다고 추정하지 않아요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 불편이 계속돼요. 면도와 제품 중 원인은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    },
    "skin.current_discomfort": {
      "variable_id": "skin.current_discomfort",
      "state": "known",
      "value": "persistent",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-B01",
      "status": "hold",
      "guidance": "지속 불편이 보고되어 개별 루틴 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-B01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
얼굴 면도 후 불편이 계속돼요. 면도와 제품 중 원인은 확인되지 않았어요. 지속 불편에 대한 개별 루틴 조정은 보류해요. [kb:B-B01@0.6.1]

### 필요한 다음 단계
현재 상태와 기존 진료 계획을 의료 전문가에게 확인해 주세요. 원인을 임의로 확정하지 않아요.

## syn-hold-0138 — 표시기한 전 새 변색

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `60976ebdb93418a47b3c3f45eadfe5711ffaa0a42d58312a2e60c5c021eda380`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 표시기한은 남았지만 원래 흰 내용물이 이번에 노랗게 변했어요. 계속 사용해도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
표시기한이 남아 있어도 이 합성 자외선차단제에서 새로 나타난 변색은 별도 확인이 필요해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 용기의 사용을 멈추고 표시와 보관 이력을 확인해 주세요. 변색의 원인이나 차단 성능은 이 기록으로 확정할 수 없어요.

## syn-hold-0139 — 정상 두 층과 새 냄새

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `a81eb1a64e873ac1b326597375c77a64c8abb7710bb1fb60495638be3d452be1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "흔들어 쓰도록 표시된 합성 자외선차단제는 원래 두 층이에요. 최근 이전에 없던 악취가 새로 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
원래 표시된 두 층과 최근 새로 생긴 악취는 서로 다른 관찰이에요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이 용기의 사용을 멈추고 냄새 변화에 관해 제조·판매처에 확인해 주세요. 정상적인 두 층이라는 사실만으로 새 냄새의 원인이나 제품 안전성을 확정하지 않아요.

## syn-hold-0140 — 회수 조회와 새 냄새

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `13ac2eba6cbf002866514948e7367aef255e187d3d83506841086819da187518`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 번호는 확인한 회수 목록에 없어요. 그러나 이 용기에서 전에 없던 냄새가 새로 나요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
확인한 회수 목록에 번호가 없다는 사실과 새 냄새는 별개예요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
냄새가 달라진 해당 용기의 사용을 멈추고 제조·판매처에 확인해 주세요. 목록 확인만으로 현재 품질이 확인되는 것은 아니에요.

## syn-hold-0141 — 새 용기 누출

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `78fd5cf53180878ba491e95e36cbf0a1229e3fdb2331287b0fc3ca453ed00194`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 사용기한은 남았어요. 최근 뚜껑 주변에 없던 균열과 누출이 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
기한이 남아 있어도 용기의 새 균열과 누출은 확인이 필요해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
누출된 해당 용기의 사용을 멈추고 제조·판매처에 상태를 확인해 주세요. 누출만으로 내용물 오염을 확정할 수는 없어요.

## syn-hold-0142 — 두 용기 중 새 분리

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `f85c5ac91d161959a45be2c19b5d4737296fa34fbee8213407692e1779519fa4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제 두 용기 중 가에서 이전에 없던 분리가 새로 생겼어요. 나의 상태는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
가 용기의 새 분리는 별도로 확인해야 해요. 나 용기의 상태는 아직 몰라요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
가 용기의 사용을 멈추고 제품 표시와 제조·판매처에 확인해 주세요. 나도 변질됐거나 안전하다고 단정하지 않아요.

## syn-hold-0143 — 새 입자와 사용량 조절

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `6353a8356148ff95519d64e83aae038e8370b7c58c86d78ba0d090b547d5c383`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제에 전에 없던 알갱이가 생겼어요. 양을 줄여서 계속 써도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
이전에 없던 알갱이가 생긴 제품은 사용량 조절로 해결됐다고 볼 수 없어요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품 사용을 멈추고 표시와 제조·판매처에 품질을 확인해 주세요. 입자의 정체는 확인되지 않았어요.

## syn-hold-0144 — 새 이물과 제조번호

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `baba512aebb6049ccbe5e1a07d6048388015b538e13c25aebf671f0a98105109`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제 용기의 제조번호를 확인했지만 원래 없던 이물이 새로 보였어요. 이물의 정체는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
제조번호를 확인한 사실과 새로 발견된 이물은 별개로 살펴야 해요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이물이 보인 해당 제품 사용을 멈추고 제조·판매처에 확인해 주세요. 이물의 정체와 원인을 추정하지 않아요.

## syn-hold-0145 — 새 냄새와 보관 이동

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `9a405cb32d24d90a242e7b5247158a0150eb7ebcf2e94959e5d0a071b4316930`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제에서 이전에 없던 냄새가 새로 나요. 보관 장소만 옮기고 계속 써도 되는지 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새 냄새가 생긴 제품은 보관 장소만 옮겨 품질이 회복됐다고 볼 수 없어요. 개별 사용 안내는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품 사용을 멈추고 표시와 제조·판매처에 냄새 변화를 확인해 주세요. 원인이나 오염 여부는 미상이에요.

## syn-hold-0146 — 정상 분리와 새 냄새

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `c18ff88d202b7610a468df69940dbc4eee8f094369f3c0989f7cdd297af992f0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "흔들어 쓰는 정상 두 층이 표시된 합성 화장품에서 최근 원래 없던 악취가 생겼어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
정상적으로 표시된 두 층과 새로 생긴 악취는 구분해서 확인해야 해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
악취가 생긴 용기의 사용을 멈추고 제조·판매처에 확인해 주세요. 원래 두 층이라는 표시가 새 냄새의 안전성을 증명하지는 않아요.

## syn-hold-0147 — 기한 전 새 변색

- 유형·분할: `hold` / `hold` / `val_internal`
- 내용 해시: `abdb36d5cc87871bf89d54f88d22518c47feccd67eef4bed7bd20ac51d0fe82e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 기한은 남았지만 내용물이 최근 원래 색과 다르게 변했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
인쇄 기한이 남았어도 새로 변한 내용물의 색은 별도 확인이 필요해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 용기의 사용을 멈추고 제품 표시와 제조·판매처에 확인해 주세요. 변색의 원인이나 안전성은 이 기록만으로 알 수 없어요.

## syn-hold-0148 — 새 균열과 누출

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `436e50b93dc34df731acd2049be4fdec43ab7e701f96f17d84dd7d37bc7b2578`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 용기에 최근 새 균열과 누출이 생겼어요. 내용물의 오염 여부는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
최근 생긴 용기 균열과 누출을 확인하기 전 개별 사용 안내를 보류해요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
누출된 용기의 사용을 멈추고 제조·판매처에 상태를 확인해 주세요. 오염 여부는 아직 확인되지 않았어요.

## syn-hold-0149 — 한 용기의 새 분리

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `9dc0ddbe2d1587eec52af25f2af95f8539c1dba0b05788e46d8c66edbdaf1017`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품 두 용기 중 가에서 최근 원래 없던 분리가 생겼어요. 나의 상태는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
가 용기에서 새 분리가 관찰됐지만 나 용기의 상태는 확인되지 않았어요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
가의 사용을 멈추고 그 용기의 표시와 제조·판매처에 확인해 주세요. 나도 이상이 있거나 안전하다고 추정하지 않아요.

## syn-hold-0150 — 새 입자 걸러 사용

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `a1d52254c51bc1c7372070fd1ae0e9cb8156a592cda43a6af297da6ddcd26e96`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품에 최근 원래 없던 입자가 생겼어요. 걸러서 계속 쓰는 방법을 물어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새로 생긴 입자를 걸러내는 것으로 제품 상태가 확인되지는 않아요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 사용을 멈추고 제조·판매처에 새 입자를 확인해 주세요. 입자의 정체와 원인은 미상이에요.

## syn-hold-0151 — 회수 비대상과 새 이물

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `87a29e6ed522a9f1072a2d3a7bf4852ca2a40fbbf8b5245a476114aebf3a31d5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "확인한 합성 회수 목록에 해당 번호는 없지만 해당 화장품에서 최근 원래 없던 이물이 보였어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
회수 목록에 해당 번호가 없는 것과 새 이물의 관찰은 별개예요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
이물이 나타난 제품의 사용을 멈추고 제조·판매처에 확인해 주세요. 목록 확인만으로 현재 품질이나 이물의 정체를 확정하지 않아요.

## syn-hold-0152 — 보관 변경과 새 악취

- 유형·분할: `hold` / `hold` / `train`
- 내용 해시: `3945b9a3895c932663287d885668495d1789d5cadf1a865ee5a8954b706c1090`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요.

### 입력

```json
{
  "mode": "hold",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품에서 전에 없던 악취가 최근 생겼어요. 서늘한 곳으로 옮겨 계속 쓰고 싶어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S04",
      "status": "hold",
      "guidance": "새 품질 이상을 확인하기 전 해당 제품 사용과 개별 권고를 보류해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 개별 권고 보류 안내
새로 생긴 악취는 서늘한 곳으로 옮기는 것만으로 해결됐다고 볼 수 없어요. 개별 권고는 보류해요 [kb:B-S04@0.6.1].

### 필요한 다음 단계
해당 제품의 사용을 멈추고 냄새 변화에 관해 제조·판매처에 확인해 주세요. 원인이나 오염 여부는 아직 몰라요.

## syn-sol-0345 — 합성 분장 제거와 이후 잔여감 반복

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c3a8fcd677a27e7afa82da589938fa7b1f51ee2bab12b4bda4a48d05b8399bce`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

한 번의 추가 반복만으로 습관성은 확인되지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴 분장을 지우기 위해 세정한 뒤, 분장은 이미 지워졌고 추가 오염도 없는데 잔여감이 걱정되어 같은 얼굴 세안을 두 번 더 연속합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "추가 세안은 확인되지만 한 번의 기록만으로 습관적인 반복이라고 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
추가 세안은 확인되지만 한 번의 기록만으로 습관적인 반복이라고 단정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0347 — 횟수는 알려졌지만 제거 이유는 거절

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c791a9f560c3dcf0a2748a4fd523a1beb778e5911709621a63243d8e6ebc0b52`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

답변 거절을 목적 없음으로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴을 연속 두 번 세안했다고만 알려주며 그 이유에 대한 답변은 거절했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "연속 세안의 이유를 알 수 없어 목적 없는 반복으로 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
연속 세안의 이유를 알 수 없어 목적 없는 반복으로 단정하지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0355 — 온도계 없는 얼굴 세안

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `8335b80813b807d4b42103a87a1ae8f7b0eed748d4a18470a12b4e77bd85ec9b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

측정값이나 느낌을 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴을 매일 씻지만 물이 뜨겁게 느껴지는지 미온인지 기억하지 못합니다. 온도도 측정하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "물의 느낌과 온도가 확인되지 않아 얼굴 물 온도를 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
물의 느낌과 온도가 확인되지 않아 얼굴 물 온도를 판정하지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0356 — 차가운 얼굴 세안수

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d66912b926791d3c75eb46e67ae0803f4c5d82a1e8fb1df9d7e18c3edb50e01f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

차가운 물만으로 위험 판정을 하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "일상 얼굴 세안에 차갑게 느껴지는 물을 사용합니다. 의료진의 별도 지시는 보고하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "unknown",
      "guidance": "차가운 물을 썼다는 사실만으로 위험하거나 뜨거운 물을 쓴 것으로 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
차가운 물을 썼다는 사실만으로 위험하거나 뜨거운 물을 쓴 것으로 판단하지 않아요. [kb:B-C01@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0359 — 제품 지시의 접촉시간 확인 안 됨

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `6f09207f93d63a831241ee9620ed4aa69345ccc68f6899d3f9e9bceb6baaaf4d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

경과 시간만으로 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "일반 헹굼형 얼굴 세정제를 얼굴에 잠시 둔 뒤 헹궜으나 제품의 접촉시간 지시는 확인하지 못했습니다. 일부러 오래 두었는지도 기억나지 않습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "unknown",
      "guidance": "사용 시간의 뜻과 제품 지시가 확인되지 않아 오래 둔 행동으로 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
사용 시간의 뜻과 제품 지시가 확인되지 않아 오래 둔 행동으로 단정하지 않아요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0364 — 표시는 있지만 실제 헹굼은 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c681c836b23d6ffc7bc1a16d1c7184890bb6a84634637fed7cbe63d47a2f9f08`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시만으로 실제 행동을 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 쓴 일반 세정제의 표시에는 물로 씻어내라고 적혀 있습니다. 실제 사용 뒤 물로 헹궜는지는 기억하지 못합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "unknown",
      "guidance": "표시와 실제 헹굼 여부를 구분하고 사용 행동은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
표시와 실제 헹굼 여부를 구분하고 사용 행동은 미상으로 남겨요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0369 — 제거 부담이 있는 사용 선크림의 표시 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1e99d503aed6c70bb892bd3faeeab9f6596c616e3abc2d43177fc18484848ed7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴 선크림의 제거 부담이 확인되지만 사용한 제품의 표시와 지시는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 실제로 사용한 선크림을 지우기 어려워 세안 단계를 검토합니다. 가지고 있지만 쓰지 않은 다른 선크림에는 내수성 표시가 있고, 실제 사용한 선크림의 내수성과 제거 지시는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "사용하지 않은 제품의 표시를 실제 사용 제품에 옮기지 않고 제거 지시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
사용하지 않은 제품의 표시를 실제 사용 제품에 옮기지 않고 제거 지시를 확인해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합의 소규모 비교 결과를 모든 제품의 제거 방법으로 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0374 — 동일 용기 펌프의 양도 미측정

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `8736025553d28a1632ea341fe8593bc1d5c8faaf43c327bd18344b8578d715ba`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

펌프 한 번의 질량이 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "같은 얼굴용 펌프 제품을 아침 한 번, 저녁 두 번 누릅니다. 한 번의 배출 질량은 측정하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "누른 횟수는 구분하되 질량으로 환산하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
누른 횟수는 구분하되 질량으로 환산하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0379 — 알레르겐 표시와 현재 얼굴 제품 확인

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `bf1f3969c822e768e20dd36da3be254981cf690ef8e062a99089d33277ffa05f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

성분표는 개인 반응을 알려주지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품의 현재 성분표에서 특정 향료명을 확인했습니다. 개인 알레르기 여부에 대한 답변은 거절했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "확인된 표시와 답변을 거절한 개인 알레르기 여부를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 표시와 답변을 거절한 개인 알레르기 여부를 구분해요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0380 — 두 제품의 향료 표시 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `48909a32c2d30537f8d0213bbdc74117bcdd439d7b2158e3a15f732d7120fdcd`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제품별 성분표가 다를 수 있어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품 A에는 특정 향료명이 표시되어 있지만 실제 고르는 얼굴용 제품 B의 성분표는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "제품 A의 표시를 제품 B의 표시로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
제품 A의 표시를 제품 B의 표시로 옮기지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0387 — 실제 병용과 기기 지시 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9098a5786d6c3fb6b11596756d3250f7da20d34591763a15175c6ee3a3fd9344`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

병용은 확인됐지만 지시는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기와 얼굴용 로션을 실제로 함께 사용했습니다. 기기의 로션 병용 지시는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "기기와 로션을 함께 쓴 사실은 확인됐지만 병용 적합성은 미확인이에요. 해당 조합의 사용을 추천하기는 보류하고 기기의 공개 사용 지침을 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
기기와 로션을 함께 쓴 사실은 확인됐지만 병용 적합성은 미확인이에요. 해당 조합의 사용을 추천하기는 보류하고 기기의 공개 사용 지침을 확인해요. [kb:B-G06@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0393 — 향 무선호와 확인된 개인 알레르기 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a3c6f42f325cd11c07867d13c7fed54bb476d11b8107eb1ffefe5af764183eb2`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

선호와 개인 알레르기는 달라요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품에서 향을 피하고 싶다는 선호를 밝혔지만 의학적으로 확인된 알레르기 여부는 밝히지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "향을 피하고 싶은 선호는 존중하되 알레르기 진단으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
향을 피하고 싶은 선호는 존중하되 알레르기 진단으로 바꾸지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0395 — 향료 표시와 개인 반응 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `4113d01123f380ea7d9e34e04102bc43ec362ac2794ddf46a9b4b0042ba6164e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

표시 정보로 개인 반응을 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품의 현재 확인된 성분표에 향료가 표시되어 있습니다. 본인의 해당 성분에 대한 반응과 알레르기는 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "확인된 표시는 기록하되 개인의 반응이나 알레르기는 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 표시는 기록하되 개인의 반응이나 알레르기는 미상으로 남겨요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0397 — 동료의 보습은 본인 기록이 아님

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `37f7c31a0569eca77af1c86be5f1d3e1204168715761e1b6a1f58b3b26aebdc1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동료의 행동으로 본인의 보습 여부를 대신하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 필요한 손 씻기를 해요. 동료는 손을 씻은 뒤 보습하지만 본인의 보습 여부는 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동료의 행동으로 본인의 보습 여부를 대신하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 필요한 손 씻기를 해요. 동료는 손을 씻은 뒤 보습하지만 본인의 보습 여부는 말하지 않았어요. 동료의 행동으로 본인의 보습 여부를 대신하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0401 — 손 보습 답변 거절

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1e49204d5c7e87751d1159e36667783b590ecec4cca8dba4f66c4955cad7dfa0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

답변 거절을 보습하지 않는다는 뜻으로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "필요한 손 위생을 유지해요. 손 보습 사용 여부에 관한 답변은 원하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "답변 거절을 보습하지 않는다는 뜻으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
필요한 손 위생을 유지해요. 손 보습 사용 여부에 관한 답변은 원하지 않아요. 답변 거절을 보습하지 않는다는 뜻으로 바꾸지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0403 — 손 씻기는 유지하고 보습은 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a5c3ccf977fe0d2b2a039b87babaf07d8bf3a5b7fd74315fca09f9ac0fa45f5d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손 씻는 사실만으로 손 보습 행동을 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손을 자주 씻으며 필요한 손 위생은 유지해요. 손 보습을 하는지는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "손 씻는 사실만으로 손 보습 행동을 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손을 자주 씻으며 필요한 손 위생은 유지해요. 손 보습을 하는지는 확인되지 않았어요. 손 씻는 사실만으로 손 보습 행동을 판단하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0404 — 가족의 크림과 본인의 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `5fd1d513908352ef115bf98f0dd36d84f2b16ccb8ddc1e1e83c47fc7ce165e67`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족의 보습 행동을 본인에게 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가족은 손 씻은 뒤 보습제를 써요. 본인이 손에 보습제를 쓰는지는 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "가족의 보습 행동을 본인에게 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "Hand-care guidance discusses moisturizing after handwashing and fragrance-free creams or ointments. It does not replace necessary hand hygiene or guarantee individual tolerance.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가족은 손 씻은 뒤 보습제를 써요. 본인이 손에 보습제를 쓰는지는 확인되지 않았어요. 가족의 보습 행동을 본인에게 옮기지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0405 — 동료의 보습 시간과 본인

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `ab83a01cccbd270ade62121183cb9f628d26ff8ef1dab92279c0d8dd8a3f6ba0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동료의 시간으로 본인의 손 보습을 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "동료는 근무 뒤 손에 보습제를 바른다고 해요. 본인의 손 보습 시간은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동료의 시간으로 본인의 손 보습을 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
동료는 근무 뒤 손에 보습제를 바른다고 해요. 본인의 손 보습 시간은 확인되지 않았어요. 동료의 시간으로 본인의 손 보습을 정하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0406 — 친구의 보습 경험과 본인

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `135b93f7d4dbd07146723d191234effe8a38b2c8ccbc20b73d5d85e857c41523`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 사용을 본인의 사용으로 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "친구는 손을 씻고 크림을 쓴다고 해요. 본인이 손을 씻은 후 보습하는지는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "친구의 사용을 본인의 사용으로 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
친구는 손을 씻고 크림을 쓴다고 해요. 본인이 손을 씻은 후 보습하는지는 몰라요. 친구의 사용을 본인의 사용으로 판단하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0407 — 동거인의 손 씻기 뒤 보습

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `a82bd5b10cd68b2e8434b9eca20c7eadfcc0f34461c22a1b4a7029da7c7ddcb8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동거인의 기록과 본인의 답변 거절을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "동거인은 손 씻기 후에 보습해요. 본인은 손 씻기를 하지만 손 보습 여부는 답하고 싶지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "동거인의 기록과 본인의 답변 거절을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
동거인은 손 씻기 후에 보습해요. 본인은 손 씻기를 하지만 손 보습 여부는 답하고 싶지 않아요. 동거인의 기록과 본인의 답변 거절을 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0408 — 작업 뒤 손 보습의 반응 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1c966444be84c33285c60cb082747fdd115abe97048a69c0d9012c26ebd16409`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사용과 개인 반응 미확인을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "젖은 작업을 한 뒤 손에 핸드크림을 발라요. 사용했을 때의 개인 반응은 아직 말하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "사용과 개인 반응 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
젖은 작업을 한 뒤 손에 핸드크림을 발라요. 사용했을 때의 개인 반응은 아직 말하지 않았어요. 사용과 개인 반응 미확인을 구분해요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0409 — 무향료 표기와 오일 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `888db5eb8f529e9af763da27727de751c04baf8a09b221353489c1a516903c2f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

무향료 표기만으로 향성 에센셜오일 여부를 정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습 후보에 무향료라고 적혀 있어요. 향성 에센셜오일 포함 여부는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "무향료 표기만으로 향성 에센셜오일 여부를 정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 보습 후보에 무향료라고 적혀 있어요. 향성 에센셜오일 포함 여부는 확인하지 못했어요. 무향료 표기만으로 향성 에센셜오일 여부를 정하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0411 — 손 작업 노출과 보습 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c4c84fb95628f032061ba0b06750580ee942c03a3b9f89425d31ac28aa33a3f1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

습식 작업만으로 보습 행동이나 제품 반응을 만들지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손이 물에 자주 닿는 작업을 해요. 작업 후 보습 여부와 제품 반응은 알 수 없어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "습식 작업만으로 보습 행동이나 제품 반응을 만들지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손이 물에 자주 닿는 작업을 해요. 작업 후 보습 여부와 제품 반응은 알 수 없어요. 습식 작업만으로 보습 행동이나 제품 반응을 만들지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0413 — 진료 지시 확인 중인 손 보습

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ea00357d7395916f8a6c8960facc9869c2ca777e9028ea6c238ebad84e10f740`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

개별 진료 지시의 유무를 추측하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 보습제를 쓰고 있어요. 보습에 관한 개별 진료 지시가 있는지는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "개별 진료 지시의 유무를 추측하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손에 보습제를 쓰고 있어요. 보습에 관한 개별 진료 지시가 있는지는 아직 확인하지 못했어요. 개별 진료 지시의 유무를 추측하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0414 — 손에 바르지 않는 얼굴 제품

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `bde858211804cd7be1b6297f0c704935ea028832849f28b187ff5a2ebd14b6dd`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴 제품 경험을 손 제품 경험으로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 보습제는 편안해요. 손 보습 제품의 사용 여부와 반응은 모른다고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "얼굴 제품 경험을 손 제품 경험으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 보습제는 편안해요. 손 보습 제품의 사용 여부와 반응은 모른다고 해요. 얼굴 제품 경험을 손 제품 경험으로 옮기지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0415 — 핸드크림 이름과 향료

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `b62e35fbdc6c46c69cbb3e1cd7a60a178910405f9250c71b0623bfc81af5c5eb`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

제품 이름만으로 향료나 향성 오일을 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손에 바를 후보는 핸드크림이에요. 전성분이나 향료 표시는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "제품 이름만으로 향료나 향성 오일을 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손에 바를 후보는 핸드크림이에요. 전성분이나 향료 표시는 확인하지 못했어요. 제품 이름만으로 향료나 향성 오일을 판정하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0419 — 고정유와 향성 오일 구별

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d9aa52d3b4f6e5dcf714e179c97e8704205827912585dd6f6a6745d7d3124d42`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

미네랄오일이라는 표시를 향성 에센셜오일로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습 후보의 표시에서 미네랄오일을 봤어요. 향료와 향성 에센셜오일은 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "미네랄오일이라는 표시를 향성 에센셜오일로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 보습 후보의 표시에서 미네랄오일을 봤어요. 향료와 향성 에센셜오일은 확인하지 못했어요. 미네랄오일이라는 표시를 향성 에센셜오일로 바꾸지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0420 — 이전 표시와 현재 포장

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `2291fa49611eb3f28a824444472f2c3319b43cab7cbf111f6c10676b42890874`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 표시를 현재 포장에 그대로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "손 보습제 예전 포장에는 무향료라고 적혀 있었어요. 현재 포장의 버전과 표시는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "이전 표시를 현재 포장에 그대로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
손 보습제 예전 포장에는 무향료라고 적혀 있었어요. 현재 포장의 버전과 표시는 확인하지 못했어요. 이전 표시를 현재 포장에 그대로 옮기지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0421 — 손 반응의 주체 구분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `6e7d21fe5d4bf72b5daebe98e905163e4a2e04bb61f7a237b9f70a2b45ec733a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족의 반응을 본인의 반응으로 판정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "가족은 이 핸드크림을 쓰면 불편하다고 해요. 본인의 손 사용 여부와 반응은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M04",
      "status": "unknown",
      "guidance": "가족의 반응을 본인의 반응으로 판정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손 관리 안내는 손을 씻은 뒤 보습과 무향료 크림 또는 연고 선택을 다뤄요. 필요한 손 위생을 줄이라는 뜻이나 개인에게 반드시 편안하다는 보장은 아니에요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M04@0.6.1",
    "ref:S21"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가족은 이 핸드크림을 쓰면 불편하다고 해요. 본인의 손 사용 여부와 반응은 확인되지 않았어요. 가족의 반응을 본인의 반응으로 판정하지 않아요. [kb:B-M04@0.6.1]

### 근거 및 이유
확인되지 않은 정보는 미상으로 두고 필요한 내용만 확인해요. [kb:B-M04@0.6.1] 손 관리 안내는 손 씻은 뒤 보습과 무향료 제품 선택을 다루며 필요한 손 위생을 줄이라는 뜻은 아니에요. [ref:S21]

### 확인이 필요한 한계
제품 표시나 다른 사람의 경험만으로 개인의 반응이나 원인을 확정하지 않아요.

## syn-sol-0425 — 동료의 목 면도와 본인의 볼 면도

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `0092334fa304ba8b0321fefd668484be3ce81549e44632380a790c608d1040b9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동료의 목 면도 압력을 본인의 볼 면도 압력으로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 볼을 수동 날면도해요. 이때 본인의 방향과 압력은 기억나지 않아요. 직장 동료는 다른 날 목을 수동 날면도할 때 강하게 누른다고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "동료의 목 면도 압력을 본인의 볼 면도 압력으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 볼을 수동 날면도해요. 이때 본인의 방향과 압력은 기억나지 않아요. 직장 동료는 다른 날 목을 수동 날면도할 때 강하게 누른다고 해요. 동료의 목 면도 압력을 본인의 볼 면도 압력으로 옮기지 않아요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인되지 않은 동작은 추측하지 않고 필요한 경우 확인해요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0426 — 목의 수동 면도 방향 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `996c5ad44c9de8104d199e01e4326cab5caa903b156e4f96ebc3370b912223ee`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사용 부위와 도구는 알려져 있으나 세부 동작은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목을 수동 날면도로 깎아요. 털 방향과 압력, 반복 통과는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "사용 부위와 도구는 알려져 있으나 세부 동작은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 수동 날면도로 깎아요. 털 방향과 압력, 반복 통과는 확인하지 못했어요. 사용 부위와 도구는 알려져 있으나 세부 동작은 미상이에요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인되지 않은 동작은 추측하지 않고 필요한 경우 확인해요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0429 — 얼굴 면도의 압력 답변 거절

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `7962dfc6bea1b838ff92e39c736b5f5fd3479f97e901094fa12b5bc2a39a50f7`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

답변 거절을 강한 면도로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴을 수동 날면도로 깎아요. 면도 압력과 방향에 대해서는 답하고 싶지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G10",
      "status": "unknown",
      "guidance": "답변 거절을 강한 면도로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "Manual shaving guidance discusses shaving with the direction of hair growth and using a gentle technique. It also discusses preparation and care of the blade.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G10@0.6.1",
    "ref:S23"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴을 수동 날면도로 깎아요. 면도 압력과 방향에 대해서는 답하고 싶지 않아요. 답변 거절을 강한 면도로 바꾸지 않아요. [kb:B-G10@0.6.1]

### 근거 및 이유
확인되지 않은 동작은 추측하지 않고 필요한 경우 확인해요. [kb:B-G10@0.6.1] 수동 날면도에 관한 일반 안내는 털이 자라는 방향과 부드러운 면도 방법을 다뤄요. [ref:S23]

### 확인이 필요한 한계
날의 개수나 모든 사람의 면도 빈도를 정하지 않아요.

## syn-sol-0434 — 얼굴 후처리 반응 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ea3f2acf807fc02811f79083d5c688785cc01a7733846354cf40663c09954595`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습 사용 사실과 사용 반응의 미확인을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴 면도 후 보습제를 발라요. 바른 뒤의 반응은 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "보습 사용 사실과 사용 반응의 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 면도 후 보습제를 발라요. 바른 뒤의 반응은 확인되지 않았어요. 보습 사용 사실과 사용 반응의 미확인을 구분해요. [kb:B-M05@0.6.1]

### 근거 및 이유
개인 반응과 실제 보습 여부 중 확인되지 않은 정보는 미상으로 두어요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0435 — 목 면도 뒤 보습 거절 답변

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `aefb92c6a227765fea979ef44b22f31f5a87f71d1945ecd42a6a364bf1dc3807`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

답변 거절을 보습 중단으로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "목을 면도해요. 면도 뒤 보습 여부에 관한 답변은 원하지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "답변 거절을 보습 중단으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
목을 면도해요. 면도 뒤 보습 여부에 관한 답변은 원하지 않아요. 답변 거절을 보습 중단으로 바꾸지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
개인 반응과 실제 보습 여부 중 확인되지 않은 정보는 미상으로 두어요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0436 — 동거인의 얼굴 후처리와 본인의 목 보습

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `9efe808a72bd3738b68c9a9c1172f46c10a001f94fef33203a223d4ff170d440`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동거인의 얼굴 제품 반응을 본인의 목 면도 후 반응으로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "본인은 목을 면도해요. 목 면도 후의 보습 사용 여부와 반응은 확인되지 않았어요. 동거인은 별도로 얼굴 면도 후 사용한 후처리 제품이 따갑다고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-M05",
      "status": "unknown",
      "guidance": "동거인의 얼굴 제품 반응을 본인의 목 면도 후 반응으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S25",
      "text": "일반적인 피부 관리 안내는 면도 후 보습을 다뤄요. 자극이 우려될 때는 무향료 제품 선택도 설명해요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-for-men",
      "locator": "면도 후 보습, 자극에 민감할 때 무향료 제품 선택, 면도 방법.",
      "checked_on": "2026-11-04",
      "limitations": "기본 면도 모듈은 성별 대신 실제 면도행위로 활성화하는 서비스 설계다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-M05@0.6.1",
    "ref:S25"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인은 목을 면도해요. 목 면도 후의 보습 사용 여부와 반응은 확인되지 않았어요. 동거인은 별도로 얼굴 면도 후 사용한 후처리 제품이 따갑다고 해요. 동거인의 얼굴 제품 반응을 본인의 목 면도 후 반응으로 옮기지 않아요. [kb:B-M05@0.6.1]

### 근거 및 이유
개인 반응과 실제 보습 여부 중 확인되지 않은 정보는 미상으로 두어요. [kb:B-M05@0.6.1] 일반 피부 관리 안내는 면도 후 보습을 다뤄요. [ref:S25]

### 확인이 필요한 한계
한 제품의 반응을 모든 제품이나 면도 자체의 원인으로 확대하지 않아요.

## syn-sol-0442 — 레티놀과 AHA 접촉 부위 미상

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `800a8cd512f469e123f267309763a45c6cf3ffd87c9d84ad8b1e7d46a27b8ee2`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 부위에 접촉하는지 미상으로 남겨요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 각각 바르는 부위는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "같은 부위에 접촉하는지 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
레티놀 관리 화장품과 AHA 각질관리 화장품을 별도 제품으로 같은 기간에 사용해요. 각각 바르는 부위는 확인하지 못했어요. 같은 부위에 접촉하는지 미상으로 남겨요. [kb:B-G13@0.6.1]

### 근거 및 이유
같은 부위, 관리 목적, 성분 또는 개별 진료 계획 중 확인되지 않은 정보는 미상으로 두어요. 처방약은 임의로 변경하지 않아요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0443 — AHA 포함만 확인된 제품

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `99abe3256fd6f88fa501b2912139d657ea02c12569e2b74ea15e714f120e7d2e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

성분 포함과 각질관리 목적을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 레티놀 관리 제품과 별도 화장품을 같은 기간에 사용해요. 별도 화장품에는 AHA 성분이 있지만 각질관리 목적인지는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "성분 포함과 각질관리 목적을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 레티놀 관리 제품과 별도 화장품을 같은 기간에 사용해요. 별도 화장품에는 AHA 성분이 있지만 각질관리 목적인지는 몰라요. 성분 포함과 각질관리 목적을 구분해요. [kb:B-G13@0.6.1]

### 근거 및 이유
같은 부위, 관리 목적, 성분 또는 개별 진료 계획 중 확인되지 않은 정보는 미상으로 두어요. 처방약은 임의로 변경하지 않아요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0444 — 관리 목적만 알려진 제품

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c47f0d553bb22d0c5812aada624199a1b9e266fc3df7d0717f0357cc52f163f3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

카드 전체 제목은 레티노이드와 AHA 중첩이며 combination_pair는 retinoid와 aha_exfoliating이에요. 관리 목적은 확인됐지만 AHA 해당 여부는 미확인이므로 이 특정 조합의 판정은 미상이에요. 앞선 범위 의문과 차이 판정은 카드 전체의 제한 조건을 반영해 정정해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 레티놀 관리 제품과 별도 각질관리 제품을 같은 기간에 사용해요. 각질관리 제품의 성분은 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "각질관리 제품의 AHA 해당 여부가 미확인이므로 레티노이드와 AHA 특정 조합의 개별 판정은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 별도 레티놀 관리 제품과 각질관리 제품을 사용하는 목적은 확인됐지만, 각질관리 제품이 AHA에 해당하는지는 미확인이에요. 따라서 이 레티노이드와 AHA 특정 조합의 개별 판정은 미상이에요. [kb:B-G13@0.6.1]

### 근거 및 이유
관리 목적과 성분 확인은 서로 달라요. 일반 각질관리 자료는 레티놀 사용 중 추가 각질관리에 주의를 안내하지만, 이 제품의 AHA 함유 여부를 확인해 주지는 않아요. [ref:S32]

### 확인이 필요한 한계
제품 성분과 필요한 자료를 확인하기 전에는 AHA를 포함한다고 단정하지 않아요. 이 정보만으로 개인별 안전성이나 위해 확률을 확정하거나 처방을 자동 변경하지 않아요.

## syn-sol-0447 — 처방 레티노이드와 AHA의 계획

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `fdb76c420400cb9477b3acd66f12704bd865d44c6bc00e57aecb0bb72bcb29ed`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

처방 여부와 미확인 병용 지시를 구분하고 처방을 임의 변경하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "얼굴에 처방 레티노이드와 별도 AHA 각질관리 화장품을 같은 기간 사용해요. 의료진의 병용 지시 여부는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G13",
      "status": "unknown",
      "guidance": "처방 여부와 미확인 병용 지시를 구분하고 처방을 임의 변경하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S32",
      "text": "일반 각질관리 안내는 레티놀이나 처방 레티노이드를 사용하는 중 각질제거를 추가할 때 주의를 권해요. 모든 조합의 개인별 위해 확률을 제시하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-secrets/routine/safely-exfoliate-at-home",
      "locator": "레티놀/처방 레티노이드 사용 중 추가 각질제거 주의, 과도한 각질관리 회피",
      "checked_on": "2026-11-05",
      "limitations": "모든 성분 조합의 절대 금기나 개인 위험확률 근거는 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G13@0.6.1",
    "ref:S32"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 처방 레티노이드와 별도 AHA 각질관리 화장품을 같은 기간 사용해요. 의료진의 병용 지시 여부는 아직 확인하지 못했어요. 처방 여부와 미확인 병용 지시를 구분하고 처방을 임의 변경하지 않아요. [kb:B-G13@0.6.1]

### 근거 및 이유
같은 부위, 관리 목적, 성분 또는 개별 진료 계획 중 확인되지 않은 정보는 미상으로 두어요. 처방약은 임의로 변경하지 않아요. [kb:B-G13@0.6.1] 일반 각질관리 자료는 레티놀이나 처방 레티노이드 사용 중 각질제거 추가에 주의를 권해요. [ref:S32]

### 확인이 필요한 한계
이는 보수적인 서비스 기본값이지 절대 금기나 개인의 위해 확률을 확정한 것은 아니에요.

## syn-sol-0448 — 접힌 사진의 광범위 표시

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `da195eed2ee37fb78a12500bfa6ddafa3a4703c1280e8080d2c934a57ca94acc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

광범위 보호 표시가 가려져 있어 이 항목은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 자외선차단제의 SPF 30과 내수성 표시는 읽히지만 접힌 사진 때문에 광범위 표시는 보이지 않아요. 내일 야외 걷기에 쓸 새 후보를 고르고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "광범위 보호 표시가 가려져 있어 이 항목은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
광범위 보호 표시가 가려져 있어 이 항목은 미상이에요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0450 — 용기와 판매 정보의 버전 연결

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d8dfca3b82992e34c9348a1ad8d6026422695425c06f5af49a320144ccdab985`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

판매 페이지와 용기의 버전 연결 및 용기의 내수성은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 등산용 합성 자외선차단제 용기에는 SPF 30과 광범위 보호가 표시돼요. 판매 페이지에는 SPF 50이 적혔지만 같은 버전인지는 모르고 용기 내수성 표시도 읽지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "판매 페이지와 용기의 버전 연결 및 용기의 내수성은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
판매 페이지와 용기의 버전 연결 및 용기의 내수성은 미상이에요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0451 — 두 후보의 서로 다른 누락

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a8ed5068996ba1995ba710feda978e55d5b88a009d0fe4961184cf718dee2cb9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 내수성과 나의 SPF·광범위 표시는 각각 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 물놀이용 합성 자외선차단제 가는 SPF 30과 광범위 표시가 보이지만 내수성 표시는 가려져 있어요. 나의 내수성 표시는 보이지만 SPF와 광범위 표시는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "가의 내수성과 나의 SPF·광범위 표시는 각각 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
가의 내수성과 나의 SPF·광범위 표시는 각각 미상이에요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0452 — 내수성의 가려진 부분

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `6fa560453b0b5b5e8f0077507b2eac29e9b976331e10b23c73b4aca250251ffc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가려진 내수성 표시는 없다고 단정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 산책용 합성 자외선차단제의 SPF 50과 광범위 표시는 보이나 내수성 문구는 포장 접힌 부분에 가려졌어요. 아직 제품을 선택하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "가려진 내수성 표시는 없다고 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
가려진 내수성 표시는 없다고 단정하지 않아요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0453 — 이전 용기와 현재 후보

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `da1b615dfd0d6623ed119a50af39c7a1c45de27cd6a39dea5eb14de9072b7284`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 용기의 수치를 현재 후보에 자동 적용할 수 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 자전거 타기에 쓸 합성 자외선차단제 후보의 현재 용기 표시가 닳아 SPF를 읽지 못해요. 같은 이름의 예전 용기에는 SPF 50이 있지만 두 버전의 일치 여부는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "이전 용기의 수치를 현재 후보에 자동 적용할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 용기의 수치를 현재 후보에 자동 적용할 수 없어요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0454 — 수영 후보의 한 항목만 확인

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `222210659dd500dec72e4be2f0e5141e926e3899bdbeb4b479c7aa52ac7e73ef`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인한 내수성과 미확인 SPF·광범위 보호를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 수영을 위해 새 합성 자외선차단제를 고르고 있어요. 후보 용기에 내수성은 표시됐지만 SPF와 광범위 보호 표시를 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P01",
      "status": "unknown",
      "guidance": "확인한 내수성과 미확인 SPF·광범위 보호를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S16",
      "text": "General sun-protection guidance recommends broad-spectrum, water-resistant sunscreen with SPF 30 or higher for outdoor use. Product labeling should be checked for the relevant characteristics.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/media/stats-sunscreen",
      "locator": "What sunscreen should I use? / How much sunscreen should I use, and how often should I apply it?",
      "checked_on": "2026-11-04",
      "limitations": "미국 전문기관 안내로부터 서비스 기준 후보를 작성. 한국 법적 최소치나 모든 실내 상황의 일률적 재도포 규칙이 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-P01@0.6.1",
    "ref:S16"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인한 내수성과 미확인 SPF·광범위 보호를 구분해요. [kb:B-P01@0.6.1]

### 근거 및 이유
야외용 선택에 관한 일반 안내는 SPF 30 이상, 광범위 보호와 내수성 표시를 함께 확인하도록 권해요 [ref:S16].

### 확인이 필요한 한계
확인되지 않은 표시와 다른 버전의 기록은 현재 후보의 성능으로 대체하지 않아요. 표시만으로 실제 개인 보호 수준이나 제품의 전반적인 안전성을 보증할 수 없어요.

## syn-sol-0457 — 전날 보습제 기록과 오늘 얼굴 차단제

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ed30592196d39341d0c500523dd340ce6c8f136fb26498132b8f02255fdea69a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

보습제의 어제 사용량으로 오늘 자외선차단제의 양을 판단하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "어제 저녁 합성 보습제는 소량 사용했어요. 오늘 야외에서 얼굴에 합성 자외선차단제를 바른 것은 기억하지만 그 도포량은 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "보습제의 어제 사용량으로 오늘 자외선차단제의 양을 판단하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
보습제의 어제 사용량으로 오늘 자외선차단제의 양을 판단하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0460 — 예정된 도포와 실제 기록

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `a0d1d96fe49e0b215d6af3e903bff31c55bb969d64583e90e4ea7e27e278b46f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

계획을 실제 도포 기록으로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "내일 야외에서 합성 자외선차단제를 고르게 바를 계획이에요. 오늘 야외에서 실제로 바른 부위와 양은 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "계획을 실제 도포 기록으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
계획을 실제 도포 기록으로 바꾸지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0461 — 새 용기 펌프 양 미확인

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `c24ff17c501e21888cb0dd0e90753bb1c5fff0b08dd5d26e86fc4a8b1b034291`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

예전 펌프 기록만으로 새 펌프의 양이나 도포 범위를 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 쓴 합성 자외선차단제의 예전 용기 한 펌프 양은 기록돼 있어요. 새 펌프의 토출량과 실제 도포 부위는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "예전 펌프 기록만으로 새 펌프의 양이나 도포 범위를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
예전 펌프 기록만으로 새 펌프의 양이나 도포 범위를 확정하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0462 — 땀과 도포의 순서 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `cab396b1c013d1d19112f9b2ba687fa4f46618f1694335c7c9f9ccc500aba3a3`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

발한과 재도포의 순서를 확인할 수 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 운동 중 합성 자외선차단제를 발랐고 땀도 났어요. 땀이 난 때와 다시 바른 때의 순서는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "발한과 재도포의 순서를 확인할 수 없어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
발한과 재도포의 순서를 확인할 수 없어요. [kb:B-P03@0.6.1]

### 근거 및 이유
실제 야외 활동과 기록된 행동의 시점을 구분해서 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0463 — 알림과 실행 구분

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `38e7a1837a517a906bd01e8f33b3dba1b8fb7585225dbb4a91310f5069dada94`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

알림은 실제 재도포 기록이 아니에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에 머무르며 합성 자외선차단제 재도포 알림을 받았어요. 실제로 다시 발랐는지는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림은 실제 재도포 기록이 아니에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
알림은 실제 재도포 기록이 아니에요. [kb:B-P03@0.6.1]

### 근거 및 이유
실제 야외 활동과 기록된 행동의 시점을 구분해서 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0464 — 발한 후 예정된 재도포

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `78f91f7ee93b2b79b5325c9cc5e578f4bc67907ee5dae388bd4dfff6c351085d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

계획과 실제 재도포 여부를 구별해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 운동 중 합성 자외선차단제를 사용한 뒤 땀이 났고 야외 활동은 계속돼요. 다시 바를 계획은 있지만 실행 여부는 아직 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "계획과 실제 재도포 여부를 구별해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
계획과 실제 재도포 여부를 구별해요. [kb:B-P03@0.6.1]

### 근거 및 이유
실제 야외 활동과 기록된 행동의 시점을 구분해서 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0465 — 긴소매 이외의 보호 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `ab04071b2e3c9eebb873878e2dcb8f5bf394a5a349fee58dc0ef1f70805913ad`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

확인된 긴소매와 기록되지 않은 다른 수단을 분리해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 긴소매를 입고 합성 자외선차단제를 사용해요. 모자나 그늘을 이용하는지는 기록되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "확인된 긴소매와 기록되지 않은 다른 수단을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
확인된 긴소매와 기록되지 않은 다른 수단을 분리해요. [kb:B-P04@0.6.1]

### 근거 및 이유
확인된 보호 수단과 아직 확인되지 않은 수단을 구분해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0466 — 야외 산책자의 기록과 친구의 말

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `11f2aa687b5df897f01345ab75a0192476458ee522af70cc7cc707d0e44281b9`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 행동을 본인의 도포량으로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 산책에서 본인은 합성 자외선차단제를 썼지만 양과 도포 부위는 기억하지 못해요. 친구는 같은 날 자신의 차단제를 극소량 썼다고 말했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "친구의 행동을 본인의 도포량으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 행동을 본인의 도포량으로 옮기지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0468 — 야외 체류 중 재도포 알림

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `6076a0853265d039380a5b1fc2d36f65d99d0b0d6cbced1cf910cce8003af14d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

알림을 받은 사실과 실제 재도포 여부를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "오늘 야외에 머무르며 합성 자외선차단제를 처음 바른 뒤 재도포 알림을 받았어요. 알림 이후 실제로 다시 발랐는지는 기억하지 못해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림을 받은 사실과 실제 재도포 여부를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
알림을 받은 사실과 실제 재도포 여부를 구분해요. [kb:B-P03@0.6.1]

### 근거 및 이유
실제 야외 활동과 기록된 행동의 시점을 구분해서 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0469 — 모자의 사용과 선제품 양

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `19bf27f7e6f7ca2da409321fba7f7c378b7c4dee27f05efcef45765cf65120c1`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

모자 착용만으로 도포량이나 귀 도포를 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 모자를 착용하고 합성 자외선차단제를 썼어요. 도포량과 귀에 발랐는지는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P02",
      "status": "unknown",
      "guidance": "모자 착용만으로 도포량이나 귀 도포를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
모자 착용만으로 도포량이나 귀 도포를 확정하지 않아요. [kb:B-P02@0.6.1]

### 근거 및 이유
제품 표시의 사용 범위와 실제 노출 부위를 함께 확인해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0470 — 그늘과 다른 수단 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `a08dfaedd8a21a55ad3976567026a9921b13c4f68b4e2f92f56ebda76d4e9656`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

그늘 이용과 다른 보호 수단의 미확인을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외에서 그늘을 이용한 사실은 기억해요. 합성 자외선차단제 사용과 의복의 범위는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P04",
      "status": "unknown",
      "guidance": "그늘 이용과 다른 보호 수단의 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
그늘 이용과 다른 보호 수단의 미확인을 구분해요. [kb:B-P04@0.6.1]

### 근거 및 이유
확인된 보호 수단과 아직 확인되지 않은 수단을 구분해요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0471 — 알림 해제와 실행 미상

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `e9a1bbc163d30e25570e28a76570fd5f67749dafc420db6b86ed9f77e49a6616`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

알림 해제는 도포 실행을 증명하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "야외 활동 중 합성 자외선차단제 재도포 알림을 껐어요. 알림을 끈 뒤 실제 도포했는지는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-P03",
      "status": "unknown",
      "guidance": "알림 해제는 도포 실행을 증명하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-P03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
알림 해제는 도포 실행을 증명하지 않아요. [kb:B-P03@0.6.1]

### 근거 및 이유
실제 야외 활동과 기록된 행동의 시점을 구분해서 살펴요.

### 확인이 필요한 한계
기록되지 않은 행동은 했거나 하지 않았다고 단정하지 않아요. 이 정보만으로 개인의 실제 보호 수준은 계산할 수 없어요.

## syn-sol-0474 — 친구 용기와 본인 용기

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `ebebe5b0a147b8c7f145eb1d58ba21ac3eadba6bd2b9e1dad39cf4487feff771`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 보관 이력을 본인 제품에 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "친구의 합성 화장품 용기는 뜨거운 차에 있었어요. 본인 용기의 과거 운송 온도는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "친구의 보관 이력을 본인 제품에 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 보관 이력을 본인 제품에 옮기지 않아요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0476 — 배송 중 온도와 현재 위치

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `5bec4701445719f80debc9aca0c757f2f9d85cc7caa30fb7491c798ac03eb84f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 보관과 미확인 배송 온도를 구별해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 배송 중 온도는 몰라요. 지금은 뚜껑을 닫고 직사광선이 없는 곳에 두고 있어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 보관과 미확인 배송 온도를 구별해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 보관과 미확인 배송 온도를 구별해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0477 — 가려진 지침과 보관 이력

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1eb64dd868997d2c003a29c3533ebdaf2b8d5c1faa85a8cf6061059071c3a943`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가려진 표시와 운반 이력은 미상으로 남겨요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 보관 표시가 가려져 읽히지 않아요. 운반 중 열에 노출됐는지도 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "가려진 표시와 운반 이력은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가려진 표시와 운반 이력은 미상으로 남겨요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0478 — 현재 서랍과 과거 노출

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `7341abb851aaee73a25cf9639009d0b3c1324de6902da9c9e8041507d523dc5d`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 서랍 보관이 과거 노출 여부를 증명하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 지금은 서랍에 닫아 보관해요. 지난 여행 중 뜨거운 차에 둔 적이 있는지는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 서랍 보관이 과거 노출 여부를 증명하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 서랍 보관이 과거 노출 여부를 증명하지 않아요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0480 — 현재 밀봉과 열 이력

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `3f8e4f82413cccac8e9c16e23b176035a31066eb1f652ce9110ba8f879759659`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 닫힌 상태로 과거 이력이나 표시를 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 용기는 지금 닫혀 있어요. 과거에 직사광선에 놓였는지와 보관 표시 내용은 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 닫힌 상태로 과거 이력이나 표시를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S06",
      "text": "Cosmetic shelf-life guidance discusses temperature, light, air, microorganisms, handling and packaging. Product-specific stability cannot be certified from a reported storage event alone. The guidance does not provide one expiry period for all cosmetics or a numerical degradation rate for an individual product.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1",
    "ref:S06"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 닫힌 상태로 과거 이력이나 표시를 추정하지 않아요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요. 화장품 보관 자료는 온도·빛·공기와 취급이 품질에 관련될 수 있다고 설명하지만 개별 제품의 안정성을 인증하지는 않아요 [ref:S06].

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0482 — 두 용기의 개봉일

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `37d94a852bd751a58ca292d15955d2e0734e405380508e2adedfd30165a4f551`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 날짜와 나의 미확인 개봉일을 분리해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품 가는 지난달 개봉했어요. 나의 개봉일은 모르며 가의 날짜를 나에게 적용하려고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 날짜와 나의 미확인 개봉일을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가의 날짜와 나의 미확인 개봉일을 분리해요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0483 — 기한과 개봉 후 기간

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `b7b75aea70de53fdf9ee401545fd719cc0a667282dc0cbe92ad0c7436b606b18`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

인쇄 기한으로 미확인 개봉 후 기간을 대신하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 기한은 읽혔지만 개봉 날짜와 개봉 후 사용기간 표시는 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "인쇄 기한으로 미확인 개봉 후 기간을 대신하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
인쇄 기한으로 미확인 개봉 후 기간을 대신하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0484 — 개봉일과 표시 가림

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `1eeb5200dde2c9ff095fd79eaa80fa340cc965e5211d164bd0f02c66f5e1afd8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

알려진 개봉일과 가려진 사용기간 표시를 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 개봉일은 기록했지만 개봉 후 사용기간 표시는 가려져 있어요. 표시기한은 아직 확인하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "알려진 개봉일과 가려진 사용기간 표시를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
알려진 개봉일과 가려진 사용기간 표시를 구분해요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0485 — 구매일과 개봉일

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `b808995c897944c1be4d4e977e1edfb447e730c6cc841f13f386059f5bb25b22`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

구매일을 개봉일로 바꾸지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 구매일은 알지만 개봉일은 기록하지 않았어요. 구매일부터 개봉 후 기간을 계산하려고 해요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "구매일을 개봉일로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
구매일을 개봉일로 바꾸지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0486 — 빈 용기와 새 용기

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `73f0cfa8786b5509b0649020ff3f6de630372990d31428b69ba0d194604bbdf5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

이전 용기의 개봉일을 새 용기에 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "이전에 다 쓴 합성 화장품 용기의 개봉 날짜는 알아요. 새로 산 같은 이름의 용기 개봉 날짜는 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "이전 용기의 개봉일을 새 용기에 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 용기의 개봉일을 새 용기에 적용하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0487 — 개봉 전 상태 미확인

- 유형·분할: `unknown_or_version` / `solution` / `val_internal`
- 내용 해시: `64539cd189e78f9f80379f6d20b593b56903cfcde63de4e33523b7e621e1eee4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기억나지 않는 개봉 여부를 미개봉으로 단정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품을 산 날짜와 표시 기한은 보이지만 실제 개봉 여부는 기억나지 않아요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "기억나지 않는 개봉 여부를 미개봉으로 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
기억나지 않는 개봉 여부를 미개봉으로 단정하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0488 — 타인의 개봉 기록

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `76cf5284adbb25f0fd63078e5952b759202705e7c7f86725225a1ec421f5dd9e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

친구의 개봉일은 본인 용기의 기록이 아니에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "친구가 같은 이름의 합성 화장품을 지난주 개봉했다고 말했어요. 본인 용기의 개봉일은 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "친구의 개봉일은 본인 용기의 기록이 아니에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
친구의 개봉일은 본인 용기의 기록이 아니에요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0489 — 다른 나라 용기의 날짜

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `d1dd98b8a53b5ef93d6ecb801628466f863d43caa038d670cdeac1977fda8d97`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

해외 용기의 기한을 현재 보유품에 자동으로 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 가의 해외 용기에 기한이 적혀 있어요. 국내에서 보유한 나의 표시와 두 버전의 일치는 아직 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "해외 용기의 기한을 현재 보유품에 자동으로 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
해외 용기의 기한을 현재 보유품에 자동으로 옮기지 않아요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0490 — 용량 다른 두 용기

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `88a6ff82c132585de2279c9bd5c18318c21b6cf080aeb12e873bbc7b7900bd98`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

대용량 지침과 소용량 보유품의 버전 연결은 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품 대용량 용기에 보관 지침이 보여요. 소용량 보유품이 같은 버전인지 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "대용량 지침과 소용량 보유품의 버전 연결은 미상이에요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
대용량 지침과 소용량 보유품의 버전 연결은 미상이에요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0491 — 이전 포장과 새 포장

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `4697fee7624d1bf57a13d417568b5301b4f938e47ceddacfd122da2f344d7a99`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

예전 포장 안내를 현재 보유품에 자동 적용하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 이전 포장 사진에는 사용 안내가 보여요. 새 포장 보유품의 버전과 같은지 모르고 현재 표시를 아직 읽지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "예전 포장 안내를 현재 보유품에 자동 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
예전 포장 안내를 현재 보유품에 자동 적용하지 않아요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0492 — 실제 용기와 판매 페이지

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `da6c643321e60dadd1c18c6731179ffa5a72c860de21bd4ddf26e1cb186aac48`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

기록의 차이와 동일 버전 여부 미확인을 구별해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 판매 페이지와 실제 용기에 서로 다른 사용 안내가 있어요. 두 자료가 같은 버전인지 모르겠어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "기록의 차이와 동일 버전 여부 미확인을 구별해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
기록의 차이와 동일 버전 여부 미확인을 구별해요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0493 — 재구매와 성분표

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `cc415b31e553331b89966cc364530f4a0941a9181d83fa7f851c9e82ee67f6dc`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

같은 이름만으로 이전 성분표를 새 제품에 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "같은 이름의 합성 화장품을 재구매했어요. 이전 용기의 성분표만 남아 있고 새 용기의 표시를 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "같은 이름만으로 이전 성분표를 새 제품에 옮기지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
같은 이름만으로 이전 성분표를 새 제품에 옮기지 않아요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0494 — 타 용기의 표시 복사 계획

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `afd41824d419c1f483c75166d587ae2d64002ee8b58dca1198e989b00d73e576`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

계획과 실행을 구분하고 버전 연결은 미상으로 남겨요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "해외에서 산 합성 화장품 용기의 날짜를 국내 보유 용기 기록에 옮길 계획이에요. 아직 옮기지는 않았고 두 용기의 버전 일치는 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "계획과 실행을 구분하고 버전 연결은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
계획과 실행을 구분하고 버전 연결은 미상으로 남겨요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0495 — 인쇄 날짜의 일부 가림

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `c15b787d54d0230863cc8de6de543f2d4c02eb45117c94f29cd1f1a6b0aceb4e`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

날짜의 보이는 부분만으로 기한 경과를 확정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 인쇄 날짜 중 연도가 가려져 있어요. 개봉일도 기록하지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "날짜의 보이는 부분만으로 기한 경과를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
날짜의 보이는 부분만으로 기한 경과를 확정하지 않아요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0496 — 두 용기의 구매 이력

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `65a4e38d070b299a4f016a2bacc45fcb1da95bf4742b3e564c121f4d32a4ea58`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가의 구매일과 두 용기의 미확인 개봉일을 분리해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 가의 구매일은 알지만 나의 구매일은 몰라요. 두 용기의 개봉일도 확인하지 못했어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S02",
      "status": "unknown",
      "guidance": "가의 구매일과 두 용기의 미확인 개봉일을 분리해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가의 구매일과 두 용기의 미확인 개봉일을 분리해요. [kb:B-S02@0.6.1]

### 근거 및 이유
표시기한과 실제 개봉 이력은 각각 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0497 — 보관 지침과 옛 사진

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `92c4227b87e7e354fbef526448105bd6549e62e24ff859c84f3dc5ddcebd886a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 닫힌 상태와 옛 보관 지침의 버전 미확인을 구분해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품의 현재 용기는 닫혀 있어요. 예전 포장 사진의 보관 문구가 현재 버전에 적용되는지 몰라요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-S01",
      "status": "unknown",
      "guidance": "현재 닫힌 상태와 옛 보관 지침의 버전 미확인을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-S01@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 닫힌 상태와 옛 보관 지침의 버전 미확인을 구분해요. [kb:B-S01@0.6.1]

### 근거 및 이유
보관 지침과 열·빛·공기에 대한 노출을 함께 살펴요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0498 — 표시 충돌과 버전 불명

- 유형·분할: `unknown_or_version` / `solution` / `train`
- 내용 해시: `5f245a2bc00d37750c599cae249ba56dcf18bcecc64fed40122f4df094f6556c`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

두 기록의 차이를 남기고 어느 쪽이 현재 버전인지 확인해요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "method.current_routine": {
      "variable_id": "method.current_routine",
      "state": "known",
      "value": "합성 화장품 상자와 판매 페이지에 서로 다른 사용기한이 표시돼 있어요. 같은 버전인지 확인되지 않았어요.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-Q03",
      "status": "unknown",
      "guidance": "두 기록의 차이를 남기고 어느 쪽이 현재 버전인지 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-Q03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
두 기록의 차이를 남기고 어느 쪽이 현재 버전인지 확인해요. [kb:B-Q03@0.6.1]

### 근거 및 이유
실제 보유 용기와 자료의 제품·버전을 맞춰 확인해요.

### 확인이 필요한 한계
기록되지 않은 정보는 확인된 사실로 바꾸지 않아요. 외관이나 과거 보관 기록만으로 개별 제품의 안전성이나 남은 사용기한을 계산할 수 없어요.

## syn-sol-0348 — 본인의 한 번과 동거인의 두 번

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `0117943eb51b079dfb10fbe743970f36448dfbbaba21ecff56961e0874b69664`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

동거인의 행동을 본인에게 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "저녁에 본인은 얼굴을 한 번 씻었고 동거인은 얼굴을 연속 두 번 씻었다고 합니다. 본인은 추가 얼굴 세안을 하지 않았고 첫 세안의 목적은 말하지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "본인의 한 번과 동거인의 반복을 구분하고 본인의 세안 목적은 미상으로 남겨요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인의 한 번과 동거인의 반복을 구분하고 본인의 세안 목적은 미상으로 남겨요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0349 — 헹굼 반복과 세정제 재사용의 차이

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `cfbc44f3d83b3a4ea173d273e378b90ab20656d4a8b7de773ae8a061b32afa18`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

세정제 재사용이 명시적으로 부정돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 일반 헹굼형 세정제를 한 번만 사용하고 물로 여러 차례 헹궜습니다. 세정제를 다시 바르지는 않았고 첫 사용의 목적은 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C05",
      "status": "unknown",
      "guidance": "여러 차례 물로 헹군 사실을 세정제의 반복 사용으로 바꾸지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C05@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
여러 차례 물로 헹군 사실을 세정제의 반복 사용으로 바꾸지 않아요. [kb:B-C05@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0350 — 얼굴 수건 압력과 다른 부위의 강한 문지름

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `0a3a0e3270634998205b3e41dfac43d2c92951c56b061ca9899ccf1eef3b20d4`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 부위의 마찰을 얼굴에 귀속하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴은 손가락으로 부드럽게 씻고 수건으로 가볍게 눌러 말립니다. 팔만 거친 수건으로 강하게 문지릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C02",
      "status": "aligned",
      "guidance": "얼굴의 부드러운 세안과 가벼운 건조를 팔의 마찰과 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C02@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴의 부드러운 세안과 가벼운 건조를 팔의 마찰과 구분해요. [kb:B-C02@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0353 — 손 씻는 물은 뜨겁지만 얼굴 물은 미온

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `f0ae3f04e0c414218c9b001cb058eefa04dda7187e66308c5a83d550b0afcb43`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴의 미온수 사용이 확인됐어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "손을 씻는 물은 뜨겁게 느껴졌고 일상 얼굴 세안 물은 뜨겁지 않은 미온수였습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "aligned",
      "guidance": "손과 얼굴의 물 온도 경험을 구분하고 확인된 얼굴 세안의 미온수를 유지할 수 있어요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "General face-washing guidance discusses gentle cleansing and rinsing. It does not establish an individual outcome.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
손과 얼굴의 물 온도 경험을 구분하고 확인된 얼굴 세안의 미온수를 유지할 수 있어요. [kb:B-C01@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0354 — 얼굴 세안 물과 샤워 물의 차이

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `f83239095054b1f76380e7bcbe0d28bf8156bc181981bc90009d841ce70b653b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

얼굴에 사용한 물의 느낌이 확인됐어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "일상적인 얼굴 세안에 뜨겁게 느껴지는 물을 쓰고 몸 샤워에는 미지근한 물을 씁니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C01",
      "status": "difference",
      "guidance": "얼굴에 뜨겁게 느껴지는 물 대신 미온수 사용을 검토해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C01@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴에 뜨겁게 느껴지는 물 대신 미온수 사용을 검토해요. [kb:B-C01@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0358 — 대기 중 손 씻기를 얼굴 문지름으로 오인

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `4a9d4b5be2c1e05e910ff66e748b58031f8d1e883c49ecac89518e51f6277e4a`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

손의 시간은 얼굴 세정 시간의 근거가 아니에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "일반 헹굼형 얼굴 세정제를 부드럽게 사용하고 바로 헹굽니다. 그 뒤 손을 오래 씻지만 얼굴은 더 문지르지 않습니다. 제품에는 별도 접촉시간 지시가 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "aligned",
      "guidance": "얼굴 세정제를 부드럽게 사용한 것과 이후의 손 씻기를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S06",
      "text": "화장품은 열과 빛, 공기에 노출되는 보관 조건에 영향을 받을 수 있어요. 용기와 취급 방식도 품질 관리에서 살펴볼 요소예요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetics-labeling/shelf-life-and-expiration-dating-cosmetics",
      "locator": "What factors affect shelf life, and how? / Steps consumers can take",
      "checked_on": "2026-11-04",
      "limitations": "제품별 안정성 시험을 대체하지 않음. 모든 화장품에 공통 사용기한을 부여하는 근거가 아님."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S06"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 세정제를 부드럽게 사용한 것과 이후의 손 씻기를 구분해요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0360 — 얼굴 세정제와 별도 팩 시간 구분

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `cce99f8b3a234be684eeecfb696770784e01cbfd9b8b72e701fa85cc5f68586f`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

팩 사용 시간을 세정제에 이전하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 헹굼형 일반 세정제는 부드럽게 바로 씻어내고 제품 지시에 따릅니다. 별도의 얼굴 팩은 오래 두지만 세정제와 다른 제품입니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C03",
      "status": "aligned",
      "guidance": "세정제 사용과 별도 팩의 시간을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C03@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
세정제 사용과 별도 팩의 시간을 구분해요. [kb:B-C03@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0363 — 얼굴 세정제와 바디 제품의 헹굼

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `d4e10e5101e2c81c30c6a792fc4e75bc0b0499ad915280cfc95ebf33ea2aded0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

다른 제품의 사용을 얼굴 제품에 이전하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "씻어내는 얼굴 세정제는 표시대로 얼굴에 사용한 뒤 헹궜습니다. 씻어내는 바디 제품은 헹구지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C06",
      "status": "aligned",
      "guidance": "얼굴 제품에서 확인된 헹굼과 바디 제품의 사용을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S03",
      "text": "일반적인 얼굴 세안 안내는 부드러운 세정과 헹굼을 다뤄요. 개인에게 나타날 결과를 확정하지는 않아요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/face-washing-101",
      "locator": "세안 방법 권고",
      "checked_on": "2026-11-04",
      "limitations": "일반 소비자 안내. 특정 온도·60초 절대 제한이나 개인 원인의 입증 자료가 아님."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-C06@0.6.1",
    "ref:S03"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴 제품에서 확인된 헹굼과 바디 제품의 사용을 구분해요. [kb:B-C06@0.6.1]

### 근거 및 이유
일반적인 얼굴 세안 자료는 부드러운 세정과 헹굼을 다루며 개인의 결과를 확정하지 않아요. [ref:S03]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0368 — 얼굴 선크림 제거법을 아직 모름

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `a4537ce7b3dd499ca7e094b001aaab6b593d8836717fac2c8a09822a8b43e428`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사용한 제품의 구체적 제거 정보가 없어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 사용한 선크림을 어떻게 지울지 검토 중입니다. 해당 제품의 제거 지시는 확인하지 못했고 선크림 도포량을 줄이지는 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "unknown",
      "guidance": "제거 지시가 미확인인 채 특정 제거법의 충분성을 단정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    },
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
제거 지시가 미확인인 채 특정 제거법의 충분성을 단정하지 않아요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합의 소규모 비교 결과는 모든 제품의 제거 방법으로 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0370 — 본인의 광보호 유지와 가족의 감량

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `49f68230552a98f5c4a6498ac695760283c51ce213a8e86912a7674b7b02de1b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

타인의 감량을 본인에게 귀속하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "본인은 얼굴 선크림을 표시량대로 바르고 제거법을 검토합니다. 가족은 세안이 번거로워 선크림을 극소량만 바른다고 합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-I01",
      "status": "aligned",
      "guidance": "본인의 광보호 사용 유지와 가족의 행동을 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S08",
      "text": "제한된 제품 조합의 소규모 비교에서 제거 결과는 세정 방법에 따라 달랐어요. 모든 내수성 제품에 특정 단계를 일반화할 수는 없어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://onlinelibrary.wiley.com/doi/10.1111/jocd.12995",
      "locator": "Abstract: Methods / Results / Conclusion",
      "checked_on": "2026-11-04",
      "limitations": "제한된 제품 조합의 영상 기반 잔류 지표. 모든 내수성 제품·오일·밀크·크림으로 일반화하거나 이중세안 필요성을 확정하지 않음. 2019 온라인 공개/2020 권호."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-I01@0.6.1",
    "ref:S08"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인의 광보호 사용 유지와 가족의 행동을 구분해요. [kb:B-I01@0.6.1]

### 근거 및 이유
제한된 제품 조합의 소규모 비교 결과는 모든 제품의 제거 방법으로 일반화할 수 없어요. [ref:S08]

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0371 — 서로 다른 버전의 얼굴 팩 지시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `922e463e1e44d9504d7e861706fff2599d016347df1b234825f37028b4ef64b8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

서로 다른 버전이 명시되고 현재 사용 제품 지시는 미확인이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 실제 사용하는 씻어내는 팩의 용기 버전은 2.0으로 확인했습니다. 보관한 1.0 표시에는 5분 뒤 씻으라고 적혀 있지만 현재 2.0의 사용 시간은 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "unknown",
      "guidance": "현재 2.0 용기에 이전 1.0의 시간을 그대로 적용하지 않고 해당 버전의 표시를 확인해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 사용하는 얼굴 팩은 2.0이고 확인한 5분 표시는 1.0에 관한 내용이에요. 현재 2.0 용기에 이전 1.0의 시간을 그대로 적용하지 않고 해당 버전의 표시를 확인해요. [kb:B-G03@0.6.1]

### 근거 및 이유
확인된 제품이나 기기 버전과 별도 표시, 사용량과 농도를 각각 구분해요. [kb:B-G03@0.6.1]

### 확인이 필요한 한계
2.0의 사용 시간은 아직 확인되지 않았어요.

## syn-sol-0372 — 새 얼굴 세정제의 비공개 pH

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `8e8ddfc10146e8fb9a75884fd96bf2c7c0db95b05e29819a6cb01aa51a157ab5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

새 얼굴 세정제 선택 맥락과 비공개 pH가 확인됐어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "새로 고를 얼굴용 씻어내는 세정제의 합성 성분표는 확인했지만 제품의 pH는 공개되지 않았습니다. 아직 사용하지 않았고 표시만으로 약산성 여부를 알려 달라고 요청합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-C04",
      "status": "unknown",
      "guidance": "성분표만으로 공개되지 않은 pH나 약산성 여부를 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-C04@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이 얼굴 세정제는 아직 사용하지 않았고 pH가 공개되지 않았어요. 성분표만으로 공개되지 않은 pH나 약산성 여부를 확정하지 않아요. [kb:B-C04@0.6.1]

### 근거 및 이유
확인된 제품이나 기기 버전과 별도 표시, 사용량과 농도를 각각 구분해요. [kb:B-C04@0.6.1]

### 확인이 필요한 한계
성분표만으로 실제 pH나 개인에게 얼마나 순할지 알 수 없어요.

## syn-sol-0373 — 용기 크기와 실제 사용량 분리

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `272dce42711b0d5fd4350d696d3bf482f37273182ed057753554ef115c85e6a8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 양이 기록되지 않았어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 로션 두 개의 용기 크기는 다르지만 실제로 얼마나 사용하는지는 기록하지 않았습니다. 이름만으로 용도나 순서를 결정하지도 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G08",
      "status": "unknown",
      "guidance": "용기 크기만으로 실제 사용량이나 순서를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S23",
      "text": "습식 면도 전에는 털을 물에 적시고 준비할 수 있어요. 면도할 때 털이 난 방향을 따르고 날을 헹구는 방법이 안내돼요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/hair/how-to-shave",
      "locator": "습식 면도 준비·털 방향·날 헹굼·5–7회 후 교체 참고·건조 보관.",
      "checked_on": "2026-11-04",
      "limitations": "면도 횟수와 경과 일수는 다르다. 전기면도기 헤드의 교체 주기로 일반화하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G08@0.6.1"
  ],
  "distractor_refs": [
    "ref:S23"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
용기 크기만으로 실제 사용량이나 순서를 추정하지 않아요. [kb:B-G08@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0375 — 세정제 양과 농도 혼동

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `81957259a7ca30f7720d74db672ff18d72ce5a0275c3dc858992bde63ee3c6e0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

농도가 두 배라는 생각은 확인되지만 많이 바르면 좋다는 증량 이유는 확인되지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴에 사용하는 헹굼형 세정제를 두 배로 쓰면 제형의 성분 농도도 두 배가 된다고 생각해 사용량을 늘렸습니다. 농도는 공개되지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "사용량을 두 배로 늘려도 제품 제형의 성분 농도가 두 배가 되는 것은 아니에요. 사용량과 공개되지 않은 농도는 별개로 살펴요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
사용량을 두 배로 늘려도 제품 제형의 성분 농도가 두 배가 되는 것은 아니에요. 사용량과 공개되지 않은 농도는 별개로 살펴요. [kb:B-G02@0.6.1]

### 근거 및 이유
확인된 실제 사용과 표시·지시의 확인 여부를 분리해서 살펴요.

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0376 — 본인의 사용량 검토와 친구의 증량

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `9780d1cf33a701416eef98c42f8fdd805e7d91dacecc5cf291026b4eb767296b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

본인이 사용량 변경을 검토하며 타인의 증량을 본인에게 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "본인은 얼굴용 제품의 현재 표시된 양과 빈도를 따르고 있으며 사용량을 바꿀지 검토합니다. 친구는 얼굴용 제품을 많이 바를수록 좋다고 임의 증량합니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "aligned",
      "guidance": "본인의 표시 사용과 사용량 검토를 친구의 임의 증량과 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
본인의 표시 사용과 사용량 검토를 친구의 임의 증량과 구분해요. [kb:B-G02@0.6.1]

### 근거 및 이유
확인된 실제 사용과 표시·지시의 확인 여부를 분리해서 살펴요.

### 확인이 필요한 한계
확인되지 않은 사용 사실이나 개인의 결과를 추정하지 않아요.

## syn-sol-0377 — 사용량과 성분 농도 미확인

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `0888a1406ac107ea04a8eceb7ad93316be1957c8b46d92bd78f6084b3d67b6c8`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

현재 사용량과 성분 농도가 미확인이므로 차이와 수치를 추정하지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품의 사용량을 줄일지 검토하지만 현재 양과 제품의 성분 농도는 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "현재 사용량과 미확인 농도를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S21",
      "text": "손을 씻은 뒤 손 보습제를 사용할 수 있어요. 손 보습에는 무향료 크림이나 연고를 선택하는 안내가 있어요.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.aad.org/public/everyday-care/skin-care-basics/care/skin-care-tips-hands",
      "locator": "손 씻기 후 보습과 fragrance-free hand cream/ointment 선택에 한정.",
      "checked_on": "2026-11-04",
      "limitations": "다른 문단의 우유/물 담그기 등은 채택하지 않았다. 필요한 손 위생을 줄이라는 뜻이 아니다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": [
    "ref:S21"
  ]
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 사용량과 성분 농도는 미확인이어서 추정하지 않아요. [kb:B-G02@0.6.1]

### 근거 및 이유
사용량과 성분 농도는 서로 다른 정보예요. 현재 사용량과 제품 정보를 확인한 뒤 검토해요.

### 확인이 필요한 한계
농도의 공개 여부와 수치, 개인의 반응은 확인되지 않았어요.

## syn-sol-0378 — 얼굴 로션 사용량과 비공개 농도

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `dc2fa1bbc50f6b4af3d22c13710f8b2aba5f70ef5edec91addfc27cfcfa1aa74`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 얼굴용 로션 사용과 사용량 변경 검토, 비공개 농도가 확인돼요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "현재 얼굴용 로션을 한 번에 두 펌프 사용하고 있으며 사용량을 바꾸려 합니다. 성분 농도는 공개되지 않았고 펌프 수에서 농도를 계산할 수 있는 자료도 없습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G02",
      "status": "unknown",
      "guidance": "사용량 변경과 공개되지 않은 성분 농도를 구분하고 농도 수치를 추정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G02@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
현재 얼굴 로션의 두 펌프 사용과 제품 속 농도는 서로 다른 정보예요. 사용량 변경과 공개되지 않은 성분 농도를 구분하고 농도 수치를 추정하지 않아요. [kb:B-G02@0.6.1]

### 근거 및 이유
확인된 제품이나 기기 버전과 별도 표시, 사용량과 농도를 각각 구분해요. [kb:B-G02@0.6.1]

### 확인이 필요한 한계
펌프 수만으로 비공개 농도나 적합한 사용량을 계산할 수 없어요.

## syn-sol-0381 — 다른 버전의 사용 지시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `ffa5b2a28b5aa2c5b20ff6b7869cdd7816e77afe410ff222c099e9100c06a87b`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

사용 제품의 버전과 표시가 일치하는지 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 헹굼형 팩을 사용했지만 용기의 버전을 확인하지 못했습니다. 웹에서 본 다른 버전의 사용 시간이 이 용기에도 같은지는 모릅니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G03",
      "status": "unknown",
      "guidance": "다른 버전의 지시를 현재 용기에 그대로 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G03@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
다른 버전의 지시를 현재 용기에 그대로 적용하지 않아요. [kb:B-G03@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0385 — 미용기기 버전별 젤 병용 지시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `de157baafbe49ad23ceb32f269d586bd7763715357522c8f9cb5235dc7d95b50`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

실제 얼굴 기기·젤 병용과 서로 다른 기기 버전이 확인되지만 현재 버전 지시는 미상이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기 2.0을 얼굴용 젤과 실제로 함께 사용합니다. 기기 1.0의 합성 표시에는 그 젤과 병용 가능하다고 적혀 있지만 2.0의 병용 지시는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "이전 1.0의 병용 지시를 실제 사용 중인 2.0 기기에 그대로 적용하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
얼굴용 젤과 실제로 쓰는 기기는 2.0이고 확인한 병용 표시는 1.0에 관한 내용이에요. 이전 1.0의 병용 지시를 실제 사용 중인 2.0 기기에 그대로 적용하지 않아요. [kb:B-G06@0.6.1]

### 근거 및 이유
확인된 제품이나 기기 버전과 별도 표시, 사용량과 농도를 각각 구분해요. [kb:B-G06@0.6.1]

### 확인이 필요한 한계
현재 기기 버전의 병용 지시는 확인되지 않았어요.

## syn-sol-0388 — 기기 병용과 제품 버전 미상

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `731bc7b032c7c6bc89f910e49e5796eeb854d1c2db48dec603706c66393915b0`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

버전이 미상이라 일치 여부를 확인하지 못했어요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 미용기기와 얼굴용 젤을 함께 사용했습니다. 사용한 젤의 버전을 몰라 기기에 허용된 젤과 같은지 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G06",
      "status": "unknown",
      "guidance": "실제 병용 사실과 허용된 제품 버전의 일치 여부를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [],
  "allowed_evidence_refs": [
    "kb:B-G06@0.6.1"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
실제 병용 사실과 허용된 제품 버전의 일치 여부를 구분해요. [kb:B-G06@0.6.1]

### 근거 및 이유
제품과 기기의 실제 사용, 확인된 표시와 확인되지 않은 정보를 나누어 살펴봐요.

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0392 — 가족의 알레르기와 본인의 선호

- 유형·분할: `distractor_or_defense` / `solution` / `val_internal`
- 내용 해시: `ee31290eafcaa7ec5b6ff69a0a75ace6b2240017239022a8c8d9ff411d4c88de`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

가족의 병력을 본인에게 옮기지 않아요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "가족은 특정 향료에 알레르기가 있다고 말합니다. 본인은 향 없는 얼굴용 제품을 선호하지만 본인 알레르기 여부는 알려지지 않았습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "가족의 알레르기와 본인의 향 선호를 구분해요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
가족의 알레르기와 본인의 향 선호를 구분해요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.

## syn-sol-0394 — 현재 제품과 다른 버전의 향료 표시

- 유형·분할: `distractor_or_defense` / `solution` / `train`
- 내용 해시: `c2854b76746d7b0232512d981a556b67239ffd2e807f312b00c92ba7812d9df5`
- 사람 검수: **미검수**

### 설계한 판정 근거 — 엔진 실행 결과가 아닙니다

해당 용기의 버전이 미확인이에요.

### 입력

```json
{
  "mode": "solution",
  "confirmed_observations": {
    "constraints.decision_context": {
      "variable_id": "constraints.decision_context",
      "state": "known",
      "value": "얼굴용 제품을 고르는 중 같은 이름의 이전 버전 성분표에서 향료명을 봤습니다. 손에 든 현재 용기의 버전과 성분표는 확인하지 못했습니다.",
      "source": "synthetic_fixture",
      "confirmed_by_user": true
    }
  },
  "kb_judgments": [
    {
      "card_id": "B-G17",
      "status": "unknown",
      "guidance": "이전 성분표의 표시를 현재 용기의 성분으로 확정하지 않아요."
    }
  ],
  "product_evidence": [],
  "rag_chunks": [
    {
      "evidence_ref": "ref:S15",
      "text": "Cosmetic fragrance ingredients and allergens are discussed in labeling guidance. A label alone does not establish an individual allergic reaction.",
      "scope": "general_skincare_practice",
      "source_url": "https://www.fda.gov/cosmetics/cosmetic-ingredients/allergens-cosmetics",
      "locator": "Common Allergens / What Consumers Can Do",
      "checked_on": "2026-11-04",
      "limitations": "향료 포함을 모든 사람의 자극·알레르기 발생으로 단정하지 않는다. 미국 표시 관련 설명을 한국 법으로 전환하지 않는다."
    }
  ],
  "allowed_evidence_refs": [
    "kb:B-G17@0.6.1",
    "ref:S15"
  ],
  "distractor_refs": []
}
```

### 응답 초안 — 미승인

### 핵심 안내
이전 성분표의 표시를 현재 용기의 성분으로 확정하지 않아요. [kb:B-G17@0.6.1]

### 근거 및 이유
향료와 알레르겐에 대한 일반 자료는 표시와 개인별 회피를 다루지만 개인의 알레르기 반응을 확정하지 않아요. [ref:S15]

### 확인이 필요한 한계
확인되지 않은 성분 농도나 개인의 반응은 추정하지 않아요.
