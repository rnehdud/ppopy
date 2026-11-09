import {useEffect,useLayoutEffect,useMemo,useRef,useState} from "react";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import MirayIntakePanel from "./MirayIntakePanel";
import CareResult from "./CareResult";
import {resetAppScroll} from "./appScroll";
import {parseTerminalFreshView,validateTerminalFreshObservation,type TerminalFreshView} from "./mirayClosedLoopTerminalFreshReview";
import type {TerminalPromotionView} from "./mirayClosedLoopTerminalPromotionReview";
import {stateFirstPlan} from "./mirayClosedLoopStateFirst";
import type {MiraySkinState} from "./miraySkinState";
import {assertTerminalUiReviewOnly,createTerminalUiIntakeStore,matchTerminalFresh,matchTerminalPromotion,terminalCanonical,type TerminalUiReviewStore} from "./mirayClosedLoopTerminalUiReview";

type Binding={requestLifetime?:{isCurrent():boolean};store:TerminalUiReviewStore;terminalNextRef:string;active:boolean;live:boolean;pending:AbortController|null;lifetime:AbortController|null;retained:TerminalFreshView|null};
type Loaded={binding:Binding;fresh:TerminalFreshView;promotion:TerminalPromotionView|null};
/** Optional injected local review. No default app mount, persistence, timer,
 * member consent proxy, answer proxy or automatic dispatch. */
export default function MirayTerminalNextReviewPanel({store,terminalNextRef,active,onClose,onEpisode,requestLifetime}:{store:TerminalUiReviewStore;terminalNextRef:string;active:boolean;onClose():void;onEpisode?(decisionRef:string):void;requestLifetime?:{isCurrent():boolean}}){
  const [loaded,setLoaded]=useState<Loaded|null>(null),[observation,setObservation]=useState<MiraySkinState|null>(null);
  const [phase,setPhase]=useState<"intro"|"state"|"intake"|"abstain">("intro"),[busy,setBusy]=useState(false),[error,setError]=useState(false),[closed,setClosed]=useState(false);
  const binding=useMemo<Binding>(()=>({store,terminalNextRef,active,requestLifetime,live:false,pending:null,lifetime:null,retained:null}),[store,terminalNextRef,active,requestLifetime]);
  const owner=useRef<Binding|null>(null),heading=useRef<HTMLHeadingElement|null>(null);
  const current=active && !closed && loaded?.binding===binding?loaded:null;
  const frame=useMemo(()=>({binding,current,observation,phase,busy,error,closed}),[binding,current,observation,phase,busy,error,closed]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const childLifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && owner.current===binding && currentFrame.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding,frame]);
  const frameLive=()=>live() && currentFrame.current===frame && !closed;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const reset=()=>{setLoaded(null);setObservation(null);setPhase("intro");setError(false);binding.retained=null;};
  const retire=()=>{binding.live=false;binding.lifetime?.abort();binding.pending?.abort();binding.pending=null;binding.lifetime=null;binding.retained=null;if(owner.current===binding)owner.current=null;invalidateFrame();};
  const reject=()=>{if(!frameLive())return;invalidateFrame();setError(true);setObservation(null);setPhase("intro");};
  const run=async(action:"read"|"precheck"|"promote"|"resume"="read",state?:MiraySkinState,initial=false)=>{
    if(!live() || !active || closed && !initial || binding.pending || !binding.lifetime || binding.lifetime.signal.aborted || !initial && !frameLive())return;
    const life=binding.lifetime,c=new AbortController();binding.pending=c;invalidateFrame();setBusy(true);setError(false);
    const gate=()=>{c.signal.throwIfAborted();life.signal.throwIfAborted();if(!live())throw new Error("Terminal connection retired");assertTerminalUiReviewOnly();};
    try{
      gate();const fixed=current?structuredClone(current.fresh):undefined,previous=current?.promotion?structuredClone(current.promotion):undefined;
      if(action!=="read" && !fixed)throw new Error("Current terminal target required");
      if(action==="precheck"){
        if(!state || fixed!.stored || phase!=="state")throw new Error("New explicit state required");
        const candidate=structuredClone(state);validateTerminalFreshObservation(candidate);const localPlan=stateFirstPlan(candidate);
        const v=matchTerminalFresh(await store.fresh.precheck(structuredClone(candidate),{signal:c.signal,isCurrent:live}),fixed!.context);gate();
        if(v.stored || !v.plan || v.plan.status==="full_intake_required" && localPlan.status!=="more_input_required")throw new Error("Current new state not confirmed");
        setObservation(candidate);setLoaded({binding,fresh:v,promotion:null});setPhase(v.plan.status==="local_abstention"?"abstain":"intake");
      }else if(action==="read"){
        const raw=await store.fresh.read({signal:c.signal,isCurrent:live});gate();
        const f=fixed?matchTerminalFresh(raw,fixed.context):parseTerminalFreshView(raw,terminalNextRef);
        if(fixed?.stored && (!f.stored || terminalCanonical(f.observation)!==terminalCanonical(fixed.observation) || terminalCanonical(f.answers)!==terminalCanonical(fixed.answers)))throw new Error("Retained input changed");
        if(binding.retained && (!f.stored || terminalCanonical(f)!==terminalCanonical(binding.retained)))throw new Error("Confirmed saved input changed");
        const p=f.stored?matchTerminalPromotion(await store.promotion.read({signal:c.signal,isCurrent:live}),f.context,previous):null;gate();
        setLoaded({binding,fresh:f,promotion:p});setObservation(null);setPhase("intro");
      }else{
        if(!fixed!.stored || !previous || action==="promote" && previous.status!=="input_ready" || action==="resume" && previous.status!=="ready")throw new Error("Explicit current action required");
        const p=matchTerminalPromotion(await store.promotion[action]({signal:c.signal,isCurrent:live}),fixed!.context,previous);gate();
        if(action==="promote" && p.status!=="ready" || action==="resume" && p.status==="input_ready")throw new Error("Action acknowledgement unconfirmed");
        setLoaded({binding,fresh:fixed!,promotion:p});setObservation(null);setPhase("intro");
      }
    }catch{if(live() && !c.signal.aborted && !life.signal.aborted){setError(true);setObservation(null);setPhase("intro");}}
    finally{if(binding.pending===c){binding.pending=null;if(live())setBusy(false);}}
  };
  useLayoutEffect(()=>{
    binding.lifetime=new AbortController();binding.live=true;owner.current=binding;reset();setBusy(false);setClosed(false);
    return()=>{retire();};
    // The exact injected member stores and terminal target own this lifetime.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useEffect(()=>{
    // A dynamic StrictMode layout replay can occur after a layout microtask.
    // The passive commit defers the initial read without retrying or caching it.
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void run("read",undefined,true);});
    return()=>{attached=false;};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[phase,current?.promotion?.status,error]);
  const close=()=>{if(!frameLive())return;retire();reset();setBusy(false);setClosed(true);onClose();};
  const intake=useMemo(()=>{
    if(!current || phase!=="intake" || !observation || busy || error || closed)return null;
    const gate=()=>{if(childLifetime.isCurrent()!==true)throw new Error("Terminal input connection retired");assertTerminalUiReviewOnly();};
    try{return createTerminalUiIntakeStore(store.fresh,current.fresh,observation,v=>{gate();binding.retained=structuredClone(v);},gate);}catch{return null;}
  },[current,phase,observation,busy,error,closed,store,binding,childLifetime]);
  const inputSaved=(context:unknown)=>{
    if(!frameLive() || phase!=="intake" || !current || busy || error)return;
    try{assertTerminalUiReviewOnly();if(terminalCanonical(context)!==terminalCanonical(current.fresh.context) || !binding.retained?.stored)throw new Error("Exact confirmed saved input required");matchTerminalFresh(binding.retained,current.fresh.context);void run();}catch{reject();}
  };
  const beginState=()=>{if(!frameLive() || busy || error || !current || current.fresh.stored)return;invalidateFrame();try{assertTerminalUiReviewOnly();setObservation(null);setPhase("state");}catch{setError(true);}};
  const handoff=()=>{if(!frameLive() || busy || error || !current || current.promotion?.status!=="completed" || !onEpisode)return;invalidateFrame();try{assertTerminalUiReviewOnly();onEpisode(current.promotion.decision_ref!);}catch{setError(true);}};
  if(!active || closed)return <main className="miray-main"><p>계정과 별도 이력 저장 동의 연결을 확인해 주세요.</p><button disabled={closed} onClick={close}>닫기</button></main>;
  if(!error && current && phase==="state" && !busy)return <MiraySkinStateCheckin requestLifetime={childLifetime} kind="checkin" historyStorageConsented={false} completionMode="collect_for_entry" questionProfile="routine_state_and_safety" continueToAnalysis={false} onCancel={close} onComplete={state=>void run("precheck",state)}/>;
  if(!error && current && phase==="intake" && intake)return <main className="miray-main"><h1>새 입력으로 루틴 점검</h1><MirayIntakePanel requestLifetime={childLifetime} store={intake} label="새 상태에 필요한 점검 입력" savedPurpose="방금 직접 답한 현재 상태" onClose={close} onSaved={inputSaved}/></main>;
  const p=current?.promotion,result=p?.result?.state==="available"?p.result:null;
  return <main className="miray-main miray-loop-entry-panel"><button onClick={close}>‹ 홈으로</button><h1 tabIndex={-1} ref={heading}>{p?.status==="completed" && !error?"저장된 새 점검 결과":"새 입력으로 루틴 점검"}</h1>
    <p>앞선 점검과 직접 확인한 실제 사용 기록을 유지해요. 입력 저장이나 점검 결과는 실제 제품 사용의 확인이 아니에요.</p>
    {busy && <p role="status">현재 연결을 확인하고 있어요.</p>}
    {error?<section role="alert"><p>진행 상태를 확인하지 못했어요. 요청이 반영됐을 수 있어요. 같은 기록을 먼저 확인해 주세요.</p><button disabled={busy} onClick={()=>void run()}>같은 기록 확인</button></section>:
     current && phase==="abstain"?<section className="miray-card"><h2>현재 정보로는 조정을 보류해요</h2><p>{current.fresh.plan?.reason==="decision_abstained"?"불편감이나 실제 사용 맥락이 충분하지 않아 추가 문진을 먼저 묻지 않아요.":"모름·답변 거부·확인하지 못한 상태를 유지해요. 다른 답변으로 대신하지 않아요."}</p><p>방금 답변은 계정에 저장하지 않았어요. 점검 횟수도 사용하지 않았어요.</p><button disabled={busy} onClick={beginState}>직접 현재 상태 다시 입력</button></section>:
     current && !current.fresh.stored?<><p>앞선 점검은 결과 없이 종료됐어요. 현재 피부 고민과 사용 중 불편감을 따로 새로 확인해요.</p><button disabled={busy} onClick={beginState}>새 현재 상태 입력</button></>:
     p?.status==="input_ready"?<><p>현재 상태와 직접 답한 입력이 저장돼 있어요. 같은 질문을 다시 묻지 않아요. 점검 준비만으로는 횟수를 사용하거나 계산하지 않아요.</p><button disabled={busy} onClick={()=>void run("promote")}>저장한 입력으로 점검 준비</button></>:
     p?.status==="ready"?<><p>저장한 원래 입력으로 점검할 준비가 됐어요. 아래 버튼을 눌러야 루틴 점검을 요청해요.</p><button className="miray-primary" disabled={busy} onClick={()=>void run("resume")}>확인한 입력으로 루틴 점검</button></>:
     p?.status==="completed" && result?<><p>이번 입력으로 완료해 저장한 결과예요. 다시 확인할 때 새로 계산하지 않아요.</p><CareResult envelope={result.result} label="저장된 루틴 점검 결과"/>{onEpisode && <button disabled={busy} onClick={handoff}>이후 실제 사용·상태 확인</button>}</>:
     p?<><p>{p.status==="pending"?"점검 진행 또는 완료 확인이 필요해요. 다른 요청으로 계산을 시작하지 않아요.":p.status==="blocked"?"현재는 새 점검을 시작할 수 없어요. 가능한 점검 횟수를 확인해 주세요.":p.status==="deferred"?"현재 정보로 조정안을 확정하지 않았어요.":"이번 점검은 결과 없이 종료됐어요. 이전 이유를 추정하지 않아요."}</p><button disabled={busy} onClick={()=>void run()}>같은 기록 확인</button></>:null}
  </main>;
}
