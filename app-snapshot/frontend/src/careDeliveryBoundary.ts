import contract from "../../skin_engine/config/consumer_care_delivery.json";

const object = (value: unknown): value is Record<string, unknown> =>
  Boolean(value) && typeof value === "object" && !Array.isArray(value);
const exact = (value: Record<string, unknown>, keys: readonly string[]) =>
  Object.keys(value).length === keys.length && keys.every(key => Object.hasOwn(value, key));
const strings = (value: unknown): value is string[] =>
  Array.isArray(value) && value.every(item => typeof item === "string");

function safeJson(value: unknown, depth = 0): boolean {
  if (depth > 32) return false;
  if (typeof value === "string") return !contract.prohibited_terms.some(term => value.includes(term));
  if (value === null || typeof value === "boolean") return true;
  if (typeof value === "number") return Number.isFinite(value);
  if (Array.isArray(value)) return value.every(item => safeJson(item, depth + 1));
  if (object(value)) return Object.entries(value).every(([key, item]) => safeJson(key, depth + 1) && safeJson(item, depth + 1));
  return false;
}

function validPlanRoutine(plan: unknown, steps: unknown): boolean {
  const doses: Record<string, readonly string[]> = contract.status_doses;
  const ingredientDoses: Record<string, readonly string[]> = contract.ingredient_doses;
  const kinds: Record<string, string> = contract.routine.palette_kind_by_status;
  if (!Array.isArray(plan) || plan.length !== contract.palette_ingredients.length
    || !plan.every(item => object(item) && exact(item, contract.palette_fields)
      && Object.values(item).every(v => typeof v === "string" && v.trim())
      && typeof item.status === "string" && Object.hasOwn(doses, item.status)
      && typeof item.dose === "string" && doses[item.status].includes(item.dose))
    || !contract.palette_ingredients.every(name => plan.filter(item => item.ingredient === name).length === 1)) return false;
  const active = new Map<string, Record<string, unknown>>();
  for (const item of plan) {
    if (Object.hasOwn(kinds, item.status)) {
      if (!ingredientDoses[item.ingredient].includes(item.dose)) return false;
      active.set(item.ingredient, item);
    }
  }
  if (contract.incompatible_groups.some(group => group.ingredients.filter(name => active.has(name)).length > group.max_active)) return false;
  if (!Array.isArray(steps)) return false;
  const kindSlots: Record<string, readonly string[]> = contract.routine.kind_slots;
  const frequency: Record<string, boolean> = contract.routine.frequency_gradual;
  const positions = new Map<string, number[]>(contract.routine.slots.map(slot => [slot, []]));
  const used = new Set<string>();
  const foundations = new Set<string>();
  const expectedFoundation = new Set(contract.routine.foundation.map(value => JSON.stringify(value)));
  for (const step of steps) {
    if (!object(step) || !exact(step, contract.routine.fields)
      || !["slot", "kind", "ingredient", "dose", "frequency"].every(key => typeof step[key] === "string" && step[key].trim())
      || typeof step.order !== "number" || !Number.isSafeInteger(step.order) || step.order < 1
      || typeof step.gradual_introduction !== "boolean"
      || typeof step.kind !== "string" || !Object.hasOwn(kindSlots, step.kind)
      || typeof step.slot !== "string" || !kindSlots[step.kind].includes(step.slot)
      || typeof step.frequency !== "string" || !Object.hasOwn(frequency, step.frequency)
      || frequency[step.frequency] !== step.gradual_introduction) return false;
    const orders = positions.get(step.slot);
    if (!orders) return false;
    orders.push(step.order);
    const name = step.ingredient as string;
    if (Object.values(kinds).includes(step.kind)) {
      const item = active.get(name);
      if (!item || used.has(name) || step.dose !== item.dose || step.kind !== kinds[item.status as string]) return false;
      used.add(name);
    } else {
      const foundation = JSON.stringify({slot:step.slot, kind:step.kind, ingredient:name});
      if (!expectedFoundation.has(foundation) || foundations.has(foundation)
        || step.dose !== contract.routine.foundation_dose || step.frequency !== contract.routine.foundation_frequency) return false;
      foundations.add(foundation);
    }
  }
  if (used.size !== active.size || foundations.size !== expectedFoundation.size) return false;
  const ends: Record<string, readonly string[]> = contract.routine.end_kinds;
  for (const [slot, orders] of positions) {
    if (!orders.sort((a, b) => a - b).every((order, index) => order === index + 1)) return false;
    const period = steps.filter(step => step.slot === slot).sort((a, b) => a.order - b.order);
    if (!period.length || period[0].kind !== contract.routine.first_kind
      || period.slice(-ends[slot].length).some((step, index) => step.kind !== ends[slot][index])) return false;
  }
  return true;
}

/** Complete existing palette, not six arbitrary rows. Never repair missing advice. */
export function isConsumerCareDelivery(value: unknown): boolean {
  if (!object(value) || !exact(value, ["schema_version", "sections", "safety"])
    || value.schema_version !== contract.care_response_schema_version || !safeJson(value)) return false;
  const sections = value.sections;
  if (!Array.isArray(sections) || sections.length !== contract.section_types.length
    || !contract.section_types.every(type => sections.filter(s => object(s) && s.type === type).length === 1)) return false;
  for (const section of sections) {
    if (!object(section) || !Object.hasOwn(section, "type") || !Object.hasOwn(section, "items")
      || !Object.keys(section).every(key => ["type", "items", "availability", "outcome"].includes(key))
      || !Array.isArray(section.items) || !section.items.every(item => typeof item === "string" || object(item))
      || ("availability" in section && typeof section.availability !== "string")
      || ("outcome" in section && !object(section.outcome))) return false;
  }
  if (!validPlanRoutine(sections.find(section => section.type === "ingredient_plan").items,
    sections.find(section => section.type === "routine").items)) return false;
  const safety = value.safety;
  return object(safety) && exact(safety, ["tolerance_level", "excluded_combinations", "warnings"])
    && typeof safety.tolerance_level === "string" && strings(safety.excluded_combinations) && strings(safety.warnings);
}
