import { FormEvent, useEffect, useRef, useState } from "react";

import CareResult from "./CareResult";
import ProductPhotoInput from "./ProductPhotoInput";
import { PRODUCT_PHOTO_POC_ENABLED } from "./productPhoto";
import RoutineFollowup from "./RoutineFollowup";
import { emptyContext, missingOptions, requiresAbstention } from "./routineObservation";
import type { IntakeDraft, MissingObservation, ObservationContext, RoutineObservation } from "./careApi";
import {
  BetaNoticeBundle,
  BetaSessionHandle,
  CareAnalysisEnvelope,
  CareAnalysisRequest,
  CareApiClient,
  PaymentOrder,
  PaymentWindowRequest,
  SupportCategory,
  careApiClient,
} from "./careApi";
import { ProductCandidate } from "./productCatalog";
import "./styles.css";

type BetaStep = "consent" | "survey" | "payment" | "result" | "search_only" | "deleted";

const PAYMENT_RESUME_STORAGE_KEY = "skinanalysis.test.payment-resume.v1";
const INTAKE_SESSION_KEY = "skinanalysis.test.intake-session.v1";

function readIntakeSession(): BetaSessionHandle | null {
  try {
    const value = JSON.parse(window.sessionStorage.getItem(INTAKE_SESSION_KEY) || "null") as BetaSessionHandle | null;
    return value && typeof value.session_token === "string" && typeof value.participant_id === "string" && Number.isFinite(Date.parse(value.expires_at)) && Date.parse(value.expires_at) > Date.now() ? value : null;
  } catch { return null; }
}

type PaymentResume = {
  session: BetaSessionHandle;
  order: PaymentOrder;
};

function readPaymentResume(): PaymentResume | null {
  try {
    const raw = window.sessionStorage.getItem(PAYMENT_RESUME_STORAGE_KEY);
    if (!raw) return null;
    const value = JSON.parse(raw) as Partial<PaymentResume>;
    if (
      typeof value.session?.session_token !== "string"
      || typeof value.session?.participant_id !== "string"
      || Date.parse(String(value.session?.expires_at || "")) <= Date.now()
      || typeof value.order?.orderId !== "string"
      || value.order?.amount !== 9900
    ) {
      window.sessionStorage.removeItem(PAYMENT_RESUME_STORAGE_KEY);
      return null;
    }
    return value as PaymentResume;
  } catch {
    window.sessionStorage.removeItem(PAYMENT_RESUME_STORAGE_KEY);
    return null;
  }
}

function persistPaymentResume(session: BetaSessionHandle, order: PaymentOrder): void {
  try {
    window.sessionStorage.setItem(PAYMENT_RESUME_STORAGE_KEY, JSON.stringify({ session, order }));
  } catch {
    throw new Error("결제 후 돌아올 탭 상태를 안전하게 저장하지 못했습니다.");
  }
}

function clearPaymentResume(): void {
  window.sessionStorage.removeItem(PAYMENT_RESUME_STORAGE_KEY);
}

declare global {
  interface Window {
    AUTHNICE?: {
      requestPay(request: PaymentWindowRequest & {
        fnError(result: { errorMsg?: string }): void;
      }): void;
    };
  }
}

function loadNicepaySdk(): Promise<void> {
  if (window.AUTHNICE) return Promise.resolve();
  return new Promise((resolve, reject) => {
    const existing = document.querySelector<HTMLScriptElement>('script[data-nicepay-sdk="v1"]');
    if (existing) {
      existing.addEventListener("load", () => resolve(), { once: true });
      existing.addEventListener("error", () => reject(new Error("NICEPAY 결제창을 불러오지 못했습니다.")), { once: true });
      return;
    }
    const script = document.createElement("script");
    script.src = "https://pay.nicepay.co.kr/v1/js/";
    script.async = true;
    script.dataset.nicepaySdk = "v1";
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("NICEPAY 결제창을 불러오지 못했습니다."));
    document.head.appendChild(script);
  });
}

function NoticeItem({ notice }: { notice: { title: string; summary: string } }) {
  return (
    <details className="notice-item">
      <summary>{notice.title} 자세히 보기</summary>
      <p>{notice.summary}</p>
    </details>
  );
}

export default function BetaApp({ client = careApiClient }: { client?: CareApiClient }) {
  const [resume] = useState<PaymentResume | null>(() => readPaymentResume());
  const [intakeSession] = useState(readIntakeSession);
  const [step, setStep] = useState<BetaStep>(() => resume ? "payment" : intakeSession ? "survey" : "consent");
  const [bundle, setBundle] = useState<BetaNoticeBundle | null>(null);
  const [session, setSession] = useState<BetaSessionHandle | null>(() => resume?.session || intakeSession || null);
  const [care, setCare] = useState<CareAnalysisEnvelope | null>(null);
  const [order, setOrder] = useState<PaymentOrder | null>(() => resume?.order || null);
  const [selected, setSelected] = useState<ProductCandidate[]>([]);
  const [query, setQuery] = useState("");
  const [searchResults, setSearchResults] = useState<ProductCandidate[]>([]);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [contactEnabled, setContactEnabled] = useState(false);
  const [supportStatus, setSupportStatus] = useState("");
  const [intakePhase, setIntakePhase] = useState<"products" | "routine" | "personalization">("products");
  const [frequencies, setFrequencies] = useState<Record<string, string>>({});
  const [discomfort, setDiscomfort] = useState<RoutineObservation["discomfort"]>("not_asked");
  const [timing, setTiming] = useState<IntakeDraft["timing"]>("not_asked");
  const [ongoing, setOngoing] = useState<IntakeDraft["ongoing"]>("not_asked");
  const [context, setContext] = useState<ObservationContext>(emptyContext);
  const [searchAttempted, setSearchAttempted] = useState(false);
  const [resolutionStatus, setResolutionStatus] = useState("");
  const [draftLoaded, setDraftLoaded] = useState(!intakeSession);
  const [draftStatus, setDraftStatus] = useState("");
  const draftSaves = useRef(Promise.resolve());
  useEffect(() => {
    if (!intakeSession || !client.readIntakeDraft) { setDraftLoaded(true); return; }
    let cancelled = false;
    client.readIntakeDraft(intakeSession.session_token).then(({draft}) => {
      if (cancelled) return;
      if (draft) {
        setIntakePhase(draft.phase); setSelected(draft.selected); setFrequencies(draft.frequencies);
        setDiscomfort(draft.discomfort); setTiming(draft.timing); setOngoing(draft.ongoing);
        setContext(draft.context || emptyContext());
        setDraftStatus("암호화된 제품·루틴 입력을 복원했습니다. 나머지 개인화 질문은 다시 확인해 주세요.");
      }
      setDraftLoaded(true);
    }).catch(() => { if (!cancelled) setDraftStatus("임시 입력을 불러오지 못했습니다. 새로고침으로 다시 시도해 주세요. 저장된 입력은 덮어쓰지 않았습니다."); });
    return () => { cancelled = true; };
  }, [client, intakeSession]);
  useEffect(() => {
    if (!session || !draftLoaded || step !== "survey" || !client.saveIntakeDraft) return;
    const timer = window.setTimeout(() => {
      // Serialize writes so a slow earlier request cannot overwrite a later
      // edit in this tab. Never put these sensitive answers in browser storage.
      draftSaves.current = draftSaves.current.then(() => client.saveIntakeDraft!(session.session_token, {phase:intakePhase,selected,frequencies,discomfort,timing,ongoing,context})).then(() => undefined)
        .catch(() => setDraftStatus("임시저장에 실패했습니다. 현재 입력은 화면에 유지됩니다."));
    }, 600);
    return () => window.clearTimeout(timer);
  }, [client,session,draftLoaded,step,intakePhase,selected,frequencies,discomfort,timing,ongoing,context]);
  const record = (event: string, questionId?: string) => {
    if (session && client.recordPilotEvent) void client.recordPilotEvent(session.session_token, event, questionId).catch(() => {
      // Analytics failure never prevents payment, deletion or input recovery.
    });
  };
  const completeRoutine = () => {
    if (selected.some(product => !frequencies[product.id])) {
      setError("제품마다 최근 7일 사용 일수 또는 모름·응답하지 않음을 선택해 주세요.");
      return;
    }
    setError("");
    setIntakePhase("routine");
    record("routine_completed");
  };
  const requestResolution = async () => {
    if (!session || !client.requestProductResolution) {
      setResolutionStatus("보호 세션에서 제품 확인을 요청할 수 있습니다. 지금은 다른 제품명으로 검색해 주세요.");
      return;
    }
    setBusy(true);
    try {
      const response = await client.requestProductResolution(session.session_token, query.trim());
      setResolutionStatus(`제품 확인 요청이 접수됐습니다 (${response.state}). 검증 전에는 자동 등록하거나 추천하지 않습니다.`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "요청을 접수하지 못했습니다. 입력은 유지됩니다.");
    } finally { setBusy(false); }
  };
  const checkResolution = async () => {
    if (!session || !client.readProductResolutions) return;
    setBusy(true);
    try {
      const status = await client.readProductResolutions(session.session_token);
      setResolutionStatus(status.requests.some(r => r.state === "PASS")
        ? "확인 가능한 제품이 있습니다. 제품명을 다시 검색한 뒤 용량·옵션을 직접 확인해 주세요."
        : "아직 확인 중입니다. 요청은 보관되어 있으며 다른 제품 입력을 계속할 수 있습니다.");
    } catch { setResolutionStatus("확인 상태를 읽지 못했습니다. 입력과 기존 요청은 유지됩니다."); }
    finally { setBusy(false); }
  };

  useEffect(() => {
    void client.getBetaNotices()
      .then(setBundle)
      .catch((caught) => setError(caught instanceof Error ? caught.message : "동의 문서를 불러오지 못했습니다."));
  }, [client]);

  useEffect(() => {
    const returnState = new URLSearchParams(window.location.search).get("nicepayReturn");
    if (!returnState) return;
    setSupportStatus(returnState === "paid"
      ? "결제 승인이 완료되었습니다. 결과 확인을 눌러 주세요."
      : "결제 승인 상태를 확인 중입니다. 잠시 뒤 결과 확인을 눌러 주세요.");
    const url = new URL(window.location.href);
    url.searchParams.delete("nicepayReturn");
    window.history.replaceState({}, "", `${url.pathname}${url.search}${url.hash}`);
  }, []);

  const startSession = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!bundle) return;
    const form = new FormData(event.currentTarget);
    const required = ["age", "terms", "general", "sensitive"];
    if (required.some((name) => form.get(name) !== "yes")) {
      setError("만 14세 이상 확인과 세 가지 필수 항목을 각각 확인해 주세요.");
      return;
    }
    const contactType = String(form.get("contact-type") || "email") as "email" | "sms" | "kakao";
    const contactValue = String(form.get("contact-value") || "").trim();
    if (contactEnabled && !contactValue) {
      setError("선택한 초기 사용자 연락처를 입력해 주세요.");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const handle = await client.startBetaSession({
        schema_version: bundle.schema_version,
        age_gate: "over_or_equal_14",
        accepted_notices: {
          service_terms: bundle.notices.service_terms.version,
          general_personal_information: bundle.notices.general_personal_information.version,
          sensitive_information: bundle.notices.sensitive_information.version,
        },
        contact: contactEnabled ? {
          type: contactType,
          value: contactValue,
          notice_version: bundle.notices.beta_contact.version,
        } : null,
      });
      setSession(handle);
      void client.recordPilotEvent?.(handle.session_token, "session_started").catch(() => undefined);
      try { window.sessionStorage.setItem(INTAKE_SESSION_KEY, JSON.stringify(handle)); } catch { setDraftStatus("이 탭에서 복귀용 세션을 저장할 수 없어 새로고침 복구가 제한됩니다."); }
      setStep("survey");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "보호 세션을 시작하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const search = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const trimmed = query.trim();
    if (!trimmed) return;
    setBusy(true);
    setError("");
    try {
      const results = await client.searchProducts(trimmed);
      setSearchResults(results);
      setSearchAttempted(true);
      record(results.length ? "product_candidate_shown" : "product_db_miss");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "제품 검색에 실패했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const routineObservation: RoutineObservation = {
    version: "1.0.0-owner-review",
    products: selected.map(item => ({product_id: item.id, days_per_week:
      /^[0-7]$/.test(frequencies[item.id] || "") ? Number(frequencies[item.id]) : (frequencies[item.id] || "not_asked") as MissingObservation})),
    discomfort, details: discomfort === "yes" ? {timing, ongoing} : null, context,
  };
  const answerFollowup = (question: string, value: string) => {
    if (question === "timing") setTiming(value as IntakeDraft["timing"]);
    else if (question === "ongoing") setOngoing(value as IntakeDraft["ongoing"]);
    setContext(previous => ({...previous,
      ...(question !== "timing" && question !== "ongoing" ? {[question]: value} : {}),
      answered: [...new Set([...previous.answered, question])]}));
  };

  const submitCare = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!session) return;
    if (requiresAbstention(routineObservation)) {
      setError("확인 정보가 부족해 개인화 판단을 보류합니다.");
      setIntakePhase("routine");
      return;
    }
    const form = new FormData(event.currentTarget);
    const currentActives: Array<"retinoid" | "acid"> = [];
    if (form.get("acid") === "yes") currentActives.push("acid");
    if (form.get("retinoid") === "yes") currentActives.push("retinoid");
    const request: CareAnalysisRequest = {
      schema_version: "0.1.0",
      deployment_context: "real_user",
      product_context_status: selected.length ? "registered" : "unregistered",
      confirmed_current_product_ids: selected.map((item) => item.id),
      routine_observation: routineObservation,
      care_priorities: [String(form.get("priority"))],
      aggravating_answers: {
        frequent_cleansing: form.get("frequent-cleansing") === "yes",
        post_cleanse_tightness: form.get("post-cleanse-tightness") === "yes",
        frequent_face_touching: form.get("face-touching") === "yes",
      },
      survey: {
        irritation_history: form.get("irritation-history") === "yes",
        current_actives: currentActives,
        retinoid_in_use: form.get("retinoid") === "yes",
        dermatology_treatment_status: String(form.get("treatment")) as "none" | "in_use" | "unknown",
        tightness_dryness_score: Number(form.get("tightness")),
      },
    };
    setBusy(true);
    setError("");
    try {
      record("questionnaire_completed");
      const submission = await client.submitBetaCare(session.session_token, request);
      if (!submission.ready_for_payment) {
        setError("등록·확인된 제품이 있어야 결제와 개인화 결과 제공을 진행할 수 있습니다.");
        return;
      }
      setStep("payment");
      record("decision_generated");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "개인화 결과를 만들지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const startPayment = async () => {
    if (!session) return;
    setBusy(true);
    setError("");
    try {
      const created = order || await client.createPaymentOrder(session.session_token);
      setOrder(created);
      const paymentWindow = await client.preparePaymentWindow(session.session_token, created.orderId);
      await loadNicepaySdk();
      if (!window.AUTHNICE) throw new Error("NICEPAY 결제창 초기화에 실패했습니다.");
      persistPaymentResume(session, created);
      record("payment_started");
      window.AUTHNICE.requestPay({
        ...paymentWindow,
        fnError: (result) => {
          const message = String(result?.errorMsg || "").trim();
          setError(message || "NICEPAY 결제창을 열지 못했습니다.");
        },
      });
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "결제를 시작하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const loadPaidResult = async () => {
    if (!session) return;
    setBusy(true);
    setError("");
    try {
      const result = await client.readBetaResult(session.session_token);
      setCare({
        api_schema_version: "0.1.0",
        deployment_context: "real_user",
        persistence: "protected_beta_session",
        result,
      });
      setStep("result");
      record("payment_completed");
      record("result_viewed");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "결제 상태 또는 결과를 확인하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const cancelPaidOrder = async () => {
    if (!session || !order) return;
    setBusy(true);
    setError("");
    try {
      record("refund_requested");
      const response = await client.cancelPayment(session.session_token, order.orderId, "구매 철회");
      clearPaymentResume();
      setOrder(null);
      setSupportStatus(`결제 취소 상태: ${response.state}`);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "결제 취소 상태를 확인하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const submitSupport = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!session) return;
    const form = new FormData(event.currentTarget);
    setBusy(true);
    setError("");
    setSupportStatus("");
    try {
      const response = await client.createSupportCase(
        session.session_token,
        String(form.get("support-category")) as SupportCategory,
        String(form.get("support-body") || ""),
      );
      setSupportStatus(`문의가 접수되었습니다 (${response.status}).`);
      event.currentTarget.reset();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "인앱 문의를 접수하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  const withdraw = async () => {
    if (!session) return;
    setBusy(true);
    setError("");
    try {
      record("withdrawal_requested");
      await client.deleteBetaSession(session.session_token);
      clearPaymentResume();
      window.sessionStorage.removeItem(INTAKE_SESSION_KEY);
      setSession(null);
      setCare(null);
      setSelected([]); setFrequencies({}); setDiscomfort("skipped"); setTiming("unknown"); setOngoing("unknown");
      setOrder(null);
      setStep("deleted");
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "동의 철회·삭제를 처리하지 못했습니다.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="app-shell beta-shell">
      <header className="site-header">
        <a className="brand" href="#main">SkinAnalysis</a>
        <span className="prototype-badge">공식 소프트런칭 스테이징</span>
      </header>
      <main id="main" className="main-content">
        <p className="eyebrow">맞춤형화장품조제관리사 기반 성분 루틴 점검</p>
        <h1>필요한 정보만 받고, 목적이 끝나면 지웁니다</h1>
        <p className="lead">개인화에 필요한 민감정보는 일반 개인정보와 분리해 동의를 받고, 연락처·문진·결과를 서로 다른 접근 경계에 보관합니다.</p>
        {error && <p className="error-note" role="alert">{error}</p>}

        {step === "consent" && (
          <section className="panel" aria-labelledby="consent-title">
            <div className="section-heading">
              <p className="step-label">1. 참여·동의 확인</p>
              <h2 id="consent-title">각 항목을 따로 확인해 주세요</h2>
            </div>
            {!bundle ? <p>동의 문서를 불러오는 중입니다.</p> : (
              <form className="consent-form" onSubmit={startSession}>
                {!bundle.beta_activated && <p className="limit-note">현재 서버는 외부 계약·영구 저장·결제·배포 검증 전 비활성 상태입니다. 스테이징에서만 명시적으로 켤 수 있습니다.</p>}
                <label className="check-row"><input type="checkbox" name="age" value="yes" /> 만 14세 이상입니다</label>
                <NoticeItem notice={bundle.notices.service_terms} />
                <label className="check-row"><input type="checkbox" name="terms" value="yes" /> 서비스 이용약관에 동의합니다 (필수)</label>
                <NoticeItem notice={bundle.notices.general_personal_information} />
                <label className="check-row"><input type="checkbox" name="general" value="yes" /> 일반 개인정보 수집·이용에 동의합니다 (필수)</label>
                <NoticeItem notice={bundle.notices.sensitive_information} />
                <label className="check-row"><input type="checkbox" name="sensitive" value="yes" /> 민감정보 수집·이용에 별도로 동의합니다 (개인화 필수)</label>
                <NoticeItem notice={bundle.notices.beta_contact} />
                <label className="check-row"><input type="checkbox" checked={contactEnabled} onChange={(event) => setContactEnabled(event.target.checked)} /> 초기 사용자 안내 연락처를 별도로 제공합니다 (선택)</label>
                {contactEnabled && (
                  <div className="contact-fields">
                    <label>연락 방법<select name="contact-type" defaultValue="email"><option value="email">이메일</option><option value="sms">문자</option><option value="kakao">카카오톡</option></select></label>
                    <label>연락처<input name="contact-value" autoComplete="off" /></label>
                  </div>
                )}
                <p className="limit-note">{bundle.processor_and_transfer}</p>
                <div className="bottom-actions inline-actions">
                  <button type="button" className="ghost-button" onClick={() => setStep("search_only")}>민감정보 없이 제품 검색만 보기</button>
                  <button type="submit" className="primary-button" disabled={busy || !bundle.beta_activated}>{busy ? "확인 중" : "동의하고 개인화 시작"}</button>
                </div>
              </form>
            )}
          </section>
        )}

        {step === "payment" && (
          <section className="panel" aria-labelledby="payment-title">
            <div className="section-heading">
              <p className="step-label">3. TEST 결제</p>
              <h2 id="payment-title">개인화 1회권 · 9,900원</h2>
              <p>가격과 상품은 서버가 확정하며, NICEPAY Server 승인 성공 뒤에만 결과가 열립니다.</p>
            </div>
            <div className="bottom-actions inline-actions">
              <button type="button" className="primary-button" onClick={startPayment} disabled={busy}>{busy ? "준비 중" : "NICEPAY 결제창 열기"}</button>
              <button type="button" className="secondary-button" onClick={loadPaidResult} disabled={busy}>결제 완료 후 결과 확인</button>
              {order && <button type="button" className="danger-button" onClick={cancelPaidOrder} disabled={busy}>결제 취소 요청</button>}
            </div>
            <p className="limit-note">카드정보는 NICEPAY 결제창에서 처리하며, 문진·개인화 결과는 NICEPAY로 보내지 않습니다. 현재 TEST 검증 경로이며 실제 공개는 꺼져 있습니다.</p>
          </section>
        )}

        {(step === "survey" || step === "search_only") && (
          <section className="panel" aria-labelledby="intake-title">
            <div className="section-heading">
              <p className="step-label">{step === "survey" ? "2. 제품·문진" : "일반 정보 경로"}</p>
              <h2 id="intake-title">사용 중인 제품을 찾아보세요</h2>
              <p>후보가 하나여도 자동으로 확정하지 않습니다.</p>
            </div>
            {draftStatus && <p role="status">{draftStatus}</p>}
            {step === "survey" && <button type="button" className="ghost-button" disabled={busy} onClick={checkResolution}>신규 제품 확인 요청 상태</button>}
            {PRODUCT_PHOTO_POC_ENABLED && <ProductPhotoInput onAnnouncement={setSupportStatus} />}
            {(intakePhase === "products" || step === "search_only") && <>
            <form className="search-form" onSubmit={search}>
              <label htmlFor="beta-product-query">제품명</label>
              <div className="search-row"><input id="beta-product-query" value={query} onChange={(event) => setQuery(event.target.value)} /><button disabled={busy}>검색</button></div>
            </form>
            {searchResults.length > 0 && (
              <ul className="candidate-list beta-candidates">
                {searchResults.map((product) => <li key={product.id}><div><span>{product.brand}</span><strong>{product.name}</strong><small>{product.option}</small></div><button type="button" className="secondary-button" disabled={selected.some(item => item.id === product.id) || selected.length >= 30} onClick={() => { setSelected((items) => items.some((item) => item.id === product.id) ? items : [...items, product]); record("product_confirmed"); }}>{selected.some((item) => item.id === product.id) ? "추가됨" : "이 제품이 맞아요"}</button></li>)}
              </ul>
            )}
            {searchAttempted && searchResults.length === 0 && <div className="limit-note" role="status"><p>일치하는 제품이 없습니다. 제품명·용량·옵션을 확인하거나 신규 제품 확인을 요청해 주세요.</p><button type="button" onClick={requestResolution} disabled={busy || !query.trim()}>신규 제품 확인 요청</button><p>{resolutionStatus}</p></div>}
            </>}
            {step === "survey" && <>
              <h3>등록한 제품 · {selected.length}개</h3>
              {selected.map(product => <div className="registered-product" key={product.id}>
                <strong>{product.name}</strong>
                <label>최근 7일 사용 일수
                  <select aria-label={`${product.name} 사용 일수`} value={frequencies[product.id] || ""} disabled={intakePhase !== "products"} onChange={event => { setFrequencies({...frequencies, [product.id]: event.target.value}); record("frequency_entered", "frequency"); }}>
                    <option value="" disabled>선택해 주세요</option>{Array.from({length: 8}, (_, n) => <option key={n} value={String(n)}>{n}일</option>)}{frequencies[product.id] === "refused" && <option value="refused">응답하지 않음</option>}{missingOptions.filter(([value]) => value !== "not_asked" && !(frequencies[product.id] === "refused" && value === "user_refused")).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
                  </select>
                </label>
                {intakePhase === "products" && <details><summary>최근 사용 변화 기록 (선택)</summary>
                  <p>현재 사용 일수와 별개입니다. 최근 2주에 달라진 점을 알고 있다면 기록할 수 있습니다.</p>
                  <label>{product.name} 이전 주 사용 일수<select value={context.recent_products[product.id]?.previous_days_per_week ?? "not_asked"} onChange={e => setContext(previous => ({...previous, recent_products: {...previous.recent_products, [product.id]: {newly_started: previous.recent_products[product.id]?.newly_started ?? "not_asked", previous_days_per_week: /^[0-7]$/.test(e.target.value) ? Number(e.target.value) : e.target.value as MissingObservation}}}))}>
                    {missingOptions.map(([value,label]) => <option key={value} value={value}>{label}</option>)}{Array.from({length:8},(_,n)=><option key={n} value={n}>{n}일</option>)}
                  </select></label>
                  <label>{product.name} 최근 2주 신규 사용<select value={context.recent_products[product.id]?.newly_started ?? "not_asked"} onChange={e => setContext(previous => ({...previous, recent_products: {...previous.recent_products, [product.id]: {previous_days_per_week: previous.recent_products[product.id]?.previous_days_per_week ?? "not_asked", newly_started: e.target.value as "yes" | "no" | MissingObservation}}}))}>
                    {missingOptions.map(([value,label]) => <option key={value} value={value}>{label}</option>)}<option value="yes">예</option><option value="no">아니요</option>
                  </select></label>
                </details>}
                {intakePhase === "products" && <button type="button" className="ghost-button" onClick={() => { setSelected(items => items.filter(item => item.id !== product.id)); setContext(previous => { const recent_products = {...previous.recent_products}; delete recent_products[product.id]; return {...previous, recent_products}; }); setFrequencies(values => { const next = {...values}; delete next[product.id]; return next; }); }}>제품 제거</button>}
              </div>)}
              {intakePhase === "products" && <button type="button" className="primary-button" onClick={completeRoutine}>전체 루틴 입력 완료</button>}
              {intakePhase !== "products" && <button type="button" className="ghost-button" onClick={() => setIntakePhase("products")}>제품·사용 일수 수정</button>}
              {intakePhase === "routine" && <section className="survey-form" aria-label="루틴 사용 경험">
                <h3>전체 루틴을 사용한 뒤의 경험</h3>
                <label>최근 사용 뒤 평소와 다른 불편감이 있었나요? (선택)
                  <select value={discomfort} onChange={event => { setDiscomfort(event.target.value as RoutineObservation["discomfort"]); record("discomfort_answered", "discomfort"); }}>
                    <option value="not_asked">아직 답하지 않음</option><option value="skipped">건너뛰기</option><option value="no">없음</option><option value="yes">있음</option>{discomfort === "refused" && <option value="refused">응답하지 않음</option>}{missingOptions.filter(([value]) => value !== "not_asked" && !(discomfort === "refused" && value === "user_refused")).map(([value,label]) => <option key={value} value={value}>{label}</option>)}
                  </select>
                </label>
                {discomfort === "yes" && <RoutineFollowup observation={routineObservation} onAnswer={answerFollowup} />}
                {requiresAbstention(routineObservation) ? <p role="status">확인 정보가 부족해 개인화 판단을 보류합니다. 답한 질문은 반복하지 않으며, 제품 검색·문의·삭제는 계속 이용할 수 있습니다.</p>
                : <button type="button" className="primary-button" onClick={() => setIntakePhase("personalization")}>나머지 질문으로</button>}
              </section>}
            </>}
            {step === "search_only" ? <p className="limit-note">민감정보 동의 없이 제품 검색·일반 성분정보만 이용 중입니다. 개인화 케어 문진과 결과 저장은 열리지 않습니다.</p> : (
              intakePhase === "personalization" &&
              <form className="survey-form" onSubmit={submitCare}>
                <fieldset><legend>가장 먼저 점검할 방향</legend><label className="check-row"><input type="radio" name="priority" value="surface_oil_tendency" defaultChecked /> 번들거림 경향</label><label className="check-row"><input type="radio" name="priority" value="texture_congestion_tendency" /> 피부결·막힘 경향</label><label className="check-row"><input type="radio" name="priority" value="redness_tendency" /> 붉어짐 경향</label></fieldset>
                <fieldset><legend>안전 확인</legend><label className="check-row"><input type="checkbox" name="irritation-history" value="yes" /> 화장품 사용 중 자극 경험이 있습니다</label><label className="check-row"><input type="checkbox" name="acid" value="yes" /> 현재 산 성분 제품을 사용합니다</label><label className="check-row"><input type="checkbox" name="retinoid" value="yes" /> 현재 레티노이드 제품을 사용합니다</label></fieldset>
                <label>피부과 치료 여부<select name="treatment" defaultValue="unknown"><option value="none">없음</option><option value="in_use">치료 중</option><option value="unknown">모름</option></select></label>
                <label>세안 뒤 건조·당김 정도<select name="tightness" defaultValue="0"><option value="0">없음</option><option value="1">가끔</option><option value="2">보통</option><option value="3">자주</option><option value="4">매우 자주</option></select></label>
                <fieldset><legend>영향을 줄 수 있는 습관</legend><label className="check-row"><input type="checkbox" name="frequent-cleansing" value="yes" /> 세안을 자주 합니다</label><label className="check-row"><input type="checkbox" name="post-cleanse-tightness" value="yes" /> 세안 뒤 당김이 있습니다</label><label className="check-row"><input type="checkbox" name="face-touching" value="yes" /> 얼굴을 자주 만집니다</label></fieldset>
                <button type="submit" className="primary-button" disabled={busy}>{busy ? "계산 중" : "보호 경로로 결과 만들기"}</button>
              </form>
            )}
          </section>
        )}

        {step === "result" && care && (
          <section className="result-layout" aria-label="개인화 케어 결과">
            <CareResult envelope={care} />
            <aside className="panel summary-panel"><h2>보호 상태</h2><p>연락처·일반 제품 정보·민감 문진과 결과가 분리되어 있습니다. 결제 복귀용 세션은 브라우저를 닫으면 사라지는 현재 탭에만 임시 보관합니다.</p><button type="button" className="danger-button" onClick={withdraw} disabled={busy}>{busy ? "삭제 중" : "동의 철회하고 내 데이터 삭제"}</button></aside>
          </section>
        )}

        {session && step !== "deleted" && (
          <section className="panel" aria-labelledby="support-title">
            <div className="section-heading"><p className="step-label">보호 인앱 CS</p><h2 id="support-title">문의 접수</h2></div>
            <form className="survey-form" onSubmit={submitSupport}>
              <label>문의 유형<select name="support-category" defaultValue="service_error"><option value="payment_issue">결제 문제</option><option value="cancellation_withdrawal">취소·철회</option><option value="service_error">서비스 오류</option><option value="privacy_request">개인정보 요청</option><option value="other">기타</option></select></label>
              <label>문의 내용<textarea name="support-body" required maxLength={1300} /></label>
              <button type="submit" className="secondary-button" disabled={busy}>문의 접수</button>
            </form>
            {supportStatus && <p role="status">{supportStatus}</p>}
            {step !== "result" && (
              <button type="button" className="danger-button" onClick={withdraw} disabled={busy}>
                {busy ? "삭제 중" : "동의 철회하고 내 데이터 삭제"}
              </button>
            )}
          </section>
        )}

        {step === "deleted" && <section className="panel" role="status"><h2>동의 철회와 세션 삭제가 완료됐습니다</h2><p>서비스·연락처·민감정보 저장 영역의 연결 레코드를 삭제했습니다. 법정 거래기록은 서비스 데이터와 분리해 해당 법정 기간만 보관합니다.</p></section>}
      </main>
      <footer><p>의료행위나 자동 피부 개선 판정을 제공하지 않습니다.</p></footer>
    </div>
  );
}
