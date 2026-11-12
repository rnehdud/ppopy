import {Capacitor} from "@capacitor/core";
import rules from "../../skin_engine/config/product_web_client.json";
import {checkedIngredientDrafts, type ProductIngredientDraft} from "./productIngredientDraft";
import type {WebProductCandidate} from "./productCatalog";
import {ownerProductSearchBridge, prepareNativeOwnerProductSearch} from "./iosProductPhotoSearch";
import {recordSearchTiming, searchDuration, type SearchTimingObserver} from "./searchTiming";
import type {ProductSearchOptions} from "./careApi";
import {awaitSearchRequest} from "./searchRequestLifetime";

type Bridge = {searchWeb(options: {requestId: string; productQuery: string; purpose?: "ingredients"}): Promise<unknown>; cancel(options: {requestId: string}): Promise<void>};
const bridge: Bridge = {searchWeb: options => ownerProductSearchBridge.searchWeb!(options), cancel: options => ownerProductSearchBridge.cancel(options)};
export const nativeIOSWebSearchAvailable = () => rules.environment === "test" && Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios"
  && (rules.enabled || (import.meta.env.VITE_OWNER_PRODUCT_WEB_TEST_ENABLED === "true" && import.meta.env.VITE_IPHONE_TEST_MODE === "true"));
const messages: Record<string,string> = {
  photo_test_access_required: "비공개 TEST 연결 코드를 확인해 주세요.",
  photo_test_access_denied: "비공개 TEST 연결 코드가 승인되지 않았어요.",
  photo_test_database_warming: "제품 검색 DB를 켜는 중이에요. 잠시 후 다시 시도해 주세요.",
  photo_test_limit: "인터넷 TEST 검색 한도에 도달했어요.",
  photo_test_busy: "이전 제품 검색이 진행 중이에요. 잠시 후 다시 시도해 주세요.",
  photo_test_input_invalid: "연락처 없이 브랜드와 제품명만 입력해 주세요.",
  photo_test_timeout: "인터넷 검색이 지연되고 있어요. 잠시 후 다시 시도해 주세요.",
};
export function checkedWebCandidates(value: unknown): WebProductCandidate[] {
  const invalid = () => new Error("인터넷 제품 후보와 출처를 확인하지 못했어요.");
  if (!value || typeof value !== "object" || Array.isArray(value)) throw invalid();
  const envelope = value as Record<string,unknown>;
  if (Object.keys(envelope).sort().join("|") !== "auto_confirmed|candidates|provider" || envelope.provider !== "openai_responses"
    || envelope.auto_confirmed !== false || !Array.isArray(envelope.candidates) || envelope.candidates.length > rules.maximum_candidates) throw invalid();
  return envelope.candidates.map(value => {
    if (!value || typeof value !== "object" || Array.isArray(value)) throw invalid();
    const item = value as Record<string,unknown>;
    const fields = ["candidate_id","provenance_hash","snippet","source_domain","source_url","title"];
    if (Object.keys(item).sort().join("|") !== fields.join("|") || fields.some(key => typeof item[key] !== "string")) throw invalid();
    const candidate = item as Record<string,string>;
    let url: URL; try {url = new URL(candidate.source_url);} catch {throw invalid();}
    if (url.protocol !== "https:" || url.username || url.password || !url.hostname || url.hostname !== candidate.source_domain
      || candidate.source_url.length > 4096 || !candidate.title.trim() || candidate.title.length > 360 || candidate.snippet.length > 480
      || !/^[a-f0-9]{64}$/.test(candidate.provenance_hash) || candidate.candidate_id !== candidate.provenance_hash.slice(0,24)) throw invalid();
    return {candidateId:candidate.candidate_id,title:candidate.title,sourceDomain:candidate.source_domain,sourceUrl:candidate.source_url,snippet:candidate.snippet,provenanceHash:candidate.provenance_hash};
  });
}
export function createIOSProductSearcher<T>(native: Bridge, enabled: () => boolean, parse: (value: unknown) => T[], purpose?: "ingredients", requestId = () => crypto.randomUUID(), observe: SearchTimingObserver = recordSearchTiming, now: () => number = () => performance.now()) {
  const cache = new Map<string, {expires: number; value: T[]}>();
  const pending = new Map<string, Promise<T[]>>();
  return async (text: string, options?: ProductSearchOptions): Promise<T[]> => {
    options?.signal?.throwIfAborted();
    if (!enabled()) throw new Error("인터넷 제품 검색은 아직 연결 전이에요.");
    const query = text.normalize("NFKC").trim().replace(/\s+/g," ");
    if (query.length < 2 || query.length > rules.maximum_query_characters || /[\r\n@]/.test(text)
      || /(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}/.test(query)) throw new Error("연락처 없이 브랜드와 제품명만 입력해 주세요.");
    // Owner-preview reuse has no member identity. A cancellable member call must
    // never join/cache another connection's pending or completed operation.
    const scoped = Boolean(options?.signal);
    const cached = scoped ? undefined : cache.get(query);
    const stage = purpose ? "ingredients" : "web_product";
    if (cached && cached.expires > Date.now()) {
      observe({version:"1.0.0", stage, outcome:cached.value.length ? "success" : "empty", reuse:"cache", duration_ms:0});
      return structuredClone(cached.value);
    }
    const existing = scoped ? undefined : pending.get(query); if (existing) {
      const started = now();
      try {
        const value = await existing;
        observe({version:"1.0.0", stage, outcome:value.length ? "success" : "empty", reuse:"coalesced", duration_ms:searchDuration(started, now())});
        return structuredClone(value);
      } catch (error) {
        observe({version:"1.0.0", stage, outcome:"failed", reuse:"coalesced", duration_ms:searchDuration(started, now())});
        throw error;
      }
    }
    const run = async () => {
    const started = now();
    const id = requestId();
    try {
      const result = await awaitSearchRequest(
        () => native.searchWeb({requestId:id,productQuery:query,...(purpose ? {purpose} : {})}),
        () => native.cancel({requestId:id}), options?.signal,
        {milliseconds:rules.timeout_milliseconds,error:{code:"photo_test_timeout"}},
      );
      options?.signal?.throwIfAborted();
      const value = parse(result);
      observe({version:"1.0.0", stage, outcome:value.length ? "success" : "empty", reuse:"network", duration_ms:searchDuration(started, now())});
      return value;
    } catch(error) {
      observe({version:"1.0.0", stage, outcome:options?.signal?.aborted ? "cancelled" : "failed", reuse:"network", duration_ms:searchDuration(started, now())});
      options?.signal?.throwIfAborted();
      const code = error && typeof error === "object" && "code" in error ? error.code : undefined;
      throw new Error(typeof code === "string" && Object.hasOwn(messages,code) ? messages[code] : "인터넷 제품 검색을 완료하지 못했어요. 잠시 후 다시 시도해 주세요.");
    }
    };
    if (scoped) return structuredClone(await run());
    const operation = run();
    pending.set(query, operation);
    try {
      const value = await operation;
      cache.delete(query); cache.set(query, {expires: Date.now() + rules.session_cache.ttl_milliseconds, value: structuredClone(value)});
      while (cache.size > rules.session_cache.maximum_entries) cache.delete(cache.keys().next().value!);
      return structuredClone(value);
    } finally {pending.delete(query);}
  };
}
export function createIOSWebSearcher(native: Bridge, enabled: () => boolean, requestId = () => crypto.randomUUID()) {
  return createIOSProductSearcher(native, enabled, checkedWebCandidates, undefined, requestId);
}
const search = createIOSWebSearcher(bridge,nativeIOSWebSearchAvailable);
export async function searchNativeIOSWebProducts(query: string, options?: ProductSearchOptions) {
  await awaitSearchRequest(prepareNativeOwnerProductSearch,async()=>{},options?.signal);
  options?.signal?.throwIfAborted();return search(query,options);
}

const ingredients = createIOSProductSearcher<ProductIngredientDraft>(bridge,nativeIOSWebSearchAvailable,checkedIngredientDrafts,"ingredients");
export async function searchNativeIOSIngredientDrafts(query: string, options?: ProductSearchOptions) {
  await awaitSearchRequest(prepareNativeOwnerProductSearch,async()=>{},options?.signal);
  options?.signal?.throwIfAborted();return ingredients(query,options);
}
