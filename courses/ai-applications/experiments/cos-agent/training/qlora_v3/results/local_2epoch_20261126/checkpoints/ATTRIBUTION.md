# 출처·배포 범위

- 원본: Qwen Team, [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507), revision `cdbee75f17c01a7cc42f958dc650907174af0554`.
- 공식 모델 카드의 라이선스는 Apache-2.0이며 원본 라이선스는 `LICENSE-QWEN`에 보존해요. tokenizer는 두 epoch에서 동일한 실제 저장본이에요.
- 원본 모델 가중치와 학습된 LoRA 가중치는 Git에 포함하지 않아요. 각 checkpoint의 SHA-256·크기를 manifest에 기록했어요.
- `adapter_config.original.json`은 실험 원문이에요. 옆의 `adapter_config.json`은 다른 PC에서 사용할 수 있게 원본 모델 경로와 revision만 고친 배포용 설정이며 변경 내역을 manifest에 명시했어요. 가중치는 수정하지 않았어요.
- raw 입력에 포함된 Reference RAG 문헌은 저장소의 `data/rag/SOURCES.md` 출처·이용 조건을 따르며 서비스 정책 또는 임상 정답으로 취급하지 않아요.
