"""Catalog adapter interface with synthetic default and read-only AWS Aurora Data API option."""
from __future__ import annotations

from copy import deepcopy
import json
import os
import subprocess
from typing import Callable, Protocol

from .contracts import OwnedProduct
from .runtime_contracts import ToolLookupResult

DEFAULT_SYNTHETIC_CATALOG: dict[str, dict] = {
    "synthetic-cleanser-a": {
        "product_id": "synthetic-cleanser-a",
        "name": "합성 순한 폼클렌저 A",
        "brand": "합성 브랜드",
        "aliases": ["순한 폼클렌저 A", "합성 폼클렌저 A"],
        "version": "1.0.0",
        "category": "cleanser",
        "label_guidance": "미온수로 거품을 내어 손으로 부드럽게 세안한 뒤 헹굽니다.",
        "evidence_ref": "catalog:synthetic-cleanser-a@1.0.0",
    },
    "synthetic-moisturizer-a": {
        "product_id": "synthetic-moisturizer-a",
        "name": "합성 장벽 보습 크림 A",
        "brand": "합성 브랜드",
        "aliases": ["장벽 크림 A", "합성 보습 크림 A"],
        "version": "1.0.0",
        "category": "moisturizer",
        "label_guidance": "세안 직후 적당량을 피부에 부드럽게 펴 바릅니다.",
        "evidence_ref": "catalog:synthetic-moisturizer-a@1.0.0",
    },
}


class CatalogAdapter(Protocol):
    """Read-only product catalog lookup contract."""

    def lookup_by_id(self, product: OwnedProduct) -> ToolLookupResult: ...

    def search_by_name(self, query_text: str) -> ToolLookupResult: ...


class SyntheticCatalogAdapter:
    """Offline synthetic catalog used when no external DB is configured."""

    def __init__(self, records: dict[str, dict] | None = None):
        self.records = deepcopy(records) if records is not None else deepcopy(DEFAULT_SYNTHETIC_CATALOG)

    def lookup_by_id(self, product: OwnedProduct) -> ToolLookupResult:
        record = self.records.get(product.product_id)
        if record is None or not product.confirmed:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=product.product_id,
                status="not_found",
                source="synthetic_catalog",
                data={"confirmed": product.confirmed, "requested_version": product.version},
                error_reason="unregistered_or_unconfirmed_product",
            )
        return ToolLookupResult(
            tool_name="product_catalog",
            query_key=product.product_id,
            status="found",
            source="synthetic_catalog",
            version=str(record["version"]),
            data=deepcopy(record),
        )

    def search_by_name(self, query_text: str) -> ToolLookupResult:
        needle = query_text.strip().casefold()
        if not needle:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key="empty",
                status="not_found",
                source="synthetic_catalog",
                error_reason="empty_query",
            )
        for record in self.records.values():
            candidates = [record.get("name", ""), record.get("product_id", ""), *record.get("aliases", [])]
            if any(needle in str(c).casefold() or str(c).casefold() in needle for c in candidates if c):
                return ToolLookupResult(
                    tool_name="product_catalog",
                    query_key=query_text,
                    status="found",
                    source="synthetic_catalog",
                    version=str(record.get("version", "unknown")),
                    data={**deepcopy(record), "confirmed_ownership": False},
                )
        return ToolLookupResult(
            tool_name="product_catalog",
            query_key=query_text,
            status="not_found",
            source="synthetic_catalog",
            data={"confirmed_ownership": False},
            error_reason="product_not_in_synthetic_catalog",
        )


def _rds_field_value(cell: dict) -> str | bool | int | float | None:
    if cell.get("isNull"):
        return None
    for key in ("stringValue", "booleanValue", "longValue", "doubleValue"):
        if key in cell:
            return cell[key]
    return None


class AuroraCatalogAdapter:
    """Opt-in read-only AWS Aurora PostgreSQL adapter via AWS CLI RDS Data API."""

    def __init__(
        self,
        *,
        resource_arn: str | None = None,
        secret_arn: str | None = None,
        database: str | None = None,
        region: str | None = None,
        runner: Callable[[list[str]], str] | None = None,
    ):
        self.resource_arn = resource_arn or os.environ.get("AURORA_CLUSTER_ARN", "").strip()
        self.secret_arn = secret_arn or os.environ.get("AURORA_SECRET_ARN", "").strip()
        self.database = database or os.environ.get("AURORA_DATABASE", "").strip()
        self.region = region or os.environ.get("AWS_REGION", "ap-northeast-2").strip()
        self._runner = runner

    def is_configured(self) -> bool:
        return bool(self.resource_arn and self.secret_arn and self.database)

    def _execute_readonly(self, sql: str, params: list[dict]) -> list[dict]:
        if not self.is_configured():
            raise RuntimeError("aurora_env_not_configured")
        cmd = [
            "aws",
            "rds-data",
            "execute-statement",
            "--region",
            self.region,
            "--resource-arn",
            self.resource_arn,
            "--secret-arn",
            self.secret_arn,
            "--database",
            self.database,
            "--sql",
            sql,
            "--parameters",
            json.dumps(params, ensure_ascii=False),
            "--include-result-metadata",
            "--output",
            "json",
        ]
        if self._runner is not None:
            raw = self._runner(cmd)
        else:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15, check=True)
            raw = proc.stdout
        payload = json.loads(raw)
        cols = [col.get("name", f"col_{i}") for i, col in enumerate(payload.get("columnMetadata", []))]
        rows: list[dict] = []
        for record in payload.get("records", []):
            rows.append({cols[i]: _rds_field_value(cell) for i, cell in enumerate(record)})
        return rows

    def lookup_by_id(self, product: OwnedProduct) -> ToolLookupResult:
        if not product.confirmed:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=product.product_id,
                status="not_found",
                source="aurora_rds_data_api",
                error_reason="unconfirmed_product",
            )
        sql = (
            "SELECT product_id, product_version, public_brand_name, public_product_name, "
            "public_search_aliases, verified_by_owner "
            "FROM catalog.product_fact "
            "WHERE product_id = :pid "
            "LIMIT 1"
        )
        params = [{"name": "pid", "value": {"stringValue": product.product_id}}]
        try:
            rows = self._execute_readonly(sql, params)
        except Exception as exc:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=product.product_id,
                status="failed",
                source="aurora_rds_data_api",
                error_reason=type(exc).__name__,
            )
        if not rows:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=product.product_id,
                status="not_found",
                source="aurora_rds_data_api",
            )
        row = rows[0]
        return ToolLookupResult(
            tool_name="product_catalog",
            query_key=product.product_id,
            status="found",
            source="aurora_rds_data_api",
            version=str(row.get("product_version") or "unknown"),
            data=row,
        )

    def search_by_name(self, query_text: str) -> ToolLookupResult:
        cleaned = query_text.strip()
        if not cleaned:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key="empty",
                status="not_found",
                source="aurora_rds_data_api",
                error_reason="empty_query",
            )
        sql = (
            "SELECT product_id, product_version, public_brand_name, public_product_name, "
            "public_search_aliases, verified_by_owner "
            "FROM catalog.product_fact "
            "WHERE public_product_name ILIKE :q "
            "OR public_brand_name ILIKE :q "
            "OR public_search_aliases::text ILIKE :q "
            "LIMIT 5"
        )
        params = [{"name": "q", "value": {"stringValue": f"%{cleaned}%"}}]
        try:
            rows = self._execute_readonly(sql, params)
        except Exception as exc:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=cleaned,
                status="failed",
                source="aurora_rds_data_api",
                error_reason=type(exc).__name__,
            )
        if not rows:
            return ToolLookupResult(
                tool_name="product_catalog",
                query_key=cleaned,
                status="not_found",
                source="aurora_rds_data_api",
                data={"confirmed_ownership": False},
            )
        first = rows[0]
        return ToolLookupResult(
            tool_name="product_catalog",
            query_key=cleaned,
            status="found",
            source="aurora_rds_data_api",
            version=str(first.get("product_version") or "unknown"),
            data={"matches": rows, "confirmed_ownership": False},
        )
