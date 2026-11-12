import {Capacitor, registerPlugin} from "@capacitor/core";
import rules from "../../skin_engine/config/product_photo_client.json";
import type {IOSSessionVaultBridge} from "./iosSessionVaultStore";
// This separate plugin stores only the photo TEST connection code; it does
// not implement the session vault's original-value cleanup operation.
interface ProductPhotoAccessBridge extends Pick<IOSSessionVaultBridge,"get"|"set"|"remove"> {
  status(options: {key: string}): Promise<{stored: boolean}>;
}
const bridge = registerPlugin<ProductPhotoAccessBridge>("IOSProductPhotoAccess");
export function createProductPhotoAccessStore(native: ProductPhotoAccessBridge, isIOS: () => boolean) {
  const ready = () => { if (!isIOS()) throw new Error("TEST 연결 설정은 iPhone 앱에서만 저장할 수 있습니다."); };
  return {
    async isStored(): Promise<boolean> {
      ready(); const response = await native.status({key: rules.token_key});
      if (!response || Object.keys(response).join("|") !== "stored" || typeof response.stored !== "boolean") throw new Error("기기 저장 여부를 확인하지 못했습니다.");
      return response.stored;
    },
    async get(): Promise<string | null> {
      ready(); const response = await native.get({key: rules.token_key});
      if (!response || Object.keys(response).join("|") !== "value" || (response.value !== null && (typeof response.value !== "string" || (response.value.startsWith("sk-") || !/^[A-Za-z0-9_-]{32,128}$/.test(response.value))))) throw new Error("TEST 연결 설정을 확인하지 못했습니다.");
      return response.value;
    },
    async set(value: string): Promise<void> {
      ready(); if ((value.startsWith("sk-") || !/^[A-Za-z0-9_-]{32,128}$/.test(value))) throw new Error("사진 검색 전용 TEST 연결 코드를 확인해 주세요.");
      await native.set({key: rules.token_key, value});
    },
    async remove(): Promise<void> { ready(); await native.remove({key: rules.token_key}); },
  };
}
export const productPhotoAccessStore = createProductPhotoAccessStore(bridge, () => Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios");
