"""Replay one scoped episode against the frozen post-wash KB. No IO or user writes."""

from math import isfinite


def _ph_evidence(record, policy):
    observation = record.get("product.ph")
    if not isinstance(observation, dict):
        return {"state": "unknown"}
    if observation.get("state") == "conflict":
        return {"state": "conflict"}
    kind = observation.get("source_type")
    raw = observation.get("reported_text")
    if (observation.get("state") != "verified" or kind not in policy["ph_sources"]
            or not observation.get("source_ref") or not isinstance(raw, str) or not raw.strip()):
        return {"state": "unknown"}
    if kind == "finished_product_test" and not observation.get("measurement_conditions"):
        return {"state": "unknown"}
    result = {"state": "reported", "source_type": kind, "reported_text": raw}
    if kind == "finished_product_test":
        result["measurement_conditions"] = observation["measurement_conditions"]
    category = observation.get("reported_category")
    if category in policy["ph_categories"]:
        result["category"] = category
    return result


def _volunteered_duration(value, policy):
    if not isinstance(value, dict) or value.get("phase", "unknown") not in policy["clarify_phases"]:
        return False
    if isinstance(value.get("reported_text"), str) and value["reported_text"].strip():
        return True
    seconds = value.get("range_seconds", [value.get("seconds")])
    return (isinstance(seconds, list) and len(seconds) in (1, 2)
            and all(type(n) in (int, float) and isfinite(n) and n >= 0 for n in seconds)
            and seconds[0] <= seconds[-1])


def evaluate_episode(seed, episode, product_record=None):
    """Use facts for this episode only. The catalog adapter supplies validated product facts."""
    contract = seed["dryness_concern_contract"]
    scope = episode["scope"]
    result = {"status": "needs_context", "actions": [], "candidate_fields": [], "product_ph": {"state": "unknown"}}
    if scope.get("safety_disposition") == "hold":
        result["status"] = "hold"
        return result
    if any(scope.get(key) != value for key, value in contract["preconditions"].items()):
        return result

    report = episode["facts"]
    pattern = report.get(contract["observation"])
    if not isinstance(pattern, dict):
        pattern = {}
    if contract["after_wash_phase"] not in pattern.get("reported_phases", ()):
        result["status"] = "outside_postwash_scope"
        return result
    target = episode.get("product_ref") or {}
    policy = contract["product_context"]
    record = product_record if product_record is not None else policy["reviewed_formulations"].get(target.get("id"), {})
    matched = all(target.get(key) and target[key] == record.get(key) for key in ("id", "version"))
    if not matched:
        record = {}
    result["product_ph"] = _ph_evidence(record, policy)
    facts = {key: value for key, value in report.items() if not key.startswith("product.")}
    for field in ("product.type", "product.instructions"):
        if field in record:
            facts[field] = record[field]
    recurrence = f"{contract['observation']}.same_cleanser_recurrence"
    facts[recurrence] = pattern.get("same_cleanser_recurrence")
    for rule in contract["supported_changes"]:
        if rule.get("requires_product_revision") and not matched:
            continue
        if all(facts.get(key) in allowed for key, allowed in rule["requires"].items()):
            result["actions"].append(rule["action"])

    result["status"] = "supported" if result["actions"] else "no_supported_change_yet"
    if result["actions"]:
        return result
    # These are eligible follow-ups on volunteered inputs. Ranking and the question budget belong to AFA.
    timing = contract["contact_duration"]
    form = timing["behavior_field"]
    asked = set(episode.get("answered_features", ()))
    if (_volunteered_duration(facts.get(timing["field"]), timing) and not facts.get(form) and form not in asked
            and facts.get("product.type") == "ordinary_rinse_off_cleanser"
            and facts.get("product.instructions") == "no_special_duration"):
        result["candidate_fields"].append(form)
    choice = "constraints.decision_context"
    if not facts.get(choice) and choice not in asked:
        comparison = next(r for r in contract["supported_changes"] if r["action"] == "offer_gentle_cleanser_comparison")
        if matched and all(facts.get(k) in values for k, values in comparison["requires"].items() if k != choice):
            result["candidate_fields"].append(choice)
    return result
