import { appOperationAllowed, type AppCompatibilityState, type AppOperation } from "./appClientCompatibility";
import { CareApiError, type CareApiClient } from "./careApi";

export function createCompatibilityGuardedCareApiClient(
  source: CareApiClient,
  currentState: () => AppCompatibilityState,
): CareApiClient {
  const run = <T>(operation: AppOperation, action: () => Promise<T>): Promise<T> => {
    const state = currentState();
    if (!appOperationAllowed(state, operation)) {
      const code = state === "update_required" ? "app_update_required" : "app_compatibility_unavailable";
      return Promise.reject(new CareApiError("현재 앱 버전에서는 이 작업을 시작할 수 없습니다.", 503, code));
    }
    return action();
  };
  return {
    mode: source.mode,
    readAppCompatibility: source.readAppCompatibility
      ? (...args) => source.readAppCompatibility!(...args)
      : undefined,
    saveIntakeDraft: source.saveIntakeDraft
      ? (...args) => run("intake", () => source.saveIntakeDraft!(...args))
      : undefined,
    readIntakeDraft: source.readIntakeDraft
      ? (...args) => run("draft_read", () => source.readIntakeDraft!(...args))
      : undefined,
    recordPilotEvent: source.recordPilotEvent
      ? (...args) => run("intake", () => source.recordPilotEvent!(...args))
      : undefined,
    requestProductResolution: source.requestProductResolution
      ? (...args) => run("intake", () => source.requestProductResolution!(...args))
      : undefined,
    readProductResolutions: source.readProductResolutions
      ? (...args) => run("result_read", () => source.readProductResolutions!(...args))
      : undefined,
    searchProducts: (...args) => run("catalog_read", () => source.searchProducts(...args)),
    analyze: (...args) => run("intake", () => source.analyze(...args)),
    getBetaNotices: (...args) => run("catalog_read", () => source.getBetaNotices(...args)),
    startBetaSession: (...args) => run("admission", () => source.startBetaSession(...args)),
    submitBetaCare: (...args) => run("intake", () => source.submitBetaCare(...args)),
    createPaymentOrder: (...args) => run("purchase", () => source.createPaymentOrder(...args)),
    preparePaymentWindow: (...args) => run("purchase", () => source.preparePaymentWindow(...args)),
    cancelPayment: (...args) => run("purchase_settlement", () => source.cancelPayment(...args)),
    createSupportCase: (...args) => run("support", () => source.createSupportCase(...args)),
    readBetaResult: (...args) => run("result_read", () => source.readBetaResult(...args)),
    deleteBetaSession: (...args) => run("account_deletion", () => source.deleteBetaSession(...args)),
  };
}
