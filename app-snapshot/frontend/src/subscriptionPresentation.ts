export type SubscriptionDisplayState =
  | "FREE"
  | "TRIALING"
  | "ACTIVE"
  | "CANCEL_AT_PERIOD_END"
  | "GRACE_PERIOD"
  | "VERIFICATION_PENDING"
  | "ACCOUNT_HOLD"
  | "EXPIRED"
  | "REVOKED";

export type SubscriptionPresentation = {
  tone: "neutral" | "attention";
  title: string;
  detail: string;
  action: "none" | "manage_subscription" | "retry_status";
  access_claimed: false;
};

const verifiedCopy: Record<SubscriptionDisplayState, Omit<SubscriptionPresentation, "access_claimed">> = {
  FREE: { tone: "neutral", title: "무료로 이용 중이에요", detail: "기능을 시작할 때 이번 달 이용 한도를 서버에서 다시 확인해요.", action: "none" },
  TRIALING: { tone: "neutral", title: "무료 이용 기간이에요", detail: "정확한 종료일은 구독 관리 화면에서 확인해 주세요.", action: "manage_subscription" },
  ACTIVE: { tone: "neutral", title: "구독 이용 중이에요", detail: "갱신일과 결제 정보는 구독 관리 화면에서 확인할 수 있어요.", action: "manage_subscription" },
  CANCEL_AT_PERIOD_END: { tone: "neutral", title: "구독 해지가 예약됐어요", detail: "현재 이용 종료일은 구독 관리 화면에서 확인해 주세요.", action: "manage_subscription" },
  GRACE_PERIOD: { tone: "attention", title: "결제 상태를 확인하고 있어요", detail: "이용 가능 여부는 서버 확인 결과에 따릅니다.", action: "manage_subscription" },
  VERIFICATION_PENDING: { tone: "attention", title: "구매 확인이 아직 끝나지 않았어요", detail: "잠시 뒤 상태를 다시 확인해 주세요.", action: "retry_status" },
  ACCOUNT_HOLD: { tone: "attention", title: "결제 수단 확인이 필요해요", detail: "구독 관리 화면에서 결제 상태를 확인해 주세요.", action: "manage_subscription" },
  EXPIRED: { tone: "neutral", title: "구독 이용 기간이 끝났어요", detail: "과거 민감 기록의 보관 기간은 구독 상태와 별도로 적용됩니다.", action: "none" },
  REVOKED: { tone: "attention", title: "구독 이용이 종료됐어요", detail: "상태가 예상과 다르면 구독 내역을 확인해 주세요.", action: "manage_subscription" },
};

export function presentSubscriptionStatus(input: {
  server_verified: boolean;
  state?: SubscriptionDisplayState;
}): SubscriptionPresentation {
  if (!input.state || !(input.state in verifiedCopy)) {
    return {
      tone: "attention",
      title: "구독 상태를 확인할 수 없어요",
      detail: "네트워크 연결을 확인한 뒤 다시 시도해 주세요.",
      action: "retry_status",
      access_claimed: false,
    };
  }
  const verificationStateIsValid = input.state === "VERIFICATION_PENDING"
    ? !input.server_verified
    : input.server_verified;
  if (!verificationStateIsValid) return {
    tone: "attention",
    title: "구독 상태를 확인할 수 없어요",
    detail: "네트워크 연결을 확인한 뒤 다시 시도해 주세요.",
    action: "retry_status",
    access_claimed: false,
  };
  return { ...verifiedCopy[input.state], access_claimed: false };
}
