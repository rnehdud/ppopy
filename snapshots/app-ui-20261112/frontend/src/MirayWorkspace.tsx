import type {MemberKbClient} from "./memberKbReview";
import type {KbAppPort} from './KbOnboarding';
import {lazy,Suspense,type ComponentProps} from "react";
import MemberKbPanel from "./MemberKbPanel";
const KbAppPanel=import.meta.env.DEV?lazy(()=>import('./KbOnboarding')):null;
import PublicOriginalLoopPanel from "./PublicOriginalLoopPanel";
import type {OriginalPublicLoopConnection} from "./publicOriginalLoop";
const TestOriginalLoopPanel=import.meta.env.VITE_APP_MODE==="app_public_candidate"?null:lazy(()=>import("./MirayOriginalLoopTestPanel"));
type OriginalPanelSelection={kind:"public";connection:OriginalPublicLoopConnection}|{kind:"TEST";connection:OriginalLoopTestConnection};
function SelectedOriginalLoopPanel({selected,...props}:{selected:OriginalPanelSelection}&Omit<ComponentProps<typeof PublicOriginalLoopPanel>,"connection">){
  if(selected.kind==="public")return <PublicOriginalLoopPanel {...props} connection={selected.connection}/>;
  if(!TestOriginalLoopPanel)return <p role="status">이 앱에서 사용할 수 없는 연결이에요.</p>;
  return <Suspense fallback={<p role="status">저장된 루틴을 확인하고 있어요.</p>}><TestOriginalLoopPanel {...props} connection={selected.connection}/></Suspense>;
}
import type {OriginalLoopTestConnection} from "./mirayOriginalLoopTest";
import type {MirayQuotaStatusStore} from "./mirayQuotaStatus";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import {useCallback, useLayoutEffect, useEffect, useMemo, useRef, useState, type ReactNode} from "react";
import AppPrototype from "./AppPrototype";
import {productPresentation} from "./productPresentation";
import {resetAppScroll} from "./appScroll";
import ProductFrequencyEditor from "./ProductFrequencyEditor";
import RoutineOrderList from "./RoutineOrderList";
import RoutinePeriodTabs from "./RoutinePeriodTabs";
import {groupRoutineProducts, reorderRoutineSubset} from "./routineProductGroups";
import MirayExplore from "./MirayExplore";
import type {CandidateComparisonReader} from "./candidateComparisonModel";
import {createMirayExploreSearch} from "./mirayExploreSearch";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import MirayClosedLoopPanel from "./MirayClosedLoopPanel";
import MirayClosedLoopEntryPanel from "./MirayClosedLoopEntryPanel";
import MirayClosedLoopJourneyReviewPanel from "./MirayClosedLoopJourneyReviewPanel";
import type {ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";
import MirayReplenishmentReview, {type ReplenishmentCheck} from "./MirayReplenishmentReview";
import type {ClosedLoopEntryReviewStore} from "./mirayClosedLoopEntry";
import type {ClosedLoopReviewStore} from "./mirayClosedLoop";
import type {ProductCandidate} from "./productCatalog";
import type {CareApiClient} from "./careApi";
import {visibleHomeTasks, type HomeTask, type MirayTab} from "./mirayNavigation";
import PpopyTabIcon from "./PpopyTabIcon";
import config from "../../skin_engine/config/miray_navigation.json";
import {parseMirayPortfolioEnvelope, portfolioFingerprint, portfolioFromWorkspace, workspaceFromPortfolio, type MirayPortfolioStore, type MirayProductDepletionStatus, type MirayRoutineOrder} from "./mirayPortfolio";
import {isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl, type MiraySavedCandidatesStore} from "./miraySavedCandidates";
import {parseSkinStateHomeTasks, validateMiraySkinState, routineDiscomfortFromSkinState, type MiraySkinState, type MiraySkinStateStore} from "./miraySkinState";
import "./mirayWorkspace.css";
import "./mirayRoutine.css";
import "./mirayCosmetics.css";
import "./mirayFigmaTabs.css";

/** Navigation layer. Optional storage contains products/routine only, never skin observations. */
/**
 * Member product lookup and routine analysis both receive their client from
 * app composition. They must not fall back to the fixture client that is
 * useful in isolated previews: a member must never see synthetic search or
 * routine data as if it were their own.
 */
type MemberCareClient = Pick<CareApiClient, "searchProducts"> & Partial<Pick<CareApiClient, "analyze" | "searchWebProducts">>;

function productEvidenceReference(product: ProductCandidate): {sourceUrl: string; provenanceHash: string} | null {
  const sourceUrl = product.sourceUrl ?? null;
  const provenanceHash = product.provenanceHash ?? null;
  if (sourceUrl === null || provenanceHash === null) return null;
  try { validateMirayCandidateSourceUrl(sourceUrl); }
  catch { return null; }
  return isMirayCandidateProvenanceHash(provenanceHash) ? {sourceUrl, provenanceHash} : null;
}

function ProductEvidenceLink({product}: {product: ProductCandidate}) {
  const reference = productEvidenceReference(product);
  if (!reference) return null;
  return <p className="miray-evidence"><a href={reference.sourceUrl} target="_blank" rel="noreferrer">제품 출처 보기</a><small>전성분 버전 확인용 · {reference.provenanceHash.slice(0, 12)}…</small></p>;
}


export default function MirayWorkspace({settings, localFirstReads=false, kbAppPort, memberKbClient, portfolioStore, savedCandidateStore, candidateComparisonReader, closedLoopReviewStore, closedLoopEntryReviewStore, closedLoopJourneyReviewFactory, originalLoopTestFactory:testLoopFactory, publicLoopFactory, quotaStatusStore, memberCareClient, skinStateEnabled = config.checkin_enabled, replenishmentEnabled = config.replenishment_enabled, sensitiveConsentVerified = false, historyStorageConsented = false, skinStateStore, homeTasks = []}: {
  settings: ReactNode;
  localFirstReads?: boolean;
  /** Explicit loopback-only development port; never supplied by public composition. */
  kbAppPort?: Omit<KbAppPort,"onClose">;
  portfolioStore?: MirayPortfolioStore;
  savedCandidateStore?: MiraySavedCandidatesStore;
  /** Explicit synthetic TEST reader; no fallback, HTTP route or feature activation. */
  candidateComparisonReader?: CandidateComparisonReader;
  /** Explicit local TEST port; no runtime fallback or feature activation. */
  closedLoopReviewStore?: ClosedLoopReviewStore;
  /** Initial/fresh state local review port; runtime supplies no default. */
  closedLoopEntryReviewStore?: ClosedLoopEntryReviewStore;
  closedLoopJourneyReviewFactory?: ()=>ClosedLoopJourneyReviewStore;
  originalLoopTestFactory?:()=>OriginalLoopTestConnection;
  publicLoopFactory?:()=>OriginalPublicLoopConnection;
  quotaStatusStore?:MirayQuotaStatusStore;
  memberKbClient?:MemberKbClient;
  memberCareClient?: MemberCareClient;
  skinStateEnabled?: boolean;
  /** A member-declared availability aid. It stays off until the launch policy enables it. */
  replenishmentEnabled?: boolean;
  sensitiveConsentVerified?: boolean;
  historyStorageConsented?: boolean;
  skinStateStore?: MiraySkinStateStore;
  /** Trusted server-produced due/action events only; never derive these from client answers. */
  homeTasks?: HomeTask[];
}) {
  const [tab, setTab] = useState<MirayTab>("home");
  const [managingProducts,setManagingProducts]=useState(false);
  const [managedProductId,setManagedProductId]=useState("");
  const [choosingRoutine,setChoosingRoutine]=useState(false);
  const [routineSelection,setRoutineSelection]=useState<string[]>([]);
  const [routinePeriod, setRoutinePeriod] = useState<"am" | "pm">("am");
  const [editing, setEditing] = useState<"kb-review" | "registration" | "skin-state" | "analysis" | "closed-loop" | "loop-entry" | "loop-journey" | "loop-original" | "replenishment" | null>(null);
  const [editorStarted, setEditorStarted] = useState(false);
  useLayoutEffect(resetAppScroll, [tab, editing]);
  const [products, setProducts] = useState<ProductCandidate[]>([]);
  const [periods, setPeriods] = useState<Record<string, string>>({});
  const [routineOrder, setRoutineOrder] = useState<MirayRoutineOrder>({am:[],pm:[]});
  const [frequencies, setFrequencies] = useState<Record<string, string>>({});
  const [depletionStatuses, setDepletionStatuses] = useState<Record<string, MirayProductDepletionStatus>>({});
  const [portfolioReady, setPortfolioReady] = useState(!portfolioStore);
  const [portfolioLoadFailed, setPortfolioLoadFailed] = useState(false);
  const [portfolioReload, setPortfolioReload] = useState(0);
  const [portfolioSaveFailed, setPortfolioSaveFailed] = useState(false);
  const [portfolioWriting, setPortfolioWriting] = useState(false);
  const [portfolioSaveFailureVersion, setPortfolioSaveFailureVersion] = useState(0);
  const [portfolioRevisionConflict, setPortfolioRevisionConflict] = useState(false);
  const [confirmConflictReload, setConfirmConflictReload] = useState(false);
  const [portfolioSaveRetry, setPortfolioSaveRetry] = useState(0);
  const [portfolioMessage, setPortfolioMessage] = useState(portfolioStore ? "내 화장품을 불러오는 중이에요." : "기록은 이번 세션에만 유지돼요.");
  const [skinState, setSkinState] = useState<MiraySkinState | null>(null);
  const [skinStateKind, setSkinStateKind] = useState<MiraySkinState["kind"]>("baseline");
  const [checkinMessage, setCheckinMessage] = useState("");
  const [stateHomeTasks, setStateHomeTasks] = useState<HomeTask[]>([]);
  const [pendingProductRemoval, setPendingProductRemoval] = useState<string | null>(null);
  const [memberCareUnavailable, setMemberCareUnavailable] = useState<"product" | "analysis" | null>(null);
  const revision = useRef(0);
  const portfolioReadFloor=useRef<{store:MirayPortfolioStore;minimumRevision:number}|null>(null);
  const lastSaved = useRef("");
  const saveQueue = useRef(Promise.resolve());
  // Every load/reload owns its revision and queued writes. Already sent writes
  // cannot be rolled back here, but must never acknowledge a different binding.
  const portfolioLifetime = useRef({active:false,pending:0});
  const saveBlocked = useRef(false);
  const [loadedBinding, setLoadedBinding] = useState<{store:MirayPortfolioStore; reload:number} | null>(null);
  const exploreSearch = useMemo(() => memberCareClient ? createMirayExploreSearch(memberCareClient) : undefined, [memberCareClient]);
  const effectivePeriods = useMemo(() => Object.fromEntries(products.map(product => [product.id, periods[product.id] || ""])), [products, periods]);
  const portfolio = useMemo(() => portfolioFromWorkspace(products, frequencies, effectivePeriods, routineOrder, depletionStatuses), [depletionStatuses, products, frequencies, effectivePeriods, routineOrder]);
  const routineReady = portfolio.periods.am.length + portfolio.periods.pm.length > 0;
  const tasks = visibleHomeTasks([
    ...[...stateHomeTasks, ...homeTasks].filter(task =>
      !["safety", "skin_change", "checkin", "adjustment"].includes(task.kind)
      || (sensitiveConsentVerified && (!["checkin", "skin_change"].includes(task.kind) || skinStateEnabled))),
    ...(products.length ? [
      {id:"routine", kind:"information", title:"등록한 제품의 사용 정보를 확인해요", route:"routine" as const},
    ] : [{id:"register", kind:"information", title:"현재 쓰는 화장품부터 추가해요", route:"cosmetics" as const}]),
    ...(replenishmentEnabled && products.some(product => ["running_low","empty"].includes(depletionStatuses[product.id])) ? [
      {id:"replenishment", kind:"depletion", title:"사용 상태를 확인하고 재구매 전 제품 정보를 다시 살펴봐요", route:"cosmetics" as const},
    ] : []),
  ]);

  const [expectedDecisionRef, setExpectedDecisionRef] = useState<string | undefined>();
  const [expectedEntryPortfolioRevision,setExpectedEntryPortfolioRevision]=useState<number|undefined>();
  // A connection is a local lifecycle boundary; authentication still belongs to
  // the server/native adapters. Ordinary same-connection renders keep drafts.
  const publicBinding = useMemo(() => ({live:false, portfolioStore, portfolioReload, memberCareClient, savedCandidateStore, candidateComparisonReader}), [portfolioStore, portfolioReload, memberCareClient, savedCandidateStore, candidateComparisonReader]);
  const originalLoopFactory=publicLoopFactory??testLoopFactory;
  const sensitiveBinding = useMemo(() => ({live:false, publicBinding, skinStateStore, closedLoopReviewStore, closedLoopEntryReviewStore, closedLoopJourneyReviewFactory, originalLoopFactory, quotaStatusStore, sensitiveConsentVerified, historyStorageConsented, skinStateEnabled, memberKbClient}), [memberKbClient, publicBinding, skinStateStore, closedLoopReviewStore, closedLoopEntryReviewStore, closedLoopJourneyReviewFactory, originalLoopFactory, quotaStatusStore, sensitiveConsentVerified, historyStorageConsented, skinStateEnabled]);
  const [journeySelection,setJourneySelection]=useState<{binding:typeof sensitiveBinding;store:ClosedLoopJourneyReviewStore;initialPage:"entry"|"episode"}|null>(null);
  const journeyOwner=useRef<ClosedLoopJourneyReviewStore|OriginalLoopTestConnection|OriginalPublicLoopConnection|null>(null);
  const [originalSelection,setOriginalSelection]=useState<{binding:typeof sensitiveBinding;initialPage:"entry"|"episode";revision:number}&OriginalPanelSelection|null>(null);
  const openOriginal=(initialPage:"entry"|"episode")=>{
    if(!originalLoopFactory || !portfolioStore || !sensitiveConsentVerified || !historyStorageConsented)return;
    try{if(publicLoopFactory&&testLoopFactory)throw new Error("Two loop profiles cannot share a screen");
      const selected:OriginalPanelSelection=publicLoopFactory?{kind:"public",connection:publicLoopFactory()}:{kind:"TEST",connection:testLoopFactory!()};
      if(!selected.connection.isCurrent())throw new Error("Original connection unavailable");journeyOwner.current?.invalidate();journeyOwner.current=selected.connection;
      setOriginalSelection({...selected,binding:sensitiveBinding,initialPage,revision:revision.current});setEditing("loop-original");}
    catch{setCheckinMessage(publicLoopFactory?"점검 연결을 확인하지 못했어요. 계정과 필수 동의 상태를 다시 확인해 주세요.":"점검 연결을 확인하지 못했어요. 계정과 별도 이력 저장 동의를 다시 확인해 주세요.");setEditing(null);}
  };
  const openJourney=(initialPage:"entry"|"episode")=>{
    if(!closedLoopJourneyReviewFactory || !sensitiveConsentVerified || !historyStorageConsented)return;
    try{const store=closedLoopJourneyReviewFactory();if(!store.isCurrent())throw new Error("Journey unavailable");journeyOwner.current?.invalidate();journeyOwner.current=store;setJourneySelection({binding:sensitiveBinding,store,initialPage});setEditing("loop-journey");}
    catch{setCheckinMessage("점검 연결을 확인하지 못했어요. 계정과 별도 이력 저장 동의를 다시 확인해 주세요.");setEditing(null);}
  };
  const replenishmentBinding=useMemo(()=>({publicBinding,sensitiveBinding,replenishmentEnabled}),[publicBinding,sensitiveBinding,replenishmentEnabled]);
  const replenishmentOwner=useRef<typeof replenishmentBinding|null>(null);
  const [replenishmentSelection,setReplenishmentSelection]=useState<{binding:typeof replenishmentBinding;id:string;fingerprint:string}|null>(null);
  const publicOwner = useRef<typeof publicBinding | null>(null);
  const sensitiveOwner = useRef<typeof sensitiveBinding | null>(null);
  const [mountedPublicBinding, setMountedPublicBinding] = useState<typeof publicBinding | null>(null);
  const [mountedSensitiveBinding, setMountedSensitiveBinding] = useState<typeof sensitiveBinding | null>(null);
  const editorExitFingerprint = useRef<string | null>(null);
  useLayoutEffect(() => {
    publicBinding.live = true; publicOwner.current = publicBinding;
    setMountedPublicBinding(publicBinding); setEditorStarted(false);setManagingProducts(false);setManagedProductId("");setChoosingRoutine(false);
    setEditing(current => current === "registration" ? null : current);
    editorExitFingerprint.current = null;
    return () => {publicBinding.live = false; if (publicOwner.current === publicBinding) publicOwner.current = null;};
  }, [publicBinding]);
  useLayoutEffect(() => {
    sensitiveBinding.live = true; sensitiveOwner.current = sensitiveBinding;
    setMountedSensitiveBinding(sensitiveBinding);
    setJourneySelection(null);setOriginalSelection(null);
    setSkinState(null); setStateHomeTasks([]); setCheckinMessage(""); setExpectedDecisionRef(undefined);setExpectedEntryPortfolioRevision(undefined);
    setEditing(current => current === "skin-state" || current === "analysis" || current === "closed-loop" || current === "loop-entry" || current === "loop-journey" || current === "loop-original" ? null : current);
    return () => {journeyOwner.current?.invalidate();journeyOwner.current=null;sensitiveBinding.live = false; if (sensitiveOwner.current === sensitiveBinding) sensitiveOwner.current = null;};
  }, [sensitiveBinding]);
  useLayoutEffect(()=>{
    replenishmentOwner.current=replenishmentBinding;
    setReplenishmentSelection(null);
    setEditing(current=>current==="replenishment"?null:current);
    return()=>{if(replenishmentOwner.current===replenishmentBinding)replenishmentOwner.current=null;};
  },[replenishmentBinding]);
  const publicFrame = useMemo(() => ({binding:publicBinding, editing, tab}), [publicBinding, editing, tab]);
  const sensitiveFrame = useMemo(() => ({binding:sensitiveBinding, editing, tab, skinStateKind, expectedDecisionRef}), [sensitiveBinding, editing, tab, skinStateKind, expectedDecisionRef]);
  const publicFrameOwner = useRef<typeof publicFrame | null>(null);
  const sensitiveFrameOwner = useRef<typeof sensitiveFrame | null>(null);
  useLayoutEffect(() => {
    publicFrameOwner.current = publicFrame;
    return () => {if (publicFrameOwner.current === publicFrame) publicFrameOwner.current = null;};
  }, [publicFrame]);
  useLayoutEffect(() => {
    sensitiveFrameOwner.current = sensitiveFrame;
    return () => {if (sensitiveFrameOwner.current === sensitiveFrame) sensitiveFrameOwner.current = null;};
  }, [sensitiveFrame]);
  const publicFrameLive = useCallback(() => publicBinding.live && publicOwner.current === publicBinding && publicFrameOwner.current === publicFrame, [publicBinding, publicFrame]);
  // The settings child sees navigation retirement before its React unmount.
  // This view gate never authenticates or disposes an account/store owner.
  const settingsLifetime=useMemo(()=>({get live(){return publicFrameLive() && !editing && tab==="my";}}),[publicFrameLive,editing,tab]);
  const sensitiveFrameLive = useCallback(() => sensitiveBinding.live && sensitiveOwner.current === sensitiveBinding && sensitiveFrameOwner.current === sensitiveFrame && sensitiveConsentVerified, [sensitiveBinding, sensitiveFrame, sensitiveConsentVerified]);
  const skinStateLifetime=useMemo(()=>({isCurrent:sensitiveFrameLive}),[sensitiveFrameLive]);
  const consumeFrame = useCallback(() => {
    publicFrameOwner.current = null; sensitiveFrameOwner.current = null;
    setExpectedEntryPortfolioRevision(undefined);
    setConfirmConflictReload(false); setPendingProductRemoval(null);
  }, []);
  const editorLive = useCallback(() => publicFrameLive() && (editing === "registration" || (editing === "analysis" && sensitiveFrameLive())), [publicFrameLive, sensitiveFrameLive, editing]);
  const onEditorProducts = useCallback((value:ProductCandidate[]) => {if (editorLive()) setProducts(structuredClone(value));}, [editorLive]);
  const onEditorFrequencies = useCallback((value:Record<string,string>) => {if (editorLive()) setFrequencies({...value});}, [editorLive]);
  const navigate = (next:MirayTab) => {
    if (!publicFrameLive() || editing || next === tab) return;
    consumeFrame(); setTab(next);
  };
  const leaveEditor = (next:MirayTab) => {
    if (!editorLive()) return;
    consumeFrame(); editorExitFingerprint.current = currentFingerprint.current;
    setEditing(null); setTab(next);
  };
  const leaveSensitive = (next:MirayTab) => {
    if (!sensitiveFrameLive()) return;
    journeyOwner.current?.invalidate();journeyOwner.current=null;setJourneySelection(null);setOriginalSelection(null);
    consumeFrame(); setExpectedDecisionRef(undefined); setEditing(null); setTab(next);
  };

  const currentFingerprint = useRef(portfolioFingerprint(portfolio));
  useLayoutEffect(() => {currentFingerprint.current = portfolioFingerprint(portfolio);}, [portfolio]);
  // Recovery and confirmation belong to their issued view/attempt. Retiring an
  // action does not cancel an already entered edit or its account-owned save.
  const portfolioActions = useMemo(() => ({publicFrame, portfolioLoadFailed, portfolioSaveFailed, portfolioSaveFailureVersion,
    portfolioRevisionConflict, portfolioSaveRetry, confirmConflictReload, pendingProductRemoval,managingProducts,managedProductId,choosingRoutine,routineSelection,routinePeriod}),
  [publicFrame, portfolioLoadFailed, portfolioSaveFailed, portfolioSaveFailureVersion, portfolioRevisionConflict,
    portfolioSaveRetry, confirmConflictReload, pendingProductRemoval,managingProducts,managedProductId,choosingRoutine,routineSelection,routinePeriod]);
  const portfolioActionOwner = useRef<typeof portfolioActions | null>(null);
  useLayoutEffect(() => {
    portfolioActionOwner.current = portfolioActions;
    return () => {if (portfolioActionOwner.current === portfolioActions) portfolioActionOwner.current = null;};
  }, [portfolioActions]);
  const portfolioActionLive = () => publicFrameLive() && !editing
    && portfolioLifetime.current.active && portfolioActionOwner.current === portfolioActions;
  const consumePortfolioAction = () => {portfolioActionOwner.current = null;};
  const productRemovalTriggers = useRef(new Map<string, HTMLButtonElement>());
  const productRemovalCancel = useRef<HTMLButtonElement>(null);
  const cosmeticsHeading = useRef<HTMLHeadingElement>(null);
  const frequencyEditDetails=useRef(new Map<string,HTMLDetailsElement>());
  const frequencyEditTarget=useRef<{binding:typeof publicBinding;lifetime:typeof portfolioLifetime.current;productId:string}|null>(null);
  useLayoutEffect(()=>{
    const target=frequencyEditTarget.current;if(!target)return;
    frequencyEditTarget.current=null;
    if(target.binding!==publicOwner.current || !target.binding.live || target.lifetime!==portfolioLifetime.current
      || !target.lifetime.active || !portfolioReady || editing || tab!=="cosmetics")return;
    const details=frequencyEditDetails.current.get(target.productId),field=details?.querySelector<HTMLButtonElement>("[data-frequency-trigger]");
    if(details?.isConnected && field?.isConnected){details.open=true;field.focus({preventScroll:true});field.scrollIntoView?.({block:"center"});}
  },[publicBinding,portfolioReady,editing,tab]);
  const productRemovalFocus = useRef<{
    binding:typeof publicBinding; frame:typeof publicFrame; lifetime:typeof portfolioLifetime.current;
    target:"cancel"|"trigger"|"heading"; productId?:string;
  } | null>(null);
  const requestProductRemovalFocus = (target:"cancel"|"trigger"|"heading", productId?:string) => {
    productRemovalFocus.current = {binding:publicBinding,frame:publicFrame,lifetime:portfolioLifetime.current,target,productId};
  };
  useLayoutEffect(() => {
    const request = productRemovalFocus.current;
    if (!request) return;
    productRemovalFocus.current = null;
    // A focus request belongs to the issuing account, loaded portfolio and view.
    // Do not move focus into a replacement account or a different tab/editor.
    if (request.binding !== publicOwner.current || !request.binding.live
        || request.frame !== publicFrameOwner.current || request.lifetime !== portfolioLifetime.current
        || !request.lifetime.active || !portfolioReady || editing || tab !== "cosmetics") return;
    const target = request.target === "cancel" ? productRemovalCancel.current
      : request.target === "heading" ? cosmeticsHeading.current
      : request.productId ? productRemovalTriggers.current.get(request.productId) : null;
    if (target?.isConnected) {
      target.focus({preventScroll:true});
      if (typeof target.scrollIntoView === "function") target.scrollIntoView({block:"center"});
    }
  }, [pendingProductRemoval, products, publicBinding, publicFrame, portfolioReady, editing, tab]);
  const reloadPortfolio = () => {
    if (!portfolioActionLive() || !portfolioStore
        || (!portfolioLoadFailed && (!portfolioSaveFailed || (portfolioRevisionConflict && !confirmConflictReload)))) return;
    consumePortfolioAction(); setPortfolioReload(value => value + 1);
  };
  useLayoutEffect(() => {
    // Keep a product search on simple exit/reopen, but do not replay an old
    // selected portfolio after an explicit edit elsewhere in the workspace.
    if (!editing && editorStarted && editorExitFingerprint.current !== null && editorExitFingerprint.current !== portfolioFingerprint(portfolio)) setEditorStarted(false);
  }, [editing, editorStarted, portfolio]);
  useLayoutEffect(() => {
    const lifetime = {active:true,pending:0};
    if(portfolioReadFloor.current?.store!==portfolioStore)portfolioReadFloor.current=null;
    portfolioLifetime.current = lifetime;
    saveQueue.current = Promise.resolve();
    saveBlocked.current = false;
    revision.current = 0;
    lastSaved.current = "";
    setLoadedBinding(null);
    setPortfolioReady(!portfolioStore);
    setPortfolioLoadFailed(false);
    setPortfolioSaveFailed(false);
    setPortfolioWriting(false);
    setPortfolioSaveFailureVersion(0);
    setPortfolioRevisionConflict(false);
    setConfirmConflictReload(false);
    setPendingProductRemoval(null);
    setMemberCareUnavailable(null);
    setSkinState(null); setStateHomeTasks([]); setCheckinMessage("");
    setEditing(null); setEditorStarted(false);
    setProducts([]); setFrequencies({}); setPeriods({});
    setRoutineOrder({am:[],pm:[]}); setDepletionStatuses({});
    setPortfolioMessage(portfolioStore ? "내 화장품을 불러오는 중이에요." : "기록은 이번 세션에만 유지돼요.");
    return () => {lifetime.active = false;};
  }, [portfolioReload, portfolioStore]);

  useEffect(() => {
    if (!portfolioStore) return;
    const lifetime = portfolioLifetime.current;
    const active = () => lifetime.active && portfolioLifetime.current === lifetime;
    // Validate even explicitly injected readers at the workspace boundary.
    Promise.resolve().then(() => active() ? portfolioStore.read() : null).then(value => {
      if (!active()) return;
      const envelope = parseMirayPortfolioEnvelope(value);
      const floor=portfolioReadFloor.current;
      if(floor?.store===portfolioStore && envelope.revision<floor.minimumRevision)throw new Error("Original corrected portfolio read is stale");
      const restored = workspaceFromPortfolio(envelope.portfolio);
      revision.current = envelope.revision;
      lastSaved.current = portfolioFingerprint(envelope.portfolio);
      setProducts(restored.products); setFrequencies(restored.frequencies); setPeriods(restored.periods); setRoutineOrder(restored.routineOrder); setDepletionStatuses(restored.depletionStatuses);
      setLoadedBinding({store:portfolioStore,reload:portfolioReload});
      setPortfolioReady(true); setPortfolioMessage("");
    }).catch(() => {
      if (!active()) return;
      setPortfolioLoadFailed(true);
      setPortfolioMessage("저장된 화장품을 불러오지 못했어요. 연결을 확인해 주세요.");
    });
  }, [portfolioReload, portfolioStore]);

  useEffect(() => {
    if (!portfolioStore || !portfolioReady || loadedBinding?.store !== portfolioStore
        || loadedBinding.reload !== portfolioReload || saveBlocked.current || portfolioRevisionConflict) return;
    const snapshot = structuredClone(portfolio);
    const serialized = portfolioFingerprint(snapshot);
    const lifetime = portfolioLifetime.current;
    if (serialized === lastSaved.current && lifetime.pending === 0 && !portfolioSaveFailed) return;
    const active = () => lifetime.active && portfolioLifetime.current === lifetime;
    const timer = window.setTimeout(() => {
      if (!active() || saveBlocked.current) return;
      setPortfolioMessage("변경 내용을 저장하는 중이에요.");
      lifetime.pending += 1;
      setPortfolioWriting(true);
      saveQueue.current = saveQueue.current.then(async () => {
        if (!active() || saveBlocked.current || (serialized === lastSaved.current && !portfolioSaveFailed)) return;
        const expectedRevision = revision.current;
        const value = await portfolioStore.save(structuredClone(snapshot), expectedRevision);
        if (!active()) return;
        const envelope = parseMirayPortfolioEnvelope(value);
        if (envelope.revision !== expectedRevision + 1 || portfolioFingerprint(envelope.portfolio) !== serialized) {
          throw new Error("저장 응답이 요청한 변경과 일치하지 않아요.");
        }
        revision.current = envelope.revision;
        lastSaved.current = serialized;
        setPortfolioSaveFailed(false);
        setPortfolioMessage(currentFingerprint.current === serialized ? "계정에 저장했어요." : "변경 내용을 저장하는 중이에요.");
      }).catch((error: unknown) => {
        if (!active()) return;
        // Stop queued writes as well as future automatic attempts on any failure.
        saveBlocked.current = true;
        setPortfolioSaveFailed(true);
        setPortfolioSaveFailureVersion(value => value + 1);
        const conflict = error instanceof Error && error.message === "다른 기기에서 변경된 내용이 있어 다시 불러와야 해요.";
        setPortfolioRevisionConflict(conflict);
        setPortfolioMessage(conflict ? "다른 기기에서 변경된 내용이 있어 현재 변경을 저장하지 않았어요." : "저장 결과를 확인하지 못했어요. 계정에 저장된 내용을 다시 확인해 주세요.");
      }).finally(() => {lifetime.pending -= 1;if(active())setPortfolioWriting(lifetime.pending>0);});
    }, 450);
    return () => window.clearTimeout(timer);
  }, [portfolio, portfolioReady, loadedBinding, portfolioReload, portfolioRevisionConflict, portfolioSaveFailed, portfolioSaveRetry, portfolioStore]);

  useEffect(() => {
    const back = (event: Event) => {
      // The existing input flow owns step-level back while it is visible.
      if (editing) return;
      event.stopImmediatePropagation();
      if (!publicFrameLive() || tab === "home") return;
      consumeFrame(); setTab("home");
    };
    window.addEventListener("skinanalysis:native-back", back, {capture:true});
    return () => window.removeEventListener("skinanalysis:native-back", back, {capture:true});
  }, [editing, tab, publicFrameLive, consumeFrame]);

  const removeProduct = (productId: string) => {
    if (!portfolioActionLive() || tab !== "cosmetics" || pendingProductRemoval !== productId) return;
    requestProductRemovalFocus("heading");
    consumePortfolioAction();
    setProducts(current => current.filter(product => product.id !== productId));
    setRoutineOrder(current => ({
      am:current.am.filter(id => id !== productId),
      pm:current.pm.filter(id => id !== productId),
    }));
    setFrequencies(current => {
      const next = {...current};
      delete next[productId];
      return next;
    });
    setDepletionStatuses(current => {
      const next = {...current};
      delete next[productId];
      return next;
    });
    setPeriods(current => {
      const next = {...current};
      delete next[productId];
      return next;
    });
    setPendingProductRemoval(null);setManagedProductId(products.find(p=>p.id!==productId)?.id??"");
  };

  const replenishmentProduct=replenishmentSelection?.binding===replenishmentBinding
    && replenishmentSelection.fingerprint===portfolioFingerprint(portfolio)
    ?products.find(product=>product.id===replenishmentSelection.id):undefined;
  const replenishmentLive=()=>publicFrameLive() && editing==="replenishment" && replenishmentEnabled
    && replenishmentOwner.current===replenishmentBinding && Boolean(replenishmentProduct)
    && replenishmentSelection?.fingerprint===currentFingerprint.current;
  // A reference screen may show an unacknowledged draft, but it cannot start a
  // server-selected entry against a different or still uncertain portfolio.
  const portfolioSettled=Boolean(portfolioStore && loadedBinding?.store===portfolioStore && loadedBinding.reload===portfolioReload
    && portfolioReady && !portfolioSaveFailed && !portfolioRevisionConflict && !saveBlocked.current
    && !portfolioWriting && portfolioLifetime.current.pending===0 && lastSaved.current===portfolioFingerprint(portfolio));
  const kbEnabled=Boolean(memberKbClient || (import.meta.env.DEV && import.meta.env.VITE_KB_APP_PREVIEW === "true" && kbAppPort));
  // A navigation target belongs only to this authorized workspace and portfolio revision.
  const kbRevision=portfolioSettled ? revision.current : null;
  const kbNavigation=useMemo(()=>({operation:null as string|null,viewKey:crypto.randomUUID()}),[sensitiveBinding,kbRevision]);
  const kbOpenedAt=useRef(0);
  const startKbReview=()=>{if(!kbEnabled || !portfolioSettled || !publicFrameLive() || !sensitiveConsentVerified || !historyStorageConsented)return;kbOpenedAt.current=performance.now();consumeFrame();setEditing("kb-review")};
  const startPublicRoutineReview=()=>{
    if(kbEnabled){startKbReview();return;}
    if(!publicLoopFactory || !publicFrameLive() || !portfolioSettled)return;
    if(sensitiveConsentVerified && historyStorageConsented && !sensitiveFrameLive())return;
    consumeFrame();setMemberCareUnavailable(null);setExpectedDecisionRef(undefined);
    if(!sensitiveConsentVerified || !historyStorageConsented){setEditing(null);setTab("my");return;}
    setExpectedEntryPortfolioRevision(revision.current);openOriginal("entry");
  };
  const replenishmentCheck:ReplenishmentCheck=!portfolioSettled?"unsettled"
    :publicLoopFactory?(!routineReady?"routine_incomplete":!sensitiveConsentVerified?"consent":!historyStorageConsented?"history_consent":"ready")
    :!closedLoopEntryReviewStore && !closedLoopJourneyReviewFactory && !(skinStateEnabled && memberCareClient?.analyze)?"unavailable":!routineReady?"routine_incomplete"
    :!sensitiveConsentVerified?"consent":(closedLoopEntryReviewStore || closedLoopJourneyReviewFactory) && historyStorageConsented?"ready"
    :skinStateEnabled && memberCareClient?.analyze?"ready":(closedLoopEntryReviewStore || closedLoopJourneyReviewFactory)?"history_consent":"unavailable";
  const closeReplenishment=()=>{
    if(!replenishmentLive())return;
    consumeFrame();setReplenishmentSelection(null);setEditing(null);setTab("cosmetics");
  };
  const checkReplenishment=()=>{
    if(!replenishmentLive() || !portfolioSettled || ["unsettled","unavailable"].includes(replenishmentCheck))return;
    consumeFrame();setReplenishmentSelection(null);setExpectedDecisionRef(undefined);setMemberCareUnavailable(null);
    if(replenishmentCheck==="consent" || replenishmentCheck==="history_consent"){setEditing(null);setTab("my");return;}
    if(replenishmentCheck==="routine_incomplete"){setEditing(null);setTab("routine");return;}
    if(publicLoopFactory && historyStorageConsented){setExpectedEntryPortfolioRevision(revision.current);openOriginal("entry");return;}
    if(closedLoopJourneyReviewFactory && historyStorageConsented){setExpectedEntryPortfolioRevision(revision.current);openJourney("entry");return;}
    if(closedLoopEntryReviewStore && historyStorageConsented){setExpectedEntryPortfolioRevision(revision.current);setEditing("loop-entry");return;}
    // Always collect concern and discomfort independently; no direct legacy
    // single-question analysis path is introduced by the rebuy handoff.
    setSkinState(null);setSkinStateKind("baseline");setEditorStarted(true);setEditing("skin-state");
  };
  useEffect(()=>{
    if(editing!=="replenishment")return;
    const back=(event:Event)=>{event.stopImmediatePropagation();closeReplenishment();};
    window.addEventListener("skinanalysis:native-back",back,{capture:true});
    return()=>window.removeEventListener("skinanalysis:native-back",back,{capture:true});
    // The rendered view's issued frame guards native back as well as buttons.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[publicFrame,replenishmentBinding,replenishmentSelection,editing]);

  if (portfolioStore && (!portfolioReady || loadedBinding?.store !== portfolioStore || loadedBinding.reload !== portfolioReload)) return <div className="miray-workspace" role="region" aria-label="내 화장품과 루틴" aria-busy={true}>
    <p className="miray-portfolio-status" role={portfolioLoadFailed ? "alert" : "status"} aria-label={portfolioMessage} aria-atomic="true"><span aria-hidden="true">{portfolioMessage}</span></p>
    <main className="miray-main">{portfolioLoadFailed && <button className="miray-primary" onClick={reloadPortfolio}>다시 불러오기</button>}</main>
  </div>;

  return <div className="miray-workspace" data-figma-tab={tab === "cosmetics" || tab === "routine" ? tab : undefined} role="region" aria-label="내 화장품과 루틴" aria-busy={false}>
    <div hidden={!editing}>
      {memberKbClient && editing==="kb-review" && mountedSensitiveBinding===sensitiveBinding && sensitiveConsentVerified && historyStorageConsented &&
        <MemberKbPanel key={kbNavigation.viewKey} client={memberKbClient} navigation={localFirstReads && portfolioSettled && memberKbClient.overview ? kbNavigation : undefined} openedAt={kbOpenedAt.current} loadingOrder={portfolioSettled?{am:portfolio.periods.am.map(id=>products.find(p=>p.id===id)).flatMap(p=>p?[productPresentation(p).name]:[]),pm:portfolio.periods.pm.map(id=>products.find(p=>p.id===id)).flatMap(p=>p?[productPresentation(p).name]:[])}:undefined} loadingProductNames={portfolioSettled?products.map(p=>productPresentation(p).name):[]} close={()=>leaveSensitive("home")} editRoutine={()=>leaveSensitive("routine")}/>}
      {!memberKbClient && KbAppPanel && kbEnabled && kbAppPort && editing==="kb-review" && mountedSensitiveBinding===sensitiveBinding && <Suspense fallback={<p>KB 점검 준비 중</p>}><KbAppPanel integration={{...kbAppPort,onClose:()=>leaveSensitive("home"),onPortfolioChanged:()=>{setTab("routine");setPortfolioReload(v=>v+1)}}}/></Suspense>}
      {mountedPublicBinding===publicBinding && editing==="replenishment" && replenishmentEnabled && replenishmentProduct && <MirayReplenishmentReview requiredConsent={Boolean(publicLoopFactory)}
        product={replenishmentProduct} status={depletionStatuses[replenishmentProduct.id]} frequency={frequencies[replenishmentProduct.id] ?? ""}
        period={periods[replenishmentProduct.id] ?? ""} total={products.length} check={replenishmentCheck} portfolioMessage={portfolioMessage}
        onClose={closeReplenishment} onCheck={checkReplenishment}/>}
      {mountedSensitiveBinding===sensitiveBinding && editing==="loop-original" && originalSelection?.binding===sensitiveBinding && <SelectedOriginalLoopPanel
        selected={originalSelection} quotaStatusStore={quotaStatusStore} initialPage={originalSelection.initialPage} expectedPortfolioRevision={originalSelection.revision}
        requestLifetime={skinStateLifetime} onClose={()=>leaveSensitive("home")} onEditFrequency={productId=>{
          if(!sensitiveFrameLive() || !historyStorageConsented || !portfolioSettled || originalSelection.binding!==sensitiveBinding
            || journeyOwner.current!==originalSelection.connection || !originalSelection.connection.isCurrent()
            || revision.current!==originalSelection.revision || !products.some(p=>p.id===productId))return false;
          frequencyEditTarget.current={binding:publicBinding,lifetime:portfolioLifetime.current,productId};
          leaveSensitive("cosmetics");return true;
        }} onPortfolioRefresh={minimumRevision=>{
          if(!sensitiveFrameLive() || !historyStorageConsented || !portfolioStore || !portfolioSettled || originalSelection.binding!==sensitiveBinding
            || journeyOwner.current!==originalSelection.connection || !originalSelection.connection.isCurrent()
            || revision.current!==originalSelection.revision || !Number.isSafeInteger(minimumRevision)
            || ![originalSelection.revision,originalSelection.revision+1].includes(minimumRevision))return false;
          portfolioReadFloor.current={store:portfolioStore,minimumRevision};
          // Retire pending saves and the old frame before any new canonical
          // read. The receipt never supplies or writes a portfolio payload.
          portfolioLifetime.current.active=false;saveBlocked.current=true;
          leaveSensitive("home");setPortfolioReload(value=>value+1);
          return true;
        }}/>}
      {mountedSensitiveBinding===sensitiveBinding && editing==="loop-journey" && journeySelection?.binding===sensitiveBinding && <MirayClosedLoopJourneyReviewPanel
        store={journeySelection.store} initialPage={journeySelection.initialPage} expectedPortfolioRevision={expectedEntryPortfolioRevision}
        requestLifetime={skinStateLifetime} active={sensitiveConsentVerified && historyStorageConsented} onClose={()=>leaveSensitive("home")}/>}
      {mountedSensitiveBinding === sensitiveBinding && editing === "loop-entry" && closedLoopEntryReviewStore && <MirayClosedLoopEntryPanel expectedPortfolioRevision={expectedEntryPortfolioRevision} requestLifetime={skinStateLifetime} store={closedLoopEntryReviewStore} active={sensitiveConsentVerified && historyStorageConsented} onClose={()=>leaveSensitive("home")} onExistingEpisode={closedLoopReviewStore?()=>{
        if (!sensitiveFrameLive() || !historyStorageConsented) return;
        consumeFrame(); setExpectedDecisionRef(undefined); setEditing("closed-loop");
      }:undefined} onEpisode={closedLoopReviewStore?decisionRef=>{
        if (!sensitiveFrameLive() || !historyStorageConsented || typeof decisionRef !== "string" || !/^sha256:[0-9a-f]{64}$/.test(decisionRef)) return;
        consumeFrame(); setExpectedDecisionRef(decisionRef); setEditing("closed-loop");
      }:undefined}/>}
      {mountedSensitiveBinding === sensitiveBinding && editing === "closed-loop" && closedLoopReviewStore && <MirayClosedLoopPanel store={closedLoopReviewStore} active={sensitiveConsentVerified && historyStorageConsented} expectedDecisionRef={expectedDecisionRef} requestLifetime={skinStateLifetime} onClose={()=>leaveSensitive("home")}/>}
      {mountedSensitiveBinding === sensitiveBinding && editing === "skin-state" && sensitiveConsentVerified && <MiraySkinStateCheckin kind={skinStateKind} continueToAnalysis={Boolean(memberCareClient?.analyze)} historyStorageConsented={historyStorageConsented} store={skinStateStore} requestLifetime={skinStateLifetime} onCancel={()=>leaveSensitive(skinStateKind === "checkin" ? "home" : "routine")} onComplete={(value, result) => {
        if (!sensitiveFrameLive()) return;
        let snapshot:MiraySkinState, trustedTasks:HomeTask[];
        try {
          validateMiraySkinState(value);
          if (value.kind !== skinStateKind) return;
          snapshot = structuredClone(value);
          trustedTasks = historyStorageConsented && skinStateStore && result ? parseSkinStateHomeTasks(result.homeTasks) : [];
        } catch {return;}
        consumeFrame(); setStateHomeTasks(trustedTasks); setSkinState(snapshot);
        if (skinStateKind === "checkin" || !memberCareClient?.analyze) {
          const label = skinStateKind === "checkin" ? "정기 상태 확인" : "현재 상태 확인";
          setCheckinMessage(historyStorageConsented && skinStateStore ? `${label}을 계정 이력에 저장했어요.` : `${label}을 마쳤어요. 이 답변은 계정 이력에 저장하지 않았어요.`);
          setEditing(null); setTab("home"); return;
        }
        setEditorStarted(true); setEditing("analysis");
      }} />}
      {mountedPublicBinding === publicBinding && portfolioReady && editorStarted && (editing === null || editing === "registration" || (editing === "analysis" && mountedSensitiveBinding === sensitiveBinding && sensitiveConsentVerified)) && memberCareClient && <AppPrototype
        key={editing === "analysis" ? "analysis" : "registration"}
        active={editing === "registration" || editing === "analysis"}
        exitLabel={editing === "analysis" ? "내 루틴으로" : "내 화장품으로"}
        onExit={()=>leaveEditor(editing === "analysis" ? "routine" : "cosmetics")}
        client={memberCareClient}
        initialDraft={{phase:editing === "analysis" && skinState ? "personalization" : editing === "analysis" ? "routine" : "products",selected:products,frequencies,discomfort:skinState ? routineDiscomfortFromSkinState(skinState) : "not_asked",timing:"not_asked",ongoing:"not_asked"}}
        onProductsChange={onEditorProducts} onFrequenciesChange={onEditorFrequencies}
        onRegistrationComplete={editing === "registration" ? ()=>leaveEditor("routine") : undefined}
        onComplete={()=>leaveEditor("home")}
        onOpenSettings={()=>leaveEditor("my")}
      />}
    </div>
    {!editing && <>
      <header className="miray-header"><button className="ppopy-header-search" aria-label="제품 탐색" onClick={() => navigate("explore")}><PpopyTabIcon tab="explore"/></button></header>
      {portfolioMessage && <p className="miray-portfolio-status" role="status" aria-label={portfolioMessage} aria-atomic="true"><span aria-hidden="true">{portfolioMessage}</span></p>}
      {portfolioSaveFailed && <section className="miray-card" role="alert">
        {portfolioRevisionConflict ? <>
          <p>다른 기기에서 저장된 내용이 있어 현재 변경을 계정에 반영하지 않았어요. 최신 내용을 불러오면 이 화면에서 바꾼 내용은 사라집니다.</p>
          {confirmConflictReload ? <div role="status"><p>현재 변경을 버리고 계정의 최신 내용을 불러올까요?</p><button onClick={reloadPortfolio}>최신 내용 불러오기</button><button onClick={() => {if (!portfolioActionLive()) return; consumePortfolioAction(); setConfirmConflictReload(false);}}>취소</button></div> : <button onClick={() => {if (!portfolioActionLive()) return; consumePortfolioAction(); setConfirmConflictReload(true);}}>계정 최신 내용 확인</button>}
        </> : <>
          <p>저장 결과를 확인하지 못했어요. 변경 내용은 이 화면에 남아 있어요. 계정에 저장된 내용을 다시 확인하거나 직접 다시 저장할 수 있어요.</p>
          <button disabled={!saveBlocked.current} onClick={() => {if (!portfolioActionLive() || !saveBlocked.current) return; consumePortfolioAction(); saveBlocked.current = false; setPortfolioSaveRetry(value => value + 1);}}>다시 저장</button>
          <button onClick={reloadPortfolio}>계정에 저장된 내용 다시 불러오기</button>
        </>}
      </section>}
      {tab === "my" ? <AppSettingsLifetimeContext.Provider value={settingsLifetime}>{settings}</AppSettingsLifetimeContext.Provider> : tab !== "explore" && <main className="miray-main">
        {tab === "home" && <div className="miray-home">
          <div className="miray-home-heading"><p className="miray-eyebrow" id="miray-home-context" aria-hidden="true">오늘의 루틴</p><h1 aria-describedby="miray-home-context">내 피부를 살피는 시간</h1><p>사용 중인 화장품과 현재 상태를 함께 살펴요.</p></div>
          {checkinMessage && <p role="status">{checkinMessage}</p>}
          {tasks.length > 0 && <section className="miray-home-tasks" aria-labelledby="miray-home-tasks-title"><h2 id="miray-home-tasks-title">지금 확인할 것</h2>
          {tasks.map((task,index) => <button className={`miray-card miray-task${index === 0 ? " miray-primary" : ""}`} key={task.id} onClick={() => {
            if (!publicFrameLive() || editing) return;
            if (["checkin", "skin_change"].includes(task.kind)) {
              if (!sensitiveConsentVerified) {navigate("my"); return;}
              consumeFrame();setCheckinMessage(""); setSkinStateKind("checkin"); setEditing("skin-state");
              return;
            }
            navigate(task.route);
          }}>{task.title}<span aria-hidden="true"> →</span></button>)}</section>}
          {(kbEnabled || closedLoopEntryReviewStore || closedLoopReviewStore || closedLoopJourneyReviewFactory || originalLoopFactory) && sensitiveConsentVerified && historyStorageConsented && <section className="miray-card miray-home-check">
            <h2>루틴 점검</h2>{kbEnabled&&<button disabled={!portfolioSettled} onClick={startKbReview}>현재 상태로 루틴 점검</button>}<p>현재 상태에 맞춰 제품 사용 정보를 점검해요.</p>
            {!kbEnabled && (closedLoopEntryReviewStore || closedLoopJourneyReviewFactory || originalLoopFactory) && <button className={tasks.length === 0 ? "miray-primary" : ""} disabled={originalLoopFactory?!portfolioSettled:Boolean(portfolioStore) && !portfolioSettled} onClick={()=>{if (!publicFrameLive() || (portfolioStore && !portfolioSettled)) return; consumeFrame();setExpectedDecisionRef(undefined);setExpectedEntryPortfolioRevision(portfolioStore?revision.current:undefined);if(originalLoopFactory)openOriginal("entry");else if(closedLoopJourneyReviewFactory)openJourney("entry");else setEditing("loop-entry");}}>현재 상태로 루틴 점검</button>}
            {(closedLoopReviewStore || closedLoopJourneyReviewFactory || originalLoopFactory) && <button className="miray-home-followup" disabled={Boolean(originalLoopFactory) && !portfolioSettled} onClick={()=>{if (!publicFrameLive() || (originalLoopFactory && !portfolioSettled)) return; consumeFrame();setExpectedDecisionRef(undefined);if(originalLoopFactory)openOriginal("episode");else if(closedLoopJourneyReviewFactory)openJourney("episode");else setEditing("closed-loop");}}>지난 점검 이후 실제 사용·현재 상태 확인</button>}
          </section>}
          <div className="miray-home-summary">
            <section className="miray-card"><h2>사용 중 화장품</h2><p>{products.length ? `${products.length}개를 등록했어요.` : "아직 등록한 제품이 없어요."}</p><button onClick={() => navigate("cosmetics")}>내 화장품 보기<span aria-hidden="true"> →</span></button></section>
            <section className="miray-card"><h2>현재 루틴</h2><p>내가 정한 사용 시간과 빈도를 확인해요.</p><button className={tasks.length === 0 && (!(closedLoopEntryReviewStore || closedLoopJourneyReviewFactory || originalLoopFactory) || !sensitiveConsentVerified || !historyStorageConsented) ? "miray-primary" : ""} onClick={() => navigate("routine")}>루틴 보기<span aria-hidden="true"> →</span></button></section>
          </div>
        </div>}
        {tab === "cosmetics" && <div className={`miray-cosmetics${products.length ? "" : " miray-cosmetics-empty"}`}>
          <h1 ref={cosmeticsHeading} tabIndex={-1}>내 화장품</h1>
          {memberCareUnavailable === "product" && <section className="miray-card" role="status">
            <h2>제품 검색 연결을 준비 중이에요</h2>
            <p>확인된 제품 검색 연결 전에는 예시 제품을 내 화장품으로 등록하지 않아요.</p>
          </section>}
          {!products.length && <p>아직 등록된 화장품이 없어요. 현재 쓰는 제품부터 추가해보세요.</p>}
          {products.length > 0 && <div className="ppopy-product-count">등록한 화장품 <strong>{products.length}</strong></div>}
          <ul className="ppopy-owned-list" aria-label="보유 화장품">{products.map(product=><li key={product.id}><h2>{productPresentation(product).name}</h2></li>)}</ul>
          <button type="button" className="miray-primary" onClick={()=>{
            if(!portfolioActionLive()||tab!=="cosmetics")return;
            if(!products.length){
              if(!memberCareClient){setMemberCareUnavailable("product");return;}
              consumeFrame();setEditorStarted(true);setEditing("registration");return;
            }
            consumePortfolioAction();setManagingProducts(!managingProducts);setManagedProductId(products[0]?.id??"");setPendingProductRemoval(null);
          }}>{managingProducts?"관리 마치기":products.length?"화장품 관리":"화장품 추가"}</button>
          {managingProducts&&<section className="ppopy-owned-manager" aria-label="화장품 관리">
          {products.length>0&&<label>관리할 화장품<select value={managedProductId} onChange={event=>{if(!portfolioActionLive())return;setManagedProductId(event.target.value);setPendingProductRemoval(null);}}>{products.map(product=><option key={product.id} value={product.id}>{productPresentation(product).name}</option>)}</select></label>}
          <button type="button" onClick={()=>{
            if(!publicFrameLive()||editing)return;
            if(!memberCareClient){setMemberCareUnavailable("product");return;}
            consumeFrame();setMemberCareUnavailable(null);setEditorStarted(true);setEditing("registration");
          }}>새 화장품 추가</button>
          {products.filter(product=>product.id===managedProductId).map(product => <section className="miray-card miray-cosmetics-product" key={product.id}>
            {replenishmentEnabled && ["running_low","empty"].includes(depletionStatuses[product.id]) && <button type="button" aria-label={`${productPresentation(product).name} 재구매 전 확인`} onClick={()=>{
              if(!portfolioActionLive() || tab!=="cosmetics" || replenishmentOwner.current!==replenishmentBinding || currentFingerprint.current!==portfolioFingerprint(portfolio))return;
              consumeFrame();setReplenishmentSelection({binding:replenishmentBinding,id:product.id,fingerprint:currentFingerprint.current});setEditing("replenishment");
            }}>다시 구매하기 전 확인</button>}
            <details ref={element=>{if(element)frequencyEditDetails.current.set(product.id,element);else frequencyEditDetails.current.delete(product.id);}} className="miray-cosmetics-details"><summary aria-label="사용 정보 보기" title="제품을 눌러 사용 빈도 보기"><h2>{productPresentation(product).name}</h2></summary><p>{productPresentation(product).name} 최근 7일 사용 빈도</p><ProductFrequencyEditor label={`${productPresentation(product).name} 최근 7일 사용 빈도`} value={frequencies[product.id] ?? ""} onChange={value => {
              if (!portfolioActionLive() || tab !== "cosmetics") return;
              setFrequencies(current=>({...current,[product.id]:value}));
            }}/><ProductEvidenceLink product={product}/>{replenishmentEnabled ? <><label>{productPresentation(product).name} 사용 상태<select aria-label={`${productPresentation(product).name} 사용 상태`} value={depletionStatuses[product.id] ?? "not_tracking"} onChange={event => {
              if (!portfolioActionLive() || tab !== "cosmetics") return;
              const value=event.target.value as MirayProductDepletionStatus; setDepletionStatuses(current=>({...current,[product.id]:value}));
            }}><option value="not_tracking">기록하지 않음</option><option value="enough">여유 있어요</option><option value="running_low">거의 다 썼어요</option><option value="empty">소진됐어요</option></select></label><p>사용자가 직접 기록하는 참고 정보예요. 소진 시점, 재구매, 구매 완료를 자동으로 판단하지 않아요.</p></> : null}</details>
            {pendingProductRemoval === product.id ? <div className="miray-cosmetics-remove-confirm" role="status">
              <p>이 제품을 내 화장품에서 삭제할까요?</p>
              <button type="button" onClick={() => removeProduct(product.id)}>삭제하기</button>
              <button ref={productRemovalCancel} type="button" onClick={() => {if (!portfolioActionLive() || tab !== "cosmetics") return; requestProductRemovalFocus("trigger", product.id); consumePortfolioAction(); setPendingProductRemoval(null);}}>취소</button>
            </div> : <button ref={element => {if (element) productRemovalTriggers.current.set(product.id,element); else productRemovalTriggers.current.delete(product.id);}} className="miray-cosmetics-remove" type="button" onClick={() => {if (!portfolioActionLive() || tab !== "cosmetics") return; requestProductRemovalFocus("cancel"); consumePortfolioAction(); setPendingProductRemoval(product.id);}} aria-label={`${productPresentation(product).name} 삭제`}>삭제</button>}
          </section>)}</section>}
        </div>}
        {tab === "routine" && <div className={`miray-routine${products.length ? "" : " miray-routine-empty"}`}>
          <h1>내 루틴</h1>{!products.length && <p>보유한 화장품에서 현재 쓰는 제품을 골라보세요.</p>}
          {!products.length ? <button className="miray-primary" onClick={() => navigate("cosmetics")}>먼저 화장품 추가</button> : <>
            <RoutinePeriodTabs period={routinePeriod} change={p=>{setRoutinePeriod(p);setChoosingRoutine(false);}}>
            {(() => {
              const period = routinePeriod;
              const ordered = portfolio.periods[period].map(id => products.find(product => product.id === id)).filter((product): product is ProductCandidate => Boolean(product));
              const label = period === "am" ? "아침" : "저녁";
              const groups = groupRoutineProducts(ordered);
              return <section className="miray-card miray-routine-order" key={period}><h2>{label}</h2>
                {groups.map(group => <div className={`miray-routine-group${group.key === "unclassified" ? " miray-routine-group-unclassified" : ""}`} key={group.key}>
                  {group.key !== "unclassified" && <h3>{group.label}</h3>}
                  <RoutineOrderList products={group.products} showVisibleHelp={false} label={groups.length === 1 ? label : `${label} ${group.label}`} onReorder={ids => {
                    if (!portfolioActionLive() || tab !== "routine" || currentFingerprint.current !== portfolioFingerprint(portfolio)) return;
                    const snapshot=[...ids]; setRoutineOrder(current => ({...current,[period]:reorderRoutineSubset(portfolio.periods[period],snapshot)}));
                  }}/>
                </div>)}
                {!ordered.length && <p>아직 정한 제품이 없어요.</p>}
              </section>;
            })()}
            </RoutinePeriodTabs>
            {!choosingRoutine?<button type="button" onClick={()=>{
              if(!portfolioActionLive()||tab!=="routine")return;
              consumePortfolioAction();setRoutineSelection([...portfolio.periods[routinePeriod]]);setChoosingRoutine(true);
            }}>{routinePeriod==="am"?"아침":"저녁"} 루틴 수정</button>:<section className="ppopy-routine-picker" aria-label="보유 화장품에서 루틴 선택">
              <h2>{routinePeriod==="am"?"아침":"저녁"}에 쓰는 화장품</h2>
              {products.map(product=><label key={product.id}><input type="checkbox" checked={routineSelection.includes(product.id)} onChange={e=>{
                if(!portfolioActionLive()||tab!=="routine")return;
                const checked=e.target.checked;setRoutineSelection(ids=>checked?[...ids,product.id]:ids.filter(id=>id!==product.id));
              }}/>{productPresentation(product).name}</label>)}
              <button type="button" className="miray-primary" onClick={()=>{
                if(!portfolioActionLive()||tab!=="routine"||routineSelection.some(id=>!products.some(p=>p.id===id)))return;
                consumePortfolioAction();const selected=new Set(routineSelection),period=routinePeriod;
                setPeriods(current=>Object.fromEntries(products.map(product=>{
                  const am=period==="am"?selected.has(product.id):current[product.id]==="am"||current[product.id]==="both";
                  const pm=period==="pm"?selected.has(product.id):current[product.id]==="pm"||current[product.id]==="both";
                  return [product.id,am&&pm?"both":am?"am":pm?"pm":""];
                })));
                setRoutineOrder(current=>({...current,[period]:[...portfolio.periods[period].filter(id=>selected.has(id)),...routineSelection.filter(id=>!portfolio.periods[period].includes(id))]}));
                setFrequencies(current=>Object.fromEntries(Object.entries(current).map(([id,value])=>[id,selected.has(id)&&value==="0"?"unknown":value])));setChoosingRoutine(false);
              }}>선택한 루틴 적용</button>
              <button type="button" onClick={()=>{if(!portfolioActionLive())return;consumePortfolioAction();setChoosingRoutine(false);}}>취소</button>
            </section>}
            {!publicLoopFactory && <button className="miray-primary" disabled={kbEnabled?!portfolioSettled:!routineReady} onClick={() => {
              if (!publicFrameLive() || editing) return;
              if(kbEnabled){startKbReview();return;}
              if ((skinStateEnabled || memberCareClient?.analyze) && !sensitiveConsentVerified) {navigate("my");return;}
              if (!skinStateEnabled && !memberCareClient?.analyze) {setMemberCareUnavailable("analysis");return;}
              consumeFrame();setMemberCareUnavailable(null);
              setEditorStarted(true);setSkinStateKind("baseline");setEditing(skinStateEnabled ? "skin-state" : "analysis");
            }}>{routineReady ? (!sensitiveConsentVerified && (skinStateEnabled || memberCareClient?.analyze) ? "민감정보 동의 후 상태 확인" : "현재 상태 확인으로 계속") : "루틴에 사용하는 제품을 추가해 주세요"}</button>}
            {!publicLoopFactory && memberCareUnavailable === "analysis" && <section className="miray-card" role="status">
              <h2>루틴 점검 연결을 준비 중이에요</h2>
              <p>검증된 점검 엔진 연결 전에는 임시 결과를 개인화 결과로 표시하지 않아요. 등록한 화장품과 사용 시간은 계속 확인할 수 있어요.</p>
            </section>}
          </>}
          {publicLoopFactory && <button className="miray-primary" disabled={!portfolioSettled} onClick={startPublicRoutineReview}>
            {!sensitiveConsentVerified || !historyStorageConsented ? "필수 동의 확인" : !products.length ? "보유 제품 없이 루틴 점검" : "현재 상태로 루틴 점검"}
          </button>}
        </div>}
      </main>}
      <nav className="miray-tabs" aria-label="주요 화면">{config.tabs.map(item => <button key={item.id} aria-current={tab === item.id ? "page" : undefined} onClick={() => navigate(item.id as MirayTab)}><PpopyTabIcon tab={item.id as MirayTab}/><span>{item.label}</span></button>)}</nav>
    </>}
    <main className="miray-main" hidden={Boolean(editing) || tab !== "explore"}>{mountedPublicBinding === publicBinding && <MirayExplore deviceProductLookup={localFirstReads} deferSavedListRead={localFirstReads} active={!editing && tab === "explore"} search={exploreSearch} savedCandidateStore={savedCandidateStore} comparisonReader={candidateComparisonReader} registeredProductIds={products.map(product => product.id)} onOpenRoutine={()=>{
      if (!publicFrameLive() || editing || tab !== "explore") return;
      consumeFrame(); setTab("routine");
    }} onRegisterProduct={(product,usage) => {
      if (!publicFrameLive() || editing || tab !== "explore" || products.some(existing=>existing.id===product.id)) return;
      const snapshot = structuredClone(product);
      consumeFrame(); setEditorStarted(false);
      setProducts(current => current.some(existing => existing.id === snapshot.id) ? current : [...current, snapshot]);
      if(usage==="not_started")setFrequencies(current=>({...current,[snapshot.id]:"0"}));
      setPendingProductRemoval(null); setTab("cosmetics");
    }} />}</main>
  </div>;
}
