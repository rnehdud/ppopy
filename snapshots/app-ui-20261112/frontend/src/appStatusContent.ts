export type AppStatusKind = "decision_abstained" | "product_confirmation_required" | "technical_error";

const content: Record<AppStatusKind, { title: string; defaultDetail: string; nextAction: string; technical: boolean }> = {
  decision_abstained: {
    title: "지금 정보만으로는 사용 방식을 정하기 어려워요",
    defaultDetail: "답하지 않은 항목이나 제품 정보를 확인할 수 있어요. 현재 상태로 종료해도 됩니다.",
    nextAction: "답하지 않은 항목 확인",
    technical: false,
  },
  product_confirmation_required: {
    title: "정확한 제품 확인이 필요해요",
    defaultDetail: "브랜드·제품명·용량이나 옵션을 다시 확인해 주세요. 후보를 자동으로 확정하지 않습니다.",
    nextAction: "제품 다시 확인",
    technical: false,
  },
  technical_error: {
    title: "처리를 완료하지 못했어요",
    defaultDetail: "입력은 유지됩니다. 연결을 확인한 뒤 다시 시도해 주세요.",
    nextAction: "다시 시도",
    technical: true,
  },
};

export function appStatusContent(kind: AppStatusKind) {
  return content[kind];
}

export function appStatusKindForApiCode(code: string | undefined): AppStatusKind {
  if (code === "decision_abstained") return "decision_abstained";
  if (code === "product_confirmation_required") return "product_confirmation_required";
  return "technical_error";
}
