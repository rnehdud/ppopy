# PPO-37 24턴 파일럿 입력 구성 — 개정 6, 미검수

기준 커밋: `53a74a013e2e3533c33ec66d3ed80e0a8ce10bc1`. 합성 개발용이며 `production_enabled=false`입니다.

초판에서는 관찰·판정·허용 근거를 응답 조립 전에 고정했습니다. 이후 내부 검토에 따른 입력 수정은 이전 버전, 사유와 해시를 보관한 뒤 다시 조립했습니다.
판정은 KB 비교 명세에 따른 작성자의 설계이며 엔진 실행 결과, 전문가 정답이나 사람의 승인이 아닙니다.

생성 모델: `gpt-6.1-sol`. 같은 계열의 Codex 내부 검토는 다른 모델 계열의 공식 검수와 구분합니다. 사람의 24턴 전수 검수와 팀 확인 전에 900턴으로 진행하지 않습니다.

| ID | 유형 | 사례 | 분할 | 계보 |
|---|---|---|---|---|
| syn-sol-0001 | normal_guidance | 미온수 사용을 확인한 기존 관찰 유지 | train | luna-v3-train-013-t02 |
| syn-sol-0002 | normal_guidance | 선크림 제거 표시와 실제 폼 세안을 대조 | train | new_synthetic |
| syn-sol-0003 | normal_guidance | 보습이 필요한 맥락의 세정 후 시점 | train | new_synthetic |
| syn-sol-0004 | normal_guidance | 보습제와 선크림을 각각 바르는 편안한 중첩 | val_internal | new_synthetic |
| syn-sol-0005 | normal_guidance | 야외 활동과 땀 이후 재도포 누락 | train | new_synthetic |
| syn-sol-0006 | normal_guidance | 별도 레티놀과 AHA 화장품의 동일 부위 중첩 | train | new_synthetic |
| syn-hold-0001 | hold | 지속되는 불편감의 안전 범위 | train | luna-v3-train-025-t01 |
| syn-hold-0002 | hold | 반복 불편감과 명시된 통증 | train | new_synthetic |
| syn-hold-0003 | hold | 새로운 색·냄새 변화 | train | new_synthetic |
| syn-hold-0004 | hold | 배송 누수와 열린 봉인 | train | luna-v3-train-041-t01 |
| syn-hold-0005 | hold | 기존 진료 계획과 일반 보습 지침 충돌 | val_internal | new_synthetic |
| syn-hold-0006 | hold | 이전과 다른 갑작스러운 층 분리 | train | new_synthetic |
| syn-sol-0007 | unknown_or_version | 세정제 pH 미공개 | train | new_synthetic |
| syn-sol-0008 | unknown_or_version | 선제품 구버전 표시를 현 버전에 이식하지 않기 | train | new_synthetic |
| syn-sol-0009 | unknown_or_version | 사용기한과 개봉일 미확인 | train | new_synthetic |
| syn-sol-0010 | unknown_or_version | 처방 레티노이드와 살리실산 제품의 관리 목적 미확인 | train | new_synthetic |
| syn-sol-0011 | unknown_or_version | 새 제품의 국소 사용 확인 결과와 용법 미확인 | train | new_synthetic |
| syn-sol-0012 | unknown_or_version | AHA와 BHA가 별도 제품인지 복합 완제품인지 미확인 | train | new_synthetic |
| syn-sol-0013 | distractor_or_defense | 세안 온도와 무관한 손 보습 청크 무시 | train | new_synthetic |
| syn-sol-0014 | distractor_or_defense | 처방 트레티노인과 추가 살리실산 각질관리의 경계 | train | new_synthetic |
| syn-sol-0015 | distractor_or_defense | 새 향료 포함 후보와 개인 알레르기 판단의 구분 | train | new_synthetic |
| syn-sol-0016 | distractor_or_defense | 눈 노출 부정과 응급 세척 정보의 적용 범위 | train | new_synthetic |
| syn-sol-0017 | distractor_or_defense | 귀 도포 누락에 무관한 지시 무시 | train | new_synthetic |
| syn-sol-0018 | distractor_or_defense | 성분 목록에서 pH를 만들어 내는 문장 거부 | train | new_synthetic |

행별 확정 관찰·KB 판정·허용 근거·입력 해시는 `pilot_24_plan.json`에 있습니다.

v67 재가공 3턴은 원본 관찰·분할·그룹·계보를 유지합니다. 신규 합성 21턴 중 2턴은 검증용입니다. 개발용 분할이며 독립 최종 평가가 아닙니다.

## 입력 설계 수정 이력

- 개정 2: `syn-sol-0014`의 정성적 시간 설명을 수치 필드에서 분리하고 분 단위 시간은 미확인으로 유지했습니다.
- 개정 3: `syn-sol-0006`의 생각과 `syn-sol-0017`의 의도를 신규 합성 사례의 입력 설정에 명시했습니다. 실제 사용자의 알려지지 않은 의도를 추측한 것이 아닙니다.
- 개정 4: `syn-sol-0013`부터 `syn-sol-0018`까지 방해 청크와 KB 안내의 메타 힌트를 제거했습니다. 관찰·KB 상태·분류·근거 ID·출처 정보·계보·분할·응답은 유지하고 입력과 검수 해시는 다시 계산했습니다. 변경된 6턴은 재검수가 필요합니다.
- 개정 5: S08·S09·S15~S18·S32~S35를 관련 근거로 확장하고 B-I01과 활성성분 중첩을 포함했습니다. S41은 눈 노출 부정 상황의 방해 근거로만 사용합니다. 한국어 청크를 2~4문장 설명체로 확인했으며, 개정 4 대비 변경된 15턴은 재검수 대상입니다.
- 수정 전 입력·응답, 최초 수정 필요 판정, 수정 사유와 해시는 `outputs/pilot_24/` 및 최초 내부 검토 기록에 보관했습니다. 기존 응답을 다시 조립해 재검사했으며 사람의 승인을 부여하지 않았습니다.
