import fixtureResponse from "./fixtures/syntheticCareResponse.json";
import { ProductCandidate, searchDemoProducts, type WebProductCandidate } from "./productCatalog";
import { parseIntakeDraft } from "./intakeDraftValidation";
import type { AppPlatform, AppReleaseChannel } from "./appClientCompatibility";
import { isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl } from "./miraySavedCandidates";

export type ProductContextStatus = "registered" | "partial" | "unregistered";

export type CareAnalysisRequest = {
  schema_version: "0.1.0";
  deployment_context: "synthetic_test" | "real_user";
  product_context_status: ProductContextStatus;
  confirmed_current_product_ids: string[];
  routine_observation?: RoutineObservation;
  care_priorities: string[];
  aggravating_answers: Record<string, boolean>;
  survey: {
    irritation_history: boolean;
    current_actives: Array<"retinoid" | "acid">;
    retinoid_in_use: boolean;
    dermatology_treatment_status: "none" | "in_use" | "unknown";
    tightness_dryness_score: number;
  };
};

export type MissingObservation = "unknown" | "refused" | "not_asked" | "user_does_not_remember" | "user_refused" | "conflicting" | "needs_confirmation";
export type ObservationContext = {
  version: "1.0.0";
  recent_products: Record<string, {previous_days_per_week: number | MissingObservation; newly_started: "yes" | "no" | MissingObservation}>;
  answered: string[];
  duration: "brief" | "persistent" | MissingObservation;
  other_recent_changes: "none" | "new_product" | "frequency_changed" | "both" | MissingObservation;
  application_site: "whole_face" | "localized" | "other" | MissingObservation;
  amount: "less_than_usual" | "usual" | "more_than_usual" | MissingObservation;
};
export type RoutineObservation = {
  version: "1.0.0-owner-review";
  products: Array<{ product_id: string; days_per_week: number | MissingObservation }>;
  discomfort: "yes" | "no" | "skipped" | MissingObservation;
  details: null | { timing: "recent" | "earlier" | MissingObservation; ongoing: "yes" | "no" | MissingObservation };
  context?: ObservationContext;
};

export type IntakeDraft = {
  phase: "products" | "routine" | "personalization";
  selected: ProductCandidate[];
  frequencies: Record<string, string>;
  discomfort: RoutineObservation["discomfort"];
  timing: "recent" | "earlier" | MissingObservation;
  ongoing: "yes" | "no" | MissingObservation;
  context?: ObservationContext;
};

export type CareItem = string | Record<string, unknown>;

export type CareSection = {
  type:
    | "aggravating_factors"
    | "ingredient_plan"
    | "routine"
    | "current_products"
    | "product_matches"
    | "unmet_gaps"
    | "disclaimers";
  availability?: string;
  outcome?: Record<string, unknown>;
  items: CareItem[];
};

export type CareAnalysisEnvelope = {
  api_schema_version: string;
  deployment_context: "synthetic_test" | "real_user";
  persistence: "none" | "protected_beta_session";
  result: {
    schema_version: string;
    sections: CareSection[];
    safety: {
      tolerance_level: string;
      excluded_combinations: string[];
      warnings: string[];
    };
  };
};

export type BetaNotice = {
  version: string;
  title: string;
  summary: string;
};

export type BetaNoticeBundle = {
  schema_version: string;
  beta_activated: boolean;
  notices: {
    service_terms: BetaNotice;
    general_personal_information: BetaNotice;
    sensitive_information: BetaNotice;
    beta_contact: BetaNotice;
  };
  processor_and_transfer: string;
};

export type BetaSessionRequest = {
  schema_version: string;
  age_gate: "over_or_equal_14" | "under_14";
  accepted_notices: {
    service_terms: string;
    general_personal_information: string;
    sensitive_information: string;
  };
  contact: null | {
    type: "email" | "sms" | "kakao";
    value: string;
    notice_version: string;
  };
};

export type BetaSessionHandle = {
  participant_id: string;
  session_token: string;
  expires_at: string;
  notice_versions: Record<string, string>;
};

export type BetaCareSubmission = {
  ready_for_payment: boolean;
  payment_required: boolean;
  product_context_status: ProductContextStatus;
  code: "payment_required" | "product_confirmation_required";
};

export type PaymentOrder = {
  orderId: string;
  amount: 9900;
  goodsName: "개인화 1회권";
};

export type PaymentWindowRequest = PaymentOrder & {
  clientId: string;
  method: "card";
  returnUrl: string;
};

export type SupportCategory =
  | "payment_issue"
  | "cancellation_withdrawal"
  | "service_error"
  | "privacy_request"
  | "other";

export type SessionDeletionReceipt = {
  deleted_zones: Array<"service" | "contact" | "sensitive">;
  backup_cleanup_required: true;
  legal_transaction_records_separate: true;
};

export type ProductSearchOptions = {signal?: AbortSignal; confirmExternalTransfer?: import("./productTransferConfirmation").ConfirmProductTransfer};

export type CareApiClient = {
  readAppCompatibility?(platform: AppPlatform, releaseChannel: AppReleaseChannel): Promise<unknown>;
  saveIntakeDraft?(token: string, draft: IntakeDraft): Promise<void>;
  readIntakeDraft?(token: string): Promise<{draft: IntakeDraft | null}>;
  recordPilotEvent?(token: string, event: string, questionId?: string): Promise<void>;
  requestProductResolution?(token: string, productName: string): Promise<{ request_id: string; state: string }>;
  readProductResolutions?(token: string): Promise<{requests: Array<{request_id: string; state: string; resolved_product_id: string | null}>; auto_confirmed: false}>;
  mode: "fixture" | "http";
  searchProducts(query: string, options?: ProductSearchOptions): Promise<ProductCandidate[]>;
  searchWebProducts?(query: string, options?: ProductSearchOptions): Promise<WebProductCandidate[]>;
  analyze(request: CareAnalysisRequest): Promise<CareAnalysisEnvelope>;
  getBetaNotices(): Promise<BetaNoticeBundle>;
  startBetaSession(request: BetaSessionRequest): Promise<BetaSessionHandle>;
  submitBetaCare(token: string, request: CareAnalysisRequest): Promise<BetaCareSubmission>;
  createPaymentOrder(token: string): Promise<PaymentOrder>;
  preparePaymentWindow(token: string, orderId: string): Promise<PaymentWindowRequest>;
  cancelPayment(token: string, orderId: string, reason: string): Promise<{ state: string }>;
  createSupportCase(token: string, category: SupportCategory, body: string): Promise<{ caseId: string; status: "OPEN" }>;
  readBetaResult(token: string): Promise<CareAnalysisEnvelope["result"]>;
  deleteBetaSession(token: string): Promise<SessionDeletionReceipt>;
};

type ProductSearchEnvelope = {
  auto_confirmed: boolean;
  candidates: Array<{
    product_id: string;
    brand: string;
    name: string;
    option: string;
    ingredient_evidence_status: "owner_verified" | "automation_verified" | "review_required";
    source_url?: string | null;
    provenance_hash?: string | null;
  }>;
};

type WebProductSearchEnvelope = {
  auto_confirmed: false;
  provider: string;
  candidates: Array<{
    candidate_id: string;
    title: string;
    source_domain: string;
    source_url: string;
    snippet: string;
    provenance_hash: string;
  }>;
};

export class CareApiError extends Error {
  readonly status: number;
  readonly code: string;

  constructor(message: string, status: number, code = "unknown_error") {
    super(message);
    this.name = "CareApiError";
    this.status = status;
    this.code = code;
  }
}

async function readJson<T>(response: Response): Promise<T> {
  const payload = await response.json() as T & { error?: { code?: string; message?: string }; code?: string; message?: string };
  if (!response.ok) throw new CareApiError(
    payload.error?.message || payload.message || "로컬 케어 API 요청에 실패했습니다.",
    response.status,
    payload.error?.code || payload.code || "unknown_error",
  );
  return payload;
}

export function parseSessionDeletionReceipt(value: unknown): SessionDeletionReceipt {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new CareApiError("삭제 완료 응답을 확인하지 못했습니다.", 502, "invalid_deletion_receipt");
  }
  const record = value as Record<string, unknown>;
  const zones = record.deleted_zones;
  const exactKeys = Object.keys(record).sort().join("|") ===
    "backup_cleanup_required|deleted_zones|legal_transaction_records_separate";
  const exactZones = Array.isArray(zones)
    && zones.length === 3
    && new Set(zones).size === 3
    && ["service", "contact", "sensitive"].every(zone => zones.includes(zone));
  if (!exactKeys || !exactZones || record.backup_cleanup_required !== true
      || record.legal_transaction_records_separate !== true) {
    throw new CareApiError("삭제 완료 응답을 확인하지 못했습니다.", 502, "invalid_deletion_receipt");
  }
  return {
    deleted_zones: zones as SessionDeletionReceipt["deleted_zones"],
    backup_cleanup_required: true,
    legal_transaction_records_separate: true,
  };
}

export function createFixtureCareApiClient(): CareApiClient {
  return {
    async readAppCompatibility() {
      throw new Error("앱 호환성 응답은 연결된 TEST API에서만 확인할 수 있습니다.");
    },
    mode: "fixture",
    async searchProducts(query, searchOptions) {
      searchOptions?.signal?.throwIfAborted();
      return searchDemoProducts(query);
    },
    async analyze(request) {
      if (request.deployment_context !== "synthetic_test") {
        throw new Error("법률 검토 반영 전에는 실제 사용자 요청을 처리할 수 없습니다.");
      }
      return structuredClone(fixtureResponse) as CareAnalysisEnvelope;
    },
    async getBetaNotices() {
      throw new Error("보호 베타 동의 문서는 HTTP 스테이징에서만 제공합니다.");
    },
    async startBetaSession() {
      throw new Error("보호 베타 세션은 HTTP 스테이징에서만 시작할 수 있습니다.");
    },
    async submitBetaCare() {
      throw new Error("보호 베타 문진은 HTTP 스테이징에서만 제출할 수 있습니다.");
    },
    async createPaymentOrder() {
      throw new Error("결제 주문은 HTTP TEST 환경에서만 만들 수 있습니다.");
    },
    async preparePaymentWindow() {
      throw new Error("결제창은 HTTP TEST 환경에서만 열 수 있습니다.");
    },
    async cancelPayment() {
      throw new Error("결제 취소는 HTTP TEST 환경에서만 요청할 수 있습니다.");
    },
    async createSupportCase() {
      throw new Error("인앱 문의는 HTTP TEST 환경에서만 접수할 수 있습니다.");
    },
    async readBetaResult() {
      throw new Error("보호 베타 결과는 HTTP 스테이징에서만 조회할 수 있습니다.");
    },
    async deleteBetaSession() {
      throw new Error("보호 베타 세션은 HTTP 스테이징에서만 삭제할 수 있습니다.");
    },
  };
}

export type HttpCareApiOptions = {
  baseUrl?: string;
  allowedBaseUrls?: readonly string[];
  testProductSearch?: {
    loadAccessToken: () => Promise<string | null>;
    timeoutMilliseconds: number;
  };
};

function canonicalHttpsBaseUrl(value: string): string {
  const parsed = new URL(value);
  if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.search || parsed.hash) {
    throw new Error("앱 API base URL은 자격정보·query·fragment가 없는 HTTPS 주소여야 합니다.");
  }
  return `${parsed.origin}${parsed.pathname.replace(/\/+$/, "")}`;
}

export function createHttpCareApiClient(fetcher: typeof fetch = fetch, options: HttpCareApiOptions = {}): CareApiClient {
  const requestedBase = options.baseUrl?.trim() || "";
  let baseUrl = "";
  if (requestedBase) {
    baseUrl = canonicalHttpsBaseUrl(requestedBase);
    const allowed = (options.allowedBaseUrls || []).map(canonicalHttpsBaseUrl);
    if (!allowed.includes(baseUrl)) throw new Error("앱 API base URL이 정확한 허용 목록에 없습니다.");
  }
  const apiFetch: typeof fetch = (input, init) => {
    if (typeof input !== "string" || !input.startsWith("/api/")) throw new Error("앱 API는 고정 상대 경로만 호출할 수 있습니다.");
    return fetcher(baseUrl ? `${baseUrl}${input}` : input, init);
  };
  return {
    async readAppCompatibility(platform, releaseChannel) {
      return readJson<unknown>(await apiFetch(
        `/api/v1/app/compatibility?platform=${platform}&release_channel=${releaseChannel}`,
        {cache: "no-store"},
      ));
    },
    async saveIntakeDraft(token, draft) {
      await readJson(await apiFetch("/api/v1/beta/draft", { method: "PUT", cache: "no-store",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` }, body: JSON.stringify(draft) }));
    },
    async readIntakeDraft(token) {
      const payload = await readJson<{draft: unknown}>(await apiFetch("/api/v1/beta/draft", { cache: "no-store", headers: { "Authorization": `Bearer ${token}` } }));
      try { return {draft: parseIntakeDraft(payload.draft)}; }
      catch { throw new CareApiError("저장된 입력 형식을 확인하지 못했습니다.", 502, "invalid_draft_response"); }
    },
    async recordPilotEvent(token, event, questionId) {
      const response = await apiFetch("/api/v1/beta/events", { method: "POST", cache: "no-store",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({ event, ...(questionId ? { question_id: questionId } : {}) }) });
      await readJson(response);
    },
    async requestProductResolution(token, productName) {
      return readJson(await apiFetch("/api/v1/products/resolution", { method: "POST", cache: "no-store",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
        body: JSON.stringify({ product_name: productName }) }));
    },
    async readProductResolutions(token) {
      return readJson(await apiFetch("/api/v1/products/resolution", {cache: "no-store", headers: {"Authorization": `Bearer ${token}`}}));
    },
    mode: "http",
    async searchProducts(query, searchOptions) {
      searchOptions?.signal?.throwIfAborted();
      const response = await apiFetch(`/api/v1/products?query=${encodeURIComponent(query)}`, {
        cache: "no-store",
        ...(searchOptions?.signal ? {signal:searchOptions.signal} : {}),
      });
      const payload = await readJson<ProductSearchEnvelope>(response);
      searchOptions?.signal?.throwIfAborted();
      if (payload.auto_confirmed) throw new Error("제품 후보 자동 확정 응답은 허용되지 않습니다.");
      return payload.candidates.map((candidate) => {
        const sourceUrl = candidate.source_url ?? null;
        const provenanceHash = candidate.provenance_hash ?? null;
        if (sourceUrl !== null && typeof sourceUrl !== "string") throw new CareApiError("제품 후보 출처를 확인하지 못했습니다.", 502, "invalid_product_candidate");
        if (provenanceHash !== null && typeof provenanceHash !== "string") throw new CareApiError("제품 후보 출처를 확인하지 못했습니다.", 502, "invalid_product_candidate");
        if ((sourceUrl === null) !== (provenanceHash === null)) throw new CareApiError("제품 후보 출처를 확인하지 못했습니다.", 502, "invalid_product_candidate");
        if (sourceUrl !== null) {
          try { validateMirayCandidateSourceUrl(sourceUrl); }
          catch { throw new CareApiError("제품 후보 출처를 확인하지 못했습니다.", 502, "invalid_product_candidate"); }
          if (!isMirayCandidateProvenanceHash(provenanceHash!)) throw new CareApiError("제품 후보 출처를 확인하지 못했습니다.", 502, "invalid_product_candidate");
        }
        return {
        id: candidate.product_id,
        brand: candidate.brand,
        name: candidate.name,
        option: candidate.option,
        evidenceStatus: candidate.ingredient_evidence_status,
        ...(sourceUrl ? {sourceUrl, provenanceHash:provenanceHash!} : {}),
        };
      });
    },
    async searchWebProducts(query, searchOptions) {
      searchOptions?.signal?.throwIfAborted();
      const access = options.testProductSearch;
      let payload: WebProductSearchEnvelope;
      if (access) {
        const token = await access.loadAccessToken();
        searchOptions?.signal?.throwIfAborted();
        if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) {
          throw new CareApiError("TEST 검색 연결을 확인해 주세요.", 401, "test_search_access_required");
        }
        if (!Number.isInteger(access.timeoutMilliseconds) || access.timeoutMilliseconds <= 0) {
          throw new Error("TEST 검색 timeout 설정을 확인해 주세요.");
        }
        const controller = new AbortController();
        const abort = () => controller.abort(searchOptions?.signal?.reason);
        searchOptions?.signal?.addEventListener("abort",abort,{once:true});
        const timer = setTimeout(() => controller.abort(), access.timeoutMilliseconds);
        try {
          const response = await apiFetch("/api/v1/products/test-web-candidates", {
            method: "POST", cache: "no-store", signal: controller.signal,
            headers: {"Content-Type": "application/json", "Authorization": `Bearer ${token}`},
            body: JSON.stringify({product_query: query}),
          });
          payload = await readJson<WebProductSearchEnvelope>(response);
        } catch (error) {
          searchOptions?.signal?.throwIfAborted();
          if (controller.signal.aborted) {
            throw new CareApiError("검색이 지연되고 있어요. 다시 시도해 주세요.", 504, "product_search_timeout");
          }
          throw error;
        } finally { clearTimeout(timer);searchOptions?.signal?.removeEventListener("abort",abort); }
      } else {
        const response = await apiFetch(`/api/v1/products/web-candidates?query=${encodeURIComponent(query)}`, {
          cache: "no-store",
          ...(searchOptions?.signal ? {signal:searchOptions.signal} : {}),
        });
        payload = await readJson<WebProductSearchEnvelope>(response);
      }
      searchOptions?.signal?.throwIfAborted();
      if (payload.auto_confirmed !== false) throw new Error("인터넷 제품 후보 자동 확정 응답은 허용되지 않습니다.");
      return payload.candidates.map(candidate => ({
        candidateId: candidate.candidate_id,
        title: candidate.title,
        sourceDomain: candidate.source_domain,
        sourceUrl: candidate.source_url,
        snippet: candidate.snippet,
        provenanceHash: candidate.provenance_hash,
      }));
    },
    async analyze(request) {
      const response = await apiFetch("/api/v1/care-analysis", {
        method: "POST",
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      });
      return readJson<CareAnalysisEnvelope>(response);
    },
    async getBetaNotices() {
      const response = await apiFetch("/api/v1/beta/notices", { cache: "no-store" });
      return readJson<BetaNoticeBundle>(response);
    },
    async startBetaSession(request) {
      const response = await apiFetch("/api/v1/beta/session", {
        method: "POST",
        cache: "no-store",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      });
      return readJson<BetaSessionHandle>(response);
    },
    async submitBetaCare(token, request) {
      const response = await apiFetch("/api/v1/beta/care", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify(request),
      });
      return readJson<BetaCareSubmission>(response);
    },
    async createPaymentOrder(token) {
      const response = await apiFetch("/api/v1/payments/orders", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ productCode: "personalized-care-once" }),
      });
      return readJson<PaymentOrder>(response);
    },
    async preparePaymentWindow(token, orderId) {
      const response = await apiFetch("/api/v1/payments/window", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ orderId }),
      });
      return readJson<PaymentWindowRequest>(response);
    },
    async cancelPayment(token, orderId, reason) {
      const response = await apiFetch("/api/v1/payments/cancel", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ orderId, reason }),
      });
      return readJson<{ state: string }>(response);
    },
    async createSupportCase(token, category, body) {
      const response = await apiFetch("/api/v1/support/cases", {
        method: "POST",
        cache: "no-store",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ category, body }),
      });
      return readJson<{ caseId: string; status: "OPEN" }>(response);
    },
    async readBetaResult(token) {
      const response = await apiFetch("/api/v1/beta/result", {
        cache: "no-store",
        headers: { "Authorization": `Bearer ${token}` },
      });
      const payload = await readJson<{ result: CareAnalysisEnvelope["result"] }>(response);
      return payload.result;
    },
    async deleteBetaSession(token) {
      const response = await apiFetch("/api/v1/beta/session", {
        method: "DELETE",
        cache: "no-store",
        headers: { "Authorization": `Bearer ${token}` },
      });
      return parseSessionDeletionReceipt(await readJson<unknown>(response));
    },
  };
}

export const careApiClient = import.meta.env.VITE_CARE_API_MODE === "http"
  ? createHttpCareApiClient()
  : createFixtureCareApiClient();
