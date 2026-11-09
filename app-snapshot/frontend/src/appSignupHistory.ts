import type {AppHistoryConsentStore} from "./appHistoryConsent";
import type {AppLoginNotices} from "./appLoginNotices";

export function signupHistoryBinding(history: {notice:{version:string};signup_storage_basis?:unknown}, notices: AppLoginNotices|null): {key:"sensitive_information"|"history_storage";version:string}|null {
  const basis=history.signup_storage_basis;
  if(basis===undefined)return notices?.history_storage ? {key:"history_storage",version:notices.history_storage.version} : null;
  if(!basis || typeof basis!=="object" || Array.isArray(basis))throw new Error("이력 저장 안내 연결을 확인해 주세요.");
  const fields=basis as Record<string,unknown>;
  if(Object.keys(fields).sort().join(",")!=="accepted_notice_key,notice_version"
      || fields.accepted_notice_key!=="sensitive_information" || notices?.history_storage
      || typeof fields.notice_version!=="string" || !fields.notice_version
      || fields.notice_version!==history.notice.version
      || fields.notice_version!==notices?.sensitive_information.version)throw new Error("이력 저장 안내 연결을 확인해 주세요.");
  return {key:"sensitive_information",version:fields.notice_version};
}

/** Fresh, explicitly accepted signup only. Session restoration never invokes this. */
export async function completeSignupHistoryConsent(options: {
  acceptedVersion: string | null;
  requiredVersion: string;
  store: AppHistoryConsentStore;
}): Promise<void> {
  if (!options.requiredVersion || options.acceptedVersion !== options.requiredVersion) {
    throw new Error("가입 시 이력 저장 동의를 확인해 주세요.");
  }
  const current = await options.store.read();
  if (current.notice_version !== options.requiredVersion || current.state === "review_required") {
    throw new Error("새 이력 저장 안내를 확인해 주세요.");
  }
  if (current.state === "consented") return;
  // One request only: a lost ACK is recovered by a later read, never a retry here.
  const receipt = await options.store.choose("grant", current);
  if (receipt.state !== "consented" || receipt.notice_version !== options.requiredVersion) {
    throw new Error("이력 저장 동의 결과를 확인하지 못했어요.");
  }
}
