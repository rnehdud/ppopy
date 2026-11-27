import {Capacitor, registerPlugin} from "@capacitor/core";
import {ProductPhotoSearchError, safeNativePhotoError} from "./productPhotoErrors";
import rules from "../../skin_engine/config/product_photo_client.json";
import {photoBase64} from "./productPhotoPreparation";
import {checkedPhotoIdentity, productPhotoClientEnabled} from "./testProductPhotoTransport";
import {recordSearchTiming, searchDuration, type SearchTimingObserver} from "./searchTiming";

export type IOSProductPhotoSearchBridge = {
  search(options: {requestId: string; imageBase64: string; productAreaConfirmed: true}): Promise<unknown>;
  cancel(options: {requestId: string}): Promise<void>;
  searchWeb?(options: {requestId: string; productQuery: string; purpose?: "ingredients"}): Promise<unknown>;
  prepare?(options: {requestId: string}): Promise<unknown>;
};
export const ownerProductSearchBridge = registerPlugin<IOSProductPhotoSearchBridge>("IOSProductPhotoSearch");

export function createIOSProductPhotoSearcher(native: IOSProductPhotoSearchBridge, enabled: () => boolean, requestId = () => crypto.randomUUID(), observe: SearchTimingObserver = recordSearchTiming, now: () => number = () => performance.now()) {
  return async (photo: Blob, confirmed: boolean, signal?: AbortSignal) => {
    if (!enabled()) throw new Error("AI 사진 검색은 아직 연결 준비 중이에요. 제품명으로 검색해 주세요.");
    if (confirmed !== true || photo.type !== "image/jpeg" || photo.size < 4 || photo.size > rules.maximum_image_bytes) throw new Error("제품 영역과 전송 안내를 확인해 주세요.");
    signal?.throwIfAborted();
    const started = now();
    const imageBase64 = await photoBase64(photo);
    signal?.throwIfAborted();
    const id = requestId();
    let cancel: (() => void) | undefined;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let cancelled = false;
    const cancelNative = () => {
      if (cancelled) return;
      cancelled = true;
      // Cancellation failure is contained; native timeout still bounds the request.
      void native.cancel({requestId: id}).catch(() => undefined);
    };
    try {
      const interrupted = new Promise<never>((_resolve, reject) => {
        cancel = () => { cancelNative(); reject(new DOMException("Capture cancelled", "AbortError")); };
        signal?.addEventListener("abort", cancel, {once: true});
        timer = setTimeout(() => { cancelNative(); reject(new ProductPhotoSearchError("photo_test_timeout")); }, rules.timeout_milliseconds);
      });
      const result = await Promise.race([native.search({requestId: id, imageBase64, productAreaConfirmed: true}), interrupted]);
      signal?.throwIfAborted();
      const identity = checkedPhotoIdentity(result);
      observe({version:"1.0.0", stage:"photo_identity", outcome:"success", reuse:"network", duration_ms:searchDuration(started, now())});
      return identity;
    } catch (error) {
      observe({version:"1.0.0", stage:"photo_identity", outcome:signal?.aborted ? "cancelled" : "failed", reuse:"network", duration_ms:searchDuration(started, now())});
      if (signal?.aborted) throw new DOMException("Capture cancelled", "AbortError");
      // No raw bridge/provider error, token, image or URL reaches the UI.
      if (cancelled) throw new ProductPhotoSearchError("photo_test_timeout");
      if (error instanceof Error && error.message === "제품명 후보를 확인하지 못했습니다.") throw new ProductPhotoSearchError("photo_test_identity_invalid");
      throw safeNativePhotoError(error);
    } finally {
      if (timer !== undefined) clearTimeout(timer);
      if (cancel) signal?.removeEventListener("abort", cancel);
    }
  };
}

const searchOwnerPhoto = createIOSProductPhotoSearcher(ownerProductSearchBridge,
  () => productPhotoClientEnabled() && Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios");

export function createNativeOwnerProductPreparation(
  native: Pick<IOSProductPhotoSearchBridge,"prepare">,
  enabled: () => boolean,
  observe: SearchTimingObserver = recordSearchTiming,
  now: () => number = () => performance.now(),
  sleep: (milliseconds: number) => Promise<void> = milliseconds => new Promise(resolve => setTimeout(resolve,milliseconds)),
  requestId: () => string = () => crypto.randomUUID(),
) {
  return async () => {
    if (!enabled() || !native.prepare) return;
    const started = now();
    for (let attempt = 0; attempt < 3; attempt += 1) {
      try {
        await native.prepare({requestId:requestId()});
        observe({version:"1.0.0", stage:"database_ready", outcome:"success", reuse:"network", duration_ms:searchDuration(started, now())});
        return;
      } catch (error) {
        const code = error && typeof error === "object" && "code" in error ? error.code : undefined;
        if (code !== "photo_test_database_warming" || attempt === 2) {
          observe({version:"1.0.0", stage:"database_ready", outcome:"failed", reuse:"network", duration_ms:searchDuration(started, now())});
          return;
        }
        // Readiness probes have no provider reservation or paid request. Give
        // Aurora another bounded window instead of consuming a failed search.
        await sleep(1_500 * (attempt + 1));
      }
    }
  };
}

let preparation: Promise<void> | undefined;
const prepareOwnerSearch = createNativeOwnerProductPreparation(ownerProductSearchBridge, productPhotoClientEnabled);
export function prepareNativeOwnerProductSearch(): Promise<void> {
  if (!productPhotoClientEnabled() || !ownerProductSearchBridge.prepare) return Promise.resolve();
  if (!preparation) preparation = prepareOwnerSearch().finally(() => {preparation=undefined;});
  return preparation;
}
export async function searchNativeIOSProductPhoto(photo: Blob, confirmed: boolean, signal?: AbortSignal) {
  signal?.throwIfAborted(); await prepareNativeOwnerProductSearch(); signal?.throwIfAborted();
  return searchOwnerPhoto(photo,confirmed,signal);
}
