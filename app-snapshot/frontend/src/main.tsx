import {Capacitor} from "@capacitor/core";
import "./nativeShell.css";
import { StrictMode,lazy,Suspense } from "react";
import { createRoot } from "react-dom/client";

import App from "./App";
import BetaApp from "./BetaApp";
import AppLaunchPreview from "./AppLaunchPreview";
import AppErrorBoundary from "./AppErrorBoundary";
import AppSettingsPreview from "./AppSettingsPreview";
import AccountStartPreview from "./AccountStartPreview";
import AppAuthTest from "./AppAuthTest";
import AppAuthLoopNativeTestReview from "./AppAuthLoopNativeTestReview";
import AppNativeReleaseCandidate from "./AppNativeReleaseCandidate";
import AppVisualFrame from "./AppVisualFrame";

if (Capacitor.isNativePlatform()) {
  document.documentElement.classList.add("poppy-native");
  document.body.classList.add("poppy-native");
}

const KbDevelopment=import.meta.env.DEV?lazy(()=>import('./AppKbDevelopment')):null;
const appMode = import.meta.env.VITE_APP_MODE;
const rootApp = KbDevelopment && import.meta.env.DEV && import.meta.env.VITE_KB_APP_PREVIEW === "true" && appMode === "kb_app_development" ? <Suspense fallback={<p>KB 개발 연결 준비 중</p>}><KbDevelopment/></Suspense> : appMode === "beta_staging"
  ? <BetaApp />
  : appMode === "app_native_release_candidate"
    ? <AppNativeReleaseCandidate />
  : appMode === "app_auth_test"
    ? (import.meta.env.VITE_APP_LOOP_NATIVE_TEST_REVIEW === "true" ? <AppAuthLoopNativeTestReview /> : <AppAuthTest />)
  : appMode === "app_account_preview"
    ? <AccountStartPreview />
  : appMode === "app_settings_preview"
    ? <AppSettingsPreview />
  : appMode === "app_preview"
    ? <AppLaunchPreview />
    : <App audience={appMode === "friend_demo" ? "friend" : "internal"} />;

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppErrorBoundary>{new Set(["app_preview", "app_settings_preview", "app_account_preview", "app_auth_test", "app_native_release_candidate"]).has(appMode)
      ? <AppVisualFrame>{rootApp}</AppVisualFrame> : rootApp}</AppErrorBoundary>
  </StrictMode>,
);

if (appMode!=="kb_app_development" && !new Set(["app_preview", "app_settings_preview", "app_account_preview", "app_auth_test", "app_native_release_candidate"]).has(appMode) && "serviceWorker" in navigator && window.isSecureContext) {
  window.addEventListener("load", () => {
    void navigator.serviceWorker.register("/sw.js").catch(() => {
      // 앱 셸 캐시 실패는 제품 검색·문진·삭제 흐름을 막지 않는다.
    });
  });
}
