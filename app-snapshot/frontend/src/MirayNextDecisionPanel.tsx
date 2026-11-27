import {useLayoutEffect,useMemo,useRef,useState} from "react";
import {assertNextReviewOnly,parseNextDecisionView,type NextDecisionContext,type NextDecisionReviewStore,type NextDecisionView} from "./mirayClosedLoopNext";
import MirayNextIntakePanel from "./MirayNextIntakePanel";
import {assertNextPrecheckReviewOnly} from "./mirayClosedLoopNextPrecheck";

/** Synthetic injected port only; mount/read never starts work or asks questions. */
export default function MirayNextDecisionPanel({store,active,parentDecisionRef,snapshotRef,onClose,onCompleted,onTerminal,requestLifetime}:{store:NextDecisionReviewStore;active:boolean;parentDecisionRef:string;snapshotRef:string;onClose():void;onCompleted(ref:string):void;onTerminal?(context:NextDecisionContext):void;requestLifetime?:{isCurrent():boolean}}){
  const binding=useMemo(()=>({store,active,parentDecisionRef,snapshotRef,requestLifetime,live:false,pending:null as AbortController|null,known:null as string|null}),[store,active,parentDecisionRef,snapshotRef,requestLifetime]);
  const current=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;value:NextDecisionView}|null>(null),[busy,setBusy]=useState(false),[error,setError]=useState(false);
  const [intakeOpen,setIntakeOpen]=useState(false),[intakeReady,setIntakeReady]=useState(false);
  const view=loaded?.binding===binding?loaded.value:null;
  const frame=useMemo(()=>({binding,view,busy,error,intakeOpen,intakeReady}),[binding,view,busy,error,intakeOpen,intakeReady]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && current.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && currentFrame.current===frame;
  const childLifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && current.current===binding && currentFrame.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding,frame]);
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;binding.known=null;if(current.current===binding)current.current=null;if(currentFrame.current?.binding===binding)currentFrame.current=null;};
  const operate=async(action:"read"|"recover"|"submit"|"resume")=>{
    if(!live() || !binding.active || binding.pending)return;
    const controller=new AbortController();binding.pending=controller;invalidateFrame();setBusy(true);setError(false);
    try{
      assertNextReviewOnly();assertNextPrecheckReviewOnly();const correlation=binding.known;
      if(action!=="read" && !correlation)throw new Error("No server correlation");
      const response=await (action==="read"?binding.store.read({signal:controller.signal,isCurrent:live}):binding.store[action](correlation!,{signal:controller.signal,isCurrent:live}));
      controller.signal.throwIfAborted();if(!live())return;const result=parseNextDecisionView(response);
      assertNextReviewOnly();assertNextPrecheckReviewOnly();controller.signal.throwIfAborted();
      if(result.context && (result.context.parent_decision_ref!==parentDecisionRef || result.context.snapshot_ref!==snapshotRef || (correlation!==null && result.context.next_ref!==correlation)))throw new Error("Next parent changed");
      binding.known=result.context?.next_ref??null;setLoaded({binding,value:result});
    }catch{if(live() && !controller.signal.aborted)setError(true);}
    finally{if(binding.pending===controller){binding.pending=null;if(live())setBusy(false);}}
  };
  const request=(action:Parameters<typeof operate>[0])=>{if(frameLive())void operate(action);};
  const close=()=>{if(!frameLive())return;retire();onClose();};
  const closeIntake=()=>{if(!frameLive())return;invalidateFrame();setIntakeOpen(false);};
  const confirmIntake=()=>{if(!frameLive() || !view?.context)return;try{assertNextReviewOnly();assertNextPrecheckReviewOnly();if(view.context.parent_decision_ref!==binding.parentDecisionRef || view.context.snapshot_ref!==binding.snapshotRef || view.context.next_ref!==binding.known)throw new Error("Input target changed");invalidateFrame();setIntakeReady(true);setIntakeOpen(false);}catch{setError(true);}};
  useLayoutEffect(()=>{
    binding.live=true;current.current=binding;setLoaded(null);setError(false);setBusy(false);setIntakeOpen(false);setIntakeReady(false);binding.known=null;
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void operate("read");});
    return()=>{attached=false;retire();};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  if(!active)return <main className="miray-main"><p>계정과 이력 저장 동의를 확인해 주세요.</p><button onClick={close}>닫기</button></main>;
  return <main className="miray-main"><button onClick={close}>‹ 이전 이력으로</button><h1>다음 루틴 점검</h1>
    {!intakeOpen && <p>저장한 후속 상태와 직접 확인한 실제 사용을 연결해 점검해요. 이전 답변으로 현재 상태를 만들거나 개선 여부를 자동 판단하지 않아요.</p>}
    {busy && <p role="status">점검 상태를 확인하는 중이에요.</p>}
    {intakeOpen && store.intake && view?.context?<MirayNextIntakePanel store={store.intake} context={view.context} requestLifetime={childLifetime} onClose={closeIntake} onSaved={confirmIntake}/>:
    error?<section role="alert" className="miray-card"><p>점검 응답을 확인하지 못했어요. 완료됐을 수도 있으므로 최신 상태를 먼저 확인해 주세요.</p><button disabled={busy} onClick={()=>request(binding.known?"recover":"read")}>최신 점검 상태 확인</button></section>:view && <section className="miray-card">
      {view.status==="completed"?<><h2>다음 루틴 점검을 저장했어요</h2><p>이번 상태와 이전 결정이 새 점검에 연결됐어요.</p><button disabled={busy} onClick={()=>{if(!frameLive())return;try{assertNextReviewOnly();assertNextPrecheckReviewOnly();if(view.context?.parent_decision_ref!==parentDecisionRef || view.context.snapshot_ref!==snapshotRef || view.context.next_ref!==binding.known)throw new Error("Completed target changed");invalidateFrame();onCompleted(view.decision_ref!);}catch{setError(true);}}}>새 점검 이력으로</button></>:
      view.status==="pending"?<><h2>진행 중인 점검이 있어요</h2><p>같은 점검을 다시 계산하지 않아요. 잠시 뒤 상태를 직접 확인할 수 있어요.</p><button disabled={busy} onClick={()=>request("recover")}>최신 점검 상태 확인</button></>:
      view.status==="terminal_without_result" || view.status==="deferred"?<><h2>이번 점검 결과를 제공하지 못했어요</h2><p>확인하지 못한 정보를 임의로 채우지 않아요. 기존 이력은 유지됩니다.</p>{onTerminal && view.context && <button disabled={busy} onClick={()=>{if(!frameLive())return;try{assertNextReviewOnly();assertNextPrecheckReviewOnly();if(view.context?.parent_decision_ref!==parentDecisionRef || view.context.snapshot_ref!==snapshotRef || view.context.next_ref!==binding.known)throw new Error("Terminal target changed");invalidateFrame();onTerminal(structuredClone(view.context));}catch{setError(true);}}}>새 입력 가능 여부 확인</button>}</>:
      view.status==="ready"?<><h2>원래 입력이 보관되어 있어요</h2><p>새 답변으로 덮어쓰지 않고 보관된 입력으로 점검할 수 있어요.</p><button disabled={busy} onClick={()=>request("resume")}>보관된 입력으로 점검 계속</button></>:
      view.reason==="full_intake_required"?<><h2>점검에 필요한 정보를 확인해요</h2><p>현재 제품과 점검에 필요한 정보를 확인한 뒤 시작해요. 정보가 부족하면 조정안을 제시하지 않아요.</p>{store.intake && !intakeReady?<button disabled={busy} onClick={()=>{if(frameLive()){invalidateFrame();setIntakeOpen(true);}}}>점검 입력 확인</button>:<button disabled={busy} onClick={()=>request("submit")}>정보 확인 후 다음 점검 요청</button>}</>:
      <><h2>점검을 진행할 조건을 확인해 주세요</h2><p>{view.reason==="followup_required"?"현재 상태를 먼저 확인해 주세요.":view.reason==="quota_unavailable"?"현재 이용 한도로 점검을 시작하지 못했어요.":"제품 구성이나 저장된 이력 확인이 필요해요."}</p><button disabled={busy} onClick={()=>request(binding.known?"recover":"read")}>최신 점검 상태 확인</button></>}
    </section>}
  </main>;
}
