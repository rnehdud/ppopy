"""Source-blind wrapper around the unchanged, inactive KB snapshot."""
from pathlib import Path
import sys

# The imported engine belongs to the repository, not the experiment wheel.
ROOT = Path(__file__).resolve().parents[6]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from skin_engine.kb_preview.engine import PreviewEngine


class KBEngineAdapter:
    def __init__(self, engine=None):
        self.engine = engine or PreviewEngine()

    def evaluate(self, observations, card_ids=None):
        if card_ids is not None and "B-P07" in card_ids:
            raise ValueError("manufacturer opinion comparison is excluded from the agent")
        facts = {}
        for key, slot in observations.items():
            if key != slot.variable_id:
                raise ValueError("observation key mismatch")
            if key.startswith("product."):
                raise ValueError("product evidence must come from a reviewed product source")
            if not slot.confirmed_by_user:
                continue
            facts[key] = {"state": slot.state, "value": slot.value,
                          "source": slot.source, "reference": "synthetic session user confirmation"}
        request = {"mode": "development_preview", "project": "Poppy",
                   "data_kind": "synthetic", "population": "adult", "facts": facts}
        if card_ids is not None:
            request["card_ids"] = card_ids
        else:
            request["card_ids"] = [cid for cid, card in self.engine.cards.items()
                if cid != "B-P07" and (set(card["observable_inputs"]) |
                    {field for branch in self.engine.rules[cid] for field in branch["when"]}) & facts.keys()]
        result = self.engine.evaluate(request)
        ask = {q["field"]: q["text"] for q in result["questions"]
               if not q["field"].startswith("product.")
               and self.engine.variables.get(q["field"], {}).get("consumer_question_allowed") is True}
        retrieve = sorted({f for row in result["results"] for f in row["missing_fields"]
                           if f.startswith("product.") and "retrieve_product_evidence" in row["action_types"]})
        holds = sorted({a for row in result["results"] for a in row["action_types"]
                        if a in ("refer_for_professional_review", "defer_specific_recommendation",
                                 "pause_specific_cosmetic_due_to_discomfort",
                                 "pause_specific_product_pending_quality_check")})
        # An unresolved comparison with no allowed acquisition path must not
        # silently become a label-based draft.
        if not ask and not retrieve and any(row["comparison_status"] in
                ("unknown", "conflicting", "exception") for row in result["results"]):
            holds = sorted(set(holds + ["unresolved_kb_comparison"]))
        return {"raw": result, "ask_slots": ask, "retrieve_slots": retrieve, "hold_signals": holds}
