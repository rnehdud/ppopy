import { Capacitor, registerPlugin } from "@capacitor/core";

import { APP_SESSION_VAULT_KEY, type SecureValueStore } from "./appSessionVault";

export interface IOSSessionVaultBridge {
  get(options: { key: string }): Promise<{ value: string | null }>;
  set(options: { key: string; value: string }): Promise<void>;
  remove(options: { key: string }): Promise<void>;
  removeIfValueMatches(options:{key:string;expectedValue:string|null}):Promise<{removed:boolean}>;
}

const nativeBridge = registerPlugin<IOSSessionVaultBridge>("IOSSessionVault");

function requireVaultKey(key: string): void {
  if (key !== APP_SESSION_VAULT_KEY) {
    throw new Error("iOS Keychain 저장소는 앱 세션 key만 허용합니다.");
  }
}

export function createIOSKeychainStore(
  bridge: IOSSessionVaultBridge,
  isNativeIOS: () => boolean,
): SecureValueStore {
  const ready = () => {
    if (!isNativeIOS()) throw new Error("iOS native Keychain bridge를 사용할 수 없습니다.");
  };
  return {
    async get(key) {
      ready();
      requireVaultKey(key);
      const response = await bridge.get({ key });
      if (
        !response
        || typeof response !== "object"
        || Object.keys(response).join("|") !== "value"
        || (response.value !== null && typeof response.value !== "string")
      ) throw new Error("iOS Keychain 응답 계약이 올바르지 않습니다.");
      return response.value;
    },
    async set(key, value) {
      ready();
      requireVaultKey(key);
      await bridge.set({ key, value });
    },
    async remove(key) {
      ready();
      requireVaultKey(key);
      await bridge.remove({ key });
    },
    async removeIfValueMatches(key,expectedValue) {
      ready();requireVaultKey(key);
      if(expectedValue!==null && typeof expectedValue!=="string")throw new Error("기존 세션 값이 올바르지 않습니다.");
      const response=await bridge.removeIfValueMatches({key,expectedValue});
      if(!response || typeof response!=="object" || Array.isArray(response)
        || Object.keys(response).join("|")!=="removed" || typeof response.removed!=="boolean") {
        throw new Error("iOS Keychain 조건부 정리 응답 계약이 올바르지 않습니다.");
      }
      return response.removed;
    },
  };
}

export function createNativeIOSKeychainStore(): SecureValueStore {
  return createIOSKeychainStore(
    nativeBridge,
    () => Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios",
  );
}
