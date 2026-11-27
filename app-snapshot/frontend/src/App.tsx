import { FormEvent, useEffect, useRef, useState } from "react";

import CareResult from "./CareResult";
import {
  CareAnalysisEnvelope,
  CareAnalysisRequest,
  CareApiClient,
  careApiClient,
} from "./careApi";
import { ProductCandidate } from "./productCatalog";
import ProductPhotoInput from "./ProductPhotoInput";
import { PRODUCT_PHOTO_POC_ENABLED } from "./productPhoto";
import "./styles.css";

type MissingProductDraft = {
  brand: string;
  name: string;
};

type FlowStep = "products" | "scenario" | "result";
type ScenarioId = "conservative" | "simple";
export type DemoAudience = "internal" | "friend";

const SYNTHETIC_SCENARIOS: Array<{
  id: ScenarioId;
  title: string;
  summary: string;
  request: Pick<CareAnalysisRequest, "care_priorities" | "aggravating_answers" | "survey">;
}> = [
  {
    id: "conservative",
    title: "합성 시나리오 A · 자극 가능성 우선",
    summary: "잦은 세안·마찰 신호와 과거 불편 이력이 있는 테스트 입력입니다.",
    request: {
      care_priorities: ["texture_congestion_tendency", "redness_tendency"],
      aggravating_answers: {
        frequent_cleansing: true,
        post_cleanse_tightness: true,
        frequent_face_touching: true,
      },
      survey: {
        irritation_history: true,
        current_actives: ["acid"],
        retinoid_in_use: false,
        dermatology_treatment_status: "none",
        tightness_dryness_score: 3,
      },
    },
  },
  {
    id: "simple",
    title: "합성 시나리오 B · 단순 루틴",
    summary: "특별한 불편 이력 없이 번들거림 관리 방향만 선택한 테스트 입력입니다.",
    request: {
      care_priorities: ["surface_oil_tendency"],
      aggravating_answers: {},
      survey: {
        irritation_history: false,
        current_actives: [],
        retinoid_in_use: false,
        dermatology_treatment_status: "none",
        tightness_dryness_score: 0,
      },
    },
  },
];

const STEP_HEADINGS: Record<FlowStep, string> = {
  products: "지금 쓰는 제품부터 확인해요",
  scenario: "합성 시나리오를 선택해요",
  result: "합성 케어 결과 미리보기",
};

const FRIEND_STEP_HEADINGS: Record<FlowStep, string> = {
  products: "지금 쓰는 제품부터 확인해요",
  scenario: "비슷한 상황을 하나 골라보세요",
  result: "루틴 점검 결과 예시",
};

export default function App({
  client = careApiClient,
  audience = "internal",
}: {
  client?: CareApiClient;
  audience?: DemoAudience;
}) {
  const isFriendDemo = audience === "friend";
  const [step, setStep] = useState<FlowStep>("products");
  const [query, setQuery] = useState("");
  const [hasSearched, setHasSearched] = useState(false);
  const [isSearching, setIsSearching] = useState(false);
  const [results, setResults] = useState<ProductCandidate[]>([]);
  const [selected, setSelected] = useState<ProductCandidate[]>([]);
  const [showMissingForm, setShowMissingForm] = useState(false);
  const [missingDrafts, setMissingDrafts] = useState<MissingProductDraft[]>([]);
  const [scenarioId, setScenarioId] = useState<ScenarioId>("conservative");
  const [careResult, setCareResult] = useState<CareAnalysisEnvelope | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [announcement, setAnnouncement] = useState("");
  const headingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    headingRef.current?.focus();
  }, [step]);

  const runSearch = async (event: FormEvent) => {
    event.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) {
      setAnnouncement("제품명을 한 글자 이상 입력해 주세요.");
      setHasSearched(false);
      return;
    }
    setIsSearching(true);
    setError("");
    try {
      const candidates = await client.searchProducts(trimmed);
      setResults(candidates);
      setHasSearched(true);
      setAnnouncement(candidates.length ? `후보 ${candidates.length}개를 찾았습니다.` : "일치하는 후보가 없습니다.");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "제품 검색에 실패했습니다.");
      setResults([]);
      setHasSearched(false);
    } finally {
      setIsSearching(false);
    }
  };

  const confirmProduct = (product: ProductCandidate) => {
    if (!selected.some((item) => item.id === product.id)) {
      setSelected((current) => [...current, product]);
      setAnnouncement(`${product.name}을 현재 제품 목록에 추가했습니다.`);
    }
  };

  const addMissingDraft = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const brand = String(form.get("brand") ?? "").trim();
    const name = String(form.get("name") ?? "").trim();
    if (!brand || !name) return;
    setMissingDrafts((current) => [...current, { brand, name }]);
    setShowMissingForm(false);
    setAnnouncement(`${brand} ${name}을 미등록 제품 검토 초안에 추가했습니다.`);
    event.currentTarget.reset();
  };

  const runAnalysis = async () => {
    const scenario = SYNTHETIC_SCENARIOS.find((item) => item.id === scenarioId)!;
    const productContextStatus = selected.length > 0
      ? (missingDrafts.length > 0 ? "partial" : "registered")
      : (missingDrafts.length > 0 ? "partial" : "unregistered");
    const request: CareAnalysisRequest = {
      schema_version: "0.1.0",
      deployment_context: "synthetic_test",
      product_context_status: productContextStatus,
      confirmed_current_product_ids: selected.map((item) => item.id),
      ...scenario.request,
    };
    setIsAnalyzing(true);
    setError("");
    try {
      const response = await client.analyze(request);
      setCareResult(response);
      setStep("result");
      setAnnouncement("합성 케어 결과를 만들었습니다.");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "합성 케어 결과를 만들지 못했습니다.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  const reset = () => {
    setStep("products");
    setQuery("");
    setHasSearched(false);
    setResults([]);
    setSelected([]);
    setMissingDrafts([]);
    setShowMissingForm(false);
    setScenarioId("conservative");
    setCareResult(null);
    setError("");
    setAnnouncement("새 합성 1회 흐름을 시작했습니다.");
  };

  return (
    <div className="app-shell">
      <header className="site-header">
        <a className="brand" href="#main">SkinAnalysis</a>
        <span className="prototype-badge">{isFriendDemo ? "친구 피드백용 · 합성 데모" : "합성 통합 시제품"}</span>
      </header>

      <main id="main" className="main-content">
        <p className="eyebrow">{isFriendDemo ? "화장품 루틴 점검 서비스" : "계정 없는 1회 케어 계약"}</p>
        <h1 ref={headingRef} tabIndex={-1}>{(isFriendDemo ? FRIEND_STEP_HEADINGS : STEP_HEADINGS)[step]}</h1>
        <p className="lead">
          {step === "products" && (isFriendDemo
            ? "사용 중인 제품을 확인하고, 악화 요인을 먼저 줄이는 성분 중심 루틴을 살펴보는 약 3분짜리 데모입니다."
            : "제품 후보를 확인한 뒤 합성 문진 시나리오로 코어 엔진 결과 구조를 점검합니다.")}
          {step === "scenario" && (isFriendDemo
            ? "실제 개인정보 대신 미리 만든 두 가지 상황 중 하나를 선택합니다."
            : "법률 검토 전에는 실제 피부·치료 정보를 묻지 않고 고정된 합성 입력만 사용합니다.")}
          {step === "result" && (isFriendDemo
            ? "현재 제품을 무조건 바꾸기보다, 먼저 줄일 행동과 필요한 성분·안전 제한을 함께 보여줍니다."
            : "악화 요인, 6성분 계획, 안전 제한, 현재 제품과 미충족 항목을 같은 계약으로 표시합니다.")}
        </p>

        <div className="privacy-note" role="note">
          <strong>{isFriendDemo ? "개인정보를 받지 않는 합성 데모입니다." : "개발·검증용 합성 시나리오입니다."}</strong>
          <span>{isFriendDemo
            ? "실제 피부 고민이나 치료 정보는 입력하지 마세요. 검색과 선택은 이 화면에서만 사용하며 서버로 보내거나 저장하지 않습니다."
            : "실제 피부 고민·치료 정보는 입력하지 마세요. 요청은 저장하지 않으며 실제 사용자 모드는 P0-H02·P3-A00 전까지 차단됩니다."}</span>
          {!isFriendDemo && <span>연결 모드: {client.mode === "http" ? "로컬 Python 코어" : "고정 계약 fixture"}</span>}
        </div>

        {isFriendDemo && step === "products" && (
          <section className="demo-brief" aria-labelledby="demo-brief-title">
            <div>
              <p className="step-label">이 데모에서 볼 것</p>
              <h2 id="demo-brief-title">제품 추천보다 먼저, 지금 루틴을 정리합니다</h2>
            </div>
            <ul>
              <li><strong>1</strong><span>현재 제품을 직접 확인해요</span></li>
              <li><strong>2</strong><span>악화에 영향을 줄 수 있는 행동부터 줄여요</span></li>
              <li><strong>3</strong><span>6성분 계획과 안전 제한을 함께 봐요</span></li>
            </ul>
          </section>
        )}

        <div className="progress" aria-label="진행 단계">
          <span className={step === "products" ? "active" : "complete"}>1. 제품 확인</span>
          <span className={step === "scenario" ? "active" : step === "result" ? "complete" : ""}>2. {isFriendDemo ? "상황 선택" : "합성 문진"}</span>
          <span className={step === "result" ? "active" : ""}>3. {isFriendDemo ? "결과 보기" : "결과 계약"}</span>
        </div>

        <p className="sr-only" aria-live="polite">{announcement}</p>
        {error && <p className="error-note" role="alert">{error}</p>}

        {step === "products" && (
          <section className="panel" aria-labelledby="search-title">
            <div className="section-heading">
              <p className="step-label">선택 단계</p>
              <h2 id="search-title">제품명 검색</h2>
              <p>브랜드나 용기에 적힌 제품명을 입력하세요. 후보가 하나여도 자동 확정하지 않습니다.</p>
            </div>

            {PRODUCT_PHOTO_POC_ENABLED && <ProductPhotoInput onAnnouncement={setAnnouncement} />}

            <form className="search-form" onSubmit={runSearch}>
              <label htmlFor="product-query">제품명</label>
              <div className="search-row">
                <input
                  id="product-query"
                  name="product-query"
                  value={query}
                  onChange={(event) => {
                    setQuery(event.target.value);
                    setHasSearched(false);
                  }}
                  placeholder="예: 데모 브랜드 크림"
                  autoComplete="off"
                />
                <button type="submit" disabled={isSearching}>{isSearching ? "검색 중" : "검색"}</button>
              </div>
            </form>

            {hasSearched && (
              <div className="results" aria-labelledby="result-title">
                <h3 id="result-title">검색 후보</h3>
                {results.length > 0 ? (
                  <ul className="candidate-list">
                    {results.map((product) => {
                      const isSelected = selected.some((item) => item.id === product.id);
                      return (
                        <li key={product.id}>
                          <div>
                            <span className="candidate-brand">{product.brand}</span>
                            <strong>{product.name}</strong>
                            <span>{product.option} · {product.evidenceStatus === "owner_verified" ? "운영자 확인" : product.evidenceStatus === "automation_verified" ? "공식 원문 자동 확인" : product.evidenceStatus === "review_required" ? "전성분 확인 필요" : "합성 데이터"}</span>
                          </div>
                          <button type="button" className="secondary-button" disabled={isSelected} onClick={() => confirmProduct(product)}>
                            {isSelected ? "추가됨" : "이 제품이 맞아요"}
                          </button>
                        </li>
                      );
                    })}
                  </ul>
                ) : (
                  <div className="empty-state">
                    <p>일치하는 제품이 없습니다.</p>
                    <button type="button" className="text-button" onClick={() => setShowMissingForm(true)}>미등록 제품 접수 초안 만들기</button>
                  </div>
                )}
              </div>
            )}

            {showMissingForm && (
              <form className="missing-form" onSubmit={addMissingDraft} aria-labelledby="missing-title">
                <h3 id="missing-title">미등록 제품 접수 초안</h3>
                <p>브라우저 메모리에만 두며 실제 검토 큐로 전송하지 않습니다.</p>
                <label htmlFor="missing-brand">브랜드</label>
                <input id="missing-brand" name="brand" required />
                <label htmlFor="missing-name">용기에 적힌 제품명</label>
                <input id="missing-name" name="name" required />
                <div className="inline-actions">
                  <button type="submit">초안에 추가</button>
                  <button type="button" className="ghost-button" onClick={() => setShowMissingForm(false)}>취소</button>
                </div>
              </form>
            )}

            {(selected.length > 0 || missingDrafts.length > 0) && (
              <section className="selection-summary" aria-labelledby="selection-title">
                <h3 id="selection-title">확인한 내용</h3>
                <ul>
                  {selected.map((product) => (
                    <li key={product.id}>
                      <span>{product.brand} {product.name}</span>
                      <button type="button" className="text-button" onClick={() => setSelected((current) => current.filter((item) => item.id !== product.id))} aria-label={`${product.name} 삭제`}>삭제</button>
                    </li>
                  ))}
                  {missingDrafts.map((draft, index) => (
                    <li key={`${draft.brand}-${draft.name}-${index}`}>
                      <span>{draft.brand} {draft.name} · 검토 대기 초안</span>
                      <button type="button" className="text-button" onClick={() => setMissingDrafts((current) => current.filter((_, itemIndex) => itemIndex !== index))} aria-label={`${draft.name} 초안 삭제`}>삭제</button>
                    </li>
                  ))}
                </ul>
              </section>
            )}

            <div className="bottom-actions">
              <button type="button" className="primary-button" onClick={() => setStep("scenario")}>{isFriendDemo ? "다음: 상황 선택" : "합성 시나리오로 계속"}</button>
              <p>{isFriendDemo ? "제품을 고르지 않아도 안전한 결과 예시를 볼 수 있습니다." : "제품을 건너뛰어도 무등록 범위의 안전한 결과 계약을 확인할 수 있습니다."}</p>
            </div>
          </section>
        )}

        {step === "scenario" && (
          <section className="panel" aria-labelledby="scenario-title">
            <div className="section-heading">
              <p className="step-label">{isFriendDemo ? "개인정보 없는 예시" : "실제 사용자 문항 비활성"}</p>
              <h2 id="scenario-title">{isFriendDemo ? "어떤 결과를 볼까요?" : "고정 합성 입력"}</h2>
              <p>{isFriendDemo ? "실제 답변을 받지 않고 미리 만든 상황으로 결과만 체험합니다." : "실제 답변을 받지 않고 미리 만든 두 시나리오로 화면과 코어 계약만 검증합니다."}</p>
            </div>
            <fieldset className="scenario-list">
              <legend className="sr-only">합성 시나리오 선택</legend>
              {SYNTHETIC_SCENARIOS.map((scenario) => (
                <label className={`scenario-card ${scenarioId === scenario.id ? "selected" : ""}`} key={scenario.id}>
                  <input type="radio" name="scenario" value={scenario.id} checked={scenarioId === scenario.id} onChange={() => setScenarioId(scenario.id)} />
                  <span>
                    <strong>{isFriendDemo
                      ? scenario.id === "conservative" ? "예시 A · 자극 가능성을 먼저 줄이는 경우" : "예시 B · 단순한 번들거림 관리"
                      : scenario.title}</strong>
                    <small>{isFriendDemo
                      ? scenario.id === "conservative" ? "잦은 세안과 마찰, 과거 불편을 우선 고려합니다." : "특별한 불편 없이 간단한 관리 방향을 살펴봅니다."
                      : scenario.summary}</small>
                  </span>
                </label>
              ))}
            </fieldset>
            <div className="bottom-actions inline-actions">
              <button type="button" className="ghost-button" onClick={() => setStep("products")}>제품 단계로 돌아가기</button>
              <button type="button" className="primary-button" disabled={isAnalyzing} onClick={runAnalysis}>{isAnalyzing ? "계산 중" : isFriendDemo ? "결과 예시 보기" : "합성 결과 보기"}</button>
            </div>
          </section>
        )}

        {step === "result" && careResult && (
          <section className="result-layout" aria-label="합성 케어 결과">
            <CareResult envelope={careResult} label={isFriendDemo ? "루틴 점검 예시" : undefined} />
            <aside className="panel summary-panel" aria-labelledby="care-summary-title">
              <h2 id="care-summary-title">{isFriendDemo ? "데모 안내" : "이번 계약 검증"}</h2>
              <dl>
                <div><dt>확인 제품</dt><dd>{selected.length}개</dd></div>
                <div><dt>{isFriendDemo ? "확인 필요 제품" : "미등록 초안"}</dt><dd>{missingDrafts.length}개</dd></div>
                <div><dt>저장</dt><dd>없음</dd></div>
                <div><dt>{isFriendDemo ? "사용한 정보" : "실제 사용자 입력"}</dt><dd>{isFriendDemo ? "합성 예시" : "차단"}</dd></div>
              </dl>
              <p className="limit-note">{isFriendDemo
                ? "이 결과는 합성 예시이며 진단·치료·피부 개선을 보장하지 않습니다."
                : "이 화면은 합성 계약 미리보기이며 실제 고객용 문진·동의·저장은 P0-H02 결론과 P3-A00 반영 뒤에만 엽니다."}</p>
              {isFriendDemo && (
                <section className="feedback-card" aria-labelledby="feedback-title">
                  <p className="step-label">친구에게 물어볼 것</p>
                  <h3 id="feedback-title">세 가지만 편하게 말해 주세요</h3>
                  <ol>
                    <li>가장 유용해 보인 결과는 무엇인가요?</li>
                    <li>이해하기 어렵거나 믿기 어려운 부분은 무엇인가요?</li>
                    <li>이 결과를 보면 실제 루틴을 바꿀 것 같나요?</li>
                  </ol>
                </section>
              )}
              <button type="button" className="primary-button" onClick={reset}>처음부터 다시</button>
            </aside>
          </section>
        )}
      </main>

      <footer><p>진단·치료 또는 자동 피부 개선 판정을 제공하지 않습니다.</p></footer>
    </div>
  );
}
