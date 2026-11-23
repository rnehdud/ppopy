# Shared knowledge base

## 2026-11-22 개발·평가 명세

- [KB v0.6.2 세안 후 당김](Poppy_KB_v0.6.2/README.md) — 60개 카드 중 7개를 갱신한 고정 개발·비교 명세와 참조 판정기. 운영 적용은 꺼져 있다.
- 재현: `python3 -m pytest -q tests/test_kb_cleansing_freeze.py`

## 2026-11-19 팀 공유본

- [KB v0.6.1 전체 명세](Poppy_KB_v0.6.1/Poppy_KB_seed_v0.6.1.json) — 세정·보습·자외선차단 등 60개 카드와 234개 변수 정의. 일반 세안은 고정 시간 대신 손끝으로 부드럽게 씻고 헹구도록 개정했다. 서로 다른 레티노이드·각질관리 제품을 겹쳐 쓸 때의 안내도 보완했다.
- [B-I01 선크림 세정 규칙](Poppy_KB_v0.6.1/sunscreen_removal_review.json) — 11월 19일 추가한 개발 앱 규칙. 선크림의 확인된 제거 조건과 사용자가 실제 쓴 세정제를 대조한다. `condition_outcomes`에 조건별 분기, `messages`에 사용자 안내 문구가 있다.
- [사례 6 문답과 결과 화면](Poppy_KB_v0.6.1/case-6/README.md) — 같은 닥터지·로벡틴 루틴에서 워터·폼·밀크 답만 바꾼 결과와, 다른 워터프루프 선크림으로 바꿨을 때의 차이를 볼 수 있다.

위 JSON 두 파일은 개발 프로젝트에서 가져온 명세다. 아래 수업 저장소의 실행 예제와 검증 명령은 11월 5일에 가져온 v0.6을 사용한다.

## November 5 reference snapshot

The [v0.6 draft](Poppy_KB_v0.6/README_Codex_v0.6.md) is the shared design asset for cleansing, moisturizing, and sun protection. It includes 60 baseline cards, 234 variable definitions, nine functional domains, and seven lifecycle stages. These are design and knowledge structures, not participant counts or validated recommendation rules.

- [Structured seed](Poppy_KB_v0.6/Poppy_KB_seed_v0.6.json): canonical imported snapshot.
- [Taxonomy](Poppy_KB_v0.6/Poppy_KB_분류표_v0.6.md): navigation and card ownership.
- [Knowledge structure](Poppy_KB_v0.6/Poppy_KB_지식구조_v0.6.md): reviewable narrative.
- [Source manifest](../docs/source-manifest.json): source file hashes and export boundaries.

All operational activation remains off. The regulatory section preserves a **historical 2024 snapshot**; current full-text reconciliation is incomplete. Its source text and reference predicates are not current legal conclusions or personal safety thresholds. Manufacturer opinions remain labeled development material and do not establish quality rankings.

The bundle includes source metadata and original review states. It excludes the social-post corpus, PDF attachments, private product spreadsheet, and user records. The empty original `Cleansing.md` was not treated as a finished cleanser KB.

Validate without overwriting the bundled historical report:

```bash
mkdir -p outputs
python3 KB/Poppy_KB_v0.6/validate_poppy_kb_v0_6.py --report outputs/kb-structure.json
```

The 95 checks cover structure, references, inactive flags, and small reference-function boundaries. They do not establish clinical validity, current legal compliance, LLM quality, or completion of the engine's 57 original acceptance scenarios.
