"""Deterministic checks for the v3 model output boundary."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from beauty_agent.slm._citations import extract_citations
from beauty_agent.slm.rule_fallback import RuleBaselineFallback
from beauty_agent.v3_contracts import SLMRequest, SLMResponse

_HOLD_RECOMMENDATION = re.compile(
    r"대체\s*(?:후보|제품)|추천(?:해요|드립니다|해\s*드려요|합니다|드려요)|"
    r"권(?:해요|합니다|장해요|장합니다)|루틴을\s*(?:유지|추천|권해)|"
    r"(?:사용|세안|도포|헹궈|발라|덧발라|씻어|써|문질러|닦아)\s*(?:해\s*)?(?:보세요|주세요)|"
    r"(?:사용|세안|도포|헹구|바르|덧바르|씻으|쓰|문지르|닦으|적용)세요|"
    r"(?:바르|닦|씻|사용하|세안하)(?:는|시기)\s*(?:게|것을)\s*(?:좋아요|좋습니다|권해요)|"
    r"(?:아침|저녁|세안\s*후|[123]단계)[^.!?\n]{0,70}(?:사용하세요|바르세요|바르고|도포하고|세안으로|클렌저로)|"
    r"(?:클렌징폼|클렌징\s*오일|보습제|선크림|자외선차단제)(?:을|를|으로)\s*"
    r"\d*\s*(?:회|번|단계)?\s*(?:사용|세안|도포|바르)|"
    r"\b(?:I recommend|apply (?:the|a|your)|use (?:the|a|your)|start with)\b",
    re.IGNORECASE,
)

_CLINICAL_ASSERTION = re.compile(
    r"(?:아토피\s*피부염|접촉\s*피부염|지루성\s*피부염|여드름|습진|주사피부염)(?:이|가)?\s*"
    r"(?:입니다|이에요|예요|맞아요|으로\s*진단)|"
    r"(?:진단|처방)\s*(?:합니다|해요|됩니다|할\s*수\s*있어요)|"
    r"(?:치료|완치|완쾌)\s*(?:됩니다|돼요|합니다|해요|할\s*수\s*있어요)|"
    r"치료\s*효과(?:가|를)?\s*(?:있어요|있습니다|보장)|"
    r"임상적으로\s*입증|(?:확실히|자동으로)\s*개선|"
    r"(?:자동(?:으로)?|AI가|사진으로)\s*[^.!?\n]{0,35}(?:피부\s*)?개선(?:\s*여부|을|이|됐|된)?"
    r"[^.!?\n]{0,20}(?:판정|확인|입증)|"
    r"\d+(?:\.\d+)?\s*%\s*(?:개선|감소|줄어|호전)(?:됩니다|합니다|돼요|해요|듭니다|들어요)|"
    r"\b(?:you have (?:acne|eczema|dermatitis|rosacea)|I diagnose|I prescribe|"
    r"will cure|guaranteed (?:cure|improvement)|clinically proven)\b",
    re.IGNORECASE,
)
_UNDISCLOSED_GUESS = re.compile(
    r"(?:pH\s*(?:는|가|를)?\s*|농도(?:는|가|를)?\s*)\d+(?:\.\d+)?\s*%?\s*"
    r"(?:[으]?로\s*(?:추정|보입)|일\s*것(?:으로| 같)|쯤|정도일)",
    re.IGNORECASE,
)
_PRODUCT_ASSERTION = re.compile(
    r"(?:제품|카탈로그|라벨|표시|성분표|전성분)[^.!?\n]{0,55}"
    r"(?:확인돼요|확인됐어요|확인되었어요|확인됩니다|확인했어요|"
    r"(?:기재돼|기재되어|표시되어|표시돼|적혀|나와)\s*(?:있어요|있습니다)|"
    r"(?:기재|표시)(?:돼요|됩니다|됐어요)|함유(?:돼요|합니다|되어\s*있어요)|"
    r"포함(?:돼요|합니다|되어\s*있어요)|들어\s*있어요|함유량은|농도는)|"
    r"(?:성분|공식\s*표시|사용법)(?:을|를|이|가)?\s*(?:확인했어요|확인됐어요|확인됩니다)|"
    r"이\s*제품(?:은|에는)?[^.!?\n]{0,38}(?:들어\s*있어요|함유|포함돼요)|"
    r"\bpH\s*(?:는|가)?\s*\d+(?:\.\d+)?\s*(?:입니다|이에요|예요)|"
    r"\b(?:this product|the label|the ingredient list)\s+(?:contains|lists|confirms|states)\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class GuardrailResult:
    passed: bool
    flags: list[str]
    safe_response: SLMResponse


class HardSafetyGuardrail:
    """Validate model output before it can reach the user."""

    def __init__(self, fallback: RuleBaselineFallback | None = None) -> None:
        self._fallback = fallback if fallback is not None else RuleBaselineFallback()

    def validate(self, request: SLMRequest, response: SLMResponse) -> GuardrailResult:
        flags: list[str] = []
        content = unicodedata.normalize("NFKC", response.content)
        actual_refs = extract_citations(response.content)
        declared_refs = set(response.cited_evidence_refs)
        refs = set(actual_refs) | declared_refs

        if response.mode != request.mode:
            flags.append("mode_mismatch")
        if declared_refs - set(actual_refs):
            flags.append("citation_metadata_mismatch")
        if any(ref.lower().startswith("kb:") for ref in refs):
            flags.append("kb_citation")
        if refs - set(request.allowed_evidence_refs):
            flags.append("citation_not_allowed")
        if refs.intersection(request.distractor_refs):
            flags.append("distractor_citation")
        if request.mode == "hold":
            if refs:
                flags.append("hold_citation")
            if _HOLD_RECOMMENDATION.search(content):
                flags.append("hold_recommendation")
        if _CLINICAL_ASSERTION.search(content) or _UNDISCLOSED_GUESS.search(content):
            flags.append("clinical_or_safety_claim")

        verified, unverified = self._product_refs(request)
        catalog_refs = {ref for ref in refs if ref.lower().startswith("catalog:")}
        if catalog_refs - verified:
            flags.append("product_version_mismatch")
        if _PRODUCT_ASSERTION.search(content) and (not verified or any(ref in content for ref in unverified)):
            flags.append("unverified_product_claim")

        if flags:
            safe = self._fallback.build(request, reason="guardrail_blocked")
            return GuardrailResult(passed=False, flags=flags, safe_response=safe)
        return GuardrailResult(passed=True, flags=[], safe_response=response)

    @staticmethod
    def _product_refs(request: SLMRequest) -> tuple[set[str], set[str]]:
        verified: set[str] = set()
        unverified: set[str] = set()
        for product in request.product_evidence:
            product_id, version = product.get("product_id"), product.get("version")
            if not isinstance(product_id, str) or not product_id.strip():
                continue
            if not isinstance(version, str) or not version.strip():
                continue
            ref = f"catalog:{product_id}@{version}"
            if product.get("status") == "verified" and product.get("evidence_ref", ref) == ref:
                verified.add(ref)
            else:
                unverified.add(ref)
        return verified - unverified, unverified
