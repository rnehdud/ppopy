"""Tests for SyntheticCatalogAdapter, opt-in AuroraCatalogAdapter, and NLP product-query lookup."""
import json

from beauty_agent.catalog_adapter import AuroraCatalogAdapter, SyntheticCatalogAdapter
from beauty_agent.contracts import OwnedProduct
from beauty_agent.nlp_layer import NLPLayer
from beauty_agent.runtime import AgentRuntime
from beauty_agent.runtime_contracts import RuntimeTurnRequest


def test_synthetic_catalog_adapter_by_id_and_name():
    adapter = SyntheticCatalogAdapter()
    found_id = adapter.lookup_by_id(
        OwnedProduct(product_id="synthetic-cleanser-a", version="1.0.0", confirmed=True)
    )
    assert found_id.status == "found"
    assert found_id.data["name"] == "합성 순한 폼클렌저 A"

    unconfirmed = adapter.lookup_by_id(
        OwnedProduct(product_id="synthetic-cleanser-a", version="1.0.0", confirmed=False)
    )
    assert unconfirmed.status == "not_found"

    found_name = adapter.search_by_name("순한 폼클렌저 A")
    assert found_name.status == "found"
    assert found_name.data["product_id"] == "synthetic-cleanser-a"
    assert found_name.data["confirmed_ownership"] is False

    missing = adapter.search_by_name("존재하지 않는 크림")
    assert missing.status == "not_found"


def test_aurora_catalog_adapter_unconfigured_fails_safely(monkeypatch):
    for key in ("AURORA_CLUSTER_ARN", "AURORA_SECRET_ARN", "AURORA_DATABASE"):
        monkeypatch.delenv(key, raising=False)
    adapter = AuroraCatalogAdapter()
    assert adapter.is_configured() is False
    res = adapter.search_by_name("센카 퍼펙트휩")
    assert res.status == "failed"
    assert res.error_reason == "RuntimeError"


def test_aurora_catalog_adapter_parses_rds_data_api_response():
    captured_cmd: list[str] = []

    def fake_runner(cmd: list[str]) -> str:
        captured_cmd.extend(cmd)
        return json.dumps(
            {
                "columnMetadata": [
                    {"name": "product_id"},
                    {"name": "product_version"},
                    {"name": "public_brand_name"},
                    {"name": "public_product_name"},
                    {"name": "public_search_aliases"},
                    {"name": "verified_by_owner"},
                ],
                "records": [
                    [
                        {"stringValue": "prod-123"},
                        {"stringValue": "v2.1"},
                        {"stringValue": "합성 브랜드"},
                        {"stringValue": "합성 폼클렌저"},
                        {"isNull": True},
                        {"booleanValue": False},
                    ]
                ],
            }
        )

    adapter = AuroraCatalogAdapter(
        resource_arn="arn:aws:rds:ap-northeast-2:123456789012:cluster:test",
        secret_arn="arn:aws:secretsmanager:ap-northeast-2:123456789012:secret:test",
        database="ppopy_test",
        runner=fake_runner,
    )
    assert adapter.is_configured() is True
    res = adapter.search_by_name("합성 폼클렌저")
    assert res.status == "found"
    assert res.version == "v2.1"
    assert res.data["matches"][0]["product_id"] == "prod-123"
    assert res.data["confirmed_ownership"] is False
    assert "--parameters" in captured_cmd


def test_runtime_looks_up_nlp_extracted_product_queries():
    def fake_extractor(message: str) -> dict:
        return {
            "schema_version": "relations-0.5",
            "source_text": message,
            "segmentation_method": "kiwi_morpheme",
            "units": [{"unit_id": "u0", "start": 0, "end": len(message), "text": message}],
            "products": [
                {
                    "text": "합성 순한 폼클렌저 A",
                    "start": 0,
                    "end": 12,
                    "relations": {
                        "usage_state": {"value": "affirmed"},
                        "subject": {"value": "self"},
                        "correction": {"value": "current"},
                    },
                }
            ],
            "symptoms": [],
            "warnings": [],
            "clarifications": [],
        }

    runtime = AgentRuntime(nlp_layer=NLPLayer(extractor=fake_extractor))
    resp = runtime.handle_turn(
        RuntimeTurnRequest(
            request_id="test-prod-query",
            message="합성 순한 폼클렌저 A 쓰고 있어요",
        )
    )
    assert "lookup_product" in resp.executed_actions
    assert "product_query:합성 순한 폼클렌저 A" in resp.tool_results
    assert resp.tool_results["product_query:합성 순한 폼클렌저 A"].status == "found"
