import policy from "../../skin_engine/config/product_entry_flow.json";
import type { IntakeDraft } from "./careApi";

const record = (value: unknown): value is Record<string, unknown> => typeof value === "object" && value !== null && !Array.isArray(value);
const exactKeys = (value: Record<string, unknown>, required: readonly string[], optional: readonly string[] = []) => {
  const keys = Object.keys(value);
  return required.every(key => keys.includes(key)) && keys.every(key => required.includes(key) || optional.includes(key));
};
const missing = new Set<string>(policy.missing_values);
const frequencies = new Set<unknown>(["", ...policy.frequency_days.map(String), ...policy.missing_values]);
const evidenceStates = new Set(["owner_verified", "automation_verified", "review_required", "fixture_only"]);
const matchSources = new Set(["catalog", "public_web", "manual"]);

function validContext(value: unknown, productIds: Set<string>): boolean {
  if (!record(value)) return false;
  const followupFields = Object.keys(policy.context_contract.followup_values);
  if (!exactKeys(value, ["version", "recent_products", "answered", ...followupFields])) return false;
  if (value.version !== policy.context_contract.version || !Array.isArray(value.answered)) return false;
  if (value.answered.some(item => typeof item !== "string") || new Set(value.answered).size !== value.answered.length) return false;
  if (value.answered.some(item => !policy.context_contract.followup_order.includes(item as never))) return false;
  for (const field of followupFields) {
    const allowed = new Set<string>([...(policy.context_contract.followup_values as Record<string, string[]>)[field], ...policy.missing_values]);
    if (typeof value[field] !== "string" || !allowed.has(value[field])) return false;
  }
  if (!record(value.recent_products) || Object.keys(value.recent_products).some(id => !productIds.has(id))) return false;
  for (const history of Object.values(value.recent_products)) {
    if (!record(history) || !exactKeys(history, ["previous_days_per_week", "newly_started"])) return false;
    const days = history.previous_days_per_week;
    if (!(typeof days === "number" && Number.isInteger(days) && policy.frequency_days.includes(days)) && !(typeof days === "string" && missing.has(days))) return false;
    if (typeof history.newly_started !== "string" || !(history.newly_started === "yes" || history.newly_started === "no" || missing.has(history.newly_started))) return false;
  }
  return true;
}

export function parseIntakeDraft(value: unknown): IntakeDraft | null {
  if (value === null) return null;
  if (!record(value) || !exactKeys(value, ["phase", "selected", "frequencies", "discomfort", "timing", "ongoing"], ["context"])) throw new Error("invalid_draft_response");
  if (!(["products", "routine", "personalization"] as unknown[]).includes(value.phase) || !Array.isArray(value.selected) || value.selected.length > policy.maximum_products) throw new Error("invalid_draft_response");
  const ids: string[] = [];
  for (const product of value.selected) {
    if (!record(product) || !exactKeys(product, ["id", "brand", "name", "option", "evidenceStatus"], ["matchSource", "sourceUrl", "provenanceHash"])) throw new Error("invalid_draft_response");
    if ([product.id, product.brand, product.name, product.option].some(item => typeof item !== "string" || item.length > 300)) throw new Error("invalid_draft_response");
    if (typeof product.evidenceStatus !== "string" || !evidenceStates.has(product.evidenceStatus)) throw new Error("invalid_draft_response");
    if (product.matchSource !== undefined && (typeof product.matchSource !== "string" || !matchSources.has(product.matchSource))) throw new Error("invalid_draft_response");
    if (product.matchSource === "public_web") {
      if (typeof product.sourceUrl !== "string" || !product.sourceUrl.startsWith("https://")
          || typeof product.provenanceHash !== "string" || !/^[0-9a-f]{64}$/.test(product.provenanceHash)) throw new Error("invalid_draft_response");
    }
    ids.push(product.id as string);
  }
  if (new Set(ids).size !== ids.length || !record(value.frequencies) || Object.keys(value.frequencies).some(id => !ids.includes(id))) throw new Error("invalid_draft_response");
  if (Object.values(value.frequencies).some(item => typeof item !== "string" || !frequencies.has(item))) throw new Error("invalid_draft_response");
  if (typeof value.discomfort !== "string" || !policy.discomfort_answers.includes(value.discomfort as never)) throw new Error("invalid_draft_response");
  if (typeof value.timing !== "string" || !(value.timing === "recent" || value.timing === "earlier" || missing.has(value.timing))) throw new Error("invalid_draft_response");
  if (typeof value.ongoing !== "string" || !(value.ongoing === "yes" || value.ongoing === "no" || missing.has(value.ongoing))) throw new Error("invalid_draft_response");
  if (value.context !== undefined && !validContext(value.context, new Set(ids))) throw new Error("invalid_draft_response");
  return value as IntakeDraft;
}
