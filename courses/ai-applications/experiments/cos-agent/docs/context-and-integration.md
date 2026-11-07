# 확인한 맥락과 통합 계획

2026-11-02에 GitHub main의 tree SHA `7d1485b3ef9d63227c66c270242fbc3621e0b615`를 확인했습니다. 관련 파일은 main URL로 열었으며 읽는 동안 각 파일의 동일 커밋 고정 여부까지 대조하지는 않았습니다. 원격 저장소와 Linear 이슈는 수정하지 않았습니다.

## 확인한 사실

- [SkinAnalysis README](https://github.com/rnehdud/SkinAnalysis/blob/main/README.md): `skin_engine/` 규칙 엔진과 API, `frontend/` React/Vite 앱 셸, iOS 디렉터리가 존재합니다.
- [frontend README](https://github.com/rnehdud/SkinAnalysis/blob/main/frontend/README.md): 합성 fixture와 로컬 HTTP 모드, 별도 보호 스테이징 경로가 있습니다. 얼굴 촬영·자동 개선 판정은 범위 밖입니다.
- [careApi.ts](https://github.com/rnehdud/SkinAnalysis/blob/main/frontend/src/careApi.ts): `CareAnalysisRequest`는 `schema_version`, `deployment_context`, `confirmed_current_product_ids`, `routine_observation`, `care_priorities`, `aggravating_answers`, `survey`를 전달합니다. 제품 ID 목록만으로 제품 버전·검토된 사용법을 알 수는 없습니다.
- [app_routine_analysis.py](https://github.com/rnehdud/SkinAnalysis/blob/main/skin_engine/app_routine_analysis.py): TEST 분석 서비스는 서버 참여자 문맥과 민감정보 동의를 검사한 뒤 기존 `analyze_care_request`를 호출하며 배포 route에 붙어 있지 않다고 명시합니다. 이 seam 하나를 읽은 것이 전체 앱 배포 상태 확인을 뜻하지 않습니다.
- [ERI-11](https://linear.app/kjhgr/issue/ERI-11): 사용자 파악·보유품·기록·루틴·근거를 연결하는 장기 비전과 6주 MVP가 구분되어 있습니다.
- [ERI-13](https://linear.app/kjhgr/issue/ERI-13), [ERI-14](https://linear.app/kjhgr/issue/ERI-14): 제품 버전·소유권·사용자 확인·승인된 동일 초안 저장을 요구합니다.
- [ERI-17](https://linear.app/kjhgr/issue/ERI-17): 고정 근거 설명은 초기 필수, 검색 RAG와 SLM 학습은 후속 실험입니다. 사용자의 이번 요청에 맞춰 SLM 연결 인터페이스를 먼저 준비했습니다.

Linear의 공유 field notes 조회는 `Tool get_agent_context not found`로 실패했습니다. 이슈 본문을 직접 조회했으며 공유 메모가 없다고 단정하지 않습니다. 이슈의 하위 문서·첨부 전체와 원격 코드 전체 실행은 확인하지 않았습니다.

## 제안하는 개선점

1. iOS·미러마다 추천 로직을 복제하지 않고 공통 API와 제품/규칙/근거 버전을 공유합니다. 스마트미러 하드웨어와 오프라인 요구는 아직 미확정입니다.
2. 기존 앱의 입력 의미를 보존하는 adapter를 둡니다. `unknown`, `refused`, `not_asked`를 false/0으로 바꾸지 않습니다. 진단이나 피부 타입을 모델이 추정해 채우지 않습니다.
3. 기존 `skin_engine`을 후속 읽기 도구로 연결합니다. 이 골격의 합성 사용법 배열기는 기존 6성분 계획 엔진을 대체하지 않습니다.
4. 파인튜닝에 앞서 같은 입력·도구의 기준선과 모델 경로를 비교합니다. 실제 오류가 대화 이해인지, 누락 제품 데이터인지 구분한 뒤 학습 여부를 결정합니다.

## 앱 연결 매핑 — 아직 구현하지 않은 계약 제안

| 앱 입력 | 공통 에이전트로 옮기는 방법 |
|---|---|
| `confirmed_current_product_ids` | 서버 카탈로그에서 제품 버전/출처를 조회하고 사용자 확인과 별도 결합 |
| `care_priorities` | 사용자가 입력한 고민/우선순위 그대로 전달; 현재 concern 필드는 계산하지 않음 |
| `routine_observation` | 다음 계약 버전에 미상·거절 상태, 빈도, 시각을 보존해 추가 |
| `survey` / `aggravating_answers` | 기존 엔진 입력 계약으로 검증; 임의로 피부 타입 변환하지 않음 |
| 로그인 세션 | 기존 서버가 검증한 사용자 문맥으로 주입; body의 user ID로 권한 결정 금지 |

`/v1/agent/turn`은 새 프로토타입 계약이며 기존 `CareAnalysisRequest`나 결과 envelope의 직접 대체물이 아닙니다. 앱에는 아직 연결하지 않았습니다. 실제 연동 전 서버 adapter와 회귀 테스트가 필요합니다. 기존 앱의 동의·세션·철회 검증을 API 앞뒤에 유지해야 합니다.

초기 운용은 iOS와 미러 모두 서버 호출을 가정합니다. 기기에 Python 코드를 직접 탑재하지 않습니다. 추후 미러에서 같은 API 프로세스와 Ollama를 실행하는 방식은 검토할 수 있지만, iPhone 완전 온디바이스 실행은 모델 런타임·배터리·메모리를 별도 검증해야 합니다.
