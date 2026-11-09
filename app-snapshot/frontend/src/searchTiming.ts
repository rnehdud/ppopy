export type SearchStage = "database_ready" | "photo_identity" | "catalog" | "web_product" | "ingredients";
export type SearchOutcome = "success" | "empty" | "failed" | "cancelled";
export type SearchReuse = "network" | "cache" | "coalesced";

export type SearchTimingSample = {
  version: "1.0.0";
  stage: SearchStage;
  outcome: SearchOutcome;
  reuse: SearchReuse;
  duration_ms: number;
};

export type SearchTimingObserver = (sample: SearchTimingSample) => void;
export type SearchTimingStageSummary = {
  samples: number;
  failures: number;
  first_call: {duration_ms: number; outcome: SearchOutcome; reuse: SearchReuse} | null;
  repeat_calls: {samples: number; p50_ms: number | null; p95_ms: number | null};
};

const MAX_SESSION_SAMPLES = 100;
const samples: SearchTimingSample[] = [];

export function searchDuration(started: number, finished: number): number {
  if (!Number.isFinite(started) || !Number.isFinite(finished)) return 0;
  return Math.max(0, Math.min(120_000, Math.round(finished - started)));
}

// Session-memory diagnostics only. No query, product, URL, image, token, user or
// device identifier is accepted by this contract, persisted, or transmitted.
export const recordSearchTiming: SearchTimingObserver = sample => {
  const checked: SearchTimingSample = {
    version: "1.0.0",
    stage: sample.stage,
    outcome: sample.outcome,
    reuse: sample.reuse,
    duration_ms: searchDuration(0, sample.duration_ms),
  };
  samples.push(checked);
  if (samples.length > MAX_SESSION_SAMPLES) samples.shift();
  if (typeof window !== "undefined") window.dispatchEvent(new CustomEvent("skinanalysis:search-timing", {detail: {...checked}}));
};

export function searchTimingSnapshot(): SearchTimingSample[] {
  return samples.map(sample => ({...sample}));
}

function nearestRank(values: number[], quantile: number): number | null {
  if (!values.length) return null;
  const ordered = [...values].sort((left, right) => left - right);
  return ordered[Math.max(0, Math.ceil(ordered.length * quantile) - 1)];
}

export function summarizeSearchTimings(values: readonly SearchTimingSample[] = samples): Partial<Record<SearchStage, SearchTimingStageSummary>> {
  const grouped = new Map<SearchStage, SearchTimingSample[]>();
  for (const value of values) grouped.set(value.stage, [...(grouped.get(value.stage) ?? []), value]);
  return Object.fromEntries([...grouped].map(([stage, stageSamples]) => {
    const first = stageSamples[0];
    const repeated = stageSamples.slice(1).map(sample => sample.duration_ms);
    return [stage, {
      samples: stageSamples.length,
      failures: stageSamples.filter(sample => sample.outcome === "failed").length,
      first_call: first ? {duration_ms: first.duration_ms, outcome: first.outcome, reuse: first.reuse} : null,
      repeat_calls: {samples: repeated.length, p50_ms: nearestRank(repeated, 0.50), p95_ms: nearestRank(repeated, 0.95)},
    }];
  }));
}

export function clearSearchTiming(): void {
  samples.splice(0, samples.length);
}
