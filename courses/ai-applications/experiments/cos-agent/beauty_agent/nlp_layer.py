"""NLP Layer wrapping Kiwi segmentation -> Jev extraction -> MappingReview."""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import re

from poc.jev.relations import SYMPTOMS
from poc.jev.segmenter import noun_candidates, segmentation_method, units

from .modules.jev_adapter import JevExtractorAdapter
from .modules.mapping_adapter import MappingReviewAdapter
from .runtime_contracts import (
    CandidateConfirmationInput,
    FeatureCandidate,
    NLPExtractionResult,
    ProductQueryCandidate,
    SymptomCandidate,
)

_COS_AGENT_DIR = Path(__file__).resolve().parents[1]
_REPO_ROOT = next(
    (p for p in _COS_AGENT_DIR.parents if (p / "docs" / "repository-scope.md").is_file()),
    _COS_AGENT_DIR,
)

TOPIC_PATTERNS: dict[str, str] = {
    "outdoor_sun": r"야외|햇빛|자외선|선크림|선세럼|선스틱|선젤|땀|물놀이|외출",
    "cleansing_method": r"세안|세수|클렌징|클렌저|폼|미온수|뜨거운\s*물|찬물|브러시|수건|마찰",
    "repeat_cleansing": r"(?:반복|이중|두\s*번)\s*(?:세안|세수)|세안(?:을)?\s*두\s*번",
    "moisturizing": r"보습|크림|로션|세럼|앰플|토너|건조|당기|땅기",
    "discomfort_report": r"따가|따갑|따끔|가려|가렵|간지|붉|빨개|홍조|화끈|쓰라|아프|통증",
}

SLOT_VALUE_PATTERNS: dict[str, tuple[tuple[str, str], ...]] = {
    "method.body_site": (
        (r"얼굴|볼|이마|코|턱|세안|세수|\bface\b", "face"),
        (r"손|\bhands\b", "hands"),
        (r"몸|바디|\bbody\b", "body"),
        (r"두피|머리|\bscalp\b", "scalp"),
    ),
    "method.water_temperature": (
        (r"미온수|미지근|따뜻|적당|\blukewarm\b", "lukewarm"),
        (r"뜨거|뜨겁|열탕|\bhot\b", "hot"),
        (r"차가|차갑|찬물|시원|\bcold\b", "cold"),
    ),
    "method.tools": (
        (r"브러시|진동\s*클렌저|클렌징\s*솔|\bsol\b|\bscrub_brush\b", "scrub_brush"),
        (r"수건|타월|\bwashcloth\b", "washcloth"),
        (r"스펀지|해면|퍼프|\bsponge\b", "sponge"),
        (r"^(?:아니|아뇨|안\s*써|안\s*쓰|사용\s*안|없어|없음|노\b)|손만|손으로|손가락|맨손|손|\bhands\b", "hands"),
    ),
    "method.friction": (
        (r"세게|강하게|빡빡|거칠|\bstrong\b", "strong"),
        (r"살살|부드럽|가볍|약하게|조심|\bgentle\b", "gentle"),
    ),
    "method.drying": (
        (r"문질|비벼|세게\s*닦|\brubbing_strongly\b", "rubbing_strongly"),
        (r"톡톡|가볍게|눌러|두드려|\bpat_gently\b", "pat_gently"),
    ),
    "sun.outdoor_time": (
        (r"없|안\s*나|실내|집에만|\bnone\b", "none"),
        (r"오래|장시간|많이|계속|긴\s*시간|\bprolonged\b", "prolonged"),
    ),
    "sun.water_contact": (
        (r"아니|안\s*닿|없|\bno\b", "no"),
        (r"네|예|응|있|많이|물놀이|\byes\b", "yes"),
    ),
    "sun.sweat": (
        (r"아니|안\s*흘|없|\bno\b", "no"),
        (r"네|예|응|있|많이|흘|\byes\b", "yes"),
    ),
    "cleansing.target_load": (
        (r"땀|운동|발한|\bheavy_sweat\b", "heavy_sweat"),
        (r"심한\s*오염|먼지|피지|노폐물|\bheavy_soiling\b", "heavy_soiling"),
        (r"메이크업|화장|선크림|자외선\s*차단|\bmakeup_requires_removal\b", "makeup_requires_removal"),
        (r"제거\s*필요|지워야|잔여|\bconfirmed_removal_need\b", "confirmed_removal_need"),
        (r"없|아니|아뇨|특별히\s*없|추가.*없|\bno_additional_removal_need\b", "no_additional_removal_need"),
    ),
    "cleansing.repeat_wash": (
        (r"목적|지우려고|제거|메이크업|땀|\bpurpose_matched\b", "purpose_matched"),
        (r"습관|그냥|이유\s*없|개운|느낌|\bhabitual_without_reason\b", "habitual_without_reason"),
    ),
}


_STRONG_RUBBING_DENIAL = re.compile(
    r"(?:세게|강하게|빡빡|거칠게)\s*"
    r"(?:(?:문지르|문질러\s*닦|비비|씻|닦)지\s*않|(?:안|못)\s*(?:문지르|문질러|비비|씻|닦))"
)


def _slot_match_text(slot_id: str, text: str) -> str:
    if slot_id in ("method.friction", "method.drying"):
        return _STRONG_RUBBING_DENIAL.sub(" ", text)
    return text


def _explicit_slot_value(slot_id: str, text: str) -> str | None:
    for pattern, value in SLOT_VALUE_PATTERNS.get(slot_id, ()):
        if re.search(pattern, text, re.IGNORECASE):
            return value
    return None


def interpret_slot_answer(
    slot_id: str,
    utterance: str,
    *,
    api_key: str | None = None,
) -> tuple[str, str | None] | None:
    """Map a Korean user reply to a KB (state, value) pair, using Jev if needed."""
    text = utterance.strip()
    if not text:
        return None
    if re.search(r"^(?:unknown|모름|모르겠|잘\s*모르|기억\s*안)", text, re.IGNORECASE):
        return ("unknown", None)
    if re.search(r"^(?:declined|거절|안\s*알려|말\s*안)", text, re.IGNORECASE):
        return ("declined", None)

    match_text = _slot_match_text(slot_id, text)
    value = _explicit_slot_value(slot_id, match_text)
    if value is not None:
        return ("known", value)
    if match_text != text:
        return None  # A denial alone leaves the actual technique unspecified.

    if api_key and slot_id in SLOT_VALUE_PATTERNS:
        try:
            from poc.jev.jev_client import ask

            choices = {val: val for _, val in SLOT_VALUE_PATTERNS[slot_id]}
            choices["unknown"] = "사용자가 모른다고 답함"
            choices["declined"] = "사용자가 답변을 거절함"
            choices["omit"] = "질문에 대한 명확한 답이 아님"
            q = {
                slot_id: {
                    "type": "choice",
                    "instructions": f"사용자 답변에서 {slot_id}에 해당하는 선택지 하나를 고르세요.",
                    "criteria": choices,
                }
            }
            ans = ask(text, q, api_key)
            choice = ans[slot_id]["choice"]
            if choice in ("unknown", "declined"):
                return (choice, None)
            if choice != "omit":
                return ("known", choice)
        except Exception:
            pass
    return None


def interpret_candidate_confirmation(
    utterance: str,
    *,
    api_key: str | None = None,
) -> CandidateConfirmationInput | None:
    """Parse a Korean user reply confirming/denying an extracted symptom candidate."""
    text = utterance.strip()
    if not text:
        return None
    if re.search(r"^(?:unknown|모름|모르겠|잘\s*모르|기억\s*안)", text, re.IGNORECASE):
        return CandidateConfirmationInput(subject="unknown", state="unknown")
    if re.search(r"^(?:declined|거절|안\s*알려|말\s*안)", text, re.IGNORECASE):
        return CandidateConfirmationInput(subject="unknown", state="declined")

    other = bool(re.search(r"친구|엄마|아빠|동생|언니|오빠|형|누나|남편|아내|지인|다른\s*사람|타인", text))
    denied = bool(re.search(r"^(?:아니|아뇨|없어|없음|아닌데)|없었|안\s*났|안\s*아팠|그런\s*적\s*없", text))
    affirmed = bool(re.search(r"^(?:네|예|응|맞아|맞습|어|그래)|있었|났어|그래요|아파|따가|가려|당겨|건조|붉", text))

    persistence: str = "unknown"
    if re.search(r"계속|지속|쭉|며칠|오래|항상|매일", text):
        persistence = "persistent"
    elif re.search(r"자주|반복|매번|가끔|종종", text):
        persistence = "repeated"
    elif re.search(r"어제|오늘|방금|최근|잠깐|한\s*번|이번", text):
        persistence = "recent"

    if other:
        return CandidateConfirmationInput(subject="other", state="denied" if denied else "affirmed", persistence="unknown")
    if denied:
        return CandidateConfirmationInput(subject="self", state="denied", persistence="unknown")
    if affirmed or persistence != "unknown":
        return CandidateConfirmationInput(subject="self", state="affirmed", persistence=persistence)

    if api_key:
        try:
            from poc.jev.jev_client import ask

            q = {
                "confirm": {
                    "type": "choice",
                    "instructions": "사용자가 방금 언급된 증상이 본인 경험인지, 지속되는지 답한 내용을 분류하세요.",
                    "criteria": {
                        "self_persistent": "본인 증상이고 계속/지속됨",
                        "self_repeated": "본인 증상이고 반복/자주 발생",
                        "self_recent": "본인 증상이고 어제/오늘 최근 1회성",
                        "self_denied": "본인에게 해당 증상이 없음",
                        "other_person": "타인의 경험임",
                        "unknown": "모른다고 답함",
                        "declined": "답변을 거절함",
                    },
                }
            }
            ans = ask(text, q, api_key)["confirm"]["choice"]
            mapping = {
                "self_persistent": CandidateConfirmationInput(subject="self", state="affirmed", persistence="persistent"),
                "self_repeated": CandidateConfirmationInput(subject="self", state="affirmed", persistence="repeated"),
                "self_recent": CandidateConfirmationInput(subject="self", state="affirmed", persistence="recent"),
                "self_denied": CandidateConfirmationInput(subject="self", state="denied"),
                "other_person": CandidateConfirmationInput(subject="other", state="denied"),
                "unknown": CandidateConfirmationInput(subject="unknown", state="unknown"),
                "declined": CandidateConfirmationInput(subject="unknown", state="declined"),
            }
            return mapping.get(ans)
        except Exception:
            pass
    return None


def load_jev_api_key(env_paths: tuple[Path, ...] | None = None) -> str | None:
    """Resolve TypeSafe Jev key from environment or .env without exposing secrets."""
    env_val = os.environ.get("TYPESAFE_API_KEY", "").strip()
    if env_val:
        return env_val
    candidates = env_paths or (_REPO_ROOT / ".env", _COS_AGENT_DIR / ".env")
    for path in dict.fromkeys(candidates):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            name, sep, value = stripped.partition("=")
            if not sep or name.strip() not in ("jev-key", "TYPESAFE_API_KEY"):
                continue
            cleaned = value.strip()
            if len(cleaned) >= 2 and cleaned[0] == cleaned[-1] and cleaned[0] in "\"'":
                cleaned = cleaned[1:-1]
            if cleaned.strip():
                return cleaned.strip()
    return None


def _relation_value(relations: dict, key: str, default: str = "unknown") -> str:
    entry = relations.get(key)
    if isinstance(entry, dict):
        return str(entry.get("value") or default)
    if entry is not None:
        return str(entry)
    return default


def _detect_topic_hints(message: str) -> list[str]:
    return [topic for topic, pattern in TOPIC_PATTERNS.items() if re.search(pattern, message)]


def extract_feature_candidates(
    message: str,
    topic_hints: list[str],
    *,
    api_key: str | None = None,
) -> list[FeatureCandidate]:
    """Extract explicitly mentioned KB slot candidates from a free-text utterance."""
    target_slots: list[str] = ["method.body_site"]
    if "cleansing_method" in topic_hints or re.search(r"미온수|뜨거|찬물|브러시|손세안|살살|세게|수건", message):
        target_slots.extend(["method.water_temperature", "method.tools", "method.friction"])
        if re.search(r"수건|타월|물기|닦|톡톡", message):
            target_slots.append("method.drying")
    if "outdoor_sun" in topic_hints:
        target_slots.append("sun.outdoor_time")

    found: list[FeatureCandidate] = []
    for slot_id in target_slots:
        value = _explicit_slot_value(slot_id, _slot_match_text(slot_id, message))
        if value is not None:
            found.append(FeatureCandidate(slot_id=slot_id, state="known", value=value))
    return found


def _extract_product_candidates(
    message: str,
    features: dict,
    units_list: list[dict],
    *,
    allow_offline_nouns: bool,
) -> list[ProductQueryCandidate]:
    raw_products = features.get("products") or []
    results: list[ProductQueryCandidate] = []
    seen: set[str] = set()
    for item in raw_products:
        text = str(item.get("text", "")).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        rels = item.get("relations") or {}
        results.append(
            ProductQueryCandidate(
                text=text,
                usage_state=_relation_value(rels, "usage_state"),
                subject=_relation_value(rels, "subject"),
                correction=_relation_value(rels, "correction"),
            )
        )
    if not results and allow_offline_nouns:
        for unit in units_list:
            for span in noun_candidates(message, unit):
                text = str(span.get("text", "")).strip()
                if text and text not in seen:
                    seen.add(text)
                    results.append(ProductQueryCandidate(text=text))
    return results


def _extract_symptom_candidates(
    message: str,
    features: dict,
    namespace: str,
) -> list[SymptomCandidate]:
    digest = namespace or hashlib.sha256(message.encode("utf-8")).hexdigest()[:12]
    candidates: list[SymptomCandidate] = []
    for idx, item in enumerate(features.get("symptoms") or []):
        symptom = str(item.get("symptom", "unknown"))
        label = str(item.get("label") or SYMPTOMS.get(symptom, symptom))
        rels = item.get("relations") or {}
        candidates.append(
            SymptomCandidate(
                candidate_id=f"clarify:{digest}:{idx}",
                symptom=symptom,
                label=label,
                state=_relation_value(rels, "state"),
                subject=_relation_value(rels, "subject"),
                prompt_ko=f"{label} 언급의 대상이 본인인지, 실제 증상이 있었는지와 관찰 시점을 확인해 주세요.",
            )
        )
    return candidates


class NLPLayer:
    """Unified Kiwi -> Jev -> MappingReview layer returning unconfirmed candidates."""

    def __init__(
        self,
        *,
        use_remote_jev: bool = True,
        api_key: str | None = None,
        extractor=None,
        mapping_adapter: MappingReviewAdapter | None = None,
    ):
        self.use_remote_jev = use_remote_jev
        self.extractor = extractor
        self.api_key = api_key if api_key is not None else (load_jev_api_key() if use_remote_jev and extractor is None else None)
        self.mapping_adapter = mapping_adapter or MappingReviewAdapter()

    def analyze(self, message: str, *, namespace: str = "turn1") -> NLPExtractionResult:
        adapter = JevExtractorAdapter(key=self.api_key, extractor=self.extractor)
        features = adapter.extract(message)
        reviewed = self.mapping_adapter.evaluate(features)
        units_list = features.get("units") or units(message)

        if self.extractor is not None:
            mode = "injected_extractor"
        elif self.api_key:
            mode = "remote_jev"
        else:
            mode = "offline_kiwi_fallback"

        warnings = list(dict.fromkeys([*(features.get("warnings") or []), *(reviewed.get("warnings") or [])]))
        products = _extract_product_candidates(
            message,
            features,
            units_list,
            allow_offline_nouns=(mode == "offline_kiwi_fallback"),
        )
        symptoms = _extract_symptom_candidates(message, features, namespace)
        topics = _detect_topic_hints(message)
        feature_cands = extract_feature_candidates(message, topics, api_key=self.api_key)

        return NLPExtractionResult(
            source_text=message,
            source_mode=mode,
            segmentation_method=str(features.get("segmentation_method") or segmentation_method()),
            units=[dict(u) for u in units_list],
            product_queries=products,
            symptom_candidates=symptoms,
            feature_candidates=feature_cands,
            topic_hints=topics,
            mapping_findings=[dict(f) for f in (reviewed.get("findings") or [])],
            warnings=warnings,
            extraction_failed=bool(features.get("extraction_failed")),
        )
