import { CareApiError, type CareApiClient, type IntakeDraft } from "./careApi";
import { resumeAppSession, type AppSessionResumeResult } from "./appSessionResume";
import type { SessionVault } from "./appSessionVault";

export type AppBackgroundSaveResult =
  | { state: "saved" }
  | { state: "signed_out" }
  | { state: "retryable_error" }
  | { state: "vault_unavailable" }
  | { state: "save_unsupported" };

export type AppLifecycleTransition =
  | { transition: "background"; result: AppBackgroundSaveResult }
  | { transition: "foreground"; result: AppSessionResumeResult };

export async function saveAppDraftForBackground(
  vault: SessionVault,
  client: Pick<CareApiClient, "saveIntakeDraft">,
  draft: IntakeDraft,
): Promise<AppBackgroundSaveResult> {
  let token: string;
  try {
    const credential = await vault.load();
    if (!credential) return { state: "signed_out" };
    token = credential.session_token;
  } catch {
    return { state: "vault_unavailable" };
  }

  if (!client.saveIntakeDraft) return { state: "save_unsupported" };
  try {
    await client.saveIntakeDraft(token, draft);
    return { state: "saved" };
  } catch (error) {
    if (error instanceof CareApiError && (error.status === 401 || error.status === 403)) {
      try {
        await vault.clear();
      } catch {
        return { state: "vault_unavailable" };
      }
      return { state: "signed_out" };
    }
    return { state: "retryable_error" };
  }
}

export function createAppLifecycleCoordinator({
  vault,
  client,
  getDraft,
  onTransition,
}: {
  vault: SessionVault;
  client: Pick<CareApiClient, "saveIntakeDraft" | "readIntakeDraft">;
  getDraft: () => IntakeDraft;
  onTransition?: (transition: AppLifecycleTransition) => void;
}) {
  let phase: "foreground" | "background" = "foreground";
  let queue = Promise.resolve();

  const enqueue = <T,>(operation: () => Promise<T>): Promise<T> => {
    const pending = queue.then(operation, operation);
    queue = pending.then(() => undefined, () => undefined);
    return pending;
  };

  return {
    toBackground() {
      if (phase === "background") return queue;
      phase = "background";
      return enqueue(async () => {
        const transition: AppLifecycleTransition = {
          transition: "background",
          result: await saveAppDraftForBackground(vault, client, getDraft()),
        };
        onTransition?.(transition);
      });
    },
    toForeground() {
      if (phase === "foreground") return queue;
      phase = "foreground";
      return enqueue(async () => {
        const transition: AppLifecycleTransition = {
          transition: "foreground",
          result: await resumeAppSession(vault, client),
        };
        onTransition?.(transition);
      });
    },
    settled() { return queue; },
  };
}

export type AppLifecycleCoordinator = ReturnType<typeof createAppLifecycleCoordinator>;

export function bindBrowserAppLifecycle(
  documentSource: Pick<Document, "visibilityState" | "addEventListener" | "removeEventListener">,
  windowSource: Pick<Window, "addEventListener" | "removeEventListener">,
  coordinator: AppLifecycleCoordinator,
) {
  const onVisibility = () => {
    if (documentSource.visibilityState === "hidden") void coordinator.toBackground();
    if (documentSource.visibilityState === "visible") void coordinator.toForeground();
  };
  const onPageHide = () => { void coordinator.toBackground(); };
  const onPageShow = () => { void coordinator.toForeground(); };
  documentSource.addEventListener("visibilitychange", onVisibility);
  windowSource.addEventListener("pagehide", onPageHide);
  windowSource.addEventListener("pageshow", onPageShow);
  return () => {
    documentSource.removeEventListener("visibilitychange", onVisibility);
    windowSource.removeEventListener("pagehide", onPageHide);
    windowSource.removeEventListener("pageshow", onPageShow);
  };
}
