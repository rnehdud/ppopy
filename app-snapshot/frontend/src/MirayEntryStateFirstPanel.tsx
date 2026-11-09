import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import {useLayoutEffect,useMemo,useRef,useState} from "react";
import MirayIntakePanel,{type IntakePanelStore,type IntakePanelView} from "./MirayIntakePanel";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import {assertStateFirstReviewOnly,stateFirstPlan} from "./mirayClosedLoopStateFirst";
import {loopEntryRequest,sameLoopEntry,type LoopEntryContext} from "./mirayClosedLoopEntry";
import type {MiraySkinState} from "./miraySkinState";
import {resetAppScroll} from "./appScroll";

/** Server-selected target first; transient state first; no new server endpoint. */
export default function MirayEntryStateFirstPanel({store,onClose,onSaved,requestLifetime}:{store:IntakePanelStore<LoopEntryContext>;onClose():void;onSaved(context:LoopEntryContext,state?:MiraySkinState):void;requestLifetime?:{isCurrent():boolean}}){
  const [selected,setSelected]=useState<IntakePanelView<LoopEntryContext>|null>(null),[state,setState]=useState<MiraySkinState|null>(null);
  const [phase,setPhase]=useState<"loading"|"state"|"intake"|"abstain"|"error">("loading");
  const binding=useMemo(()=>({store,requestLifetime,live:false,pending:null as AbortController|null}),[store,requestLifetime]);
  const current=useRef<typeof binding|null>(null),heading=useRef<HTMLHeadingElement|null>(null);
  const frame=useMemo(()=>({binding,selected,state,phase}),[binding,selected,state,phase]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && current.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const childLifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && current.current===binding && currentFrame.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding,frame]);
  const frameLive=()=>live() && currentFrame.current===frame;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;if(current.current===binding)current.current=null;invalidateFrame();};
  const load=async()=>{
    if(binding.pending || !live())return;
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setPhase("loading");setState(null);setSelected(null);
    try{assertStateFirstReviewOnly();const v=await binding.store.read({signal:attempt.signal,isCurrent:live});attempt.signal.throwIfAborted();if(!live())return;assertStateFirstReviewOnly();setSelected(structuredClone(v));setPhase(v.stored?"intake":"state");}
    catch{if(live() && !attempt.signal.aborted)setPhase("error");}
    finally{if(binding.pending===attempt)binding.pending=null;}
  };
  useLayoutEffect(()=>{binding.live=true;current.current=binding;let attached=true;void Promise.resolve().then(()=>{if(attached)void load();});return()=>{attached=false;retire();};
    // Exact bound store owns both unsaved state and selected target lifetime.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[phase]);
  const close=()=>{if(!frameLive())return;retire();setState(null);setSelected(null);onClose();};
  const intakeStore=useMemo<IntakePanelStore<LoopEntryContext>|null>(()=>{
    if(!selected || phase!=="intake")return null;
    const fixed=structuredClone(selected),observation=state===null?null:structuredClone(state);let first=true;
    const consumer=(o:Parameters<IntakePanelStore<LoopEntryContext>["read"]>[0])=>({signal:o.signal,isCurrent:()=>{try{return childLifetime.isCurrent() && (!o.isCurrent || o.isCurrent()===true);}catch{return false;}}});
    const gate=(c:LoopEntryContext,o:MemberStatusReadOptions)=>{
      o.signal?.throwIfAborted();if(!childLifetime.isCurrent() || o.isCurrent?.()!==true)throw new Error("State input connection retired");
      assertStateFirstReviewOnly();if(!sameLoopEntry(c,fixed.context))throw new Error("State input target changed");
      if(!fixed.stored && (!observation || stateFirstPlan(observation).status!=="more_input_required"))throw new Error("Current state requires abstention");
    };
    // A child's layout read waits for the parent to commit its exact frame.
    // Retirement during this queue also prevents the request from dispatching.
    return {read:async options=>{const o=consumer(options);await Promise.resolve();gate(fixed.context,o);if(first){first=false;return structuredClone(fixed);}const v=await binding.store.read(o);gate(v.context,o);return v;},save:async(c,a,options)=>{const o=consumer(options);await Promise.resolve();gate(c,o);const v=await binding.store.save(c,a,o);gate(v.context,o);return v;}};
  },[selected,state,phase,binding,childLifetime]);
  if(phase==="state" && selected)return <MiraySkinStateCheckin requestLifetime={childLifetime} kind={selected.context.mode==="initial"?"baseline":"checkin"} historyStorageConsented={false} completionMode="collect_for_entry" questionProfile="routine_state_and_safety" continueToAnalysis={false} onCancel={close} onComplete={v=>{
    if(!frameLive())return;invalidateFrame();
    try{loopEntryRequest(selected.context,v);const plan=stateFirstPlan(v);setState(structuredClone(v));setPhase(plan.status==="local_abstention"?"abstain":"intake");}catch{setState(null);setPhase("error");}
  }}/>;
  if(phase==="intake" && selected && intakeStore)return <main className="miray-main"><h1>현재 점검 입력 확인</h1><MirayIntakePanel requestLifetime={childLifetime} store={intakeStore} label="현재 점검 입력 확인" savedPurpose={selected.context.mode==="initial"?"첫 점검":"새로 확인한 현재 상태"} onClose={close} onSaved={c=>{
    if(!frameLive())return;invalidateFrame();
    try{assertStateFirstReviewOnly();if(!sameLoopEntry(c,selected.context))throw new Error("State target changed");if(state && stateFirstPlan(state).status!=="more_input_required")throw new Error("State no longer eligible");onSaved(c,state?structuredClone(state):undefined);}catch{setState(null);setPhase("error");}
  }}/></main>;
  return <main className="miray-main"><button onClick={close}>입력 확인 닫기</button><h1 ref={heading} tabIndex={-1}>현재 상태 먼저 확인</h1><p>피부 고민과 사용 중 불편감을 따로 확인해요. 모르는 내용은 추측하지 않아도 돼요.</p>
    {phase==="loading"?<p role="status">현재 점검에 연결할 입력을 확인해요.</p>:phase==="error"?<section role="alert"><p>현재 입력의 연결을 확인하지 못했어요. 저장을 시도했다면 반영됐을 수 있어요. 같은 입력 연결부터 확인해 주세요.</p><button onClick={()=>{if(frameLive())void load();}}>입력 연결 다시 확인</button></section>:<section className="miray-card"><h2>현재 정보로는 조정안을 확정하지 않아요</h2>
      <p>{state?.discomfort_presence==="reported"?"불편감의 종류만으로 사용 시간·양 등 필요한 관찰 정보를 확인할 수 없어 조정을 보류해요.":"피부 고민과 사용 중 불편감 중 확인하지 못한 항목이 있어 조정을 보류해요."}</p>
      <p>추가 점검 문진을 이어 묻지 않아요. 방금 답변은 계정 이력에 저장하지 않았고, 점검 횟수도 사용하지 않았어요.</p>
      <button onClick={()=>{if(!frameLive())return;invalidateFrame();try{assertStateFirstReviewOnly();setState(null);setPhase("state");}catch{setPhase("error");}}}>직접 현재 상태 다시 입력</button></section>}
  </main>;
}
