import {resetAppScroll} from "./appScroll";
import ProductFrequencySelect from "./ProductFrequencySelect";
import { productPresentation } from "./productPresentation";
import { FormEvent, type ReactNode, useCallback, useLayoutEffect, useEffect, useMemo, useRef, useState } from "react";

import type { CareAnalysisEnvelope, CareAnalysisRequest, CareApiClient, IntakeDraft, RoutineObservation } from "./careApi";
import { CareApiError, careApiClient } from "./careApi";
import type { ProductCandidate, WebProductCandidate } from "./productCatalog";
import AppStatusNotice from "./AppStatusNotice";
import AppConnectivityNotice from "./AppConnectivityNotice";
import CareResult from "./CareResult";
import TestProductPhotoInput from "./TestProductPhotoInput";
import RoutineFollowup from "./RoutineFollowup";
import { appStatusKindForApiCode, type AppStatusKind } from "./appStatusContent";
import { PRODUCT_PHOTO_POC_ENABLED } from "./productPhoto";
import { recognizeProductText } from "./iosProductTextRecognizer";
import webClientRules from "../../skin_engine/config/product_web_client.json";
import {nativeIOSWebSearchAvailable, searchNativeIOSWebProducts, searchNativeIOSIngredientDrafts} from "./iosProductWebSearch";
import type {ProductIngredientDraft} from "./productIngredientDraft";
import {useIngredientLookup, ingredientLookupMessage} from "./useIngredientLookup";
import { nativeIOSCatalogAvailable, searchNativeIOSCatalog } from "./iosCatalogSearch";
import { searchPhotoIdentity } from "./photoIdentitySearch";
import type {ProductPhotoIdentity} from "./testProductPhotoTransport";
import { answerRoutineFollowup, emptyContext, followupQuestions, requiresAbstention } from "./routineObservation";
import "./appPrototype.css";

type Step = "welcome" | "products" | "frequency" | "q04" | "followup" | "prepared" | "personalization" | "result";

const stepNumber: Record<Step, number> = { welcome: 0, products: 1, frequency: 2, q04: 3, followup: 4, prepared: 4, personalization: 4, result: 4 };
const q04Options: Array<[RoutineObservation["discomfort"], string, string]> = [
  ["yes", "불편감이 있었어요", "관련 후속 질문을 이어서 확인해요."],
  ["no", "불편감이 없었어요", "명시적으로 답한 경우에만 이렇게 기록해요."],
  ["unknown", "잘 모르겠어요", "불편감 없음으로 바꾸지 않아요."],
  ["user_does_not_remember", "기억나지 않아요", "회상 실패 상태를 그대로 보존해요."],
  ["user_refused", "답하지 않을게요", "거절 상태를 보존하고 반복해서 묻지 않아요."],
];

function observationFromDraft(draft: IntakeDraft): RoutineObservation | null {
  if (draft.discomfort !== "yes") return null;
  return {
    version: "1.0.0-owner-review",
    products: draft.selected.map(item => ({
      product_id: item.id,
      days_per_week: /^[0-7]$/.test(draft.frequencies[item.id] || "") ? Number(draft.frequencies[item.id]) : draft.frequencies[item.id] as RoutineObservation["products"][number]["days_per_week"],
    })),
    discomfort: "yes",
    details: {timing: draft.timing, ongoing: draft.ongoing},
    context: draft.context ?? emptyContext(),
  };
}

function stepFromDraft(draft: IntakeDraft | null | undefined): Step {
  if (!draft) return "welcome";
  if (draft.phase === "products") return "products";
  if (draft.phase === "personalization") return "prepared";
  return draft.discomfort === "yes" ? "followup" : "q04";
}

function Scaffold({ step, title, description, children, action, onBack, backLabel = "이전", onOpenSettings }: {
  step: Step;
  title: string;
  description: string;
  children?: ReactNode;
  action: ReactNode;
  onBack?: () => void;
  backLabel?: string;
  onOpenSettings?: () => void;
}) {
  const current = stepNumber[step];
  const headingRef = useRef<HTMLHeadingElement>(null);
  useLayoutEffect(() => { resetAppScroll(); headingRef.current?.focus({preventScroll: true}); }, [step]);
  return <div className="app-prototype">
    <header className="app-topbar">
      {onBack
        ? <button className="app-back-button" type="button" onClick={onBack} aria-label={backLabel === "이전" ? "이전 단계로" : backLabel}><span aria-hidden="true">‹</span> {backLabel}</button>
        : <strong>뽀피</strong>}
      <div className="app-topbar-actions"><span>LOCAL PREVIEW</span>{onOpenSettings && <button type="button" onClick={onOpenSettings}>설정</button>}</div>
    </header>
    <main className="app-screen" id="app-main">
      {current > 0 && <div className="app-progress" role="progressbar" aria-label="루틴 점검 진행 단계" aria-valuemin={1} aria-valuemax={4} aria-valuenow={current} aria-valuetext={`4단계 중 ${current}단계`}>
        <span>{current} / 4</span><div><i style={{width: `${current * 25}%`}} /></div>
      </div>}
      <p className="app-eyebrow">내 루틴 점검</p>
      <h1 ref={headingRef} tabIndex={-1}>{title}</h1>
      <p className="app-description">{description}</p>
      <AppConnectivityNotice />
      <section className="app-content">{children}</section>
    </main>
    <footer className="app-actionbar">{action}</footer>
  </div>;
}

export default function AppPrototype({ client = careApiClient, initialDraft = null, ingredientSearch, onOpenSettings, active = true, onProductsChange, onFrequenciesChange, onRegistrationComplete, onComplete, onExit, exitLabel }: {
  client?: Pick<CareApiClient, "searchProducts"> & Partial<Pick<CareApiClient, "analyze" | "searchWebProducts">>;
  initialDraft?: IntakeDraft | null;
  ingredientSearch?: (query: string) => Promise<ProductIngredientDraft[]>;
  onOpenSettings?: () => void;
  active?: boolean;
  onProductsChange?: (products: ProductCandidate[]) => void;
  onFrequenciesChange?: (frequencies: Record<string, string>) => void;
  onRegistrationComplete?: () => void;
  onComplete?: () => void;
  onExit?: () => void;
  exitLabel?: string;
}) {
  const [step, setStep] = useState<Step>(() => stepFromDraft(initialDraft));
  const [query, setQuery] = useState("");
  const [storedResults, setResults] = useState<ProductCandidate[]>([]);
  const [storedWebResults, setWebResults] = useState<WebProductCandidate[]>([]);
  const [selected, setSelected] = useState<ProductCandidate[]>(() => initialDraft?.selected ?? []);
  const [frequencies, setFrequencies] = useState<Record<string, string>>(() => initialDraft?.frequencies ?? {});
  useEffect(() => { onProductsChange?.(selected); }, [selected, onProductsChange]);
  useEffect(() => { onFrequenciesChange?.(frequencies); }, [frequencies, onFrequenciesChange]);
  const [q04, setQ04] = useState<RoutineObservation["discomfort"]>(() => initialDraft?.discomfort ?? "not_asked");
  const [followup, setFollowup] = useState<RoutineObservation | null>(() => initialDraft ? observationFromDraft(initialDraft) : null);
  const [storedBusy, setBusy] = useState(false);
  const [storedError, setError] = useState("");
  const [storedSearchAttempted, setSearchAttempted] = useState(false);
  const [storedWebSearchStatus, setWebSearchStatus] = useState<"idle" | "searching" | "done" | "unavailable">("idle");
  const [showManualProduct, setShowManualProduct] = useState(false);
  const [storedManualStatus, setManualStatus] = useState("");
  const [storedPhotoAnnouncement, setPhotoAnnouncement] = useState("");
  const [storedPhotoIdentity, setPhotoIdentity] = useState<ProductPhotoIdentity | null>(null);
  const [careResult, setCareResult] = useState<CareAnalysisEnvelope | null>(null);
  const [storedOutcomeStatus, setOutcomeStatus] = useState<AppStatusKind | null>(null);
  const searchGeneration = useRef(0);
  const manualSequence = useRef(0);
  const nativePreview = client === careApiClient && nativeIOSCatalogAvailable();
  const nativeCatalog = nativePreview || (client.searchProducts === searchNativeIOSCatalog && nativeIOSCatalogAvailable());
  const webSearch = nativePreview && nativeIOSWebSearchAvailable() ? searchNativeIOSWebProducts : client.searchWebProducts;
  const lookupIngredients = ingredientSearch ?? (nativePreview && nativeIOSWebSearchAvailable() ? searchNativeIOSIngredientDrafts : undefined);
  // A provider change retires fetched data. Page changes retire work, while the
  // same provider's completed candidates and the user's registered draft remain.
  const serviceScope = useMemo(() => ({client, nativeCatalog, webSearch, lookupIngredients, active}), [client, nativeCatalog, webSearch, lookupIngredients, active]);
  const [careResultScope, setCareResultScope] = useState<typeof serviceScope | null>(null);
  const scopedIngredientSearch = useMemo(() => serviceScope.lookupIngredients
    ? (query: string) => serviceScope.lookupIngredients!(query) : undefined, [serviceScope]);
  const ingredientLookup = useIngredientLookup(active && step === "products" ? scopedIngredientSearch : undefined);
  const pageLifetime = useMemo(() => ({serviceScope, step, live: false}), [serviceScope, step]);
  const currentPage = useRef(pageLifetime);
  const [displayScope, setDisplayScope] = useState(serviceScope);
  const [activityPage, setActivityPage] = useState(pageLifetime);
  useLayoutEffect(() => {
    currentPage.current = pageLifetime;
    pageLifetime.live = true;
    setBusy(false);
    setWebSearchStatus(current => current === "searching" ? "idle" : current);
    return () => { pageLifetime.live = false; searchGeneration.current += 1; };
  }, [pageLifetime]);
  useLayoutEffect(() => {
    setResults([]); setWebResults([]); setSearchAttempted(false);
    setWebSearchStatus("idle"); setError(""); setWebError("");
    setBusy(false); setOutcomeStatus(null); setManualStatus("");
    setPhotoAnnouncement(""); setPhotoIdentity(null);
    setDisplayScope(serviceScope);
  }, [serviceScope]);
  const pageIsCurrent = () => active && pageLifetime.live && currentPage.current === pageLifetime;
  const requestIsCurrent = (generation: number) => pageIsCurrent() && generation === searchGeneration.current;
  const displaysCurrentScope = displayScope === serviceScope;
  const results = displaysCurrentScope ? storedResults : [];
  const webResults = displaysCurrentScope ? storedWebResults : [];
  const busy = displaysCurrentScope && activityPage === pageLifetime && storedBusy;
  const error = displaysCurrentScope ? storedError : "";
  const searchAttempted = displaysCurrentScope && storedSearchAttempted;
  const webSearchStatus = displaysCurrentScope ? storedWebSearchStatus : "idle";
  const manualStatus = displaysCurrentScope ? storedManualStatus : "";
  const photoAnnouncement = displaysCurrentScope ? storedPhotoAnnouncement : "";
  const photoIdentity = displaysCurrentScope ? storedPhotoIdentity : null;
  const outcomeStatus = displaysCurrentScope ? storedOutcomeStatus : null;
  const [storedWebError,setWebError] = useState("");
  const webError = displaysCurrentScope ? storedWebError : "";
  const frequencyComplete = useMemo(() => selected.length > 0 && selected.every(item => frequencies[item.id]), [frequencies, selected]);
  const routineObservation = useMemo<RoutineObservation>(() => followup ?? {
    version: "1.0.0-owner-review",
    products: selected.map(item => ({
      product_id: item.id,
      days_per_week: /^[0-7]$/.test(frequencies[item.id] || "")
        ? Number(frequencies[item.id])
        : frequencies[item.id] as RoutineObservation["products"][number]["days_per_week"],
    })),
    discomfort: q04,
    details: null,
    context: emptyContext(),
  }, [followup, frequencies, q04, selected]);

  const goBack = useCallback(() => {
    searchGeneration.current += 1;
    setBusy(false);
    setError("");
    setOutcomeStatus(null);
    if (step === "products" && onExit) { onExit(); return; }
    const previous: Step = step === "products" ? "welcome"
      : step === "frequency" ? "products"
      : step === "q04" ? "frequency"
      : step === "followup" ? "q04"
      : step === "prepared" ? (q04 === "yes" && followup ? "followup" : "q04")
      : step === "personalization" ? "prepared"
      : step === "result" ? "personalization"
      : "welcome";
    setStep(previous);
  }, [followup, q04, step, onExit]);

  useEffect(() => {
    const handleNativeBack = () => { if (active) goBack(); };
    window.addEventListener("skinanalysis:native-back", handleNativeBack);
    return () => window.removeEventListener("skinanalysis:native-back", handleNativeBack);
  }, [goBack, active]);

  const toggleProduct = (product: ProductCandidate) => {
    if (!pageIsCurrent() || step !== "products") return;
    const registered = selected.some(value => value.id === product.id);
    setSelected(current => registered ? current.filter(value => value.id !== product.id) : [...current, product]);
    if (registered) ingredientLookup.remove(product.id);
    if (registered) setFrequencies(current => {
      const next = {...current};
      delete next[product.id];
      return next;
    });
  };

  const continueAfterQ04 = () => {
    if (q04 === "not_asked") setQ04("skipped");
    if (q04 !== "yes") { setStep("prepared"); return; }
    setFollowup(current => current ?? {
      version: "1.0.0-owner-review",
      products: selected.map(item => ({
        product_id: item.id,
        days_per_week: /^[0-7]$/.test(frequencies[item.id] || "") ? Number(frequencies[item.id]) : frequencies[item.id] as RoutineObservation["products"][number]["days_per_week"],
      })),
      discomfort: "yes",
      details: {timing: "not_asked", ongoing: "not_asked"},
      context: emptyContext(),
    });
    setStep("followup");
  };

  const runProductSearch = async (rawQuery: string) => {
    const searchText = rawQuery.normalize("NFKC").trim().replace(/\s+/g, " ");
    if (!searchText || !pageIsCurrent() || step !== "products") return;
    const generation = ++searchGeneration.current;
    setActivityPage(pageLifetime);
    setBusy(true); setError(""); setWebError("");
    setResults([]); setWebResults([]); setSearchAttempted(false); setWebSearchStatus("idle");
    try {
      const candidates = nativeCatalog
        ? await searchNativeIOSCatalog(searchText)
        : await client.searchProducts(searchText);
      if (requestIsCurrent(generation)) {
        setResults(candidates);
        setSearchAttempted(true);
        setWebResults([]);
        if (!candidates.length) {
          if (!webSearch) {
            setWebSearchStatus("unavailable");
          } else {
            setWebSearchStatus("searching");
            try {
              const found = await webSearch(searchText);
              if (requestIsCurrent(generation)) {
                setWebResults(found.slice(0, 5));
                setWebSearchStatus("done");
              }
            } catch(error) {
              if (requestIsCurrent(generation)) {setWebSearchStatus("unavailable");setWebError(nativeCatalog && error instanceof Error ? error.message : "인터넷 제품 검색을 완료하지 못했어요. 잠시 후 다시 시도해 주세요.");}
            }
          }
        } else setWebSearchStatus("idle");
      }
    }
    catch { if (requestIsCurrent(generation)) { setError("제품 검색에 실패했습니다. 입력은 유지됩니다."); setSearchAttempted(false); } }
    finally { if (requestIsCurrent(generation)) setBusy(false); }
  };

  const search = (event: FormEvent) => {
    event.preventDefault();
    void runProductSearch(query);
  };

  const searchFromPhoto = async (lines: string[]): Promise<number> => {
    if (!pageIsCurrent() || step !== "products") throw new DOMException("Search superseded", "AbortError");
    setActivityPage(pageLifetime);
    const generation = ++searchGeneration.current;
    setBusy(true);
    setError("");
    setWebResults([]);
    setWebSearchStatus("idle");
    try {
      const candidates = await searchPhotoIdentity(
        lines,
        nativeCatalog ? searchNativeIOSCatalog : client.searchProducts,
        () => requestIsCurrent(generation),
      );
      if (!requestIsCurrent(generation)) throw new DOMException("Search superseded", "AbortError");
      setResults(candidates);
      setSearchAttempted(true);
      return candidates.length;
    } catch {
      if (!requestIsCurrent(generation)) throw new DOMException("Search superseded", "AbortError");
      if (requestIsCurrent(generation)) {
        setResults([]);
        setSearchAttempted(false);
        setError("사진 후보 검색에 실패했습니다. 제품명을 직접 검색해 주세요.");
      }
      throw new Error("사진 후보 검색에 실패했습니다. 연결을 확인한 뒤 다시 검색해 주세요.");
    } finally {
      if (requestIsCurrent(generation)) setBusy(false);
    }
  };

  const addWebProduct = (candidate: WebProductCandidate) => {
    if (!pageIsCurrent() || step !== "products") return;
    const product: ProductCandidate = {
      id: `web-${candidate.candidateId}`,
      brand: candidate.sourceDomain,
      name: candidate.title,
      option: "용량·옵션 확인 필요",
      evidenceStatus: "review_required",
      matchSource: "public_web",
      sourceUrl: candidate.sourceUrl,
      provenanceHash: candidate.provenanceHash,
    };
    if (selected.some(item => item.id === product.id)) return;
    setSelected(current => [...current, product]);
    ingredientLookup.enqueue(product);
    setManualStatus(lookupIngredients ? "제품을 추가했어요. 전성분도 자동으로 확인할게요." : "제품을 추가했어요. 전성분 검증 전에는 확인이 필요해요.");
  };

  const addManualProduct = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!pageIsCurrent() || step !== "products") return;
    const form = new FormData(event.currentTarget);
    const brand = String(form.get("manual-brand") ?? "").trim();
    const name = String(form.get("manual-name") ?? "").trim();
    const option = String(form.get("manual-option") ?? "").trim() || "용량·옵션 미확인";
    if (!brand || !name) return;
    const normalized = (value: string) => value.normalize("NFKC").toLocaleLowerCase("ko-KR").replace(/\s+/g, "");
    const duplicate = selected.some(item => normalized(`${item.brand}|${item.name}|${item.option}`) === normalized(`${brand}|${name}|${option}`));
    if (duplicate) {
      setManualStatus("이미 등록한 제품입니다.");
      return;
    }
    const product: ProductCandidate = {
      id: `manual-${Date.now()}-${manualSequence.current++}`,
      brand,
      name,
      option,
      evidenceStatus: "review_required",
      matchSource: "manual",
    };
    setSelected(current => [...current, product]);
    setResults([]);
    setSearchAttempted(false);
    ingredientLookup.enqueue(product);
    setManualStatus(lookupIngredients ? "제품을 추가했어요. 전성분도 자동으로 확인할게요." : "제품을 추가했어요. 전성분 확인이 필요해요.");
    setShowManualProduct(false);
    event.currentTarget.reset();
  };

  const submitPersonalization = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!pageIsCurrent() || step !== "personalization" || busy) return;
    const generation = ++searchGeneration.current;
    setActivityPage(pageLifetime);
    if (selected.some(item => item.evidenceStatus === "review_required")) {
      setOutcomeStatus("product_confirmation_required");
      setError("인터넷 후보나 직접 입력 제품은 전성분을 확인한 뒤 결과에 반영할 수 있습니다. 현재 입력은 유지됩니다.");
      return;
    }
    const form = new FormData(event.currentTarget);
    const currentActives: Array<"retinoid" | "acid"> = [];
    if (form.get("acid") === "yes") currentActives.push("acid");
    if (form.get("retinoid") === "yes") currentActives.push("retinoid");
    const request: CareAnalysisRequest = {
      schema_version: "0.1.0",
      deployment_context: "synthetic_test",
      product_context_status: selected.some(item => item.evidenceStatus === "review_required") ? "partial" : "registered",
      confirmed_current_product_ids: selected.map(item => item.id),
      routine_observation: routineObservation,
      care_priorities: form.get("priority") === "none" ? [] : [String(form.get("priority"))],
      aggravating_answers: {
        frequent_cleansing: form.get("frequent-cleansing") === "yes",
        post_cleanse_tightness: form.get("post-cleanse-tightness") === "yes",
        frequent_face_touching: form.get("face-touching") === "yes",
      },
      survey: {
        irritation_history: form.get("irritation-history") === "yes" || q04 === "yes",
        current_actives: currentActives,
        retinoid_in_use: currentActives.includes("retinoid"),
        dermatology_treatment_status: String(form.get("treatment")) as CareAnalysisRequest["survey"]["dermatology_treatment_status"],
        tightness_dryness_score: Number(form.get("tightness")),
      },
    };
    setBusy(true);
    setError("");
    setOutcomeStatus(null);
    try {
      if (!client.analyze) throw new Error("루틴 점검 연결을 준비 중이에요.");
      const response = await client.analyze(request);
      if (!requestIsCurrent(generation)) return;
      setCareResultScope(serviceScope);
      setCareResult(response);
      setStep("result");
    } catch (caught) {
      if (!requestIsCurrent(generation)) return;
      setOutcomeStatus(appStatusKindForApiCode(caught instanceof CareApiError ? caught.code : undefined));
      setError(caught instanceof Error ? caught.message : "결과를 만들지 못했습니다.");
    } finally {
      if (requestIsCurrent(generation)) setBusy(false);
    }
  };

  if (step === "welcome") return <Scaffold step={step} onOpenSettings={onOpenSettings} title="내가 쓰는 제품부터 차근히 정리해요" description="제품과 사용 빈도를 먼저 확인한 뒤, 필요한 경험만 질문합니다. 진단이나 자동 피부 개선 판정은 하지 않아요." action={<button className="app-primary" type="button" onClick={() => setStep("products")}>내 루틴 정리 시작</button>}>
    <div className="app-hero-card"><strong>약 3분</strong><span>제품 등록 · 빈도 · 선택 경험 질문</span></div>
    <p className="app-safe-note">제품명 검색이나 제품 사진 촬영으로 시작하며 후보는 직접 확인합니다.</p>
  </Scaffold>;

  if (step === "products") return <Scaffold step={step} onBack={goBack} backLabel={onExit ? exitLabel : undefined} onOpenSettings={onOpenSettings} title="쓰는 제품을 찾아볼게요" description={lookupIngredients ? "제품명을 검색하거나 사진으로 찾아보세요. 새 제품을 확인하면 전성분도 함께 찾아드려요." : "제품명을 검색하거나 사진으로 찾아보세요. 제품명과 용량을 확인한 뒤 추가해 주세요."} action={<button className="app-primary" type="button" disabled={!active || !selected.length} onClick={() => setStep("frequency")}>제품 등록 완료</button>}>
    <section className="product-finder" aria-labelledby="product-finder-title">
      <div className="product-finder-heading"><h2 id="product-finder-title">제품 찾기</h2><span>{nativeCatalog ? (webSearch ? "DB + 인터넷" : "AWS TEST DB") : webSearch ? "DB + 인터넷" : "LOCAL TEST"}</span></div>
      <form id="app-product-search" className="app-search" onSubmit={search}>
        <label className="sr-only" htmlFor="app-product-query">제품명 검색</label>
        <div><input id="app-product-query" value={query} maxLength={200} onChange={event => { searchGeneration.current += 1; setQuery(event.target.value); setPhotoIdentity(null); setResults([]); setWebResults([]); setSearchAttempted(false); setWebSearchStatus("idle"); setError(""); setBusy(false); }} placeholder="브랜드와 제품명을 입력하세요" /><button className="app-secondary" disabled={!active || busy}>{busy ? "찾는 중" : "검색"}</button></div>
      </form>
      {PRODUCT_PHOTO_POC_ENABLED && <TestProductPhotoInput
        onAnnouncement={message => { if (pageIsCurrent()) setPhotoAnnouncement(message); }}
        extractText={recognizeProductText}
        onRecognizedLines={searchFromPhoto}
        onProductIdentity={async identity => {
          if (!pageIsCurrent()) throw new DOMException("Search superseded", "AbortError");
          if (!identity.brand || !identity.product_name) throw new Error("제품명을 읽지 못했습니다.");
          const productQuery = `${identity.brand} ${identity.product_name} ${identity.variant ?? ""} ${identity.volume ?? ""}`.normalize("NFKC").trim().replace(/\s+/g, " ");
          if (productQuery.length > 200) throw new Error("제품명을 확인한 뒤 직접 검색해 주세요.");
          setQuery(productQuery); setPhotoIdentity(identity);
          setResults([]); setWebResults([]); setSearchAttempted(false); setWebSearchStatus("idle"); setError("");
          setPhotoAnnouncement("사진에서 제품명을 읽었어요. DB와 인터넷에서 제품 후보를 자동으로 찾고 있어요.");
          void runProductSearch(productQuery);
        }}
        onCaptureStart={() => {
          if (!pageIsCurrent()) return () => false;
          const generation = ++searchGeneration.current;
          setPhotoIdentity(null);
          setBusy(false);
          return () => requestIsCurrent(generation);
        }}
      />}
      {photoAnnouncement && <p className="sr-only" aria-live="polite">{photoAnnouncement}</p>}
    </section>
    {photoIdentity && <section className="product-empty" aria-label="사진에서 읽은 제품명 후보">
      <small className="source-badge">사진에서 읽은 이름</small>
      <strong>{photoIdentity.brand} {photoIdentity.product_name}</strong>
      {(photoIdentity.variant || photoIdentity.volume) && <span>{[photoIdentity.variant, photoIdentity.volume].filter(Boolean).join(" · ")}</span>}
      <span>{busy && !searchAttempted ? "이 이름으로 DB를 확인하고 있어요. DB에 없으면 인터넷 후보까지 자동으로 찾아드려요." : "제품명 후보예요. 이름이 다르면 위 검색창에서 수정해 주세요."}</span>
    </section>}
    {webSearch && <p className="app-safe-note">{webClientRules.disclosure}</p>}
    {error && <AppStatusNotice kind="technical_error" detail={error} />}
    {!!results.length && <div className="result-heading"><strong>확인된 카탈로그</strong><span>{results.length}개</span></div>}
    <ul className="app-list" aria-label="DB 제품 검색 결과">{results.map(item => <li key={item.id}>
      <div><small className="source-badge verified">DB 확인</small><strong>{productPresentation(item).name}</strong>{productPresentation(item).subtitle && <span>{productPresentation(item).subtitle}</span>}{productPresentation(item).originalName && <details><summary>판매 상품명 보기</summary><span>{item.name}</span></details>}</div>
      <button className="app-text-action" type="button" onClick={() => toggleProduct(item)}>{selected.some(value => value.id === item.id) ? "등록 취소" : "이 제품 등록"}</button>
    </li>)}</ul>
    {webSearchStatus === "searching" && <div className="web-search-state" role="status"><span className="search-spinner" />인터넷에서도 제품을 찾고 있어요</div>}
    {webSearchStatus === "done" && <div className="result-heading"><strong>인터넷에서 찾은 후보</strong><span>{webResults.length}개</span></div>}
    {webSearchStatus === "done" && webResults.length === 0 && <div className="product-empty" role="status"><strong>일치하는 제품을 찾지 못했어요</strong><span>제품명과 브랜드를 다시 확인하거나 아래에서 직접 입력해 주세요.</span></div>}
    {webSearchStatus === "unavailable" && searchAttempted && <div className="product-empty" role="status"><strong>{webSearch ? (webError || "인터넷 제품 검색을 완료하지 못했어요") : "인터넷 제품 검색은 아직 연결 전이에요"}</strong><span>검색어를 임의의 후보로 만들지 않습니다. 입력을 확인하거나 직접 등록해 주세요.</span></div>}
    <ul className="web-result-list" aria-label="인터넷 제품 후보">{webResults.map(candidate => <li key={candidate.candidateId}>
      <div className="web-result-top"><span className="source-badge">인터넷 후보</span><small>{candidate.sourceDomain}</small></div>
      <strong>{candidate.title}</strong>
      <p>{candidate.snippet}</p>
      <a href={candidate.sourceUrl} target="_blank" rel="noopener noreferrer">제품 출처 보기</a>
      {(() => {
        const productId = `web-${candidate.candidateId}`;
        const added = selected.some(item => item.id === productId);
        const ingredientStatus = ingredientLookup.entries[productId]?.status;
        const label = !added ? "이 제품이 맞아요" : ingredientStatus === "queued" || ingredientStatus === "searching" ? "추가됨 · 전성분 확인 중" : ingredientStatus === "found" ? "추가됨 · 전성분 찾음" : "추가됨";
        return <button className="web-confirm-button" type="button" onClick={() => addWebProduct(candidate)} disabled={added}>{label}</button>;
      })()}
    </li>)}</ul>
    {searchAttempted && results.length === 0 && <button className="app-inline-action manual-toggle" type="button" aria-expanded={showManualProduct} onClick={() => { setShowManualProduct(value => !value); setManualStatus(""); }}>그래도 못 찾았나요? 직접 입력</button>}
    {showManualProduct && <form className="app-manual-product" onSubmit={addManualProduct}>
      <strong>제품 정보를 직접 입력해 주세요</strong>
      <p>확인 필요 상태로 루틴에 담고, 전성분은 나중에 검증합니다.</p>
      <label htmlFor="manual-brand">브랜드</label><input id="manual-brand" name="manual-brand" required maxLength={120} autoComplete="off" />
      <label htmlFor="manual-name">제품명</label><input id="manual-name" name="manual-name" required maxLength={180} autoComplete="off" />
      <label htmlFor="manual-option">용량·옵션 <span>선택</span></label><input id="manual-option" name="manual-option" maxLength={120} placeholder="예: 50 mL" autoComplete="off" />
      <button className="app-secondary" type="submit">직접 입력한 제품 담기</button>
    </form>}
    {manualStatus && <p className="app-manual-status" role="status">{manualStatus}</p>}
    {!!selected.length && <section className="app-selected-products" aria-labelledby="selected-products-title">
      <div className="app-summary"><span id="selected-products-title">등록한 제품</span><strong>{selected.length}개</strong></div>
      <ul>{selected.map(item => {
        const entry = ingredientLookup.entries[item.id];
        const pending = entry?.status === "queued" || entry?.status === "searching";
        return <li key={item.id} className="selected-product-card">
          <div className="selected-product-heading">
            <div><strong>{productPresentation(item).name}</strong>{productPresentation(item).subtitle && <span>{productPresentation(item).subtitle}</span>}</div>
            <button type="button" className="app-text-action selected-product-remove" aria-label={`${item.name} 삭제`} onClick={() => toggleProduct(item)}>삭제</button>
          </div>
          {productPresentation(item).originalName && <details><summary>판매 상품명 보기</summary><span>{item.name}</span></details>}
          {item.evidenceStatus === "review_required" && <div className="selected-product-ingredients">
            <small className="ingredient-verification-label">{pending ? "전성분 자동 확인 중" : entry?.status === "found" ? "전성분 찾음 · 확인 필요" : "전성분 확인 필요"}</small>
            {entry && <p className="ingredient-lookup-message" role="status" aria-live="polite">{pending && <i className="search-spinner" aria-hidden="true"/>}{ingredientLookupMessage(entry.status)}</p>}
            {lookupIngredients && !pending && entry?.status !== "found" && <button type="button" className="app-text-action ingredient-retry" onClick={() => ingredientLookup.enqueue(item)}>{entry ? "전성분 다시 확인" : "전성분 확인"}</button>}
            {entry?.drafts.map(draft => <details className="ingredient-draft" key={draft.provenance_hash}>
              <summary>전성분 목록 보기</summary>
              <div className="ingredient-draft-content">
                <strong>{draft.product_name}</strong>{draft.option && <span className="ingredient-draft-option">용량·옵션: {draft.option}</span>}
                <p className="ingredient-raw-text">{draft.raw_ingredients}</p>
                {draft.version_note && !/^(no version note available\.?|none|n\/a)$/i.test(draft.version_note.trim()) && <p>{draft.version_note}</p>}
                <a href={draft.source_url} target="_blank" rel="noopener noreferrer">전성분 출처 보기 ↗</a>
                <p className="ingredient-evidence-note">원문·용량·판매 지역을 확인한 뒤 추천에 반영할 수 있어요.</p>
              </div>
            </details>)}
          </div>}
        </li>;
      })}</ul>
    </section>}
  </Scaffold>;

  if (step === "frequency") return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="제품별 현재 사용 빈도를 알려 주세요" description="최근 7일을 기준으로 제품마다 한 번씩 확인합니다." action={<button className="app-primary" type="button" disabled={!frequencyComplete} onClick={() => {if (onRegistrationComplete) {setStep("q04"); onRegistrationComplete(); return;} setStep("q04");}}>{onRegistrationComplete ? "사용 빈도 저장" : "전체 루틴 완료"}</button>}>
    <button className="app-inline-action" type="button" onClick={() => setStep("products")}>제품 목록 수정</button>
    <ul className="app-question-list">{selected.map(item => <li key={item.id}>
      <label htmlFor={`frequency-${item.id}`}><strong>{productPresentation(item).name}</strong>{productPresentation(item).subtitle && <span>{productPresentation(item).subtitle}</span>}{productPresentation(item).originalName && <details><summary>판매 상품명 보기</summary><span>{item.name}</span></details>}</label>
      <ProductFrequencySelect aria-label={item.name} id={`frequency-${item.id}`} value={frequencies[item.id] || ""} onChange={event => setFrequencies(current => ({...current, [item.id]: event.target.value}))}/>
    </li>)}</ul>
  </Scaffold>;

  if (step === "q04") return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="사용하면서 불편감이 있었나요?" description="선택 질문입니다. 건너뛰거나 모르는 상태를 ‘없음’으로 기록하지 않습니다." action={<button className="app-primary" type="button" onClick={continueAfterQ04}>{q04 === "yes" ? "관련 질문으로 계속" : q04 === "not_asked" ? "건너뛰고 계속" : "이대로 계속"}</button>}>
    <button className="app-inline-action" type="button" onClick={() => setStep("frequency")}>빈도 수정</button>
    <fieldset className="app-choice-list"><legend className="sr-only">불편감 여부</legend>{q04Options.map(([value, label, help]) => <label key={value} className={q04 === value ? "selected" : ""}>
      <input aria-label={label} type="radio" name="q04" value={value} checked={q04 === value} onChange={() => setQ04(value)} />
      <span><strong>{label}</strong><small>{help}</small></span>
    </label>)}</fieldset>
  </Scaffold>;

  if (step === "followup" && followup) {
    const remaining = followupQuestions(followup);
    return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="불편감을 조금 더 확인할게요" description="시점과 지속 여부부터 승인된 순서로 한 항목씩 묻습니다. 모름·회상 실패·거절도 그대로 보존합니다." action={<button className="app-primary" type="button" disabled={remaining.length > 0} onClick={() => setStep("prepared")}>관련 질문 입력 완료</button>}>
      <button className="app-inline-action" type="button" onClick={() => setStep("q04")}>Q04 답변 수정</button>
      <RoutineFollowup observation={followup} onAnswer={(question, value) => setFollowup(current => current ? answerRoutineFollowup(current, question, value) : current)} />
    </Scaffold>;
  }

  if (step === "prepared") {
    const abstained = requiresAbstention(routineObservation);
    return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title={q04 === "yes" ? "관련 사용 경험까지 정리했어요" : "현재 루틴 입력을 정리했어요"} description={q04 === "yes" ? "답변은 불편감의 맥락으로만 보존합니다. 아직 제품이 원인이라고 판단하지 않습니다." : "현재 입력을 확인한 뒤 기존 개인화 질문으로 이어집니다. 자동으로 제품이나 행동을 확정하지 않습니다."} action={abstained
      ? <button className="app-primary" type="button" onClick={() => setStep(frequencyComplete ? "q04" : "frequency")}>입력 확인</button>
      : <button className="app-primary" type="button" onClick={event => { event.preventDefault(); setStep("personalization"); }}>개인화 질문으로 계속</button>}>
      <div className="app-result-card" role="status"><span>제품</span><strong>{selected.length}개</strong><span>Q04 상태</span><strong>{q04}</strong></div>
      {abstained && <AppStatusNotice kind="decision_abstained" />}
      <p className="app-safe-note">구독 상품·가격·trial·결제는 아직 연결되지 않았습니다.</p>
    </Scaffold>;
  }

  if (step === "personalization") return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="안전에 필요한 내용만 더 확인할게요" description="점검 방향과 현재 사용 정보를 확인합니다. 질환명·약명·사진·자유서술은 받지 않습니다." action={<button className="app-primary" type="submit" form="app-personalization" disabled={!active || busy}>{busy ? "확인 중" : "결과 확인"}</button>}>
    <button className="app-inline-action" type="button" onClick={() => setStep("prepared")}>루틴 요약으로 돌아가기</button>
    {outcomeStatus && <AppStatusNotice kind={outcomeStatus} detail={error} />}
    <form id="app-personalization" className="app-personalization" onSubmit={submitPersonalization}>
      <fieldset><legend>현재 가장 먼저 확인할 변화</legend>
        <label><input type="radio" name="priority" value="none" defaultChecked /> 지금은 특정 고민이 없어요</label>
        <label><input type="radio" name="priority" value="surface_oil_tendency" /> 번들거림 경향</label>
        <label><input type="radio" name="priority" value="texture_congestion_tendency" /> 피부결·막힘 경향</label>
        <label><input type="radio" name="priority" value="redness_tendency" /> 붉어짐 경향</label>
      </fieldset>
      <fieldset><legend>안전 확인</legend>
        <label><input type="checkbox" name="irritation-history" value="yes" /> 화장품 사용 중 자극 경험이 있어요</label>
        <label><input type="checkbox" name="acid" value="yes" /> 현재 산 성분 제품을 사용해요</label>
        <label><input type="checkbox" name="retinoid" value="yes" /> 현재 레티노이드 제품을 사용해요</label>
      </fieldset>
      <label>피부과 치료 여부<select name="treatment" defaultValue="unknown"><option value="none">없음</option><option value="in_use">치료 중</option><option value="unknown">모름</option></select></label>
      <label>세안 뒤 건조·당김 정도<select name="tightness" defaultValue="0"><option value="0">없음</option><option value="1">가끔</option><option value="2">보통</option><option value="3">자주</option><option value="4">매우 자주</option></select></label>
      <fieldset><legend>영향을 줄 수 있는 습관</legend>
        <label><input type="checkbox" name="frequent-cleansing" value="yes" /> 세안을 자주 해요</label>
        <label><input type="checkbox" name="post-cleanse-tightness" value="yes" /> 세안 뒤 당김이 있어요</label>
        <label><input type="checkbox" name="face-touching" value="yes" /> 얼굴을 자주 만져요</label>
      </fieldset>
    </form>
  </Scaffold>;

  if (step === "result" && (!active || careResultScope !== serviceScope)) return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="입력을 다시 확인해 주세요" description="연결이 바뀌어 이전 점검 결과를 표시하지 않아요. 등록한 제품과 사용 빈도는 유지돼요. 점검 답변은 다시 확인해 주세요." action={<button className="app-primary" type="button" disabled={!active} onClick={event => { event.preventDefault(); setStep("personalization"); }}>입력 확인하기</button>} />;

  if (step === "result" && careResult) return <Scaffold step={step} onBack={goBack} onOpenSettings={onOpenSettings} title="루틴 점검 결과를 확인해 보세요" description="악화에 영향을 줄 수 있는 요인과 성분 계획, 안전 제한을 함께 보여드립니다." action={<button className="app-primary" type="button" onClick={() => { if (onComplete) {setStep("products"); setCareResult(null); onComplete(); return;} searchGeneration.current += 1; setStep("welcome"); setQuery(""); setSelected([]); setResults([]); setSearchAttempted(false); setFrequencies({}); setQ04("not_asked"); setFollowup(null); setCareResult(null); setOutcomeStatus(null); setError(""); }}>{onComplete ? "홈으로" : "새 루틴 시작"}</button>}>
    <CareResult envelope={careResult} label="합성 케어 결과" />
    <p className="app-safe-note">합성 프리뷰 결과입니다. 진단·치료·자동 피부 개선 판정이 아니며, 구독이나 결제를 시작하지 않습니다.</p>
  </Scaffold>;

  return null;
}
