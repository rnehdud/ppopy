"""Return the selected field of the exact, confirmed product version."""
from datetime import datetime, timezone

from .runtime_contracts import FoundProductEvidence, UnavailableProductEvidence


def lookup_product_evidence(selection, products, lookup):
    product = next((p for p in products if p.product_id == selection.product_id), None)

    def unavailable(reason):
        return UnavailableProductEvidence(selection=selection, reason=reason)

    if product is None or not product.confirmed or product.version != selection.version:
        return unavailable("product_or_version_not_confirmed")
    hit = lookup(product)
    if hit.status != "found":
        return unavailable(hit.status)
    if hit.query_key != product.product_id or hit.version != product.version or hit.version.strip().casefold() in {"", "unknown"}:
        return unavailable("catalog_identity_or_version_mismatch")
    fields = hit.data.get("label_fields")
    item = fields.get(selection.target_id) if isinstance(fields, dict) else None
    if not isinstance(item, dict):
        item = {"label_text": hit.data.get("label_guidance"), "evidence_ref": hit.data.get("evidence_ref"),
                "expires_at": hit.data.get("label_expires_at")} if selection.target_id == "product.instructions" else {}
    text, source = item.get("label_text"), item.get("evidence_ref")
    if not isinstance(text, str) or not text.strip() or not isinstance(source, str) or not source.strip():
        return unavailable("field_or_source_missing")
    expires_at = item.get("expires_at")
    if expires_at is not None:
        try:
            expiry = datetime.fromisoformat(expires_at)
            if expiry.utcoffset() is None:
                return unavailable("invalid_expiry")
        except (ValueError, TypeError):
            return unavailable("invalid_expiry")
        if expiry <= datetime.now(timezone.utc):
            return unavailable("expired")
    return FoundProductEvidence(selection=selection, label_text=text, evidence_ref=source,
                                freshness="version_only" if expires_at is None else "dated")
