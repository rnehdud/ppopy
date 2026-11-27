import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import type {HomeTask} from "./mirayNavigation";
export type MiraySkinState = {
  version: "1.0.0";
  kind: "baseline" | "checkin";
  observed_at: string;
  concern_presence: "reported" | "none_reported" | "unknown" | "not_asked" | "user_refused";
  persistence: "recent" | "recurring" | "persistent" | "not_applicable" | "unknown" | "not_asked" | "user_refused";
  recent_change: "better" | "worse" | "unchanged" | "fluctuating" | "not_applicable" | "unknown" | "not_asked" | "user_refused";
  discomfort_presence: "reported" | "none_reported" | "unknown" | "not_asked" | "user_refused";
  discomfort_types: Array<"stinging" | "burning" | "itching" | "tightness" | "increased_scaling" | "redness_tendency" | "other_no_free_text">;
  sensitivity_history: "reported" | "none_reported" | "unknown" | "not_asked" | "user_refused";
};

export type MiraySkinStateSaveResult = {homeTasks: HomeTask[]};
export type MiraySkinStateStore = {save(value: MiraySkinState, options?: MemberStatusReadOptions): Promise<void | MiraySkinStateSaveResult>};

/** Accept only canonical neutral tasks; no raw state or internal identifiers. */
export function parseSkinStateHomeTasks(value: unknown): HomeTask[] {
  if (!Array.isArray(value) || value.length > config.home_tasks.max_response_tasks) throw new Error("홈 안내 응답을 확인하지 못했습니다.");
  return value.map(task => {
    if (!task || typeof task !== "object" || Array.isArray(task)
        || Object.keys(task).length !== 4 || !Object.values(config.home_tasks.templates).some(template =>
          Object.entries(template).every(([key, expected]) => task[key] === expected))) throw new Error("홈 안내 응답을 확인하지 못했습니다.");
    return {...task} as HomeTask;
  });
}

export type MiraySkinStateHttpOptions = {
  baseUrl: string;
  allowedBaseUrls: readonly string[];
  loadSessionToken: () => Promise<string | null>;
  /** Explicit UI lifecycle notification; never clears credentials or retries HTTP. */
  onSessionChanged?: () => void;
};

function httpsBase(value: string): string {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
}

/** Reject extra/plaintext fields before crossing any network boundary. */
export function validateMiraySkinState(value: unknown): asserts value is MiraySkinState {
  const invalid = () => {throw new Error("현재 상태 입력을 다시 확인해 주세요.");};
  const keys = ["version","kind","observed_at",...Object.keys(config.fields)];
  if (!value || typeof value !== "object" || Array.isArray(value)) return invalid();
  const state = value as Record<string, unknown>;
  if (Object.keys(state).length !== keys.length || keys.some(key => !Object.hasOwn(state,key))
      || state.version !== config.version || typeof state.kind !== "string" || !config.record_kinds.includes(state.kind)) return invalid();
  if (typeof state.observed_at !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(state.observed_at)) return invalid();
  const timestamp = new Date(state.observed_at);
  if (!Number.isFinite(timestamp.getTime()) || timestamp.toISOString().slice(0,19) !== state.observed_at.slice(0,19)) return invalid();
  for (const [field,allowed] of Object.entries(config.fields)) {
    if (field === "discomfort_types") continue;
    if (typeof state[field] !== "string" || !allowed.includes(state[field] as string)) return invalid();
  }
  const details = state.discomfort_types;
  if (!Array.isArray(details) || details.some(item => typeof item !== "string" || !config.fields.discomfort_types.includes(item))
      || new Set(details).size !== details.length || (state.discomfort_presence === "reported") !== Boolean(details.length)) return invalid();
  if (state.concern_presence !== "reported" && [state.persistence,state.recent_change].some(item => !["not_applicable",...config.missing_states].includes(String(item)))) return invalid();
}

export function createHttpMiraySkinStateStore(fetcher: typeof fetch, options: MiraySkinStateHttpOptions): MiraySkinStateStore {
  const loadSessionToken=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  const requested=options.baseUrl.trim();
  if (!requested) throw new Error("앱 API 주소를 확인해 주세요.");
  const base=httpsBase(requested);
  if (!options.allowedBaseUrls.map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  return {save:async (value, requestOptions) => {
    const scope=memberStatusReadScope(loadSessionToken,requestOptions);
    scope.gate();
    validateMiraySkinState(value);
    const body=JSON.stringify({skin_state:value});
    if (new TextEncoder().encode(body).byteLength > config.http.max_request_bytes) throw new Error("현재 상태 입력이 허용 크기를 넘었습니다.");
    const token=await scope.wait(scope.load);
    if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response=await scope.wait(()=>scope.fetch(fetcher)(`${base}${config.http.path}`,{
      method:"POST",cache:"no-store",redirect:"error",credentials:"omit",signal:requestOptions?.signal,
      headers:{Authorization:`Bearer ${token}`,"Content-Type":"application/json"},
      body,
    }));
    await scope.wait(()=>assertCurrentMemberResponseSession(scope.load, token, options.onSessionChanged));
    let payload: unknown=null;
    try {payload=await scope.wait(()=>response.json());} catch {scope.gate(); /* fail below */ }
    await scope.wait(()=>assertCurrentMemberResponseSession(scope.load, token, options.onSessionChanged));
    if (!response.ok) throw new Error(response.status === 403 ? "민감정보와 이력 저장 동의를 다시 확인해 주세요." : "현재 상태를 저장하지 못했습니다.");
    if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("현재 상태 저장 응답을 확인하지 못했습니다.");
    const result=payload as Record<string,unknown>;
    if (result.saved !== true || Object.keys(result).some(key => !["saved","home_tasks"].includes(key))) throw new Error("현재 상태 저장 응답을 확인하지 못했습니다.");
    // Older saved-only servers remain compatible, but do not manufacture tasks.
    if (!Object.hasOwn(result,"home_tasks")) return;
    return {homeTasks:parseSkinStateHomeTasks(result.home_tasks)};
  }};
}

export function routineDiscomfortFromSkinState(value: MiraySkinState) {
  if (value.discomfort_presence === "reported") return "yes" as const;
  if (value.discomfort_presence === "none_reported") return "no" as const;
  if (value.discomfort_presence === "user_refused") return "user_refused" as const;
  return "unknown" as const;
}
import config from "../../skin_engine/config/miray_skin_state.json";
