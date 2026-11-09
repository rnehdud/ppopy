import rules from "../../skin_engine/config/product_photo_client.json";
import {photoBase64} from "./productPhotoPreparation";
import {Capacitor} from "@capacitor/core";

export type ProductPhotoIdentity = {brand: string | null; product_name: string | null; variant: string | null; volume: string | null; needs_user_confirmation: true; auto_confirmed: false};
export const productPhotoClientEnabled = () => rules.environment === "test" && (rules.enabled === true
  || (import.meta.env.VITE_OWNER_PRODUCT_PHOTO_TEST_ENABLED === "true"
    && import.meta.env.VITE_IPHONE_TEST_MODE === "true"
    && Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios"));
const fields = ["auto_confirmed", "brand", "needs_user_confirmation", "product_name", "variant", "volume"];
export function checkedPhotoIdentity(payload: unknown): ProductPhotoIdentity {
  if (!payload || typeof payload !== "object" || Array.isArray(payload)) throw new Error("제품명 후보를 확인하지 못했습니다.");
  const incoming = payload as Record<string, unknown>;
  const {schema_version, ...identity} = incoming;
  if (Object.hasOwn(incoming, "schema_version") && schema_version !== "2.0.0") throw new Error("제품명 후보를 확인하지 못했습니다.");
  const record = Object.hasOwn(incoming, "schema_version") ? identity : incoming;
  if (Object.keys(record).sort().join("|") !== fields.join("|") || record.auto_confirmed !== false || record.needs_user_confirmation !== true
    || ["brand", "product_name", "variant", "volume"].some(key => record[key] !== null && (typeof record[key] !== "string" || (record[key] as string).length > 180))) {
    throw new Error("제품명 후보를 확인하지 못했습니다.");
  }
  return record as ProductPhotoIdentity;
}

export function createTestProductPhotoSearcher(fetcher: typeof fetch, options: {enabled: () => boolean; loadAccessToken: () => Promise<string | null>}) {
  return async (photo: Blob, confirmed: boolean, signal?: AbortSignal): Promise<ProductPhotoIdentity> => {
    if (!options.enabled()) throw new Error("AI 사진 검색은 아직 연결 준비 중이에요. 제품명으로 검색해 주세요.");
    if (confirmed !== true || photo.type !== "image/jpeg" || photo.size < 4 || photo.size > rules.maximum_image_bytes) throw new Error("제품 영역과 전송 안내를 확인해 주세요.");
    signal?.throwIfAborted();
    const token = await options.loadAccessToken();
    if (!token || (token.startsWith("sk-") || !/^[A-Za-z0-9_-]{32,128}$/.test(token))) throw new Error("TEST 연결 설정이 필요합니다.");
    signal?.throwIfAborted();
    const image_base64 = await photoBase64(photo);
    signal?.throwIfAborted();
    const controller = new AbortController();
    const abort = () => controller.abort();
    signal?.addEventListener("abort", abort, {once: true});
    const timeout = setTimeout(abort, rules.timeout_milliseconds);
    try {
      const response = await fetcher(rules.api_base_url + rules.route, {
        method: "POST", headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`},
        body: JSON.stringify({image_base64, product_area_confirmed: true}),
        credentials: "omit", cache: "no-store", redirect: "error", referrerPolicy: "no-referrer", signal: controller.signal,
      });
      if (!response.ok) throw new Error(response.status === 429 ? "사진 검색 한도에 도달했어요. 제품명으로 검색해 주세요." : "AI 사진 검색을 완료하지 못했어요. 제품명으로 검색해 주세요.");
      if (Number(response.headers.get("content-length")) > rules.maximum_response_bytes) throw new Error("제품명 후보를 확인하지 못했습니다.");
      const reader = response.body?.getReader();
      if (!reader) throw new Error("제품명 후보를 확인하지 못했습니다.");
      const chunks: Uint8Array[] = []; let size = 0;
      try {
        while (true) {
          const {done, value} = await reader.read(); if (done) break;
          size += value.byteLength;
          if (size > rules.maximum_response_bytes) { await reader.cancel(); throw new Error("제품명 후보를 확인하지 못했습니다."); }
          chunks.push(value);
        }
      } finally { reader.releaseLock(); }
      const bytes = new Uint8Array(size); let offset = 0;
      for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
      return checkedPhotoIdentity(JSON.parse(new TextDecoder().decode(bytes)));
    } catch (error) {
      if (signal?.aborted) throw new DOMException("Capture cancelled", "AbortError");
      if (controller.signal.aborted) throw new Error("사진 검색이 지연되고 있어요. 제품명으로 검색해 주세요.");
      // No raw provider response, image, token or request URL is surfaced/logged.
      if (error instanceof Error && /^(AI 사진|사진 검색|제품명 후보)/.test(error.message)) throw error;
      throw new Error("AI 사진 검색을 완료하지 못했어요. 제품명으로 검색해 주세요.");
    } finally { clearTimeout(timeout); signal?.removeEventListener("abort", abort); }
  };
}
