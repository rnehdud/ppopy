import {useLayoutEffect,useMemo,useRef,useState} from "react";
import {canonicalUtcInstant} from "./mirayUtcInstant";
import {resetAppScroll} from "./appScroll";
import policy from "../../skin_engine/config/miray_closed_loop_app_test.json";
import loopUiPolicy from "../../skin_engine/config/miray_closed_loop_ui.json";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import MirayIntakePanel,{type IntakePanelStore} from "./MirayIntakePanel";
import MirayClosedLoopPanel from "./MirayClosedLoopPanel";
import MirayAddedProductConfirmation from "./MirayAddedProductConfirmation";
import CareResult from "./CareResult";
import {assertOriginalLoopAppTest,type OriginalLoopTestConnection} from "./mirayOriginalLoopTest";
import {parseTestLoopStateView,type TestLoopStateView,type TestLoopRegistrationRequest,type TestLoopAddedProductRequest} from "./mirayClosedLoopStateTest";
import {parseTestLoopWorkerView,type TestLoopWorkerView,type TestLoopWorkerContext} from "./mirayClosedLoopWorkerTest";
import {emptyIntake,parseIntakeAnswers,completeIntake,type IntakeAnswers} from "./mirayClosedLoopIntake";
import {stateFirstPlan} from "./mirayClosedLoopStateFirst";
import type {MiraySkinState} from "./miraySkinState";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import {parseFrequencyCorrectionView} from "./mirayClosedLoopFrequency";
import {parseClosedLoopEpisode} from "./mirayClosedLoop";
import {loopTestFailureCode} from "./loopTestFailureCode";
import quotaPolicy from "../../skin_engine/config/app_freemium.json";
import {parseMirayQuotaStatus,type MirayQuotaStatus,type MirayQuotaStatusStore} from "./mirayQuotaStatus";

// These strictly parsed schemas have scalar fields and the original ordered
// discomfort array. JSON object member order is not identity.
const exactFields=(value:object)=>JSON.stringify(Object.entries(value).sort(([a],[b])=>a.localeCompare(b)));
const exactObservation=(value:MiraySkinState)=>exactFields({...value,observed_at:canonicalUtcInstant(value.observed_at)});

type Phase="loading"|"state"|"registration"|"refresh-state"|"refresh-save"|"products"|"intake"|"request"|"result"|"episode"|"hold"|"quota"|"error";
type QuotaHold={reason:"allocation_limit"|"concurrent_pending";feature:MirayQuotaStatus["features"][number]}|{reason:"unavailable"};
export default function MirayOriginalLoopTestPanel({connection,quotaStatusStore,expectedPortfolioRevision,initialPage,onClose,onPortfolioRefresh,onEditFrequency,requestLifetime}:{connection:OriginalLoopTestConnection;quotaStatusStore?:MirayQuotaStatusStore;expectedPortfolioRevision:number;initialPage:"entry"|"episode";onClose():void;onPortfolioRefresh?(minimumRevision:number):boolean;onEditFrequency?(productId:string):boolean;requestLifetime?:{isCurrent():boolean}}){
  const [failureCode,setFailureCode]=useState("L-V-C");
  const [quotaHold,setQuotaHold]=useState<QuotaHold|null>(null);
  const [phase,setPhase]=useState<Phase>("loading"),[state,setState]=useState<TestLoopStateView|null>(null),[worker,setWorker]=useState<TestLoopWorkerView|null>(null),[draft,setDraft]=useState<MiraySkinState|null>(null),[input,setInput]=useState<IntakeAnswers|null>(null),[busy,setBusy]=useState(false);
  const refreshHeading=useRef<HTMLHeadingElement|null>(null);
  const productTrigger=useRef<HTMLButtonElement|null>(null),restoreProductFocus=useRef(false);
  const binding=useMemo(()=>({connection,quotaStatusStore,expectedPortfolioRevision,requestLifetime,live:false,pending:null as AbortController|null,registration:null as TestLoopRegistrationRequest|null,attempt:null as {context:TestLoopWorkerContext;answers:IntakeAnswers}|null}),[connection,quotaStatusStore,expectedPortfolioRevision,requestLifetime]);
  const owner=useRef<typeof binding|null>(null),frame=useMemo(()=>({binding,phase,state,worker,draft,input,busy,quotaHold}),[binding,phase,state,worker,draft,input,busy,quotaHold]),committed=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && connection.isCurrent() && (!requestLifetime || requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && committed.current===frame;
  const consume=()=>{if(committed.current===frame)committed.current=null;};
  const lifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && owner.current===binding && connection.isCurrent() && committed.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding,frame,connection]);
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;binding.registration=null;binding.attempt=null;connection.invalidate();if(owner.current===binding)owner.current=null;consume();};
  const acceptState=(v:unknown)=>{const s=parseTestLoopStateView(v);if(s.context.portfolio_revision!==binding.expectedPortfolioRevision)throw new Error("Visible original portfolio changed");return s;};
  const acceptWorker=(v:unknown,s:TestLoopStateView)=>{const w=parseTestLoopWorkerView(v);if(!s.snapshot || w.context.snapshot_ref!==s.snapshot.snapshot_ref || w.context.portfolio_revision!==s.context.portfolio_revision || (w.context.mode==="next" && w.context.previous_decision_ref!==s.episode?.decision_ref))throw new Error("Original state/worker correlation changed");return w;};
  const run=async(action:(options:MemberStatusReadOptions)=>Promise<void>)=>{
    if(!live() || binding.pending)return;const c=new AbortController();binding.pending=c;consume();setFailureCode("L-V-C");setBusy(true);
    try{assertOriginalLoopAppTest();await action({signal:c.signal,isCurrent:live});c.signal.throwIfAborted();if(!live())return;assertOriginalLoopAppTest();}
    catch(error){if(live() && !c.signal.aborted){setFailureCode(loopTestFailureCode(error));setPhase("error");}}
    finally{if(binding.pending===c){binding.pending=null;if(live())setBusy(false);}}
  };
  const select=async(s:TestLoopStateView,o:MemberStatusReadOptions,page:"entry"|"episode")=>{
    if(!live())return;setState(s);setDraft(null);setInput(null);setWorker(null);setQuotaHold(null);
    if(binding.attempt && !s.snapshot)throw new Error("Submitted original snapshot unavailable");
    if(!s.snapshot){setPhase("state");return;}
    if(page==="episode" && s.episode){setPhase("episode");return;}
    if(stateFirstPlan(s.snapshot.observation).status!=="more_input_required"){setPhase("hold");return;}
    const w=acceptWorker(s.worker_view===undefined?await connection.worker.read(o):s.worker_view,s);if(!live())return;setWorker(w);
    // A fresh account-bound display read can withhold a new intake, but never
    // authorize dispatch. Completed reads and an existing reservation bypass
    // this display gate; only the server can allocate or settle a unit.
    if(w.status==="not_started" && quotaStatusStore){
      let hold:QuotaHold|null=null;
      try{
        const status=parseMirayQuotaStatus(await quotaStatusStore.read(o));
        o.signal?.throwIfAborted();if(!live())return;
        const feature=status.features.find(f=>f.feature==="routine_review")!;
        if(Date.parse(feature.period_ends_at)<=Date.now())throw new Error("Quota display period expired");
        if(feature.remaining===0)hold={reason:"allocation_limit",feature};
        else if(feature.limit===null && feature.pending>=quotaPolicy.workflow.unlimited_review_max_concurrent)hold={reason:"concurrent_pending",feature};
      }catch{
        if(!live() || o.signal?.aborted)return;
        hold={reason:"unavailable"};
      }
      if(hold){setQuotaHold(hold);setPhase("quota");return;}
    }
    if(binding.attempt){
      const original=binding.attempt.context;
      // Completion can change only the mode to original. Never carry answers
      // to a different snapshot, parent, portfolio, account/consent target.
      const receiptContext={...w.context,mode:w.status==="completed"?original.mode:w.context.mode};
      if(exactFields(original)!==exactFields(receiptContext)){binding.attempt=null;throw new Error("Submitted original target changed");}
      if(w.status==="not_started"){
        setInput(structuredClone(binding.attempt.answers));setPhase("request");return;
      }
      binding.attempt=null;
    }
    setPhase(w.status==="completed"?"result":w.status==="not_started"?"intake":"hold");
  };
  const load=(page:"entry"|"episode"="entry")=>run(async o=>{
    const s=acceptState(await (page==="entry" && connection.state.readEntry?connection.state.readEntry(o):connection.state.read(o)));if(!live())return;
    if(binding.registration){
      if(!s.snapshot){setState(s);setDraft(structuredClone(binding.registration.observation));setInput(null);setWorker(null);setPhase("registration");return;}
      if(exactObservation(s.snapshot.observation)!==exactObservation(binding.registration.observation))throw new Error("Original registration receipt differs");
      binding.registration=null;
    }
    await select(s,o,page);
  });
  useLayoutEffect(()=>{binding.live=true;owner.current=binding;setState(null);setWorker(null);setDraft(null);setInput(null);setQuotaHold(null);setPhase("loading");setBusy(false);
    let attached=true;void Promise.resolve().then(()=>{if(attached)void load(initialPage);});// Effect replay retires only this view/request. The workspace owns the
    // selected connection and revokes it on close, consent/member change or unmount.
    return()=>{attached=false;binding.live=false;binding.pending?.abort();binding.pending=null;binding.registration=null;binding.attempt=null;if(owner.current===binding)owner.current=null;consume();};
    // The selected original connection and consent/portfolio lifetime own all IO and drafts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding,initialPage]);
  useLayoutEffect(()=>{committed.current=frame;return()=>{if(committed.current===frame)committed.current=null;};},[frame]);
  useLayoutEffect(()=>{
    if(phase==="refresh-save"){
      resetAppScroll();refreshHeading.current?.focus({preventScroll:true});
    }
  },[phase]);
  useLayoutEffect(()=>{
    if(phase==="hold" && restoreProductFocus.current){restoreProductFocus.current=false;productTrigger.current?.focus({preventScroll:true});productTrigger.current?.scrollIntoView?.({block:"center"});}
  },[phase]);
  const close=()=>{if(!frameLive())return;retire();setDraft(null);setInput(null);onClose();};
  const intakeStore=useMemo<IntakePanelStore<TestLoopWorkerContext>|null>(()=>{
    if(phase!=="intake" || !worker || !state)return null;
    const fixed=structuredClone(worker.context);
    return {read:async o=>{await Promise.resolve();o.signal.throwIfAborted();if(!lifetime.isCurrent() || o.isCurrent?.()!==true)throw new Error("Input frame retired");return {context:fixed,stored:false,answers:emptyIntake()};},save:async()=>{throw new Error("Input review cannot dispatch or save engine work");}};
  },[phase,worker,state,lifetime]);
  if(phase==="state")return <MiraySkinStateCheckin kind="baseline" questionProfile={policy.state_profile as "routine_state_and_safety"} historyStorageConsented={false} completionMode="collect_for_entry" continueToAnalysis={false} requestLifetime={lifetime} onCancel={close} onComplete={v=>{
    if(!frameLive())return;consume();try{const plan=stateFirstPlan(v);setDraft(structuredClone(v));setPhase(plan.status==="more_input_required"?"registration":"hold");}catch{setPhase("error");}
  }}/>;
  if(phase==="refresh-state")return <MiraySkinStateCheckin kind="checkin" questionProfile={policy.state_profile as "routine_state_and_safety"} historyStorageConsented={false} completionMode="collect_for_entry" continueToAnalysis={false} requestLifetime={lifetime} onCancel={close} onComplete={v=>{
    if(!frameLive())return;consume();setDraft(structuredClone(v));setPhase("refresh-save");
  }}/>;
  if(phase==="intake" && intakeStore)return <main className="miray-main"><h1>현재 점검 입력 확인</h1><MirayIntakePanel store={intakeStore} requestLifetime={lifetime} label="현재 점검 입력 확인" savedPurpose="현재 상태의 점검" onClose={close} onSaved={()=>{}} onReviewed={(c,a)=>{
    if(!frameLive() || !worker)return;consume();try{if(exactFields(c)!==exactFields(worker.context))throw new Error("Original input target changed");const value=parseIntakeAnswers(a);if(!completeIntake(value))throw new Error("Complete explicit intake required");setInput(value);setPhase("request");}catch{setInput(null);setPhase("error");}
  }}/></main>;
  if(phase==="episode")return <MirayClosedLoopPanel store={connection.state.episode} active={live()} expectedDecisionRef={state?.episode?.decision_ref} requestLifetime={lifetime} onClose={close} onNextRequested={()=>{if(frameLive())void load();}} onFrequencyClosed={onPortfolioRefresh?value=>{
    if(!frameLive() || binding.pending || !state?.episode)return;
    try{const view=value?parseFrequencyCorrectionView(value):undefined;let floor=binding.expectedPortfolioRevision;
      if(view){
        if(view.decision_ref!==state.episode.decision_ref)throw new Error("Original correction decision changed");
        if(view.portfolio_revision!==floor){
          if(!view.corrections.some(c=>c.before_revision===floor && c.after_revision===floor+1))throw new Error("Original correction revision unconfirmed");
          floor+=1; // A later edit may exist; only a separate canonical read can show it.
        }
      }
      // Closing an uncertain attempt requests only an account read. It does
      // not infer a successful correction or replay any POST.
      if(onPortfolioRefresh(floor)!==true)throw new Error("Original workspace read handoff unconfirmed");
      retire();setDraft(null);setInput(null);setWorker(null);setState(null);
    }catch{setPhase("error");}
  }:undefined}/>;
  return <main className="miray-main"><button onClick={close}>‹ 홈으로</button><h1>현재 상태로 루틴 점검</h1>
    {busy && <p role="status">저장·점검 상태를 확인해요.</p>}
    {phase==="products" && state?.unregistered_products && <MirayAddedProductConfirmation key={JSON.stringify(state.unregistered_products)} products={state.unregistered_products.products} decisionAt={state.unregistered_products.decision_at} allowCurrentUse={state.unregistered_products.confirmation_modes?.includes("current_use")} busy={busy} onEditFrequency={onEditFrequency?productId=>{
      if(!frameLive() || binding.pending || !state.unregistered_products?.products.some(p=>p.id===productId))return;
      // Navigation never copies the draft into the portfolio or confirms use.
      if(onEditFrequency(productId)===true){retire();setDraft(null);setInput(null);setState(null);setWorker(null);}
    }:undefined} onClose={()=>{if(frameLive() && !binding.pending){consume();restoreProductFocus.current=true;setPhase("hold");}}} onConfirm={(productId,frequency,effectiveFrom,mode)=>{
      if(!frameLive() || !state.episode || !connection.state.confirmAddedProduct)return;
      const common={version:state.episode.version,decision_ref:state.episode.decision_ref,request_id:crypto.randomUUID(),product_id:productId,frequency,expected_portfolio_revision:state.context.portfolio_revision};
      if(mode!=="current_use" && effectiveFrom===null)return;
      const request:TestLoopAddedProductRequest=mode==="current_use"?{...common,action_type:"current_use_confirmed",effective_from:null}:{...common,action_type:"product_added",effective_from:effectiveFrom!};
      void run(async o=>{const saved=acceptState(await connection.state.confirmAddedProduct!(request,o));
        const actions=saved.unregistered_products?.confirmations.filter(a=>a.product_id===productId && a.frequency===frequency && (mode==="current_use"?a.action_type==="current_use_confirmed":canonicalUtcInstant(a.effective_from)===canonicalUtcInstant(effectiveFrom!)));
        if(saved.episode?.decision_ref!==request.decision_ref || actions?.length!==1 || saved.unregistered_products?.products.some(p=>p.id===productId))throw new Error("Explicit product addition unconfirmed");
        const next=acceptState(await (connection.state.readEntry?connection.state.readEntry(o):connection.state.read(o)));await select(next,o,"entry");});
    }}/>}
    {phase==="refresh-save" && draft && state?.episode && <section className="miray-card"><h2 ref={refreshHeading} tabIndex={-1}>현재 상태를 변경된 루틴에 연결할까요?</h2><p>방금 답한 피부 고민과 불편감을 현재 등록된 루틴에 연결해 새 상태로 저장해요. 이전 상태와 직접 확인한 실제 사용은 유지해요. 이 단계에서는 점검을 실행하거나 이용 횟수를 사용하지 않아요.</p><button className="miray-primary" disabled={busy} onClick={()=>{
      if(!frameLive() || !state.episode)return;
      const request={version:state.episode.version,decision_ref:state.episode.decision_ref,request_id:crypto.randomUUID(),observation:structuredClone(draft),expected_portfolio_revision:state.context.portfolio_revision,other_changes:loopUiPolicy.other_changes_default as "not_asked"};
      void run(async o=>{const saved=parseClosedLoopEpisode(await connection.state.episode.saveFollowup(request,o));if(saved.decision_ref!==request.decision_ref || !saved.followup || canonicalUtcInstant(saved.followup.observed_at)!==canonicalUtcInstant(request.observation.observed_at) || saved.followup.snapshot_ref===state.snapshot?.snapshot_ref)throw new Error("Refreshed state unconfirmed");
        const next=acceptState(await (connection.state.readEntry?connection.state.readEntry(o):connection.state.read(o)));await select(next,o,"entry");});
    }}>현재 상태 저장·점검 입력 확인</button></section>}
    {phase==="registration" && draft && state && <section className="miray-card"><h2>상태를 저장하고 점검 입력을 확인할까요?</h2><p>직접 답한 피부 고민과 불편감을 현재 루틴에 연결해 저장해요. 점검을 실행하거나 실제 제품 사용을 기록하지 않아요.</p><button className="miray-primary" disabled={busy} onClick={()=>{
      if(!frameLive())return;const request=binding.registration??{request_id:crypto.randomUUID(),expected_portfolio_revision:state.context.portfolio_revision,observation:structuredClone(draft)};binding.registration=request;
      void run(async o=>{const saved=acceptState(await connection.state.register(request,o));if(!saved.snapshot || exactObservation(saved.snapshot.observation)!==exactObservation(request.observation))throw new Error("Original registration unconfirmed");binding.registration=null;await select(saved,o,"entry");});
    }}>상태 저장·점검 입력 확인</button></section>}
    {phase==="request" && worker && input && <section className="miray-card"><h2>확인한 입력으로 루틴을 점검할까요?</h2><p>{binding.attempt?"현재 조회에서는 시작된 점검이 확인되지 않았어요. 이 화면에 남아 있는 원래 답변으로 다시 요청할 수 있어요. 자동으로 다시 보내지는 않아요.":"현재 상태와 방금 확인한 전체 답변으로 점검을 요청해요. 저장·점검 성공은 서버에서 확인한 뒤 표시해요."}</p><button className="miray-primary" disabled={busy} onClick={()=>{
      if(!frameLive() || !state)return;const answers=structuredClone(input),target=worker.context.target_ref;
      binding.attempt={context:structuredClone(worker.context),answers:structuredClone(answers)};
      void run(async o=>{const w=acceptWorker(await connection.worker.submit(target,answers,null,o),state);if(!live())return;if(w.context.target_ref!==target)throw new Error("Submitted original target changed");binding.attempt=null;setWorker(w);setInput(null);setPhase(w.status==="completed"?"result":"hold");});
    }}>입력 확인·루틴 점검</button></section>}
    {phase==="result" && worker?.result && <><CareResult envelope={worker.result.response} label="현재 상태의 점검 결과"/><button className="miray-primary" disabled={busy} onClick={()=>{if(frameLive())void load("episode");}}>실제 사용·현재 상태 확인</button></>}
    {phase==="quota" && quotaHold && <section className="miray-card" role="status"><h2>{quotaHold.reason==="unavailable"?"이용 한도를 확인하지 못했어요":quotaHold.reason==="concurrent_pending"?"다른 점검의 완료를 확인해야 해요":"현재 이용 한도로 새 점검을 시작할 수 없어요"}</h2>
      <p>{quotaHold.reason==="unavailable"?"새 점검의 입력 확인은 한도를 확인한 뒤 계속할 수 있어요.":quotaHold.reason==="concurrent_pending"?"처리 중인 점검이 있어 새 점검의 입력 확인을 열지 않아요.":`${quotaHold.feature.limit}회 중 ${quotaHold.feature.remaining}회 남았어요.`}</p>
      {quotaHold.reason!=="unavailable" && <p>현재 제공 구간 종료: {new Date(quotaHold.feature.period_ends_at).toLocaleString("ko-KR",{timeZone:quotaPolicy.timezone})} (한국 시간)</p>}
      <p>기존 결과와 이력은 유지해요. 홈에서 지난 점검 이후의 실제 사용·현재 상태 확인을 계속할 수 있어요. 조회는 횟수를 사용하거나 새 점검을 실행하지 않아요.</p>
      <button disabled={busy} onClick={()=>{if(frameLive())void load();}}>최신 저장·점검 상태 확인</button>
    </section>}
    {phase==="hold" && <section className="miray-card" role="status"><h2>{worker?.status==="pending"?"점검 완료를 확인하지 못했어요":worker?.reason==="allocation_limit"?"현재 이용 한도로 점검을 시작하지 못했어요":"현재 정보로는 점검을 진행하지 않아요"}</h2><p>{worker?.status==="pending"?"점검 요청은 기록됐지만 완료된 결과를 확인하지 못했어요. 상태 확인은 결과만 조회하며 중단된 점검을 다시 실행하지 않아요. 같은 화면이 계속되면 반복해서 누르거나 답변을 다시 제출하지 않아도 돼요.":draft?"확인하지 못한 정보는 답을 채우지 않아요. 방금 답변은 계정에 저장하지 않았고 이용 횟수도 사용하지 않았어요.":"기존 이력과 직접 확인한 사용 내용을 유지해요. 최신 상태 확인만으로 새 점검을 실행하지 않아요."}</p><button disabled={busy} onClick={()=>{if(frameLive())void load();}}>최신 저장·점검 상태 확인</button>{worker?.status==="pending" && connection.worker.resume && <><p>저장된 원 답변으로 점검을 복구할 수 있어요. 이용 횟수를 추가로 사용하지 않으며, 이미 완료됐다면 기존 결과를 보여드려요.</p><button disabled={busy} onClick={()=>{
      if(!frameLive() || !state || !worker || !connection.worker.resume)return;
      const resume=connection.worker.resume,target=worker.context.target_ref;
      void run(async o=>{const w=acceptWorker(await resume(target,o),state);if(!live())return;setWorker(w);setPhase(w.status==="completed"?"result":"hold");});
    }}>저장된 답변으로 점검 복구</button></>}</section>}
    {phase==="hold" && worker?.reason==="portfolio_changed" && state?.episode?.followup && worker.context.mode==="next" && <section className="miray-card"><h2>저장한 상태 이후 루틴이 다시 저장됐어요</h2>
      {state.unregistered_products?.products.length && connection.state.confirmAddedProduct?<><p>현재 목록의 새 제품에 실제 사용 확인이 필요해요. 제품 등록만으로 사용했다고 기록하지 않아요. 직접 확인한 뒤 현재 상태를 새 루틴에 연결할 수 있어요.</p><button ref={productTrigger} className="miray-primary" disabled={busy} onClick={()=>{if(!frameLive())return;consume();setDraft(null);setPhase("products");}}>새 제품 사용 직접 확인</button></>:<><p>이전 상태를 새 루틴의 입력으로 바꾸지 않아요. 현재 상태를 직접 확인해 연결한 뒤 점검 입력을 이어갈 수 있어요.</p><button className="miray-primary" disabled={busy} onClick={()=>{if(!frameLive())return;consume();setDraft(null);setPhase("refresh-state");}}>현재 상태와 루틴 다시 확인</button></>}
    </section>}
    {phase==="error" && <section role="alert"><p>저장이나 점검 여부를 확인하지 못했어요. 이미 반영됐을 수 있으므로 답변을 다시 보내기 전에 저장 상태를 확인해 주세요.</p><p>확인 코드: {failureCode}</p><button disabled={busy} onClick={()=>{if(frameLive())void load();}}>저장·점검 상태 확인</button></section>}
  </main>;
}
