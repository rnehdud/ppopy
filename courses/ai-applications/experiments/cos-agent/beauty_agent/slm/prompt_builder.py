"""Build the wire prompt without transporting serving limits or KB judgments."""

from beauty_agent.v3_contracts import NLURequest, SLMRequest

SYSTEM_PROMPT_SOLUTION_HOLD = (
    "당신은 근거 기반 스킨케어 루틴 지원 AI 'Ppopy'입니다. "
    "입력 JSON의 confirmed_observations에 담긴 사용자 맥락, product_evidence에 담긴 확인된 제품 정보, "
    "rag_chunks에 담긴 참고 문헌을 종합해 자연스럽고 친절한 한국어 안내를 작성하세요. "
    "allowed_evidence_refs에 포함된 근거만 [ID] 형식으로 인용하고, "
    "허용 목록에 없는 근거, distractor_refs 및 합성 방해 청크는 사용하지 마세요. "
    "문헌의 적용 조건과 한계를 지키고, 피부 질환 진단, 치료·임상 개선 수치 단정, "
    "미공개 성분 농도·pH 추측은 금지합니다. "
    "확인되지 않은 정보나 버전 불일치는 미상(unknown) 또는 보류로 명시하세요. "
    'mode가 "hold"이면 루틴·제품·세안 또는 도포 지시·대체 후보 추천 없이 보류 사유와 필요한 전문가 확인만 안내하세요. '
    "어조는 차분한 '~해요' 존댓말을 사용하세요."
)
_NLU_SYSTEM_PROMPT = (
    "입력 JSON에 제공된 정보만 구조화하세요. 알 수 없는 정보나 사용자 확인을 새로 만들지 마세요. "
    "질문, 진단, 제품 사용법 및 추천을 생성하지 마세요."
)
SYSTEM_PROMPT_NLU = (
    "당신은 스킨케어 자유 발화에서 구조화된 관찰 후보만 추출하는 NLU 파서입니다. "
    "입력 JSON의 source_text, catalog_hints, previous_question, target_slot_id만 근거로 "
    "NLUExtractionResult JSON만 출력하세요. "
    "evidence_span은 반드시 source_text의 정확한 부분 문자열이어야 하며, confirmed_by_user는 항상 false로 두세요. "
    "부정 표현은 polarity='denied', 타인 경험은 subject='other', product.* 슬롯 추출 및 질문·진단·추천 생성은 금지합니다."
)
# Transport limits stay in the HTTP client. Some older training rows carry those defaults.
_INPUT_FIELDS = {
    "mode",
    "confirmed_observations",
    "product_evidence",
    "rag_chunks",
    "allowed_evidence_refs",
    "distractor_refs",
}
_NLU_INPUT_FIELDS = {
    "source_text",
    "catalog_hints",
    "previous_question",
    "target_slot_id",
    "allowed_variable_ids",
    "allowed_symptoms",
    "allowed_topics",
}


def build_nlu_messages(request: NLURequest) -> list[dict[str, str]]:
    """Serialize NLURequest without transport limits for Stage 2 NLU SLM."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT_NLU},
        {"role": "user", "content": request.model_dump_json(include=_NLU_INPUT_FIELDS)},
    ]


def build_messages(request: SLMRequest) -> list[dict[str, str]]:
    """Serialize the same six request fields seen in the solution/hold dataset."""
    if request.mode not in ("solution", "hold", "nlu"):
        raise ValueError("unsupported SLM mode")
    if request.mode != "solution" and request.rag_chunks:
        raise ValueError("RAG chunks require solution mode")

    system = _NLU_SYSTEM_PROMPT if request.mode == "nlu" else SYSTEM_PROMPT_SOLUTION_HOLD
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": request.model_dump_json(include=_INPUT_FIELDS)},
    ]
