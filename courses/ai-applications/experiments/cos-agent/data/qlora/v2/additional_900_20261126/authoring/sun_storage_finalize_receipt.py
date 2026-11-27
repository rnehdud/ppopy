"""Windows 파이프 문자 인코딩과 무관하게 한국어 한계 및 검증 기록을 저장한다."""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
path=HERE/'sun_storage_generation_receipt.json'
receipt=json.loads(path.read_text(encoding='utf-8'))
receipt['limitations']=[
 '독립 Cross-Model Critic과 사람 검수는 수행하지 않았어요.',
 '가족 분할은 기존 flame-warning/uncovered-gap/packaging-breach/clinician-conflict의 validation 역할을 참고한 개발 분할이며, 독립 최종 test라는 뜻이 아니에요.',
 '동일 문헌의 일반 규칙을 다루는 새 사례라 기존 자료와 넓은 주제 중첩은 남아요. 의미적 독립성은 입력 해시 중복 0건만으로 증명되지 않아요.',
 '일부 정형 입력은 실제 사용자 발화가 아니라 가상의 표시 해석 질문이에요. 합성 제품 정보는 실제 상용품 사실이 아니에요.',
]
receipt['authoring_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(HERE.glob('sun_storage*')) if p.is_file() and p!=path}
path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'receipt':str(path),'batch_hashes':len(receipt['batch_sha256']),'formal_critic':receipt['formal_cross_model_critic']},ensure_ascii=False))
