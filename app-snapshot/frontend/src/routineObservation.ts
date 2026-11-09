import policy from "../../skin_engine/config/product_entry_flow.json";
import type { MissingObservation, ObservationContext, RoutineObservation } from "./careApi";

export const missingOptions: Array<[MissingObservation, string]> = [
  ["not_asked", "아직 확인하지 않음"], ["unknown", "모름"],
  ["user_does_not_remember", "기억나지 않음"], ["user_refused", "응답하지 않음"],
  ["conflicting", "답이 서로 달라 확인 필요"], ["needs_confirmation", "확인 후 답변 필요"],
];
export function emptyContext(): ObservationContext {
  return {version: "1.0.0", recent_products: {}, answered: [], duration: "not_asked",
    other_recent_changes: "not_asked", application_site: "not_asked", amount: "not_asked"};
}
export function followupQuestions(observation: RoutineObservation): string[] {
  if (observation.discomfort !== "yes") return [];
  const values: Record<string, unknown> = {...observation.context, ...observation.details};
  return policy.context_contract.followup_order.filter(q =>
    ["not_asked", "unknown"].includes(String(values[q] ?? "not_asked")) && !observation.context?.answered.includes(q));
}
export function answerRoutineFollowup(observation: RoutineObservation, question: string, value: string): RoutineObservation {
  if (observation.discomfort !== "yes" || !observation.details || !policy.context_contract.followup_order.includes(question)) {
    throw new Error("invalid_routine_followup_answer");
  }
  const context = observation.context ?? emptyContext();
  const nextContext = {...context, answered: [...new Set([...context.answered, question])]};
  if (question === "timing" || question === "ongoing") {
    return {...observation, details: {...observation.details, [question]: value}, context: nextContext} as RoutineObservation;
  }
  return {...observation, context: {...nextContext, [question]: value} as ObservationContext};
}
export function requiresAbstention(observation: RoutineObservation): boolean {
  const missing: readonly unknown[] = policy.missing_values;
  if (observation.discomfort !== "not_asked" && missing.includes(observation.discomfort)) return true;
  if (observation.products.some(p => missing.includes(p.days_per_week))) return true;
  if (observation.discomfort !== "yes") return false;
  const values: Record<string, unknown> = {...observation.context, ...observation.details};
  return policy.context_contract.followup_order.some(q => missing.includes(values[q] ?? "not_asked"));
}
