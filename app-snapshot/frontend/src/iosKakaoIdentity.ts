import {Capacitor, registerPlugin} from "@capacitor/core";

type IOSKakaoSignInBridge = {
  signIn(): Promise<{accessToken: string}>;
};

const bridge = registerPlugin<IOSKakaoSignInBridge>("IOSKakaoSignIn");

/** Acquire a native access token; only the app server authenticates it. */
export async function getIOSKakaoAccessToken(): Promise<string> {
  if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
    throw new Error("카카오 로그인은 iPhone 앱에서만 사용할 수 있습니다.");
  }
  const result = await bridge.signIn();
  if (!result || Object.keys(result).join(",") !== "accessToken"
      || typeof result.accessToken !== "string"
      || !/^[A-Za-z0-9._~+/=-]{20,2048}$/.test(result.accessToken)) {
    throw new Error("카카오 로그인 정보를 확인하지 못했습니다.");
  }
  return result.accessToken;
}
