import { CareAnalysisEnvelope, CareItem, CareSection } from "./careApi";
import { isConsumerCareDelivery } from "./careDeliveryBoundary";

const SECTION_TITLES: Record<CareSection["type"], string> = {
  aggravating_factors: "먼저 줄여볼 악화 요인",
  ingredient_plan: "6성분 케어 계획",
  routine: "사용 순서",
  current_products: "현재 제품 평가",
  product_matches: "제품 후보",
  unmet_gaps: "아직 충족되지 않은 항목",
  disclaimers: "확인해야 할 한계",
};

const STATUS_LABELS: Record<string, string> = {
  selected: "선택",
  support: "안전 지지",
  excluded: "제외",
  not_prioritized: "이번 우선순위 아님",
  keep: "유지 가능",
  adjust: "조정 필요",
  review_required: "확인 필요",
};

function text(item: Record<string, unknown>, key: string): string {
  return typeof item[key] === "string" ? item[key] : "";
}

function texts(item: Record<string, unknown>, key: string): string[] {
  return Array.isArray(item[key]) ? item[key].filter((value): value is string => typeof value === "string") : [];
}

function ResultItem({ sectionType, item }: { sectionType: CareSection["type"]; item: CareItem }) {
  if (typeof item === "string") return <li>{item}</li>;

  if (sectionType === "aggravating_factors") {
    return <li><strong>{text(item, "factor")}</strong><p>{text(item, "guidance")}</p></li>;
  }
  if (sectionType === "ingredient_plan") {
    const status = text(item, "status");
    return (
      <li>
        <div className="result-item-heading">
          <strong>{text(item, "ingredient")}</strong>
          <span className={`status-chip status-${status}`}>{STATUS_LABELS[status] || status} · {text(item, "dose")}</span>
        </div>
        <p>{text(item, "reason")}</p>
      </li>
    );
  }
  if (sectionType === "routine") {
    return (
      <li>
        <div className="result-item-heading">
          <strong>{text(item, "slot")} {String(item.order ?? "")} · {text(item, "ingredient")}</strong>
          <span className="status-chip">{text(item, "dose")}</span>
        </div>
        <p>{text(item, "frequency")}{item.gradual_introduction === true ? " · 단계적으로 도입" : ""}</p>
      </li>
    );
  }
  if (sectionType === "current_products") {
    const status = text(item, "decision");
    // New semantic/research/shadow vocabularies are not v0.2 wire decisions.
    // Unknown decisions must not surface a raw action or its inferred guidance.
    if (!["keep", "adjust", "review_required"].includes(status)) {
      return <li><strong>{text(item, "brand")} {text(item, "name")}</strong>
        <span className="status-chip status-review_required">확인 필요</span>
        <p>제품 평가를 확인할 수 없어 사용 변경 안내를 보류합니다.</p></li>;
    }
    const covered = texts(item, "covered_ingredients");
    const notes = texts(item, "notes");
    return (
      <li>
        <div className="result-item-heading">
          <strong>{text(item, "brand")} {text(item, "name")}</strong>
          <span className={`status-chip status-${status}`}>{STATUS_LABELS[status] || status}</span>
        </div>
        {covered.length > 0 && <p>충족 방향: {covered.join(", ")}</p>}
        {notes.map((note) => <p key={note}>{note}</p>)}
      </li>
    );
  }
  if (sectionType === "product_matches") {
    return (
      <li>
        <strong>{text(item, "brand")} {text(item, "name")}</strong>
        <p>충족 방향: {texts(item, "covered_ingredients").join(", ") || "확인 필요"}</p>
      </li>
    );
  }
  if (sectionType === "unmet_gaps") {
    return <li><strong>{text(item, "ingredient")}</strong><p>{text(item, "message")}</p></li>;
  }
  return <li>{JSON.stringify(item)}</li>;
}

function Outcome({ value }: { value?: Record<string, unknown> }) {
  if (!value) return null;
  const guidance = texts(value, "guidance");
  return (
    <div className="result-outcome" role="note">
      <strong>{text(value, "headline")}</strong>
      <p>{text(value, "reason")}</p>
      {guidance.length > 0 && <ul>{guidance.map((item) => <li key={item}>{item}</li>)}</ul>}
    </div>
  );
}

export default function CareResult({
  envelope,
  label = "합성 엔진 결과",
}: {
  envelope: CareAnalysisEnvelope;
  label?: string;
}) {
  // Direct/injected clients also pass through the display boundary. Withhold all
  // dependent routine instructions if the complete palette cannot be verified.
  if (!isConsumerCareDelivery(envelope.result)) {
    return <p role="alert">점검 결과를 확인할 수 없어 안내를 보류합니다. 다시 점검해 주세요.</p>;
  }
  return (
    <div className="result-stack">
      <section className="panel safety-summary" aria-labelledby="safety-title">
        <p className="step-label">안전 우선 요약</p>
        <h2 id="safety-title">도입 강도: {envelope.result.safety.tolerance_level}</h2>
        {[...envelope.result.safety.warnings, ...envelope.result.safety.excluded_combinations].length > 0 && (
          <ul>
            {[...envelope.result.safety.warnings, ...envelope.result.safety.excluded_combinations].map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        )}
      </section>

      {envelope.result.sections.map((section) => (
        <section className={`panel result-section result-${section.type}`} key={section.type}>
          <div className="section-heading">
            <p className="step-label">{label}</p>
            <h2>{SECTION_TITLES[section.type]}</h2>
          </div>
          <Outcome value={section.outcome} />
          {section.items.length > 0 ? (
            <ul className="result-list">
              {section.items.map((item, index) => (
                <ResultItem sectionType={section.type} item={item} key={`${section.type}-${index}`} />
              ))}
            </ul>
          ) : (
            <p className="empty-result">표시할 항목이 없습니다. 안전 조건을 낮춰 후보를 채우지 않습니다.</p>
          )}
        </section>
      ))}
    </div>
  );
}
