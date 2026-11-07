import hashlib
import json

from .catalog import CATALOG, RULE_VERSION
from .contracts import Draft, Question, Step, TurnRequest, TurnResponse
from .planner import select_question


def missing_information(request: TurnRequest) -> list[Question]:
    questions = []
    if not request.profile.confirmed:
        questions.append(Question(id="confirm_profile", text="입력한 프로필과 제외 제품을 확인해 주세요."))
    if not request.products:
        questions.append(Question(id="add_products", text="사용자가 확인한 보유 제품과 정확한 버전을 추가해 주세요."))
    for owned in request.products:
        product = CATALOG.get(owned.product_id)
        if product is None or owned.version != product.version:
            questions.append(Question(id=f"resolve:{owned.product_id}", text="제품의 정확한 버전과 표시 사용법을 확인할 수 없어 초안을 보류했습니다."))
        elif not owned.confirmed:
            questions.append(Question(id=f"confirm:{owned.product_id}", text=f"{product.name}의 버전과 보유 여부를 확인해 주세요."))
    if request.products and all(p.product_id in request.profile.excluded_product_ids for p in request.products):
        questions.append(Question(id="all_excluded", text="모든 보유 제품이 제외되어 있습니다. 보유 목록과 제외 조건을 검토해 주세요."))
    return questions


async def run_turn(request: TurnRequest) -> TurnResponse:
    questions = missing_information(request)
    if questions:
        selected, provider, model = await select_question(request.message, questions)
        # All blockers remain visible regardless of model selection.
        ordered = [selected] + [q for q in questions if q.id != selected.id]
        return TurnResponse(status="needs_information", message=selected.text,
                            questions=ordered, provider=provider, model=model)
    products = sorted((CATALOG[p.product_id] for p in request.products
                       if p.product_id not in request.profile.excluded_product_ids),
                      key=lambda p: (p.order, p.product_id))
    steps = [Step(product_id=p.product_id, version=p.version, period=period,
                  label_instruction=p.instruction, evidence_id=p.evidence_id)
             for period in ("am", "pm") for p in products if period in p.periods]
    content = {"rule_version": RULE_VERSION, "steps": [s.model_dump() for s in steps]}
    digest = hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    return TurnResponse(status="draft", message="합성 제품의 표시 사용법에 따른 초안입니다. 저장·적용되지 않았습니다.",
                        questions=[], draft=Draft(draft_hash=digest, **content), provider="baseline")
