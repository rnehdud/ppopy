import {useEffect, useLayoutEffect, useMemo, useRef, useState} from "react";
import type {MirayExploreCandidate as Candidate, MirayExploreSearch} from "./mirayExploreSearch";
import type {MiraySavedCandidate, MiraySavedCandidatesStore} from "./miraySavedCandidates";
import { MiraySavedCandidatesRevisionConflict, parseMiraySavedCandidatesEnvelope, isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl } from "./miraySavedCandidates";
import type {ProductCandidate} from "./productCatalog";
import MirayCandidateComparison from "./MirayCandidateComparison";
import type {CandidateComparisonReader} from "./candidateComparisonModel";
import "./mirayExplore.css";
import {useProductTransferConfirmation} from "./productTransferConfirmation";
import {productNamePresentation} from "./productPresentation";

type EvidenceReference = {sourceUrl: string; provenanceHash: string};

function evidenceReference(candidate: Pick<Candidate, "sourceUrl" | "provenanceHash">): EvidenceReference | null {
  const sourceUrl = candidate.sourceUrl ?? null;
  const provenanceHash = candidate.provenanceHash ?? null;
  if (sourceUrl === null || provenanceHash === null) return null;
  try { validateMirayCandidateSourceUrl(sourceUrl); }
  catch { return null; }
  return isMirayCandidateProvenanceHash(provenanceHash) ? {sourceUrl, provenanceHash} : null;
}

function stored(candidate: Candidate): MiraySavedCandidate {
  if (candidate.evidenceStatus === "fixture_only") throw new Error("미리보기 후보는 계정에 저장하지 않아요.");
  const sourceUrl = candidate.sourceUrl ?? null;
  const provenanceHash = candidate.provenanceHash ?? null;
  if ((sourceUrl === null) !== (provenanceHash === null) || (candidate.source === "web" && (sourceUrl === null || provenanceHash === null))) {
    throw new Error("후보 출처를 확인하지 못해 저장하지 않았어요.");
  }
  if (sourceUrl !== null && evidenceReference(candidate) === null) {
    throw new Error("후보 출처를 확인하지 못해 저장하지 않았어요.");
  }
  return {
    id:candidate.id, title:candidate.registrationProduct && productNamePresentation(candidate.registrationProduct.name).originalName
      ? candidate.registrationProduct.name : candidate.title, detail:candidate.detail, source:candidate.source,
    evidence_status:candidate.evidenceStatus, source_url:sourceUrl, provenance_hash:provenanceHash,
  };
}

// Compare validated field values, not transport JSON property order.
function candidateSignature(items:readonly MiraySavedCandidate[]):string {
  return JSON.stringify(items.map(c=>[c.id,c.title,c.detail,c.source,c.evidence_status,c.source_url,c.provenance_hash]));
}

function restored(candidate: MiraySavedCandidate): Candidate {
  return {
    id:candidate.id, title:candidate.title, detail:candidate.detail, source:candidate.source,
    evidenceStatus:candidate.evidence_status, sourceUrl:candidate.source_url ?? undefined,
    provenanceHash:candidate.provenance_hash ?? undefined,
  };
}

function evidenceLabel(candidate: Candidate): string | null {
  if (candidate.evidenceStatus === "fixture_only") return "미리보기 후보 · 저장 불가";
  return candidate.source === "web" ? "인터넷에서 찾은 제품" : null;
}

function EvidenceLink({candidate}: {candidate: Candidate}) {
  const reference = evidenceReference(candidate);
  if (!reference) return null;
  return <p className="miray-evidence"><a href={reference.sourceUrl} target="_blank" rel="noreferrer">제품 출처 보기</a></p>;
}

function ingredientDisclosure(candidate: Candidate): {text:string; date:string} | null {
  const product = candidate.registrationProduct;
  const disclosure = product?.ingredientDisclosure;
  if (!product || !disclosure || !["owner_verified", "automation_verified"].includes(product.evidenceStatus)
      || !evidenceReference(product) || productNamePresentation(product.name).originalName
      || typeof disclosure.text !== "string" || !disclosure.text.trim() || disclosure.text.length > 24000
      || typeof disclosure.observedAt !== "string" || !/^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(disclosure.observedAt)
      || !Number.isFinite(Date.parse(disclosure.observedAt))) return null;
  return {text:disclosure.text, date:disclosure.observedAt.slice(0, 10)};
}

function IngredientSection({candidate}: {candidate: Candidate}) {
  const disclosure = ingredientDisclosure(candidate);
  return <section className="miray-product-ingredients" aria-label="전성분"><h3>전성분</h3>
    {disclosure ? <><p>{disclosure.text.length > 120 ? `${disclosure.text.slice(0, 120)}…` : disclosure.text}</p>
      {disclosure.text.length > 120 && <details><summary>전성분 전체 보기</summary><p>{disclosure.text}</p></details>}</> : <><p>전성분 정보를 아직 확인하지 못했어요.</p><p>제품 용기의 전성분 표시를 확인해 주세요.</p></>}
    <EvidenceLink candidate={candidate}/>
  </section>;
}

/**
 * Search display data never gets to invent portfolio provenance. A malformed
 * pair is omitted before a catalog result can enter the member's cosmetics
 * list; a web result with no verifiable pair is not registrable at all.
 */
function registrationCandidate(candidate: Candidate | null): ProductCandidate | null {
  const product = candidate?.registrationProduct;
  if (!product || product.evidenceStatus === "fixture_only") return null;
  const reference = evidenceReference(product);
  if (product.matchSource === "public_web" && !reference) return null;
  return {
    ...product,
    sourceUrl:reference?.sourceUrl,
    provenanceHash:reference?.provenanceHash,
  };
}

/** Search results become account data only through this explicit, evidence-preserving save. */
export default function MirayExplore({search, savedCandidateStore, comparisonReader, onRegisterProduct, onOpenRoutine, registeredProductIds = [], active = true}: {
  /** A hidden tab retires searches, saved reads/writes and issued UI actions. */
  active?: boolean;
  search?: MirayExploreSearch;
  savedCandidateStore?: MiraySavedCandidatesStore;
  /** Explicit local TEST composition; does not enable a deployed comparison route. */
  comparisonReader?: CandidateComparisonReader;
  /** A fresh, structured catalog result may enter a member portfolio only after confirmation. */
  onRegisterProduct?: (product: ProductCandidate, usage?: "not_started") => void;
  /** Opens the member's existing routine; it deliberately does not evaluate the selected candidate. */
  onOpenRoutine?: () => void;
  registeredProductIds?: readonly string[];
}) {
  type Binding = {live:boolean; search:MirayExploreSearch|undefined; store:MiraySavedCandidatesStore|undefined; active:boolean; revision:number; searchController:AbortController|null; saveAttempt:object|null};
  const binding = useMemo<Binding>(() => ({live:false,search,store:savedCandidateStore,active,revision:0,searchController:null,saveAttempt:null}), [search,savedCandidateStore,active]);
  const transfer=useProductTransferConfirmation(binding);
  const initial = (binding:Binding) => ({binding,query:"",results:[] as Candidate[],saved:[] as MiraySavedCandidate[],selected:null as Candidate|null,busy:false,message:"",savedReady:!binding.store,savedLoadFailed:false,
    savedMessage:binding.store ? "저장한 후보를 불러오는 중이에요." : "후보 저장 연결을 준비 중이에요. 이 화면에서 임시로 저장하지 않아요.",savedReload:0,savingId:null as string|null,savedRevisionConflict:false,comparisonIds:[] as string[],confirmRegistration:false,notStarted:false});
  const [state,setState] = useState(() => initial(binding));
  // Mask the retired account's view during the replacement render itself.
  const view = state.binding === binding ? state : initial(binding);
  const {query,results,saved,selected,busy,message,savedReady,savedLoadFailed,savedMessage,savedReload,savingId,savedRevisionConflict,comparisonIds,confirmRegistration,notStarted} = view;
  const owner = useRef<Binding|null>(null);
  const registeredSignature = JSON.stringify(registeredProductIds);
  const frame = useMemo(() => ({view,onRegisterProduct,onOpenRoutine,registeredSignature}), [view,onRegisterProduct,onOpenRoutine,registeredSignature]);
  const currentFrame = useRef<typeof frame|null>(null);
  const live = () => active && binding.live && owner.current === binding;
  const frameLive = () => live() && currentFrame.current === frame;
  const invalidateFrame = () => {if(currentFrame.current === frame) currentFrame.current = null;};
  const update = (patch:Partial<typeof state>|((previous:typeof state)=>Partial<typeof state>)) => {
    if(!live()) return;
    setState(previous => {const current=previous.binding===binding?previous:initial(binding);return {...current,...(typeof patch==="function"?patch(current):patch),binding};});
  };
  useLayoutEffect(() => {
    binding.live = true; owner.current = binding; setState(initial(binding));
    return () => {binding.live=false;binding.searchController?.abort();binding.searchController=null;binding.saveAttempt=null;if(owner.current===binding)owner.current=null;};
    // This exact search/store/tab binding owns the account view and pending work.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [binding]);
  useLayoutEffect(() => {currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);

  useEffect(() => {
    if(!live() || !savedCandidateStore) return;
    let reading=true;
    binding.revision=0;
    update({saved:[],savedReady:false,savedLoadFailed:false,savedMessage:"저장한 후보를 불러오는 중이에요.",comparisonIds:[]});
    const read = async () => {
      try {
        const raw = await savedCandidateStore.read();
        if(!reading || !live()) return;
        const envelope = structuredClone(parseMiraySavedCandidatesEnvelope(raw));
        binding.revision=envelope.revision;
        update({saved:envelope.candidates.candidates,savedReady:true,savedRevisionConflict:false,savedMessage:"계정에 저장한 후보를 불러왔어요."});
      } catch {
        if(reading && live()) update({savedLoadFailed:true,savedMessage:"저장한 후보를 불러오지 못했어요. 연결을 확인해 주세요."});
      }
    };
    void read();return()=>{reading=false;};
    // Async completions are owned by this binding and this explicit reload.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [binding,savedReload]);

  const save = async (next:MiraySavedCandidate[], id:string, success:string) => {
    if(!frameLive() || !savedCandidateStore || binding.saveAttempt || !savedReady || savedRevisionConflict) return;
    let fixed:ReturnType<typeof parseMiraySavedCandidatesEnvelope>;
    try {fixed=structuredClone(parseMiraySavedCandidatesEnvelope({revision:binding.revision,candidates:{version:"1.0.0",candidates:next}}));}
    catch {update({savedMessage:"후보 출처를 확인하지 못해 저장하지 않았어요."});return;}
    const attempt={};binding.saveAttempt=attempt;invalidateFrame();update({savingId:id});
    try {
      const raw=await savedCandidateStore.save(structuredClone(fixed.candidates),fixed.revision);
      if(!live() || binding.saveAttempt!==attempt) return;
      const envelope=structuredClone(parseMiraySavedCandidatesEnvelope(raw));
      if(envelope.revision<=fixed.revision || candidateSignature(envelope.candidates.candidates)!==candidateSignature(fixed.candidates.candidates)) throw new Error("Unconfirmed candidate save");
      binding.revision=envelope.revision;
      const ids=new Set(envelope.candidates.candidates.map(c=>c.id));
      update(previous=>({saved:envelope.candidates.candidates,comparisonIds:previous.comparisonIds.filter(id=>ids.has(id)),savedMessage:success}));
    } catch(error) {
      if(live() && binding.saveAttempt===attempt) update({savedRevisionConflict:true,savedMessage:error instanceof MiraySavedCandidatesRevisionConflict ? error.message : "후보 저장을 확인하지 못했어요. 반영됐을 수 있으니 저장한 후보를 다시 불러와 주세요."});
    } finally {
      if(binding.saveAttempt===attempt){binding.saveAttempt=null;update({savingId:null});}
    }
  };
  const saveSelected = () => {
    if(!frameLive() || !selected || saved.some(item=>item.id===selected.id)) return;
    let candidate:MiraySavedCandidate;
    try {candidate=stored(selected);} catch(error){update({savedMessage:error instanceof Error ? error.message : "후보를 저장하지 못했어요."});return;}
    return save([...saved,candidate],candidate.id,"후보를 계정에 저장했어요.");
  };
  const remove = (id:string) => {
    if(!frameLive() || !saved.some(item=>item.id===id)) return;
    return save(saved.filter(item=>item.id!==id),id,"후보 저장을 취소했어요.");
  };
  const choose = (candidate:Candidate) => {if(!frameLive())return;invalidateFrame();update({selected:structuredClone(candidate),confirmRegistration:false,notStarted:false});};
  const reload = () => {if(!frameLive() || binding.saveAttempt || !savedRevisionConflict && !savedLoadFailed)return;invalidateFrame();update({selected:null,confirmRegistration:false,notStarted:false,savedReady:false,saved:[],comparisonIds:[],savedReload:savedReload+1});};
  const cancelSearch = () => {if(!frameLive() || !binding.searchController)return;invalidateFrame();binding.searchController.abort();binding.searchController=null;update({busy:false,message:"이번 검색 화면을 멈췄어요. 새 제품명으로 다시 검색할 수 있어요."});};
  const changeQuery = (value:string) => {if(!frameLive())return;invalidateFrame();binding.searchController?.abort();binding.searchController=null;update({query:value,busy:false,results:[],selected:null,confirmRegistration:false,notStarted:false,message:""});};
  const submit = async () => {
    if(!frameLive() || !query.trim() || binding.searchController)return;
    if(!search){update({message:"제품 탐색 연결을 준비 중이에요. 확인된 검색 연결 전에는 예시 후보를 표시하지 않아요."});return;}
    const controller=new AbortController();binding.searchController=controller;invalidateFrame();update({busy:true,message:"",selected:null,confirmRegistration:false,notStarted:false,results:[]});
    const current=()=>live() && !controller.signal.aborted && binding.searchController===controller;
    try {
      const found=await search(query.trim(),stage=>{if(current())update({message:stage==="catalog" ? "카탈로그에서 제품명을 확인하고 있어요." : "카탈로그에 없어 인터넷 후보를 확인하고 있어요. 결과를 확인한 뒤 직접 선택해 주세요."});},{signal:controller.signal,confirmExternalTransfer:transfer.confirm});
      if(!current())return;
      const fixed=structuredClone(found);
      update({results:fixed,message:fixed.length ? `후보 ${fixed.length}개를 찾았어요. 제품명과 용량을 확인해 주세요.` : "제품을 찾지 못했어요. 브랜드와 제품명을 다시 확인해 주세요."});
    }catch{if(current())update({message:"검색을 완료하지 못했어요. 잠시 후 다시 검색해 주세요."});}
    finally{if(binding.searchController===controller){binding.searchController=null;update({busy:false});}}
  };
  const selectedIsSaved = Boolean(selected && saved.some(item => item.id === selected.id));
  const selectedIsFixture = selected?.evidenceStatus === "fixture_only";
  const registrationProduct = registrationCandidate(selected);
  const selectedIsRegistered = Boolean(registrationProduct && registeredProductIds.includes(registrationProduct.id));
  const canRegisterSelected = Boolean(onRegisterProduct && registrationProduct);
  const comparison = comparisonIds.flatMap(id => {
    const item = saved.find(candidate => candidate.id === id);
    return item ? [restored(item)] : [];
  });
  const toggleComparison = (id:string) => {
    if(!frameLive() || !savedReady || !saved.some(item=>item.id===id && evidenceReference(restored(item))))return;
    invalidateFrame();update({comparisonIds:comparisonIds.includes(id) ? comparisonIds.filter(candidateId=>candidateId!==id) : comparisonIds.length<2 ? [...comparisonIds,id] : comparisonIds});
  };
  const register = () => {
    if(!frameLive() || !canRegisterSelected || !registrationProduct || selectedIsRegistered)return;
    invalidateFrame();
    if(!confirmRegistration){update({confirmRegistration:true});return;}
    update({confirmRegistration:false,notStarted:false});
    if(notStarted)onRegisterProduct?.(structuredClone(registrationProduct),"not_started");
    else onRegisterProduct?.(structuredClone(registrationProduct));
  };
  const cancelRegistration = () => {if(!frameLive())return;invalidateFrame();update({confirmRegistration:false,notStarted:false});};
  const openRoutine = () => {if(!frameLive() || !selected || !onOpenRoutine)return;invalidateFrame();update({});onOpenRoutine();};
  const saveBlocked = selectedIsSaved || Boolean(savingId) || savedRevisionConflict || selectedIsFixture || !savedCandidateStore || !savedReady;
  const primaryAction = canRegisterSelected && !selectedIsRegistered ? "register"
    : savedRevisionConflict ? "reload-conflict" : savedLoadFailed ? "reload-failed"
    : selected && !saveBlocked ? "save" : comparison.length === 2 && comparisonReader ? "compare" : "search";
  if(!active)return <><h1>탐색</h1><p>제품을 검색하려면 탐색 화면을 열어 주세요.</p></>;
  return <div className="miray-explore">
    {transfer.content}
    <h1>탐색</h1><p>궁금한 제품을 찾아보고, 구매 전에 확인할 후보로 저장해요.</p>
    <form className="miray-explore-search" onSubmit={event=>{event.preventDefault();void submit();}}><label>제품명 또는 브랜드<input maxLength={200} value={query} onChange={event=>changeQuery(event.target.value)}/></label><div className="miray-explore-actions"><button className={primaryAction === "search" ? "miray-primary" : undefined} type="submit" disabled={busy || !query.trim()}>{busy ? "찾는 중…" : "검색"}</button>{busy && <button type="button" onClick={cancelSearch}>검색 그만두기</button>}</div></form>
    <p className="miray-explore-message" role="status" aria-live="polite">{message}</p>
    {results.map(p => <button className="miray-card miray-explore-result" key={p.id} onClick={() => choose(p)}><span>{p.title}</span>{(p.detail || evidenceLabel(p)) && <small>{[p.detail, evidenceLabel(p)].filter(Boolean).join(" · ")}</small>}{p.registrationProduct && productNamePresentation(p.registrationProduct.name).originalName && <small>기획 구성 포함</small>}</button>)}
    {selected && <section className="miray-card miray-explore-detail" aria-label="제품 상세">
      <h2>{selected.title}</h2>
      {selected.detail && <p>{selected.detail}</p>}
      {evidenceLabel(selected) && <p>{evidenceLabel(selected)}</p>}
      {selected.registrationProduct && productNamePresentation(selected.registrationProduct.name).originalName && <div className="miray-product-original"><p>이 판매명에는 기획 구성이 포함되어 있어요. 실제 사용하는 제품과 용량을 확인해 주세요.</p><details><summary>원래 판매명 보기</summary><p>{selected.registrationProduct.name}</p></details></div>}
      <IngredientSection candidate={selected}/>
      {canRegisterSelected && (selectedIsRegistered ? <button disabled>내 화장품에 추가됨</button> : confirmRegistration ? <div className="miray-explore-registration" role="status"><p>이 제품을 내 화장품에 추가할까요? 제품명과 용량을 한 번 더 확인해 주세요.</p><label className="miray-explore-checkbox"><input type="checkbox" checked={notStarted} onChange={event=>{if(!frameLive() || !confirmRegistration)return;invalidateFrame();update({notStarted:event.target.checked});}}/>아직 사용하지 않는 제품이에요</label><p>선택하면 사용 빈도를 0일로 등록해요. 제품 등록은 실제 사용 시작이나 구매 완료 기록과 별도예요.</p><button className={primaryAction === "register" ? "miray-primary" : undefined} onClick={register}>내 화장품에 추가</button><button onClick={cancelRegistration}>취소</button></div> : <button className={primaryAction === "register" ? "miray-primary" : undefined} onClick={register}>내 화장품에 추가</button>)}
      <button className={primaryAction === "save" ? "miray-primary" : undefined} disabled={saveBlocked} onClick={() => void saveSelected()}>{selectedIsSaved ? "저장됨" : selectedIsFixture ? "미리보기 후보는 저장하지 않아요" : !savedCandidateStore ? "후보 저장 연결 필요" : savingId === selected.id ? "저장 중…" : "후보로 저장"}</button>
      {onOpenRoutine && <button onClick={openRoutine}>현재 루틴 보기</button>}
    </section>}
    <h2 className="miray-explore-saved-heading">저장한 후보</h2><p>저장은 추천 확정이나 내 화장품 등록이 아니에요. 후보 두 개를 선택하면 출처를 나란히 확인할 수 있어요.</p>
    <p className={`miray-explore-message${savedReady && !savedLoadFailed && savedMessage === "계정에 저장한 후보를 불러왔어요." ? " miray-explore-loaded-quiet" : ""}`} role={savedLoadFailed ? "alert" : "status"}>{savedMessage}</p>
    {savedRevisionConflict && <button className={primaryAction === "reload-conflict" ? "miray-primary" : undefined} disabled={Boolean(savingId)} onClick={reload}>다른 기기의 후보 다시 불러오기</button>}
    {savedLoadFailed && <button className={primaryAction === "reload-failed" ? "miray-primary" : undefined} onClick={reload}>후보 다시 불러오기</button>}
    {savedReady && saved.length ? saved.map(item => {
      const candidate = restored(item);
      const addedToComparison = comparisonIds.includes(item.id);
      const comparisonFull = comparisonIds.length >= 2;
      const hasEvidence = evidenceReference(candidate) !== null;
      const comparisonDisabled = !addedToComparison && (!hasEvidence || comparisonFull);
      const comparisonText = addedToComparison ? "비교에서 빼기" : !hasEvidence ? "출처 확인이 필요한 후보는 비교에 추가할 수 없어요" : comparisonFull ? "비교는 두 개까지 선택할 수 있어요" : "비교에 추가";
      return <section className="miray-card miray-explore-saved" key={item.id}><button onClick={() => choose(candidate)}>{item.title}</button>{evidenceLabel(candidate) && <small>{evidenceLabel(candidate)}</small>}<EvidenceLink candidate={candidate}/><button aria-label={`${item.title} ${addedToComparison ? "비교에서 빼기" : "비교에 추가"}`} aria-pressed={addedToComparison} disabled={comparisonDisabled} onClick={() => toggleComparison(item.id)}>{comparisonText}</button><button disabled={Boolean(savingId) || savedRevisionConflict} onClick={() => void remove(item.id)}>{savingId === item.id ? "저장 취소 중…" : "저장 취소"}</button></section>;
    }) : savedReady && !savedLoadFailed ? <p>아직 저장한 후보가 없어요.</p> : null}
    {comparison.length === 2 && <section className="miray-card miray-explore-comparison" aria-label="후보 출처 비교"><h2>후보 둘 비교</h2><p>제품명, 용량과 출처를 나란히 확인해 주세요.</p>{comparison.map(candidate => <article key={candidate.id}><h3>{candidate.title}</h3><p>{candidate.detail}</p>{evidenceLabel(candidate) && <p>{evidenceLabel(candidate)}</p>}<EvidenceLink candidate={candidate}/></article>)}<p>두 후보의 적합성, 우열, 대체 가능성은 현재 정보만으로 판단하지 않아요. 제품 버전과 전성분, 현재 루틴을 함께 확인해 주세요.</p></section>}
    {comparison.length === 2 && comparisonReader && <MirayCandidateComparison candidates={comparison} reader={comparisonReader} active={active} primaryAction={primaryAction === "compare"}/>}
  </div>;
}
