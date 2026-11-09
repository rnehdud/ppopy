import {Capacitor, registerPlugin} from "@capacitor/core";

type IOSAppleSignInBridge = {
  signIn(options: {nonce: string; includeAuthorizationCode?: true}): Promise<{idToken: string; authorizationCode?: string}>;
};

export type AppleLoginAuthorization = {idToken: string; authorizationCode: string};

const bridge = registerPlugin<IOSAppleSignInBridge>("IOSAppleSignIn");

/** Native credential acquisition only; the app server verifies and consumes the nonce. */
export async function getIOSAppleIDToken(nonce: string): Promise<string> {
  if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
    throw new Error("Apple 로그인은 iPhone 앱에서만 사용할 수 있습니다.");
  }
  if (typeof nonce !== "string" || !/^[A-Za-z0-9_-]{32,128}$/.test(nonce)) {
    throw new Error("Apple 로그인 요청을 다시 시작해 주세요.");
  }
  const result = await bridge.signIn({nonce});
  if (!result || Object.keys(result).join(",") !== "idToken"
      || typeof result.idToken !== "string" || result.idToken.length > 8192
      || !/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(result.idToken)) {
    throw new Error("Apple 로그인 정보를 확인하지 못했습니다.");
  }
  return result.idToken;
}

/** Opt-in original login; the one-time code stays in invocation memory only. */
export async function getIOSAppleLoginAuthorization(nonce: string): Promise<AppleLoginAuthorization> {
  if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
    throw new Error("Apple 로그인은 iPhone 앱에서만 사용할 수 있습니다.");
  }
  if (typeof nonce !== "string" || !/^[A-Za-z0-9_-]{32,128}$/.test(nonce)) {
    throw new Error("Apple 로그인 요청을 다시 시작해 주세요.");
  }
  const result = await bridge.signIn({nonce, includeAuthorizationCode: true});
  if (!result || Object.keys(result).sort().join(",") !== "authorizationCode,idToken"
      || typeof result.idToken !== "string" || result.idToken.length > 8192
      || !/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(result.idToken)
      || typeof result.authorizationCode !== "string"
      || result.authorizationCode.length < 16 || result.authorizationCode.length > 1024
      || /[^A-Za-z0-9._~+/=-]/.test(result.authorizationCode)) {
    throw new Error("Apple 로그인 정보를 확인하지 못했습니다.");
  }
  return {idToken: result.idToken, authorizationCode: result.authorizationCode};
}
