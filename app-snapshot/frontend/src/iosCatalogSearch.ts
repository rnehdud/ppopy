import { Capacitor, registerPlugin } from "@capacitor/core";

import {isRoutineProductCategory} from "./routineProductGroups";
import type { ProductCandidate } from "./productCatalog";
import {recordSearchTiming, searchDuration, type SearchTimingObserver} from "./searchTiming";
import { isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl } from "./miraySavedCandidates";
import type {ProductSearchOptions} from "./careApi";
import {awaitSearchRequest} from "./searchRequestLifetime";

export interface IOSCatalogSearchBridge {
  search(options: { query: string; requestId?: string }): Promise<unknown>;
  cancel?(options: {requestId: string}): Promise<void>;
}

const nativeBridge = registerPlugin<IOSCatalogSearchBridge>("IOSCatalogSearch");
const EVIDENCE = new Set(["owner_verified", "automation_verified", "review_required"]);

export function nativeIOSCatalogAvailable(): boolean {
  return Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios";
}

export function createIOSCatalogSearcher(
  bridge: IOSCatalogSearchBridge,
  isNativeIOS: () => boolean,
  observe: SearchTimingObserver = recordSearchTiming,
  now: () => number = () => performance.now(),
): (query: string, options?: ProductSearchOptions) => Promise<ProductCandidate[]> {
  return async (query, options) => {
    options?.signal?.throwIfAborted();
    if (!isNativeIOS()) throw new Error("AWS TEST 카탈로그는 iPhone TEST 앱에서만 직접 조회할 수 있습니다.");
    const normalized = query.normalize("NFKC").trim().replace(/\s+/g, " ");
    if (normalized.length < 1 || normalized.length > 200 || normalized.includes("@") || /(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}/.test(normalized)) {
      throw new Error("연락처 없이 제품명만 1~200자로 입력해 주세요.");
    }
    const started = now();
    let payload: unknown;
    try {
      const signal = options?.signal;
      if (signal) {
        if (!bridge.cancel) throw new Error("검색 중단을 지원하는 TEST 앱 업데이트가 필요해요.");
        const requestId = crypto.randomUUID();
        payload = await awaitSearchRequest(() => bridge.search({query:normalized,requestId}),() => bridge.cancel!({requestId}),signal);
        signal.throwIfAborted();
      } else payload = await bridge.search({query: normalized});
      if (!payload || typeof payload !== "object" || Array.isArray(payload)) {
        throw new Error("AWS TEST 카탈로그 응답을 확인하지 못했습니다.");
      }
      const record = payload as Record<string, unknown>;
      if (record.auto_confirmed !== false || !Array.isArray(record.candidates)) {
        throw new Error("제품 후보 자동 확정 응답은 허용되지 않습니다.");
      }
      const candidates = record.candidates.map(value => {
        if (!value || typeof value !== "object" || Array.isArray(value)) {
          throw new Error("AWS TEST 제품 후보 형식이 올바르지 않습니다.");
        }
        const item = value as Record<string, unknown>;
        const evidence = item.ingredient_evidence_status;
        const sourceUrl = item.source_url ?? null;
        const provenanceHash = item.provenance_hash ?? null;
        if (
          typeof item.product_id !== "string"
          || typeof item.brand !== "string"
          || typeof item.name !== "string"
          || typeof item.option !== "string"
          || typeof evidence !== "string"
          || !EVIDENCE.has(evidence)
          || (sourceUrl !== null && typeof sourceUrl !== "string")
          || (provenanceHash !== null && typeof provenanceHash !== "string")
          || (sourceUrl === null) !== (provenanceHash === null)
        ) throw new Error("AWS TEST 제품 후보 형식이 올바르지 않습니다.");
        if (sourceUrl !== null) {
          try { validateMirayCandidateSourceUrl(sourceUrl); }
          catch { throw new Error("AWS TEST 제품 후보 형식이 올바르지 않습니다."); }
          if (!isMirayCandidateProvenanceHash(provenanceHash!)) throw new Error("AWS TEST 제품 후보 형식이 올바르지 않습니다.");
        }
        return {
          id: item.product_id,
          brand: item.brand,
          name: item.name,
          option: item.option,
          evidenceStatus: evidence as ProductCandidate["evidenceStatus"],
          matchSource: "catalog" as const,
          ...(isRoutineProductCategory(item.category) ? {category:item.category} : {}),
          ...(sourceUrl ? {sourceUrl, provenanceHash:provenanceHash!} : {}),
        };
      });
      observe({version:"1.0.0", stage:"catalog", outcome:candidates.length ? "success" : "empty", reuse:"network", duration_ms:searchDuration(started, now())});
      return candidates;
    } catch (error) {
      observe({version:"1.0.0", stage:"catalog", outcome:options?.signal?.aborted ? "cancelled" : "failed", reuse:"network", duration_ms:searchDuration(started, now())});
      throw error;
    }
  };
}

export const searchNativeIOSCatalog = createIOSCatalogSearcher(nativeBridge, nativeIOSCatalogAvailable);
