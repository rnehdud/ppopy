import { Browser } from "@capacitor/browser";
import { Capacitor } from "@capacitor/core";

import type { AppExternalLinkOpener } from "./appExternalLinks";

export interface IOSSystemBrowserBridge {
  open(options: { url: string }): Promise<void>;
}

export function createIOSSystemBrowserOpener(
  bridge: IOSSystemBrowserBridge,
  isNativeIOS: () => boolean,
): AppExternalLinkOpener {
  return {
    async openExternal(url) {
      if (!isNativeIOS()) throw new Error("iOS system browser bridge를 사용할 수 없습니다.");
      const parsed = new URL(url);
      if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.hash) {
        throw new Error("iOS 외부 링크는 안전한 HTTPS URL이어야 합니다.");
      }
      await bridge.open({ url: parsed.href });
    },
  };
}

export function createNativeIOSSystemBrowserOpener(): AppExternalLinkOpener {
  return createIOSSystemBrowserOpener(
    Browser,
    () => Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios",
  );
}
