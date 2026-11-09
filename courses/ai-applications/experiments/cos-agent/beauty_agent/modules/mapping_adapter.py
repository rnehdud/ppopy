"""Mapping review never promotes candidates to observations."""
from datetime import datetime, timezone

from poc.jev.mapping_review.review import review
from .jev_adapter import JevExtractorAdapter


class MappingReviewAdapter:
    def evaluate(self, features, skin_state=None):
        if skin_state is None:
            skin_state = {"version": "1.0.0", "kind": "baseline",
                          "observed_at": datetime.now(timezone.utc).isoformat(),
                          "discomfort_types": []}
            for field in ("concern_presence", "persistence", "recent_change",
                          "discomfort_presence", "sensitivity_history"):
                skin_state[field] = "not_asked"
        result = review(JevExtractorAdapter.to_mapping_review_features(features), skin_state)
        if result["contract_errors"]:
            raise ValueError("invalid skin_state: " + ", ".join(result["contract_errors"]))
        result["candidates"] = [f for f in result["findings"]
                                if f["issue"] == "candidate_requires_user_and_time_confirmation"
                                or f.get("no_direct_skin_state_field")]
        return result
