import {productNamePresentation} from "./productPresentation";
import {sameUtcInstant} from "./mirayUtcInstant";
import {useEffect,useLayoutEffect,useMemo,useRef,useState} from "react";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import MirayNextDecisionPanel from "./MirayNextDecisionPanel";
import MirayProductChangePanel from "./MirayProductChangePanel";
import MirayFrequencyCorrectionPanel from "./MirayFrequencyCorrectionPanel";
import {resetAppScroll} from "./appScroll";
import {confirmActualRequest,followupCompletionCode,parseClosedLoopEpisode,saveFollowupRequest,validateFollowupObservation,type ClosedLoopEpisode,type ClosedLoopReviewStore} from "./mirayClosedLoop";
import type {MiraySkinState} from "./miraySkinState";
import {nextRef,type NextDecisionContext} from "./mirayClosedLoopNext";
import config from "../../skin_engine/config/miray_closed_loop_ui.json";
import "./mirayClosedLoopPanel.css";
import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import {parseFrequencyCorrectionView,type FrequencyCorrectionView} from "./mirayClosedLoopFrequency";

/** Only an explicitly injected local TEST port can open this flow. */
export default function MirayClosedLoopPanel({store,active,onClose,expectedDecisionRef,onTerminal,onCompleted,onNextRequested,onFrequencyClosed,requestLifetime}:{store:ClosedLoopReviewStore;active:boolean;onClose():void;expectedDecisionRef?:string;onTerminal?(context:NextDecisionContext):void;onCompleted?(decisionRef:string):void;onNextRequested?():void;onFrequencyClosed?(view?:FrequencyCorrectionView):void;requestLifetime?:{isCurrent():boolean}}){
  const binding=useMemo(()=>({store,active,expectedDecisionRef,requestLifetime,live:false,pending:null as AbortController|null}),[store,active,expectedDecisionRef,requestLifetime]);
  const current=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;episode:ClosedLoopEpisode}|null>(null);
  const [busy,setBusy]=useState(false),[error,setError]=useState("");
  const [frequency,setFrequency]=useState(""),[started,setStarted]=useState("");
  const [stage,setStage]=useState<"use"|"changes"|"frequency"|"state"|"review"|"next">("use");
  const [observation,setObservation]=useState<MiraySkinState|null>(null);
  const heading=useRef<HTMLHeadingElement|null>(null);
  const episode=active && loaded?.binding===binding?loaded.episode:null;
  const frame=useMemo(()=>({binding,episode,frequency,started,stage,observation,busy,error}),[binding,episode,frequency,started,stage,observation,busy,error]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && current.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && currentFrame.current===frame;
  const childLifetime=useMemo(()=>({isCurrent:()=>{
    try{return binding.live && current.current===binding && currentFrame.current===frame && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}
  }}),[binding,frame]);
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;if(current.current===binding)current.current=null;if(currentFrame.current?.binding===binding)currentFrame.current=null;};
  const question=episode?.actual_use_questions[0];
  const numeric=Boolean(question && config.frequency_values.includes(question.previous_frequency));
  const changed=Boolean(question && config.frequency_values.includes(frequency) && frequency!==question.previous_frequency);
  const reset=()=>{setLoaded(null);setFrequency("");setStarted("");setStage("use");setObservation(null);setError("");};
  const read=async(expectedDecision=expectedDecisionRef)=>{
    if(!live() || !binding.active || binding.pending)return;
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();reset();setBusy(true);
    try{const response=await binding.store.read({signal:attempt.signal,isCurrent:live});attempt.signal.throwIfAborted();if(!live())return;const next=parseClosedLoopEpisode(response);if(expectedDecision && next.decision_ref!==expectedDecision)throw new Error("Next decision not current");setLoaded({binding,episode:next});}
    catch{if(live() && !attempt.signal.aborted)setError("read");}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  useLayoutEffect(()=>{
    binding.live=true;current.current=binding;reset();setBusy(false);
    return()=>{retire();};
    // A different account/store/consent lifetime discards drafts and late ACKs.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useEffect(()=>{
    // The parent layout gate and a dynamic StrictMode replay must commit
    // before an initial member read starts. Cleanup still fences the callback.
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void read();});
    return()=>{attached=false;};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[question?.recommendation_id,stage]);
  const close=()=>{if(!frameLive())return;retire();reset();onClose();};
  const move=(next:typeof stage)=>{if(!frameLive() || binding.pending)return;invalidateFrame();setObservation(null);setStage(next);};
  const refresh=()=>{if(frameLive())void read();};
  const mutate=async(operation:(options:MemberStatusReadOptions)=>Promise<unknown>,check:(next:ClosedLoopEpisode)=>boolean)=>{
    if(!frameLive() || binding.pending || !active || !episode || error)return;
    const previous=episode;const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);setError("");
    try{const response=await operation({signal:attempt.signal,isCurrent:live});attempt.signal.throwIfAborted();if(!live())return;const next=parseClosedLoopEpisode(response);
      if(next.decision_ref!==previous.decision_ref || !check(next))throw new Error("Unconfirmed write");
      setLoaded({binding,episode:next});setFrequency("");setStarted("");setObservation(null);setStage("use");
    }catch{if(live() && !attempt.signal.aborted)setError("save");}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  const confirm=()=>{
    if(!frameLive() || !episode || !question || !frequency)return;
    try{const effective=config.unconfirmed_values.includes(frequency)?null:changed?new Date(started).toISOString():new Date().toISOString();
      const request=confirmActualRequest(episode,question,frequency,effective);
      void mutate(options=>store.confirmActual(request,options),next=>!next.actual_use_questions.some(q=>q.product_id===question.product_id) && (config.unconfirmed_values.includes(frequency)
        ?next.unconfirmed_count>episode.unconfirmed_count && next.unconfirmed_answers.some(a=>a.recommendation_id===question.recommendation_id && a.response===frequency)
        :next.actual_actions.some(a=>!episode.actual_actions.some(old=>old.ref===a.ref) && a.recommendation_id===question.recommendation_id && a.product_id===question.product_id && a.frequency===frequency && sameUtcInstant(a.effective_from,effective!))));
    }catch{setError("time");}
  };
  const save=()=>{
    if(!frameLive() || !episode || !observation)return;
    try{const request=saveFollowupRequest(episode,observation);void mutate(options=>store.saveFollowup(request,options),next=>Boolean(next.followup && sameUtcInstant(next.followup.observed_at,observation.observed_at)));}
    catch(failure){setError(followupCompletionCode(failure));}
  };
  if(!active)return <main className="miray-main"><p>이력 저장 동의와 계정 연결을 확인해 주세요.</p><button onClick={close}>닫기</button></main>;
  if(!error && episode && stage==="frequency" && store.frequencyCorrections)return <MirayFrequencyCorrectionPanel store={store.frequencyCorrections} active={active} decisionRef={episode.decision_ref} holdPendingReturn={Boolean(onFrequencyClosed)} returnLabel={onFrequencyClosed?"홈에서 최신 루틴 확인":undefined} onClose={value=>{
    if(!frameLive())return;if(!onFrequencyClosed){refresh();return;}
    try{const view=value?parseFrequencyCorrectionView(value):undefined;
      if(view && (view.decision_ref!==episode.decision_ref || view.corrections.some(c=>!episode.actual_actions.some(a=>a.ref===c.actual_action_ref))))throw new Error("Original correction action changed");
      retire();reset();onFrequencyClosed(view);
    }catch{setError("read");}
  }} requestLifetime={childLifetime}/>;
  if(!error && episode?.followup && stage==="next" && store.nextDecision)return <MirayNextDecisionPanel store={store.nextDecision} active={active} parentDecisionRef={episode.decision_ref} snapshotRef={episode.followup.snapshot_ref} requestLifetime={childLifetime} onClose={()=>move("use")} onCompleted={ref=>{if(!frameLive())return;invalidateFrame();try{nextRef(ref);if(onCompleted)onCompleted(ref);else void read(ref);}catch{setError("read");}}} onTerminal={onTerminal?context=>{if(!frameLive())return;invalidateFrame();try{nextRef(context.next_ref);if(context.parent_decision_ref!==episode.decision_ref || context.snapshot_ref!==episode.followup!.snapshot_ref)throw new Error("Terminal target changed");onTerminal(structuredClone(context));}catch{setError("read");}}:undefined}/>;
  if(!error && episode && stage==="changes" && store.productChanges)return <MirayProductChangePanel store={store.productChanges} active={active} decisionRef={episode.decision_ref} onClose={refresh} requestLifetime={childLifetime}/>;
  if(!error && episode && stage==="state")return <MiraySkinStateCheckin kind="checkin" historyStorageConsented={false} completionMode="collect_for_followup" continueToAnalysis={false} onCancel={()=>move("use")} onComplete={value=>{if(!frameLive())return;invalidateFrame();try{
    validateFollowupObservation(episode,value);setObservation(structuredClone(value));setStage("review");
  }catch(failure){setObservation(null);setError(followupCompletionCode(failure));}}}/>;
  return <main className="miray-main miray-loop-panel">
    <button onClick={close}>‹ 홈으로</button><p className="miray-eyebrow" id="miray-loop-context" aria-hidden="true">지난 루틴 점검 이후</p><h1 ref={heading} tabIndex={-1} aria-describedby="miray-loop-context">실제 사용과 현재 상태 확인</h1>
    <p>권장안을 선택한 것과 실제 사용한 것은 따로 기록해요. 제품이나 루틴 편집만으로 사용했다고 판단하지 않아요.</p>
    {error && <section className="miray-card" role="alert"><p>{error==="time"?"변경을 시작한 날짜와 시간을 점검 이후부터 지금 사이로 입력해 주세요.":error.startsWith("F-C-")?"이번 답변을 기존 점검에 연결하지 못했어요. 이번 후속 상태 답변은 서버로 보내거나 저장하지 않았어요. 최신 이력을 확인한 뒤 이어가세요.":"이력 확인이나 저장을 완료하지 못했어요. 저장됐을 수도 있으므로 최신 이력을 확인한 뒤 이어가세요."}</p>{error.startsWith("F-C-") && <p>확인 코드: {error}</p>}<button className="miray-primary" disabled={busy} onClick={refresh}>최신 이력 확인</button></section>}
    {busy && <p role="status">이력을 확인하는 중이에요.</p>}
    {episode && !error && <>
      {episode.followup?<section className="miray-card" role="status"><h2>후속 상태를 저장했어요</h2><p>이전 상태, 직접 확인한 실제 사용, 이번 상태가 이력에 연결됐어요. 개선 여부나 제품의 원인을 자동 판단하지 않아요.</p>{onNextRequested?<button className="miray-primary" disabled={busy} onClick={()=>{if(!frameLive() || binding.pending)return;retire();onNextRequested();}}>다음 루틴 점검으로</button>:store.nextDecision?<button className="miray-primary" disabled={busy} onClick={()=>move("next")}>다음 루틴 점검으로</button>:<p>다음 루틴 점검은 필요한 정보와 엔진 연결을 확인한 뒤 진행할 수 있어요.</p>}</section>:stage==="review" && observation?<section className="miray-card">
        <h2>후속 상태를 이력에 저장할까요?</h2><p>방금 답한 피부 고민과 불편감을 이번 점검에 연결해 저장해요. 이전 답변을 현재 상태로 사용하지 않아요.</p>
        <p>다른 변화는 추가로 묻지 않았으며, 확인하지 않은 정보로 남겨요.</p>
        <button disabled={busy} onClick={()=>move("state")}>상태 다시 입력</button><button className="miray-primary" disabled={busy} onClick={save}>후속 상태 이력 저장</button>
      </section>:<>
        {question && <section className="miray-card" aria-labelledby="actual-use-question">
          <h2 id="actual-use-question">{productNamePresentation(question.product_name).name}을 지금 실제로 얼마나 사용하고 있나요?</h2>

          <p>빈도를 선택한 뒤 실제 사용 내용을 확인해 주세요. 권장 빈도는 자동 선택하지 않아요.</p>
          <label>현재 실제 사용 빈도<select aria-label="현재 실제 사용 빈도" disabled={busy} value={frequency} onChange={e=>{if(!frameLive() || binding.pending)return;invalidateFrame();setFrequency(e.target.value);setStarted("");}}><option value="" disabled>선택해 주세요</option>
            {numeric && config.frequency_values.map(v=><option key={v} value={v}>{v==="0"?"현재 사용하지 않음":`주 ${v}일`}</option>)}
            <option value="unknown">모름</option><option value="user_refused">답변하지 않음</option>
          </select></label>
          {!numeric && <p>이전 사용 빈도를 확인하지 못해 변경 여부를 판단할 수 없어요. 이번에는 확인하지 못한 답변으로 남겨요.</p>}
          {changed && <label>이 빈도로 사용하기 시작한 때<input aria-label="사용 빈도 변경 시작" type="datetime-local" value={started} onChange={e=>{if(frameLive() && !binding.pending){invalidateFrame();setStarted(e.target.value);}}} disabled={busy}/>{started && <span className="miray-loop-time-value">입력한 시작 시각: {started.replace("T"," ")}</span>}</label>}
          {frequency && !changed && !config.unconfirmed_values.includes(frequency) && <p>지금 확인한 빈도로 계속 사용하고 있다는 내용으로 기록해요.</p>}
          <button className="miray-primary" disabled={busy || !frequency || (changed && !started)} onClick={confirm}>{config.unconfirmed_values.includes(frequency)?"확인하지 못한 답변 기록":"실제 사용 내용 확인·저장"}</button>
        </section>}
        {store.productChanges && <button disabled={busy} onClick={()=>move("changes")}>제품 추가·교체·새 용기 사용 직접 기록</button>}
        {store.frequencyCorrections && episode.actual_actions.length>0 && <button disabled={busy} onClick={()=>move("frequency")}>확인한 사용 빈도와 입력값 비교</button>}
        <button className={question?undefined:"miray-primary"} disabled={busy} onClick={()=>move("state")}>현재 상태 확인{question?"만 계속":"으로 계속"}</button>
      </>}
      {episode.actual_actions.length>0 && <section className="miray-card"><h2>직접 확인한 실제 사용</h2><ul role="list">{episode.actual_actions.map(a=><li key={a.ref}><p>{`${productNamePresentation(a.product_name).name} · ${a.frequency===null?"제품 사용 종료":config.frequency_values.includes(a.frequency)?`주 ${a.frequency}일`:"빈도 미확인"}${a.action_type==="current_use_confirmed"?" · 현재 사용 확인, 시작일 미확인":""}`}</p></li>)}</ul></section>}
      {episode.unconfirmed_count>0 && <p>{`실제 사용을 확인하지 못한 답변 ${episode.unconfirmed_count}건이 있어요. 사용 완료로 판단하지 않아요.`}</p>}
      {episode.unsupported_count>0 && <p>{store.productChanges?"제품·용기 변경은 직접 기록 버튼으로 확인할 수 있어요. 구매 클릭만으로 사용 완료를 기록하지 않아요.":"제품 추가·교체·재구매에 대한 실제 사용 입력은 연결을 준비 중이에요. 구매 클릭만으로 사용 완료를 기록하지 않아요."}</p>}
    </>}
  </main>;
}
