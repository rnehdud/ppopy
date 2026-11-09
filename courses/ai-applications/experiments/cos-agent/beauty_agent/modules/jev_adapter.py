"""Explicit remote Jev opt-in, with conservative offline candidate fallback."""
from copy import deepcopy
import re

from poc.jev.relations import extract_features, SYMPTOM_ANCHORS
from poc.jev.segmenter import units, segmentation_method
from poc.jev.mapping_review.review import SUPPORTED_SCHEMAS


class JevExtractorAdapter:
    def __init__(self, key=None, extractor=None):
        self.key = key
        self.extractor = extractor

    def extract(self, message):
        if self.extractor is not None:
            return self.extractor(message)
        if self.key:
            result = extract_features(message, self.key)
            result["extraction_failed"] = bool(result.get("warnings"))
            return result
        # Offline detection asserts neither subject, polarity nor time. It is not
        # a Jev inference, and never changes profile/product/observation facts.
        spans = units(message)
        symptoms = [{"symptom": name, "relations": {
            "state": {"value": "unknown"}, "subject": {"value": "unknown"}}}
            for name, pattern in SYMPTOM_ANCHORS.items() if re.search(pattern, message)]
        return {"schema_version": "relations-0.3", "products": [],
                "symptoms": symptoms, "units": spans,
                "segmentation_method": segmentation_method(),
                "warnings": ["offline_candidate_detection_not_jev_inference"],
                "clarifications": []}

    @staticmethod
    def to_mapping_review_features(features):
        if features.get("schema_version") not in SUPPORTED_SCHEMAS:
            raise ValueError("unsupported relations schema")
        # Current main reviews 0.2–0.5 directly. Downgrading a modern header
        # would bypass its assessment-metadata checks through the legacy path.
        return deepcopy(features)
