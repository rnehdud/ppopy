import {useLayoutEffect,useMemo,useRef,useState} from "react";
import {resetAppScroll} from "./appScroll";
import "./mirayFrequencyCorrection.css";
import {assertFrequencyCorrectionReviewOnly,frequencyCorrectionRequest,parseFrequencyCorrectionAck,parseFrequencyCorrectionView,type FrequencyCorrectionView,type FrequencyCorrectionReviewStore} from "./mirayClosedLoopFrequency";

const frequencyLabel=(v:string)=>/^\d$/.test(v)?v==="0"?"현재 사용하지 않음":`주 ${v}일`:v==="user_refused"?"답변하지 않음":v==="user_does_not_remember"?"기억나지 않음":"모름";
/** User-opened optional declaration edit, never another mandatory state question. */
export default function MirayFrequencyCorrectionPanel({store,active,decisionRef,onClose,returnLabel="현재 상태 확인으로 돌아가기",holdPendingReturn=false,requestLifetime}:{store:FrequencyCorrectionReviewStore;active:boolean;decisionRef:string;onClose(view?:FrequencyCorrectionView):void;returnLabel?:string;holdPendingReturn?:boolean;requestLifetime?:{isCurrent():boolean}}){
  const binding=useMemo(()=>({store,active,decisionRef,requestLifetime,live:false,pending:null as AbortController|null}),[store,active,decisionRef,requestLifetime]);
  const current=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;view:FrequencyCorrectionView}|null>(null);
  const [busy,setBusy]=useState(false),[error,setError]=useState(false),[explicit,setExplicit]=useState(false),[saved,setSaved]=useState(false);
  const heading=useRef<HTMLHeadingElement|null>(null);
  const view=active && loaded?.binding===binding?loaded.view:null;
  const frame=useMemo(()=>({binding,view,busy,error,explicit,saved}),[binding,view,busy,error,explicit,saved]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && current.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && currentFrame.current===frame;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;if(current.current===binding)current.current=null;if(currentFrame.current?.binding===binding)currentFrame.current=null;};
  const conflict=view?.conflicts.find(c=>c.correctable);
  const reset=()=>{setLoaded(null);setExplicit(false);setSaved(false);setError(false);};
  const read=async()=>{
    if(!live() || !binding.active || binding.pending)return;
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();reset();setBusy(true);
    try{attempt.signal.throwIfAborted();assertFrequencyCorrectionReviewOnly();const response=await binding.store.read({signal:attempt.signal,isCurrent:live});attempt.signal.throwIfAborted();if(!live())return;const value=parseFrequencyCorrectionView(response);assertFrequencyCorrectionReviewOnly();
      if(value.decision_ref!==binding.decisionRef)throw new Error("Correction decision changed");setLoaded({binding,view:value});
    }catch{if(live() && !attempt.signal.aborted)setError(true);}finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  const refresh=()=>{if(frameLive())void read();};
  useLayoutEffect(()=>{binding.live=true;current.current=binding;reset();setBusy(false);
    // Wait for the parent frame to commit; cleanup also fences StrictMode replay.
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void read();});
    return()=>{attached=false;retire();};
    // Store/account/consent/decision lifetime changes discard late responses and drafts.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[conflict?.actual_action_ref,saved]);
  const close=()=>{if(!frameLive() || (holdPendingReturn && binding.pending))return;const confirmed=view?structuredClone(view):undefined;retire();reset();onClose(confirmed);};
  const confirm=async()=>{
    if(!frameLive() || !active || !view || !conflict || !explicit || binding.pending || error)return;
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);setError(false);
    try{const request=frequencyCorrectionRequest(view,conflict.actual_action_ref);attempt.signal.throwIfAborted();assertFrequencyCorrectionReviewOnly();const response=await binding.store.confirm(structuredClone(request),{signal:attempt.signal,isCurrent:live});attempt.signal.throwIfAborted();if(!live())return;const ack=parseFrequencyCorrectionAck(response,request);assertFrequencyCorrectionReviewOnly();
      setLoaded({binding,view:ack.view});setExplicit(false);setSaved(true);
    }catch{if(live() && !attempt.signal.aborted)setError(true);}finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  return <main className="miray-main miray-loop-panel">
    <button disabled={holdPendingReturn && busy} onClick={close}>‹ 실제 사용·상태 확인으로</button><p className="miray-eyebrow">입력한 사용 빈도 확인</p><h1 ref={heading} tabIndex={-1}>입력 빈도를 정정할까요?</h1>
    <p>이미 직접 확인한 실제 사용 기록과 입력한 빈도를 비교해요. 정정해도 이전 사용 기록이나 상태 답변을 바꾸지 않아요.</p>
    {!active?<p>이력 저장 동의와 계정 연결을 확인해 주세요.</p>:error?<section className="miray-card" role="alert"><p>정정을 확인하지 못했어요. 저장됐을 수도 있으므로 최신 기록을 확인한 뒤 이어가세요.</p><button disabled={busy} onClick={refresh}>최신 빈도 정정 기록 확인</button></section>:<>
      {busy && <p role="status">기록을 확인하는 중이에요.</p>}
      {saved && <p role="status">빈도 정정 기록을 저장했어요.</p>}
      {conflict && <section className="miray-card" aria-labelledby="frequency-conflict"><h2 id="frequency-conflict">{conflict.product_name}</h2>
        <p>입력한 빈도: {frequencyLabel(conflict.declared_frequency)}</p><p>직접 확인한 실제 사용: {frequencyLabel(conflict.confirmed_frequency)}</p>
        <p>사용 기록 확인 시각: {new Date(conflict.confirmed_at).toLocaleString("ko-KR")}</p>
        <p>이 기록이 지금의 입력 빈도에도 맞을 때만 정정해 주세요. 새로운 사용이나 빈도 변경을 기록하는 기능은 아니에요.</p>
        <label className="miray-frequency-confirm"><input type="checkbox" checked={explicit} disabled={busy} onChange={e=>{if(frameLive() && !binding.pending){invalidateFrame();setExplicit(e.target.checked);setSaved(false);}}}/><span>직접 확인한 빈도를 현재 입력값에 반영할게요</span></label>
        <button className="miray-primary" disabled={busy || !explicit} onClick={()=>void confirm()}>{frequencyLabel(conflict.confirmed_frequency)}로 입력 빈도 정정</button>
      </section>}
      {view && !conflict && <section className="miray-card" role="status"><h2>{view.conflicts.length?"이 기록은 바로 정정할 수 없어요":"정정할 빈도 차이가 없어요"}</h2><p>{view.conflicts.length?"이미 후속 상태를 저장했거나 정정 뒤 입력값이 다시 바뀌었어요. 기존 기록은 유지하고 현재 상태를 새로 확인해야 해요.":"새 답변이나 사용 기록을 추가하지 않았어요."}</p></section>}
      {view && <button disabled={busy} onClick={close}>{returnLabel}</button>}
    </>}
  </main>;
}
