"""PPO-46 Step 1: 원문부터 개별 작성한 49개 NLU 후보 정답을 직렬화해요."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

COS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(COS))
from beauty_agent.nlu_schema import (
    ALLOWED_SYMPTOMS,
    ALLOWED_TOPICS,
    load_nlu_whitelist,
    verify_nlu_extraction,
)
from beauty_agent.slm.prompt_builder import build_nlu_messages
from beauty_agent.v3_contracts import NLUExtractionResult, NLURequest

HERE = COS / "data/nlu/v1"
CORE_SLOTS = [
    "method.body_site",
    "method.water_temperature",
    "method.tools",
    "method.friction",
    "method.drying",
    "cleansing.target_load",
    "cleansing.repeat_wash",
    "cleansing.steps",
    "method.current_routine",
    "method.sequence",
    "method.skin_wetness",
    "method.rinse",
    "method.mixing",
    "moisturizing.after_wash_delay",
    "moisturizing.comfort",
    "moisturizing.coverage",
    "moisturizing.dryness_return",
    "moisturizing.reapplication",
    "sun.outdoor_time",
    "sun.water_contact",
    "sun.sweat",
    "sun.coverage_gaps",
    "sun.exposed_sites",
    "sun.shade_clothing",
    "sun.reapplication",
    "storage.opened_at",
    "storage.decanting",
    "storage.container",
    "storage.sensory_change",
    "storage.expiry",
    "storage.pao",
    "storage.water_ingress",
    "storage.light_air",
    "skin.eye_symptom_context",
]
CASES = []


def slot(variable, value, span, *, polarity="affirmed", subject="self"):
    return {
        "variable_id": variable,
        "value": value,
        "polarity": polarity,
        "subject": subject,
        "confidence": "high",
        "evidence_span": span,
    }


def symptom(name, span, *, polarity="affirmed", subject="self", persistence="unknown"):
    return {
        "symptom": name,
        "polarity": polarity,
        "subject": subject,
        "persistence": persistence,
        "evidence_span": span,
    }


def product(raw, usage, hint=None):
    return {"raw_text": raw, "usage_state": usage, "matched_catalog_hint": hint}


def hint(raw, identifier):
    return {"raw_span": raw, "matched_catalog_hint": identifier, "match_score": 0.95}


def case(
    bucket,
    family,
    text,
    topics,
    *,
    slots=(),
    symptoms=(),
    products=(),
    previous=None,
    target=None,
    hints=(),
    why,
):
    CASES.append(
        {
            "bucket": bucket,
            "family": family,
            "text": text,
            "topics": topics,
            "slots": list(slots),
            "symptoms": list(symptoms),
            "products": list(products),
            "previous": previous,
            "target": target,
            "hints": list(hints),
            "rationale": why,
        }
    )


# 1. 초기 복합 발화: 조언을 생성하지 않고 실제 표현의 후보만 추출해요.
case(
    "turn1_utterance",
    "wash_temperature",
    "얼굴은 손으로 미지근한 물에 씻고, 보습제는 세안하고 5분 뒤에 발라요.",
    ["cleansing_method", "moisturizing"],
    slots=[
        slot("method.body_site", "face", "얼굴은"),
        slot("method.tools", "hands", "손으로"),
        slot("method.water_temperature", "lukewarm", "미지근한 물에"),
        slot("moisturizing.after_wash_delay", "5분", "세안하고 5분 뒤에"),
    ],
    products=[product("보습제", "using")],
    why="부위·도구·물 온도·보습 간격은 각각 원문에 있어요. 5분은 단위까지 보존하고 효과는 추론하지 않아요.",
)
case(
    "turn1_utterance",
    "removal_steps",
    "워터프루프 선크림을 바른 날에는 그 이유만으로 무조건 두 번 연달아 세안해요.",
    ["repeat_cleansing"],
    slots=[
        slot(
            "cleansing.steps",
            "repeated_only_because_water_resistant",
            "그 이유만으로 무조건 두 번 연달아 세안해요",
        )
    ],
    products=[product("워터프루프 선크림", "using")],
    why="B-I01의 원인 조건인 내수성만을 이유로 한 반복을 표준 문자열로 옮겨요. 제품의 실제 내수성 검증이나 변경 권고는 하지 않아요.",
)
case(
    "turn1_utterance",
    "outdoor_water_sweat",
    "수영하고 나와서 땀도 많이 났고, 모자는 쓰고 있었어요.",
    ["outdoor_sun"],
    slots=[
        slot("sun.water_contact", "yes", "수영하고 나와서"),
        slot("sun.sweat", "yes", "땀도 많이 났고"),
        slot("sun.shade_clothing", "모자 착용", "모자는 쓰고 있었어요"),
    ],
    why="물 접촉·발한·모자는 별도 후보예요. 재도포 필요성이나 보호 성능을 판단하지 않아요.",
)
case(
    "turn1_utterance",
    "moisture_sensation_delay",
    "로션을 바를 때마다 끈적하고, 매번 두 시간쯤 지나면 다시 건조해져요.",
    ["moisturizing", "discomfort_report"],
    slots=[
        slot("moisturizing.comfort", "끈적함", "끈적하고"),
        slot(
            "moisturizing.dryness_return",
            "두 시간쯤",
            "매번 두 시간쯤 지나면 다시 건조해져요",
        ),
    ],
    symptoms=[
        symptom(
            "dryness", "매번 두 시간쯤 지나면 다시 건조해져요", persistence="repeated"
        )
    ],
    products=[product("로션", "using")],
    why="반복 조건과 대략적 시간은 보존해요. 건조감의 반복과 제품 효능·성분 사실은 구분해요.",
)
case(
    "turn1_utterance",
    "storage_light_opened",
    "이 크림은 지난주 토요일에 열었고 욕실 창가에 두고 쓰고 있어요.",
    ["storage_label"],
    slots=[
        slot("storage.opened_at", "지난주 토요일", "지난주 토요일에 열었고"),
        slot("storage.light_air", "욕실 창가 보관", "욕실 창가에 두고"),
    ],
    products=[product("크림", "using")],
    why="상대 날짜를 실제 달력 날짜로 만들지 않고 보관 위치만 추출해요. 고온·변질·사용기한을 추정하지 않아요.",
)
case(
    "turn1_utterance",
    "wash_touch_mechanics",
    "세안할 때 브러시로 세게 문지르고 수건으로도 박박 비벼 닦아요.",
    ["cleansing_method"],
    slots=[
        slot("method.tools", "scrub_brush", "브러시로"),
        slot("method.friction", "strong", "세게 문지르고"),
        slot("method.drying", "rubbing_strongly", "수건으로도 박박 비벼 닦아요"),
    ],
    why="도구·마찰·물기 마무리를 분리하고 피부 손상이나 증상을 덧붙이지 않아요.",
)
case(
    "turn1_utterance",
    "routine_order",
    "저녁에는 보습제를 먼저 바르고 그다음 차단제를 발라요. 이 순서가 맞는지 궁금해요.",
    ["routine_conflict", "moisturizing", "outdoor_sun"],
    slots=[
        slot(
            "method.sequence",
            "보습제 다음 차단제",
            "보습제를 먼저 바르고 그다음 차단제를 발라요",
        )
    ],
    products=[product("보습제", "using"), product("차단제", "using")],
    why="질문의 정답을 설명하지 않고 실제로 보고한 순서만 후보로 남겨요.",
)

# 2. 자유 타이핑 후속 발화: 근거 구절은 반드시 현재 source_text 안에 있어요.
case(
    "turn2_followup",
    "wash_temperature",
    "뜨겁지는 않고 미지근해요.",
    ["cleansing_method"],
    previous="세안할 때 물 온도는 어떤가요?",
    target="method.water_temperature",
    slots=[
        slot("method.water_temperature", "hot", "뜨겁지는 않고", polarity="denied"),
        slot("method.water_temperature", "lukewarm", "미지근해요"),
    ],
    why="직전 질문으로 물 온도를 해석하되 부정된 hot과 명시된 lukewarm을 구분해요.",
)
case(
    "turn2_followup",
    "removal_steps",
    "제품 표시대로 한 번만 해요.",
    ["repeat_cleansing"],
    previous="한 번 씻을 때 세정 단계를 몇 번 거치나요?",
    target="cleansing.steps",
    slots=[slot("cleansing.steps", 1, "한 번만 해요")],
    why="질문에 대한 실제 횟수 1을 정수로 추출해요. 제품 자체의 제거 성능은 만들지 않아요.",
)
case(
    "turn2_followup",
    "moisturizer_site",
    "팔에는 바르는데 다리에는 안 발라요.",
    ["moisturizing"],
    previous="보습제를 어느 부위에 바르나요?",
    target="moisturizing.coverage",
    slots=[
        slot("moisturizing.coverage", ["팔"], "팔에는 바르는데"),
        slot(
            "moisturizing.coverage", ["다리"], "다리에는 안 발라요", polarity="denied"
        ),
    ],
    why="같은 질문의 부위별 긍정·부정을 나눠요. 다른 부위까지 사용 여부를 채우지 않아요.",
)
case(
    "turn2_followup",
    "outdoor_duration",
    "점심부터 해 질 때까지 계속 밖에 있어요.",
    ["outdoor_sun"],
    previous="야외에 머무는 시간은 어느 정도인가요?",
    target="sun.outdoor_time",
    slots=[
        slot("sun.outdoor_time", "prolonged", "점심부터 해 질 때까지 계속 밖에 있어요")
    ],
    why="장시간 야외라는 범주만 옮기며 지역별 일몰시각이나 숫자 시간을 추정하지 않아요.",
)
case(
    "turn2_followup",
    "opened_date_unknown",
    "언제 열었는지는 기억이 안 나요.",
    ["storage_label"],
    previous="지금 쓰는 제품은 언제 개봉했나요?",
    target="storage.opened_at",
    slots=[
        slot(
            "storage.opened_at",
            None,
            "언제 열었는지는 기억이 안 나요",
            polarity="unknown",
        )
    ],
    why="개봉일 미상을 null로 보존해요. 구매일이나 오늘 날짜로 대체하지 않아요.",
)
case(
    "turn2_followup",
    "wash_touch_mechanics",
    "손이 아니라 스펀지로 씻어요.",
    ["cleansing_method"],
    previous="피부를 씻을 때 어떤 도구를 사용하나요?",
    target="method.tools",
    slots=[
        slot("method.tools", "hands", "손이 아니라", polarity="denied"),
        slot("method.tools", "sponge", "스펀지로 씻어요"),
    ],
    why="도구의 명시적 정정만 반영하고 스펀지의 청결도·강도를 추론하지 않아요.",
)
case(
    "turn2_followup",
    "eye_stinging_context",
    "한 번이 아니라 씻을 때마다 눈이 시려요.",
    ["discomfort_report"],
    previous="눈이 시린 증상은 한 번 있었나요, 반복되나요?",
    target="skin.eye_symptom_context",
    symptoms=[
        symptom("eye_stinging", "씻을 때마다 눈이 시려요", persistence="repeated")
    ],
    why="반복되는 눈 시림만 추출해요. 눈에 제품이 직접 들어갔다거나 눈 질환이라고 단정하지 않아요.",
)

# 3. 명시적 부정: enum 값 자체를 임의의 반대값으로 치환하지 않아요.
case(
    "denied_polarity",
    "wash_temperature",
    "뜨거운 물로 씻지 않아요.",
    ["cleansing_method"],
    slots=[
        slot(
            "method.water_temperature",
            "hot",
            "뜨거운 물로 씻지 않아요",
            polarity="denied",
        )
    ],
    why="hot을 부정할 뿐 cold 또는 lukewarm을 긍정하지 않아요.",
)
case(
    "denied_polarity",
    "wash_touch_mechanics",
    "브러시는 안 써요.",
    ["cleansing_method"],
    slots=[slot("method.tools", "scrub_brush", "브러시는 안 써요", polarity="denied")],
    why="브러시 미사용만 추출하며 손이나 수건을 쓴다고 채우지 않아요.",
)
case(
    "denied_polarity",
    "wash_touch_mechanics",
    "세게 문지르는 건 아니에요.",
    ["cleansing_method"],
    slots=[
        slot(
            "method.friction", "strong", "세게 문지르는 건 아니에요", polarity="denied"
        )
    ],
    why="강한 마찰 부정을 gentle의 실제 확인으로 바꾸지 않아요.",
)
case(
    "denied_polarity",
    "wash_touch_mechanics",
    "수건으로 박박 비비지는 않아요.",
    ["cleansing_method"],
    slots=[
        slot(
            "method.drying",
            "rubbing_strongly",
            "수건으로 박박 비비지는 않아요",
            polarity="denied",
        )
    ],
    why="강하게 닦기 부정을 pat_gently 확인으로 바꾸지 않아요.",
)
case(
    "denied_polarity",
    "outdoor_water_sweat",
    "오늘 야외에서는 물에 닿지 않았어요.",
    ["outdoor_sun"],
    slots=[slot("sun.water_contact", "yes", "물에 닿지 않았어요", polarity="denied")],
    why="물 접촉 yes 명제를 부정해요. 다른 시간대의 접촉 이력은 만들지 않아요.",
)
case(
    "denied_polarity",
    "outdoor_water_sweat",
    "운동했지만 땀은 나지 않았어요.",
    ["outdoor_sun"],
    slots=[slot("sun.sweat", "yes", "땀은 나지 않았어요", polarity="denied")],
    why="운동을 발한으로 자동 변환하지 않고 명시적 부정을 유지해요.",
)
case(
    "denied_polarity",
    "symptom_negation",
    "따갑거나 가렵지 않아요.",
    ["discomfort_report"],
    symptoms=[
        symptom("stinging", "따갑거나 가렵지 않아요", polarity="denied"),
        symptom("itching", "따갑거나 가렵지 않아요", polarity="denied"),
    ],
    why="두 증상의 부정을 추출하고 모든 불편이 없다고 넓히지 않아요.",
)

# 4. 타인 경험: 자기 상태·증상으로 옮기지 않아요.
case(
    "other_subject",
    "wash_temperature",
    "동생은 찬물로 얼굴을 씻는대요.",
    ["cleansing_method"],
    slots=[
        slot(
            "method.water_temperature",
            "cold",
            "동생은 찬물로 얼굴을 씻는대요",
            subject="other",
        ),
        slot(
            "method.body_site", "face", "동생은 찬물로 얼굴을 씻는대요", subject="other"
        ),
    ],
    why="물 온도와 얼굴 부위의 주어를 모두 other로 유지해요.",
)
case(
    "other_subject",
    "other_lotion_itch",
    "친구가 로션 B를 바른 뒤 어제부터 가렵다고 해요.",
    ["moisturizing", "discomfort_report"],
    symptoms=[
        symptom(
            "itching",
            "친구가 로션 B를 바른 뒤 어제부터 가렵다고 해요",
            subject="other",
            persistence="recent",
        )
    ],
    products=[product("로션 B", "other_person")],
    why="친구의 최근 가려움과 제품 언급만 추출해요. 인과관계나 본인의 반응은 판단하지 않아요.",
)
case(
    "other_subject",
    "outdoor_duration",
    "아빠는 하루 종일 밖에서 일하고 챙 넓은 모자를 쓰세요.",
    ["outdoor_sun"],
    slots=[
        slot(
            "sun.outdoor_time",
            "prolonged",
            "아빠는 하루 종일 밖에서 일하고",
            subject="other",
        ),
        slot(
            "sun.shade_clothing",
            "챙 넓은 모자 착용",
            "아빠는 하루 종일 밖에서 일하고 챙 넓은 모자를 쓰세요",
            subject="other",
        ),
    ],
    why="다른 사람의 장시간 야외와 모자 사용을 분리하며 사용자 본인의 노출로 저장하지 않아요.",
)
case(
    "other_subject",
    "other_hand_dryness",
    "친구는 손등이 건조하대요. 저는 제 피부 얘기는 아직 안 했어요.",
    ["discomfort_report"],
    symptoms=[symptom("dryness", "친구는 손등이 건조하대요", subject="other")],
    why="친구의 건조함만 후보예요. 자기 피부 미보고를 자기 건조함 부정으로 바꾸지 않아요.",
)
case(
    "other_subject",
    "other_product_routine",
    "엄마는 수분크림 C를 매일 쓰고 계세요.",
    ["moisturizing"],
    slots=[
        slot(
            "method.current_routine",
            "수분크림 C 매일 사용",
            "엄마는 수분크림 C를 매일 쓰고 계세요",
            subject="other",
        )
    ],
    products=[product("수분크림 C", "other_person")],
    why="루틴 주어와 제품 사용 주체는 엄마예요. 성분·농도는 추출하지 않아요.",
)
case(
    "other_subject",
    "other_decanting",
    "룸메이트는 쓰던 화장수를 다른 용기에 덜어 썼대요.",
    ["storage_label"],
    slots=[
        slot(
            "storage.decanting",
            "다른 용기로 소분",
            "룸메이트는 쓰던 화장수를 다른 용기에 덜어 썼대요",
            subject="other",
        )
    ],
    products=[product("화장수", "other_person")],
    why="타인의 소분 사실만 추출하고 용기 손상·오염 여부를 추가하지 않아요.",
)
case(
    "other_subject",
    "eye_stinging_context",
    "언니는 선크림을 쓰고 눈이 시리대요. 저는 오늘 실내에서만 지냈어요.",
    ["discomfort_report", "outdoor_sun"],
    slots=[slot("sun.outdoor_time", "none", "저는 오늘 실내에서만 지냈어요")],
    symptoms=[
        symptom("eye_stinging", "언니는 선크림을 쓰고 눈이 시리대요", subject="other")
    ],
    products=[product("선크림", "other_person")],
    why="타인의 눈 시림과 본인의 실내 체류를 서로 다른 주어로 유지해요.",
)

# 5. 증상 후보: 11종 어휘와 지속성은 원문 수준에서만 정해요.
case(
    "high_risk_symptom",
    "persistent_redness_pain",
    "며칠째 계속 볼이 붉고 아파요.",
    ["discomfort_report"],
    symptoms=[
        symptom("redness", "며칠째 계속 볼이 붉고 아파요", persistence="persistent"),
        symptom("pain", "며칠째 계속 볼이 붉고 아파요", persistence="persistent"),
    ],
    why="지속된 붉음과 통증을 별도 후보로 남기고 질환을 진단하지 않아요.",
)
case(
    "high_risk_symptom",
    "new_burning",
    "방금 얼굴이 화끈거리기 시작했어요.",
    ["discomfort_report"],
    symptoms=[
        symptom("burning", "방금 얼굴이 화끈거리기 시작했어요", persistence="recent")
    ],
    why="방금 시작된 화끈거림을 recent로 표현하고 원인 제품은 만들지 않아요.",
)
case(
    "high_risk_symptom",
    "swelling_onset_unknown",
    "입가가 부었는데 언제부터인지는 잘 모르겠어요.",
    ["discomfort_report"],
    symptoms=[
        symptom(
            "swelling",
            "입가가 부었는데 언제부터인지는 잘 모르겠어요",
            persistence="unknown",
        )
    ],
    why="붓기는 언급됐지만 시작·지속성은 미상이에요. 최근 발생이라고 바꾸지 않아요.",
)
case(
    "high_risk_symptom",
    "repeated_peeling",
    "세수할 때마다 피부가 벗겨지는 일이 반복돼요.",
    ["discomfort_report"],
    symptoms=[
        symptom(
            "peeling",
            "세수할 때마다 피부가 벗겨지는 일이 반복돼요",
            persistence="repeated",
        )
    ],
    why="반복이라는 명시적 빈도를 유지하고 한 번의 최근 발생이나 지속 상태로 바꾸지 않아요.",
)
case(
    "high_risk_symptom",
    "new_tightness",
    "세수는 평소처럼 했는데, 볼이 당기는 증상은 오늘 처음 시작됐어요.",
    ["discomfort_report"],
    symptoms=[
        symptom(
            "tightness", "볼이 당기는 증상은 오늘 처음 시작됐어요", persistence="recent"
        )
    ],
    why="증상의 시작 시점이 명시된 당김만 추출하며 장벽 손상이나 원인을 추가하지 않아요.",
)
case(
    "high_risk_symptom",
    "persistent_breakout",
    "트러블이 몇 주째 계속 남아 있어요.",
    ["discomfort_report"],
    symptoms=[
        symptom(
            "breakout", "트러블이 몇 주째 계속 남아 있어요", persistence="persistent"
        )
    ],
    why="트러블이라는 표준 후보를 사용하고 여드름 진단이나 치료 답변으로 확장하지 않아요.",
)
case(
    "high_risk_symptom",
    "repeated_discomfort_cluster",
    "최근 들어 씻을 때마다 건조하고 가렵고 따가워요.",
    ["discomfort_report"],
    symptoms=[
        symptom(
            name,
            "최근 들어 씻을 때마다 건조하고 가렵고 따가워요",
            persistence="repeated",
        )
        for name in ["dryness", "itching", "stinging"]
    ],
    why="최근이라는 시작 표현보다 '때마다'의 반복 양상을 지속성 분류에 반영해요. 세 증상 모두 후보이며 자동 확인하지 않아요.",
)

# 6. 제품명은 hint가 있어도 확정 제품 사실이 아니에요. 접두사 충돌을 포함해요.
case(
    "product_mention",
    "known_lotion_using",
    "라임 로션 A를 요즘 매일 쓰고 있어요.",
    ["moisturizing"],
    products=[product("라임 로션 A", "using", "syn-catalog:lime-lotion-a@v1")],
    hints=[hint("라임 로션 A", "syn-catalog:lime-lotion-a@v1")],
    why="정확히 같은 raw span의 가상 카탈로그 힌트만 연결해요. 이름으로 농도·효능을 추출하지 않아요.",
)
case(
    "product_mention",
    "unregistered_cream",
    "크림 Z를 요즘 쓰고 있는데 검색에는 안 나오더라고요.",
    ["moisturizing"],
    products=[product("크림 Z", "using")],
    why="현재 사용과 미등록 제품명을 보존하고 catalog hint를 만들어 넣지 않아요.",
)
case(
    "product_mention",
    "product_prefix_collision",
    "지금은 Lotion AB를 써 볼까 생각 중이에요.",
    ["moisturizing"],
    products=[product("Lotion AB", "considering")],
    hints=[hint("Lotion A", "syn-catalog:lotion-a@v1")],
    why="Lotion A는 원문 부분 문자열이지만 Lotion AB와 동일 span이 아니므로 matched_catalog_hint는 null이에요.",
)
case(
    "product_mention",
    "stopped_lotion",
    "Lotion A는 이제 안 써요.",
    ["moisturizing"],
    products=[product("Lotion A", "stopped", "syn-catalog:lotion-a@v1")],
    hints=[hint("Lotion A", "syn-catalog:lotion-a@v1")],
    why="정확한 힌트는 연결하되 사용 상태는 stopped예요. 성분·안전성은 만들지 않아요.",
)
case(
    "product_mention",
    "other_gel_product",
    "동생이 젤 Q를 쓰고 있어요.",
    ["other"],
    products=[product("젤 Q", "other_person")],
    why="도포 목적이나 피부 상태는 알 수 없어요. 주체가 타인인 제품 언급만 남겨요.",
)
case(
    "product_mention",
    "product_usage_unknown",
    "세럼 R이라는 이름만 들었고 누가 쓰는지는 몰라요.",
    ["other"],
    products=[product("세럼 R", "unknown")],
    why="사용 여부·주체가 불명확하므로 using이나 considering으로 추측하지 않아요.",
)
case(
    "product_mention",
    "product_prefix_collision",
    "로션 M은 살까 고민 중이고 지금 바르는 건 로션 MN이에요.",
    ["moisturizing"],
    products=[
        product("로션 M", "considering", "syn-catalog:lotion-m@v1"),
        product("로션 MN", "using"),
    ],
    hints=[hint("로션 M", "syn-catalog:lotion-m@v1")],
    why="M은 정확히 일치하는 힌트가 있지만 MN에는 연결하지 않아요. 두 제품의 사용 상태도 분리해요.",
)

# 7. 무관·추출 불가 자유 발화. 온보딩 폼·버튼 탭 입력은 없어요.
case(
    "no_signal_noise",
    "greeting_only",
    "안녕하세요, 반가워요.",
    [],
    why="인사만 있으므로 슬롯·증상·제품 후보가 없어요.",
)
case(
    "no_signal_noise",
    "unrelated_meal",
    "오늘 점심은 김밥 먹었어요.",
    [],
    why="식사 발화에서 피부 효과·상태를 추론하지 않아요.",
)
case(
    "no_signal_noise",
    "filler_only",
    "음… 어…",
    [],
    why="추출할 구체적 내용이 없는 머뭇거림이에요.",
)
case(
    "no_signal_noise",
    "unrelated_delivery",
    "택배가 내일 온대요.",
    [],
    why="배송 발화만으로 화장품 구매·보유·사용을 만들지 않아요.",
)
case(
    "no_signal_noise",
    "unrelated_device",
    "휴대폰 배터리가 거의 없어요.",
    [],
    why="기기 상태는 이 NLU의 피부·제품 후보가 아니에요.",
)
case(
    "no_signal_noise",
    "emoji_only",
    "✅",
    [],
    why="정형 버튼 탭이 아닌 자유 채팅 문자예요. 추출할 사실이 없어요.",
)
case(
    "no_signal_noise",
    "missing_chat_context",
    "이어서요.",
    [],
    why="직전 질문이 없는 단독 발화이므로 대상 슬롯을 임의로 정하지 않아요.",
)

VAL_FAMILIES = {
    "swelling_onset_unknown",
    "persistent_breakout",
    "product_prefix_collision",
    "emoji_only",
}


def write(path, value, *, jsonl=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = (
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in value)
        if jsonl
        else json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def content_hash(row):
    value = {k: row[k] for k in ["id", "scenario_family_id", "split", "primary_bucket"]}
    value["system"] = row["messages"][0]["content"]
    value["request"] = json.loads(row["messages"][1]["content"])
    value["expected"] = json.loads(row["messages"][2]["content"])
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()


def main():
    assert len(CASES) == 49 and set(CORE_SLOTS) <= load_nlu_whitelist().variable_ids
    assert all(v == 7 for v in Counter(c["bucket"] for c in CASES).values())
    rows = []
    review = []
    for i, c in enumerate(CASES, 1):
        req = NLURequest(
            source_text=c["text"],
            catalog_hints=c["hints"],
            previous_question=c["previous"],
            target_slot_id=c["target"],
            allowed_variable_ids=CORE_SLOTS,
            allowed_symptoms=sorted(ALLOWED_SYMPTOMS),
            allowed_topics=sorted(ALLOWED_TOPICS),
        )
        ext = NLUExtractionResult(
            source_text=c["text"],
            topics=c["topics"],
            slot_candidates=c["slots"],
            symptom_candidates=c["symptoms"],
            product_mentions=c["products"],
            confirmed_by_user=False,
        )
        verify_nlu_extraction(ext, request=req)
        row = {
            "id": f"nlu-pilot-{i:04d}",
            "scenario_family_id": "nlu-v1-" + c["family"],
            "split": "val_internal" if c["family"] in VAL_FAMILIES else "train",
            "primary_bucket": c["bucket"],
            "messages": build_nlu_messages(req)
            + [{"role": "assistant", "content": ext.model_dump_json()}],
            "provenance": {
                "source_origin": "new_synthetic",
                "generator_model": "gpt-6",
                "critic_status": "unreviewed",
                "human_review": "unreviewed",
            },
            "runtime_invariants": {
                "mode": "development_preview",
                "production_enabled": False,
                "requires_approval": True,
                "saved": False,
            },
        }
        rows.append(row)
        review.append(
            {
                "row_id": row["id"],
                "content_sha256": content_hash(row),
                "scenario_family_id": row["scenario_family_id"],
                "split": row["split"],
                "primary_bucket": c["bucket"],
                "request": json.loads(row["messages"][1]["content"]),
                "expected": ext.model_dump(mode="json"),
                "author_rationale": c["rationale"],
                "critic_status": "unreviewed",
                "human_review": "unreviewed",
            }
        )
    write(HERE / "pilot_nlu_v1.jsonl", rows, jsonl=True)
    write(HERE / "reviews/pilot_nlu_v1_critic_requests.jsonl", review, jsonl=True)
    write(
        HERE / "validation/generation_manifest.json",
        {
            "rows": 49,
            "primary_buckets": dict(Counter(c["bucket"] for c in CASES)),
            "splits": dict(Counter(r["split"] for r in rows)),
            "common_allowed_variable_count": len(CORE_SLOTS),
            "common_whitelist_is_not_gold_conditioned": True,
            "val_families": sorted(VAL_FAMILIES),
            "all_new_synthetic": True,
            "cross_model_critic_performed": False,
            "human_approved": False,
            "base_zero_shot_executed": False,
            "training_executed": False,
            "dataset_sha256": hashlib.sha256(
                (HERE / "pilot_nlu_v1.jsonl").read_bytes()
            ).hexdigest(),
            "row_hashes": {r["row_id"]: r["content_sha256"] for r in review},
            "model_identity_note": "GPT-6 기반 Codex 작성이며 세부 호스팅 변형은 확인되지 않아 추정하지 않았어요.",
        },
    )
    lines = [
        "# NLU 파일럿 49건 — 원문·예상 후보·작성 근거",
        "",
        "합성 작성본이며 독립 Critic·사람 검수·Base 모델 측정 결과가 아니에요.",
        "",
    ]
    for item in review:
        lines += [
            f"## {item['row_id']} · {item['primary_bucket']} · {item['split']}",
            "",
            f"가족: `{item['scenario_family_id']}`",
            "",
            "### 실제 자유 발화",
            "",
            item["request"]["source_text"],
            "",
            f"직전 질문: {item['request']['previous_question']}",
            f"대상 슬롯: {item['request']['target_slot_id']}",
            "",
            "### 예상 추출 JSON",
            "",
            "```json",
            json.dumps(item["expected"], ensure_ascii=False, indent=2),
            "```",
            "",
            "### 원문과 판단의 연결",
            "",
            item["author_rationale"],
            "",
            f"내용 SHA-256: `{item['content_sha256']}`",
            "",
        ]
    (HERE / "pilot_nlu_v1_review.md").write_text(
        "\n".join(lines), encoding="utf-8", newline="\n"
    )
    print(
        json.dumps(
            {
                "rows": len(rows),
                "primary_buckets": dict(Counter(c["bucket"] for c in CASES)),
                "splits": dict(Counter(r["split"] for r in rows)),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
