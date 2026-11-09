import {Capacitor} from "@capacitor/core";

/** Build selection only. This does not authorize publishing or change the server environment. */
export const NATIVE_RELEASE_CANDIDATE_SELECTED = import.meta.env.PROD === true
  && import.meta.env.VITE_APP_MODE === "app_native_release_candidate"
  && import.meta.env.VITE_APP_NATIVE_RELEASE_CANDIDATE === "true";

export function nativeReleaseCandidateHostAvailable(): boolean {
  return NATIVE_RELEASE_CANDIDATE_SELECTED
    && Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios";
}
