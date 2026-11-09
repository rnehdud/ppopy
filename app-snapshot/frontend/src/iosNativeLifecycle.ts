import { App as CapacitorApp } from "@capacitor/app";
import { Capacitor } from "@capacitor/core";

import type { AppLifecycleCoordinator } from "./appLifecycle";

export interface IOSAppLifecycleBridge {
  addListener(
    eventName: "appStateChange",
    listener: (state: { isActive: boolean }) => void,
  ): Promise<{ remove(): Promise<void> }>;
}

export async function bindIOSNativeLifecycle(
  bridge: IOSAppLifecycleBridge,
  coordinator: AppLifecycleCoordinator,
  isNativeIOS: () => boolean,
): Promise<() => Promise<void>> {
  if (!isNativeIOS()) throw new Error("iOS native lifecycle bridge를 사용할 수 없습니다.");
  const handle = await bridge.addListener("appStateChange", state => {
    if (state.isActive) void coordinator.toForeground();
    else void coordinator.toBackground();
  });
  return () => handle.remove();
}

export function bindCurrentIOSNativeLifecycle(
  coordinator: AppLifecycleCoordinator,
): Promise<() => Promise<void>> {
  return bindIOSNativeLifecycle(
    CapacitorApp,
    coordinator,
    () => Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios",
  );
}
