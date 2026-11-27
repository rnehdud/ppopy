import {Capacitor, registerPlugin} from "@capacitor/core";

type IOSGoogleSignInBridge = {
  signIn(options?: {includeAuthorizationCode: true}): Promise<{idToken: string; authorizationCode?: string}>;
};

export type GoogleLoginAuthorization = {idToken: string; authorizationCode: string};

const bridge = registerPlugin<IOSGoogleSignInBridge>("IOSGoogleSignIn");

/** Native credential acquisition only; the app server validates the ID token. */
export async function getIOSGoogleIDToken(): Promise<string> {
  if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
    throw new Error("Google 로그인은 iPhone 앱에서만 사용할 수 있습니다.");
  }
  const result = await bridge.signIn();
  if (!result || Object.keys(result).join(",") !== "idToken"
      || typeof result.idToken !== "string" || result.idToken.length > 8192
      || !/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(result.idToken)) {
    throw new Error("Google 로그인 정보를 확인하지 못했습니다.");
  }
  return result.idToken;
}

/** Original login only; no code persistence or second authentication screen. */
export async function getIOSGoogleLoginAuthorization(): Promise<GoogleLoginAuthorization> {
  if (!Capacitor.isNativePlatform() || Capacitor.getPlatform() !== "ios") {
    throw new Error("Google 로그인은 iPhone 앱에서만 사용할 수 있습니다.");
  }
  const result = await bridge.signIn({includeAuthorizationCode: true});
  if (!result || Object.keys(result).sort().join(",") !== "authorizationCode,idToken"
      || typeof result.idToken !== "string" || result.idToken.length > 8192
      || !/^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(result.idToken)
      || typeof result.authorizationCode !== "string" || result.authorizationCode.length < 16
      || result.authorizationCode.length > 1024 || /[^A-Za-z0-9._~+/=-]/.test(result.authorizationCode)) {
    throw new Error("Google 로그인 정보를 확인하지 못했습니다.");
  }
  return {idToken: result.idToken, authorizationCode: result.authorizationCode};
}
