"""Exercise the local runtime, KB, AFA, and catalog in the same request."""

import pytest

from beauty_agent.catalog_adapter import SyntheticCatalogAdapter
from beauty_agent.contracts import ObservationSlot, OwnedProduct, Profile
from beauty_agent.nlp_layer import interpret_slot_answer
from beauty_agent.runtime import AgentRuntime
from beauty_agent.runtime_contracts import RuntimeTurnRequest


PRODUCT_ID = "synthetic-cleanser-a"
PRODUCT_KEY = f"product:{PRODUCT_ID}"
PRODUCT_REF = f"catalog:{PRODUCT_ID}@1.0.0"


def _observation(field, value, *, state="known"):
    return ObservationSlot(
        variable_id=field, value=value, state=state, confirmed_by_user=True,
    )


def _start_cleansing(runtime, *, tools_known):
    observations = {
        "method.body_site": _observation("method.body_site", "face"),
        "method.water_temperature": _observation("method.water_temperature", "lukewarm"),
    }
    if tools_known:
        observations["method.tools"] = _observation("method.tools", "scrub_brush")
    return runtime.handle_turn(RuntimeTurnRequest(
        request_id="cleansing-with-owned-product",
        message="세안 방법을 확인해 주세요.",
        profile=Profile(confirmed=True),
        products=[OwnedProduct(product_id=PRODUCT_ID, version="1.0.0", confirmed=True)],
        observations=observations,
    ))


def _answer_tools(runtime, response, *, products=None):
    field, = [question.id for question in response.questions]
    assert field == "method.tools"
    state, value = interpret_slot_answer(field, "세안 브러시를 써요")
    return runtime.handle_turn(RuntimeTurnRequest(
        request_id=response.request_id,
        observations={field: _observation(field, value, state=state)},
        products=products,
    ))


@pytest.mark.parametrize("tools_known", [True, False], ids=["no-question", "ask-and-resume"])
def test_confirmed_context_and_catalog_lead_to_cleansing_recommendation(tools_known):
    runtime = AgentRuntime(catalog_adapter=SyntheticCatalogAdapter())
    first = _start_cleansing(runtime, tools_known=tools_known)
    assert first.tool_results[PRODUCT_KEY].status == "found"
    assert first.tool_results[PRODUCT_KEY].source == "synthetic_catalog"
    lookups = first.executed_actions[:-1]
    assert lookups and set(lookups) == {"lookup_product"}
    final = first
    if tools_known:
        assert first.executed_actions[-1] == "recommend"
    else:
        assert first.status == "awaiting_user"
        assert first.executed_actions[-1] == "ask_user"
        assert not first.recommendation and not first.afa_handoff
        final = _answer_tools(runtime, first)
        assert final.executed_actions == ["recommend"]
        assert final.tool_results == first.tool_results

    assert final.status == "completed"
    assert final.request_id == first.request_id
    assert not final.questions and not final.required_product_evidence
    assert final.afa_handoff.status == "sufficient"
    assert final.afa_handoff.asked_feature_order == ([] if tools_known else ["method.tools"])
    assert final.afa_handoff.acquired_features["method.water_temperature"].value == "lukewarm"
    assert final.afa_handoff.acquired_features["method.tools"].value == "scrub_brush"
    assert runtime.get_session(first.request_id).turn_index == (1 if tools_known else 2)

    bundle = final.recommendation
    owned, = bundle.owned_product_usage
    assert owned.product_id == PRODUCT_ID
    assert owned.evidence_refs == [PRODUCT_REF]
    assert owned.guidance == first.tool_results[PRODUCT_KEY].data["label_guidance"]
    assert any("kb:B-C02" in item.evidence_refs for item in bundle.lifestyle_adjustments)
    assert bundle.requires_approval and not bundle.saved
    assert final.mode == "development_preview" and not final.production_enabled


@pytest.mark.parametrize("catalog_has_label", [False, True], ids=["catalog-miss", "label-only"])
def test_required_kb_evidence_stays_unknown_after_local_lookup(catalog_has_label):
    catalog = SyntheticCatalogAdapter() if catalog_has_label else SyntheticCatalogAdapter({})
    runtime = AgentRuntime(catalog_adapter=catalog)
    observations = {
        "method.body_site": _observation("method.body_site", "face"),
        "cleansing.target_load": _observation("cleansing.target_load", "no_additional_removal_need"),
        # An unresolved structured requirement stays open after these declined answers.
        **{
            field: _observation(field, None, state="declined")
            for field in ("cleansing.repeat_wash", "cleansing.steps", "dose.frequency", "method.current_routine")
        },
    }
    result = runtime.handle_turn(RuntimeTurnRequest(
        request_id="cleansing-with-missing-product-evidence",
        products=[OwnedProduct(product_id=PRODUCT_ID, version="1.0.0", confirmed=True)],
        observations=observations,
    ))

    assert result.tool_results[PRODUCT_KEY].status == ("found" if catalog_has_label else "not_found")
    assert result.status == "held"
    assert result.executed_actions == ["lookup_product", "hold"]
    assert result.required_product_evidence == ["product.instructions"]
    assert result.afa_handoff.status == "insufficient"
    assert "product.instructions" not in result.afa_handoff.acquired_features
    assert not result.questions and not result.recommendation


def test_user_report_cannot_fill_required_catalog_evidence():
    runtime = AgentRuntime()
    with pytest.raises(ValueError, match=r"invalid user observation slot: product\.instructions"):
        runtime.handle_turn(RuntimeTurnRequest(
            request_id="reported-product-instructions",
            observations={
                "product.instructions": _observation(
                    "product.instructions", "specific_instruction_overrides_general",
                ),
            },
        ))


@pytest.mark.parametrize(
    ("version", "confirmed", "lookup_status"),
    [("2.0.0", True, "found"), ("1.0.0", False, "not_found")],
    ids=["version-changed", "confirmation-withdrawn"],
)
def test_resume_does_not_recommend_a_stale_product_label(version, confirmed, lookup_status):
    runtime = AgentRuntime(catalog_adapter=SyntheticCatalogAdapter())
    first = _start_cleansing(runtime, tools_known=False)
    assert first.tool_results[PRODUCT_KEY].version == "1.0.0"
    final = _answer_tools(
        runtime, first, products=[OwnedProduct(product_id=PRODUCT_ID, version=version, confirmed=confirmed)],
    )
    assert final.status == "completed"
    assert final.executed_actions.count("lookup_product") == 1
    assert final.tool_results[PRODUCT_KEY].status == lookup_status
    assert not final.recommendation.owned_product_usage
    assert not final.recommendation.alternatives
    assert final.executed_actions[-1] == "recommend"
    assert [(item.product_id, item.disposition) for item in final.recommendation.exclusions_or_holds] == [
        (PRODUCT_ID, "usage_held")
    ]
