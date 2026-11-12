import {Capacitor, CapacitorHttp, type HttpResponse} from "@capacitor/core";
import navigationConfig from "../../skin_engine/config/miray_navigation.json";
import loginConfig from "../../skin_engine/config/app_login_plan.json";
import skinStateConfig from "../../skin_engine/config/miray_skin_state.json";
import historyConsentConfig from "../../skin_engine/config/app_history_consent.json";
import withdrawalConfig from "../../skin_engine/config/app_account_withdrawal.json";
import {serializeIOSAppTestRequest} from "./iosAppTestRequestQueue";
import executionBudget from "../../skin_engine/config/app_test_execution_budget.json";
import withdrawalClientPolicy from "../../skin_engine/config/app_account_withdrawal_client.json";
import {accountWithdrawalNotStarted} from "./appAccountWithdrawal";

export const APP_AUTH_TEST_API_ORIGIN = "https://j9xwsogwph.execute-api.ap-northeast-2.amazonaws.com";

const authMethods: Record<string, readonly string[]> = {
  "/api/v1/app/auth/protection-session":["POST"],
  "/api/v1/app/auth/session":["GET", "DELETE"],
  "/api/v1/app/auth/apple":["POST"],
  "/api/v1/app/auth/apple/challenge":["POST"],
  "/api/v1/app/auth/google":["POST"],
  "/api/v1/app/auth/kakao":["POST"],
};
const allowedHeaders = new Set(["authorization", "content-type"]);

function checkedUrl(input: RequestInfo | URL, methods: Record<string, readonly string[]>): URL {
  if (input instanceof Request) throw new Error("AWS TEST 인증 요청은 Request 객체를 허용하지 않습니다.");
  const url = new URL(String(input));
  if (url.origin !== APP_AUTH_TEST_API_ORIGIN || !Object.hasOwn(methods, url.pathname)
      || url.username || url.password || url.search || url.hash) {
    throw new Error("AWS TEST 인증 요청 주소가 허용 목록에 없습니다.");
  }
  return url;
}

function checkedHeaders(init?: RequestInit): Record<string, string> {
  const result: Record<string, string> = {};
  new Headers(init?.headers).forEach((value, key) => {
    if (!allowedHeaders.has(key.toLowerCase())) throw new Error("AWS TEST 인증 요청 헤더가 허용 목록에 없습니다.");
    result[key] = value;
  });
  return result;
}

function responseBody(response: HttpResponse): string {
  const value = typeof response.data === "string" ? response.data : JSON.stringify(response.data ?? null);
  if (new TextEncoder().encode(value).byteLength > 65_536) throw new Error("AWS TEST 인증 응답이 허용 크기를 넘었습니다.");
  return value;
}

/** URLSession cannot be cancelled here; abandon its result and any retry. */
function awaitUnlessAborted<T>(operation: Promise<T>, signal?: AbortSignal): Promise<T> {
  if (!signal) return operation;
  return new Promise((resolve, reject) => {
    const abort = () => reject(signal.reason ?? new DOMException("Aborted", "AbortError"));
    if (signal.aborted) abort();
    else signal.addEventListener("abort", abort, {once:true});
    operation.then(value => {
      signal.removeEventListener("abort", abort);
      if (!signal.aborted) resolve(value);
    }, error => {
      signal.removeEventListener("abort", abort);
      reject(error);
    });
  });
}

/** Native URLSession transport for the fixed AWS TEST auth surface; this avoids WebView CORS expansion. */
export function createIOSAppAuthFetcher(options: {portfolioTestEnabled?: boolean; skinStateTestEnabled?: boolean; historyConsentTestEnabled?: boolean; coreTestReviewEnabled?: boolean;
  accountWithdrawalTestEnabled?:boolean;beforeAccountWithdrawalDispatch?:(token:string)=>Promise<void>} = {}): typeof fetch {
  if(options.accountWithdrawalTestEnabled===true && typeof options.beforeAccountWithdrawalDispatch!=="function")
    throw new Error("기존 탈퇴 세션 확인 연결이 필요합니다.");
  const portfolioPath = navigationConfig.portfolio_http.path;
  const baseMethods = options.portfolioTestEnabled === true
    ? {...authMethods, [portfolioPath]:["GET", "PUT"]} : authMethods;
  // Only the explicit Q3 TEST composition enables the prepared POST transport.
  const stateMethods = options.skinStateTestEnabled === true
    ? {...baseMethods,[skinStateConfig.http.path]:[skinStateConfig.http.method]} : baseMethods;
  const historyPath=historyConsentConfig.http.path;
  const historyMethods=options.historyConsentTestEnabled===true
    ? {...stateMethods,[historyPath]:[historyConsentConfig.http.read_method,historyConsentConfig.http.choice_method]} : stateMethods;
  // Held composition only. This option never enables a deployed server route.
  const savedPath=navigationConfig.saved_candidates_http.path;
  const coreMethods=options.coreTestReviewEnabled===true ? {...historyMethods,
    [savedPath]:["GET","PUT"],
    [navigationConfig.quota_status_http.path]:[navigationConfig.quota_status_http.method],
  } : historyMethods;
  const methods=options.accountWithdrawalTestEnabled===true
    ?{...coreMethods,[withdrawalConfig.http.path]:[withdrawalConfig.http.method]}:coreMethods;
  const execute=async (input: RequestInfo | URL, init:RequestInit|undefined,current:()=>boolean,prepare?:()=>Promise<void>) => {
    const currentGate=()=>{init?.signal?.throwIfAborted();if(!current())throw new DOMException("Request lifetime ended","AbortError");};
    currentGate();
    if(executionBudget.scope!=="existing_seoul_test_runtime_only" ||
      executionBudget.native_request_timeout_milliseconds!==35000 || executionBudget.native_auth_budget_milliseconds!==60000 ||
      executionBudget.ambiguous_write_retry!==false || executionBudget.quota_reset_or_member_data_changes!==false) {
      throw new Error("AWS TEST 요청 시간 설정을 확인하지 못했어요.");
    }
    init?.signal?.throwIfAborted();
    if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
      throw new Error("AWS TEST 인증 연결은 iPhone TEST 앱에서만 사용할 수 있습니다.");
    }
    const url = checkedUrl(input, methods);
    const method = (init?.method ?? "GET").toUpperCase();
    if (!methods[url.pathname].includes(method)) throw new Error("AWS TEST 인증 요청 방식이 허용 목록에 없습니다.");
    const rawBody = init?.body;
    if (rawBody !== undefined && rawBody !== null && typeof rawBody !== "string") {
      throw new Error("AWS TEST 인증 요청 본문 형식이 올바르지 않습니다.");
    }
    if ((method === "GET" || method === "DELETE") && rawBody != null && rawBody !== "") {
      throw new Error("AWS TEST 조회 요청에는 본문을 보낼 수 없습니다.");
    }
    const maxRequestBytes = url.pathname === skinStateConfig.http.path ? skinStateConfig.http.max_request_bytes
      : url.pathname === historyPath ? historyConsentConfig.http.max_request_bytes
      : url.pathname === savedPath ? navigationConfig.saved_candidates_http.max_request_bytes
      : url.pathname === portfolioPath ? navigationConfig.portfolio_http.max_request_bytes : 16_384;
    if (typeof rawBody === "string" && new TextEncoder().encode(rawBody).byteLength > maxRequestBytes) {
      throw new Error("AWS TEST 인증 요청이 허용 크기를 넘었습니다.");
    }
    let data: unknown = undefined;
    if (rawBody) {
      try { data = JSON.parse(rawBody); } catch { throw new Error("AWS TEST 인증 요청 JSON이 올바르지 않습니다."); }
    }
    const policy = loginConfig.client_database_resume_retry;
    const ordinaryWithdrawal=url.pathname===withdrawalConfig.http.path;
    const resume=withdrawalClientPolicy.bootstrap_resume;
    if(!Number.isSafeInteger(resume.maximum_attempts) || resume.maximum_attempts<1 || resume.maximum_attempts>policy.max_attempts ||
      !Number.isSafeInteger(resume.delay_milliseconds) || resume.delay_milliseconds<=0 ||
      (resume.maximum_attempts-1)*resume.delay_milliseconds>=executionBudget.native_auth_budget_milliseconds)
      throw new Error("탈퇴 준비 시간 설정을 확인해 주세요.");
    const maximumAttempts=ordinaryWithdrawal?resume.maximum_attempts:policy.max_attempts;
    const delay=ordinaryWithdrawal?resume.delay_milliseconds:policy.delay_milliseconds;
    const headers = checkedHeaders(init);
    const deadline = Date.now() + executionBudget.native_auth_budget_milliseconds;
    for (let attempt = 0; attempt < maximumAttempts; attempt++) {
      init?.signal?.throwIfAborted();
      const remaining = deadline - Date.now();
      if (remaining <= 0) throw new Error("서버 연결을 준비하지 못했어요. 잠시 뒤 다시 시도해 주세요.");
      const dispatch=async()=>{
        currentGate();
        if(prepare)await prepare();
        if(url.pathname===withdrawalConfig.http.path){
          const bearer=headers.authorization;
          if(!/^Bearer [A-Za-z0-9_-]{32,200}$/.test(bearer??""))throw new Error("기존 탈퇴 세션을 확인해 주세요.");
          await options.beforeAccountWithdrawalDispatch!(bearer.slice(7));
        }
        currentGate();
        const dispatchRemaining=deadline-Date.now();
        if(dispatchRemaining<=0)throw new Error("서버 연결을 준비하지 못했어요. 잠시 뒤 다시 시도해 주세요.");
        return CapacitorHttp.request({url:url.href,method,headers,data,
          connectTimeout:Math.min(executionBudget.native_request_timeout_milliseconds,dispatchRemaining),
          readTimeout:Math.min(executionBudget.native_request_timeout_milliseconds,dispatchRemaining),
          disableRedirects:true,responseType:"json"});
      };
      const nativeResponse=await awaitUnlessAborted(options.coreTestReviewEnabled===true
        ?serializeIOSAppTestRequest(url.origin,dispatch,{signal:init?.signal,beforeDispatch:currentGate})
        :dispatch(),init?.signal??undefined);
      currentGate();
      init?.signal?.throwIfAborted();
      const finalUrl = checkedUrl(nativeResponse.url, methods);
      if (finalUrl.href !== url.href) throw new Error("AWS TEST 인증 응답이 다른 주소로 이동했습니다.");
      const body = responseBody(nativeResponse);
      let resuming = false;
      try {
        const payload = JSON.parse(body);
        resuming = nativeResponse.status === policy.retryable_status
          && payload?.code === policy.retryable_error_code
          && Object.keys(payload).length === 1;
      } catch { /* A malformed response is never replayed. */ }
      if(ordinaryWithdrawal)resuming=accountWithdrawalNotStarted(nativeResponse.status,new Headers(nativeResponse.headers),body);
      // This code is issued only before route dispatch. Never retry an ambiguous
      // timeout, generic 503, provider call, or possibly committed portfolio write.
      if (resuming && !(url.pathname===historyPath && method===historyConsentConfig.http.choice_method)
          && url.pathname!==savedPath
          && attempt + 1 < maximumAttempts
          && Date.now() + delay < deadline) {
        await new Promise(resolve => window.setTimeout(resolve, delay));
        init?.signal?.throwIfAborted();
        continue;
      }
      return new Response(body, {status:nativeResponse.status, headers:nativeResponse.headers});
    }
    throw new Error("서버 연결을 준비하지 못했어요. 잠시 뒤 다시 시도해 주세요.");
  };
  const scoped=(current:()=>boolean,prepare?:()=>Promise<void>):typeof fetch=>Object.assign(
    ((input:RequestInfo|URL,init?:RequestInit)=>execute(input,init,current,prepare)) as typeof fetch,
    {within:(nested:()=>boolean,nestedPrepare?:()=>Promise<void>)=>scoped(()=>current()&&nested(),
      prepare||nestedPrepare?async()=>{if(prepare)await prepare();if(nestedPrepare)await nestedPrepare();}:undefined)},
  );
  return scoped(()=>true);
}
