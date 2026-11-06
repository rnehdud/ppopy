"""Deliberately fictional fixtures; not cosmetic or medical evidence."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    product_id: str
    version: str
    name: str
    order: int
    periods: tuple[str, ...]
    instruction: str
    evidence_id: str


CATALOG = {
    "demo-cleanser": Product("demo-cleanser", "fixture-v1", "합성 클렌저", 1,
                            ("pm",), "저녁에 씻어내는 합성 사용법", "fixture-label-cleanser-v1"),
    "demo-moisturizer": Product("demo-moisturizer", "fixture-v1", "합성 보습제", 2,
                               ("am", "pm"), "아침과 저녁에 바르는 합성 사용법", "fixture-label-moisturizer-v1"),
}
RULE_VERSION = "fixture-label-order-v1"
