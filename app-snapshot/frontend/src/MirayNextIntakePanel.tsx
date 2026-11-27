import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import {useLayoutEffect,useMemo,useRef,useState} from "react";
import MirayIntakePanel, {type IntakePanelStore} from "./MirayIntakePanel";
import {parseIntakeView,type NextIntakeReviewStore} from "./mirayClosedLoopIntake";
import type {NextDecisionContext} from "./mirayClosedLoopNext";
import {assertNextPrecheckReviewOnly,matchNextPrecheck,type NextPrecheckView} from "./mirayClosedLoopNextPrecheck";
import {resetAppScroll} from "./appScroll";

/** Saved followup first. Never re-ask it or manufacture full intake answers. */
export default function MirayNextIntakePanel({store,context,onClose,onSaved,requestLifetime}:{store:NextIntakeReviewStore;context:NextDecisionContext;onClose():void;onSaved():void;requestLifetime?:{isCurrent():boolean}}){
  const [phase,setPhase]=useState<"loading"|"open"|"stopped"|"error">("loading");
  const [reason,setReason]=useState<string|null>(null),[busy,setBusy]=useState(false);
  const current=useRef<object|null>(null),heading=useRef<HTMLHeadingElement|null>(null);
  const bound=useMemo(()=>{
    const target={next_ref:context.next_ref,parent_decision_ref:context.parent_decision_ref,snapshot_ref:context.snapshot_ref,portfolio_revision:context.portfolio_revision};
    const binding={live:false,pending:null as AbortController|null};
    const live=()=>{try{return binding.live && current.current===binding && (!requestLifetime || requestLifetime.isCurrent()===true);}catch{return false;}};
    const consumer=(o?:MemberStatusReadOptions)=>({signal:o?.signal,isCurrent:()=>{try{return live() && (!o?.isCurrent || o.isCurrent()===true);}catch{return false;}}});
    const assertLive=(o?:MemberStatusReadOptions)=>{o?.signal?.throwIfAborted();if(!live() || o?.isCurrent && o.isCurrent()!==true)throw new Error("Input connection retired");assertNextPrecheckReviewOnly();};
    const sameTarget=(c:NextDecisionContext)=>(Object.keys(target) as (keyof NextDecisionContext)[]).every(k=>c[k]===target[k]);
    const check=async(options?:MemberStatusReadOptions)=>{
      const o=consumer(options);assertLive(o);
      if(!store.precheck)throw new Error("Saved followup precheck unavailable");
      const response=await store.precheck(o);assertLive(o);
      return matchNextPrecheck(response,target);
    };
    const requireInput=async(o?:MemberStatusReadOptions)=>{
      const v=await check(o);assertLive(o);
      if(v.plan.status==="local_abstention"){setReason(v.plan.reason);setPhase("stopped");throw new Error("Saved followup insufficient");}
    };
    const parse=(v:unknown,o?:MemberStatusReadOptions)=>{assertLive(o);const value=parseIntakeView(v);if(!sameTarget(value.context))throw new Error("Input target changed");return value;};
    const intake:IntakePanelStore<NextDecisionContext>={
      read:async options=>{const o=consumer(options);await requireInput(o);assertLive(o);const v=parse(await store.read(o),o);await requireInput(o);assertLive(o);return v;},
      save:async(c,a,options)=>{const o=consumer(options);assertLive(o);if(!sameTarget(c))throw new Error("Input target changed");await requireInput(o);assertLive(o);const v=parse(await store.save(target.next_ref,a,o),o);await requireInput(o);assertLive(o);return v;}
    };
    const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;if(current.current===binding)current.current=null;};
    return {binding,live,assertLive,sameTarget,retire,check,intake,lifetime:{isCurrent:live}};
    // Exact target fields own the component lifetime.
  },[store,context.next_ref,context.parent_decision_ref,context.snapshot_ref,context.portfolio_revision,requestLifetime]);
  const accept=(v:NextPrecheckView)=>{setReason(v.plan.reason);setPhase(v.plan.status==="local_abstention"?"stopped":"open");};
  const run=async(handoff=false)=>{
    if(bound.binding.pending || !bound.live())return;
    const c=new AbortController();bound.binding.pending=c;setBusy(true);
    try{const v=await bound.check({signal:c.signal});bound.assertLive({signal:c.signal});
      if(handoff && v.plan.status==="full_intake_required"){assertNextPrecheckReviewOnly();onSaved();}else accept(v);
    }catch{if(bound.live() && !c.signal.aborted)setPhase("error");}
    finally{if(bound.binding.pending===c){bound.binding.pending=null;if(bound.live())setBusy(false);}}
  };
  useLayoutEffect(()=>{
    bound.binding.live=true;current.current=bound.binding;setPhase("loading");setReason(null);setBusy(false);
    let attached=true;void Promise.resolve().then(()=>{if(attached)void run();});
    return()=>{attached=false;bound.retire();};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[bound]);
  useLayoutEffect(()=>{resetAppScroll();if(phase==="stopped" || phase==="error")heading.current?.focus({preventScroll:true});},[phase]);
  const close=()=>{if(!bound.live())return;bound.retire();onClose();};
  if(phase==="open")return <MirayIntakePanel key={context.next_ref} store={bound.intake} requestLifetime={bound.lifetime} label="다음 점검 입력 확인" savedPurpose="이번 후속 상태" onClose={close} onSaved={c=>{if(bound.sameTarget(c))void run(true);}}/>;
  return <section className="miray-card miray-intake" aria-label="후속 상태 확인"><button onClick={close}>입력 확인 닫기</button>
    {phase==="loading"?<p role="status">저장된 후속 상태를 확인하는 중이에요.</p>:
     phase==="error"?<div role="alert"><h2 tabIndex={-1} ref={heading}>후속 상태 확인을 완료하지 못했어요</h2><p>확인이 끝나기 전에는 추가 질문을 열거나 입력을 저장하지 않아요.</p><button disabled={busy} onClick={()=>void run()}>후속 상태 확인 다시 요청</button></div>:
     <><h2 tabIndex={-1} ref={heading}>현재 정보로는 다음 점검을 보류해요</h2>
       <p>{reason?.startsWith("previous_episode:")?"이전 행동 기록과 현재 루틴이 달라, 추가 문진만으로 다음 조정안을 정할 수 없어요.":reason==="decision_abstained"?"사용 빈도나 불편감의 맥락이 충분하지 않아 추가 문진을 먼저 묻지 않아요.":"저장된 후속 상태의 모름·답변 거부·미질문을 구분해 유지해요. 추가 문진으로 그 답변을 대신하지 않아요."}</p>
       <p>원래 후속 상태와 실제 행동 기록을 유지해요. 이 확인만으로 새 점검 결과를 저장하거나 한도를 사용하지 않아요.</p>
       <button disabled={busy} onClick={()=>void run()}>저장된 후속 상태 다시 확인</button></>}
  </section>;
}
