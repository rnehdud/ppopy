import {useEffect,useLayoutEffect,useMemo,useRef,useState} from "react";
import MirayEntryIntakePanel from "./MirayEntryIntakePanel";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import CareResult from "./CareResult";
import {resetAppScroll} from "./appScroll";
import {assertLoopEntryReviewOnly,loopEntryRequest,parseLoopEntryView,sameLoopEntry,validateLoopEntryRequest,type ClosedLoopEntryReviewStore,type LoopEntryContext,type LoopEntryRequest,type LoopEntryView} from "./mirayClosedLoopEntry";
import type {MiraySkinState} from "./miraySkinState";
import config from "../../skin_engine/config/miray_closed_loop_entry_ui.json";
import {assertOriginalEntryResumeReviewOnly} from "./mirayClosedLoopAdmission";
import {assertAccountEntrySelectorReviewOnly} from "./mirayClosedLoopEntrySelector";
import {assertStateFirstReviewOnly,stateFirstPlan} from "./mirayClosedLoopStateFirst";

/** Synthetic local entry only; supplied server port owns admission and full intake. */
export default function MirayClosedLoopEntryPanel({store,active,onClose,onEpisode,onExistingEpisode,requestLifetime,expectedPortfolioRevision}:{store:ClosedLoopEntryReviewStore;active:boolean;onClose():void;onEpisode?(decisionRef?:string):void;onExistingEpisode?():void;requestLifetime?:{isCurrent():boolean};/** Visible account snapshot fence only; never server admission authority. */expectedPortfolioRevision?:number}){
  const binding=useMemo(()=>({store,active,requestLifetime,expectedPortfolioRevision,live:false,pending:null as AbortController|null,submitted:null as LoopEntryRequest|null}),[store,active,requestLifetime,expectedPortfolioRevision]);
  const owner=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;view:LoopEntryView}|null>(null);
  const [stage,setStage]=useState<"intro"|"state"|"review"|"intake">("intro");
  const [intakeParent,setIntakeParent]=useState<LoopEntryContext|null>(null);
  const [observation,setObservation]=useState<MiraySkinState|null>(null);
  const [busy,setBusy]=useState(false),[error,setError]=useState(false);
  // Retained exact request allows explicit same-payload replay only after recovery.
  // Never recreate observation time or an operation ID on a lost acknowledgement.
  const [attempted,setAttempted]=useState(false);
  const heading=useRef<HTMLHeadingElement|null>(null);
  const current=active && loaded?.binding===binding?loaded.view:null;
  const frame=useMemo(()=>({binding,current,stage,intakeParent,observation,busy,error,attempted}),[binding,current,stage,intakeParent,observation,busy,error,attempted]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const childLifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && owner.current===binding && currentFrame.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding,frame]);
  const frameLive=()=>live() && currentFrame.current===frame;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;binding.submitted=null;if(owner.current===binding)owner.current=null;invalidateFrame();};
  const reset=()=>{setLoaded(null);setStage("intro");setObservation(null);setIntakeParent(null);binding.submitted=null;setAttempted(false);setError(false);};
  const load=async(recovery=false,fresh=false,confirmedIntake?:LoopEntryContext,confirmedState?:MiraySkinState)=>{
    if(!live() || !active || binding.pending)return;
    const previous=current?.context;
    if(fresh && store.intake && !confirmedIntake){
      if(!store.startFresh || !previous || !current || !["deferred","terminal_without_result"].includes(current.status)){setError(true);return;}
      invalidateFrame();setIntakeParent(previous);setObservation(null);setStage("intake");return;
    }
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);setError(false);
    setStage("intro");setObservation(null);
    try{
      assertLoopEntryReviewOnly();assertStateFirstReviewOnly();
      if(binding.expectedPortfolioRevision!==undefined && (!Number.isSafeInteger(binding.expectedPortfolioRevision) || binding.expectedPortfolioRevision<0))throw new Error("Invalid visible portfolio revision");
      const explicitFresh=fresh && Boolean(store.startFresh);
      if(explicitFresh){
        if(!previous || !current || !["deferred","terminal_without_result"].includes(current.status))throw new Error("Terminal original required");
        assertAccountEntrySelectorReviewOnly(previous.entry_ref);
      }
      const next=parseLoopEntryView(await (explicitFresh?store.startFresh!(previous!.entry_ref,{signal:attempt.signal,isCurrent:live}):recovery && previous?store.recover(previous.entry_ref,{signal:attempt.signal,isCurrent:live}):store.read({signal:attempt.signal,isCurrent:live})));
      if(attempt.signal.aborted || !live())return;
      if(binding.expectedPortfolioRevision!==undefined && next.context && next.context.portfolio_revision!==binding.expectedPortfolioRevision)throw new Error("Visible portfolio changed before entry");
      assertStateFirstReviewOnly();
      if(confirmedIntake && (!next.context || !sameLoopEntry(confirmedIntake,next.context) || next.status!=="ready"))throw new Error("Saved input target changed");
      if(confirmedState){
        if(!confirmedIntake || !next.context || stateFirstPlan(confirmedState).status!=="more_input_required")throw new Error("Unconfirmed state-first input");
        loopEntryRequest(next.context,confirmedState);
      }
      if(explicitFresh){
        assertAccountEntrySelectorReviewOnly(previous!.entry_ref);
        if(next.status!=="blocked" && (next.status!=="ready" || next.context?.mode!=="fresh" || next.context.entry_ref===previous!.entry_ref || next.context.portfolio_revision!==previous!.portfolio_revision))throw new Error("Unconfirmed fresh entry selection");
      }
      if(recovery && previous && (!next.context || !sameLoopEntry(previous,next.context)))throw new Error("Different recovery entry");
      if(!recovery && binding.submitted && next.context?.entry_ref===binding.submitted.entry_ref){
        if(!previous || !next.context || !sameLoopEntry(previous,next.context))throw new Error("Changed existing entry");
      }else if(!recovery && binding.submitted && !(explicitFresh && next.status==="blocked")){
        // Only a server-selected fresh entry can replace a terminal first entry.
        if(!current || !["deferred","terminal_without_result"].includes(current.status) || next.status!=="ready" || next.context?.mode!=="fresh")throw new Error("Unconfirmed new entry");
        binding.submitted=null;setAttempted(false);
      }
      if(live() && !attempt.signal.aborted){setLoaded({binding,view:next});if(confirmedState){setObservation(structuredClone(confirmedState));setStage("review");}}
    }catch{if(live() && !attempt.signal.aborted)setError(true);}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  useLayoutEffect(()=>{
    binding.live=true;owner.current=binding;reset();setBusy(false);
    return()=>{retire();};
    // Current account/store/consent owns draft, original request and pending IO.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useEffect(()=>{
    // Dynamically mounted StrictMode children replay layout effects at the
    // passive commit. Start only after that replay; no timer or cached read.
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void load();});
    return()=>{attached=false;};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[stage,current?.status,error]);
  const close=()=>{if(!frameLive())return;retire();reset();setBusy(false);onClose();};
  const transition=(change:()=>void)=>{if(!frameLive())return;invalidateFrame();change();};
  const episode=()=>{const handoff=current?.status==="completed"?()=>onEpisode?.(current.decision_ref!):current?.status==="blocked" && current.reason==="existing_episode"?(onExistingEpisode??onEpisode):undefined;if(!frameLive() || busy || !handoff)return;invalidateFrame();try{assertLoopEntryReviewOnly();handoff();}catch{setError(true);}};
  const submit=async()=>{
    if(!frameLive() || !active || binding.pending || error || current?.status!=="ready" || !current.context)return;
    const context=current.context;
    let request:LoopEntryRequest;
    try{assertStateFirstReviewOnly();request=binding.submitted??loopEntryRequest(context,observation!);validateLoopEntryRequest(request);}catch{setError(true);return;}
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();binding.submitted=structuredClone(request);setAttempted(true);setBusy(true);setError(false);
    try{
      const next=parseLoopEntryView(await store.submit(structuredClone(request),{signal:attempt.signal,isCurrent:live}));
      if(attempt.signal.aborted || !live())return;
      assertStateFirstReviewOnly();
      if(!next.context || !sameLoopEntry(context,next.context) || next.status==="ready")throw new Error("Unconfirmed entry acknowledgement");
      if(live() && !attempt.signal.aborted){setLoaded({binding,view:next});setObservation(null);setStage("intro");}
    }catch{if(live() && !attempt.signal.aborted){setError(true);setObservation(null);setStage("intro");}}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  const resumeOriginal=async()=>{
    if(!frameLive() || !active || binding.pending || error || current?.status!=="blocked" || current.reason!=="saved_input_requires_recovery" || !current.context || !store.resume)return;
    const context=current.context;const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);setError(false);
    setStage("intro");setObservation(null);
    try{
      assertOriginalEntryResumeReviewOnly(context.entry_ref);
      const next=parseLoopEntryView(await store.resume(context.entry_ref,{signal:attempt.signal,isCurrent:live}));
      if(attempt.signal.aborted || !live())return;
      assertOriginalEntryResumeReviewOnly(context.entry_ref);
      if(!next.context || !sameLoopEntry(context,next.context) || next.status==="ready")throw new Error("Unconfirmed original entry resume");
      if(live() && !attempt.signal.aborted)setLoaded({binding,view:next});
    }catch{if(live() && !attempt.signal.aborted)setError(true);}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  if(!active)return <main className="miray-main"><p>이력 저장 동의와 계정 연결을 확인해 주세요.</p><button type="button" onClick={close}>닫기</button></main>;
  if(!error && stage==="intake" && store.intake)return <MirayEntryIntakePanel expectedPortfolioRevision={expectedPortfolioRevision} requestLifetime={childLifetime} collectStateFirst store={store.intake} originalContext={intakeParent} onClose={()=>transition(()=>{setIntakeParent(null);setStage("intro");})} onSaved={(context,state)=>{if(!frameLive())return;invalidateFrame();const fresh=intakeParent!==null;setIntakeParent(null);setStage("intro");void load(false,fresh,structuredClone(context),state?structuredClone(state):undefined);}}/>;
  if(!error && current?.status==="ready" && stage==="state" && !attempted)return <MiraySkinStateCheckin requestLifetime={childLifetime} kind={current.context!.mode==="initial"?"baseline":"checkin"} historyStorageConsented={false} completionMode="collect_for_entry" questionProfile={config.question_profile as "routine_state_and_safety"} continueToAnalysis={false} onCancel={()=>transition(()=>{setStage("intro");setObservation(null);})} onComplete={value=>transition(()=>{try{loopEntryRequest(current.context!,value);setObservation(structuredClone(value));setStage("review");}catch{setObservation(null);setError(true);setStage("intro");}})}/>;
  const available=current?.result?.state==="available"?current.result:null;
  return <main className="miray-main miray-loop-entry-panel">
    <button type="button" onClick={close}>‹ 홈으로</button>
    <h1 ref={heading} tabIndex={-1}>{current?.status==="completed"?"점검 결과를 확인했어요":"현재 상태로 루틴 점검"}</h1>
    {busy && <p role="status">진행 상태를 확인하고 있어요.</p>}
    {error?<>
      <p role="alert">진행 상태를 확인하지 못했어요. 제출했다면 저장됐을 수 있어요. 같은 작업을 먼저 확인해 주세요.</p>
      <button type="button" disabled={busy} onClick={()=>{if(frameLive())void load(Boolean(current?.context));}}>같은 작업 확인</button>
    </>:current?.status==="ready"?<>
      {stage==="review" && observation?<section className="miray-card">
        <h2>현재 상태로 점검할까요?</h2><p>방금 답한 현재 상태와 준비된 루틴 정보를 함께 점검해요. 답변은 이전 기록을 덮어쓰지 않고 별도 동의에 따라 저장해요.</p>
        <button type="button" disabled={busy} onClick={()=>transition(()=>{setObservation(null);setStage("state");})}>답변 수정</button>
        <button className="miray-primary" type="button" disabled={busy} onClick={()=>void submit()}>현재 상태 저장·루틴 점검</button>
      </section>:attempted?<>
        <p>이 작업의 완료는 아직 확인되지 않았어요. 다시 제출할 때는 앞서 보낸 동일한 답변을 사용해요.</p>
        <button type="button" disabled={busy} onClick={()=>void submit()}>같은 입력으로 다시 제출</button>
      </>:<>
        <p>{current.context?.mode==="fresh"?"앞선 점검은 완료되지 않았어요. 새 답변으로 현재 상태를 확인해요.":"지금 피부 고민과 사용 중 불편감을 각각 확인해요. 불편감이 있을 때만 종류를 더 물어봐요."}</p>
        <button className="miray-primary" type="button" disabled={busy} onClick={()=>transition(()=>setStage("state"))}>현재 상태 입력 시작</button>
      </>}
    </>:current?.status==="completed" && available?<>
      <p>이 작업에서 완료해 저장한 결과예요. 다시 불러올 때 새 점검을 시작하지 않아요.</p>
      <CareResult envelope={available.result} label="저장된 루틴 점검 결과"/>
      {onEpisode && <button type="button" disabled={busy} onClick={episode}>이후 실제 사용·상태 확인</button>}
    </>:current?.status==="pending"?<>
      <p>점검이 진행 중이거나 완료 확인이 필요해요. 새 점검을 시작하지 않고 이 작업을 확인해요.</p>
      <button type="button" disabled={busy} onClick={()=>{if(frameLive())void load(true);}}>같은 작업 확인</button>
    </>:current?.status==="deferred" || current?.status==="terminal_without_result"?<>
      <p>{current.status==="deferred"?"현재 정보로는 조정안을 확정하지 않았어요.":"이 작업은 결과 없이 종료됐어요. 이전 보류 이유를 추정하지 않아요."}</p>
      <button type="button" disabled={busy} onClick={()=>{if(frameLive())void load(false,true);}}>새 입력 가능 여부 확인</button>
    </>:current?.status==="blocked"?<>
      <p role="status">{current.reason==="full_intake_required"?"전체 루틴 점검에 필요한 정보가 아직 준비되지 않았어요. 상태 답변만으로 나머지 정보를 채우지 않아요.":current.reason==="existing_episode"?"지난 점검 이후 실제 사용과 후속 상태부터 확인해 주세요.":current.reason==="portfolio_changed"?"등록한 제품 정보가 바뀌어 점검 연결을 다시 확인해야 해요.":current.reason==="saved_input_requires_recovery"?"앞서 저장된 입력과 작업 연결을 확인해야 해요. 새 답변으로 덮어쓰지 않아요.":current.reason==="quota_unavailable"?"지금은 새 점검을 시작할 수 없어요. 점검 가능한 횟수를 확인해 주세요.":"계정과 이력 저장 동의 상태를 확인해 주세요."}</p>
      {current.reason==="full_intake_required" && !current.context && store.intake && <button type="button" disabled={busy} onClick={()=>transition(()=>{setIntakeParent(null);setStage("intake");})}>점검 입력 확인</button>}
      {current.reason==="existing_episode" && (onExistingEpisode || onEpisode) && <button type="button" disabled={busy} onClick={episode}>이후 실제 사용·상태 확인</button>}
      {current.reason==="saved_input_requires_recovery" && current.context && store.resume && <>
        <p>앞서 저장한 답변으로 점검을 이어가요. 현재 상태를 새로 입력하는 단계는 아니에요.</p>
        <button type="button" disabled={busy} onClick={()=>void resumeOriginal()}>저장된 원래 입력으로 계속</button>
      </>}
    </>:null}
  </main>;
}
