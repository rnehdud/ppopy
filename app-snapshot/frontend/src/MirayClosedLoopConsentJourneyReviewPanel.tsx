import {useCallback,useLayoutEffect,useMemo,useRef,useState} from "react";
import AppHistoryConsentPanel from "./AppHistoryConsentPanel";
import {useAppHistoryConsent} from "./useAppHistoryConsent";
import MirayClosedLoopJourneyReviewPanel from "./MirayClosedLoopJourneyReviewPanel";
import MiraySkinStateCheckin from "./MiraySkinStateCheckin";
import {assertConsentJourneyReviewOnly,type ConsentJourneyReviewConnection} from "./mirayClosedLoopConsentJourneyReview";
import type {ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";

/** Unregistered review host. active means the caller independently verified
 * membership and sensitive-information consent. Optional history is separate. */
export default function MirayClosedLoopConsentJourneyReviewPanel({connection,active,onClose}:{connection:ConsentJourneyReviewConnection;active:boolean;onClose():void}){
  const binding=useMemo(()=>({connection,active,live:false,pending:null as AbortController|null}),[connection,active]);
  const owner=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;store:ClosedLoopJourneyReviewStore}|null>(null);
  const [ephemeral,setEphemeral]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState(false),[blocked,setBlocked]=useState(false);
  const [closed,setClosed]=useState(false);
  const previous=useRef<{connection:ConsentJourneyReviewConnection;active:boolean}|null>(null);
  const usable=active && !blocked && !closed && connection.isCurrent();
  const control=useAppHistoryConsent(connection.consent,usable);
  const {busy:consentBusy,error:consentError,status:consentStatus,refresh:refreshConsent,choose:chooseConsent}=control;
  const live=useCallback(()=>binding.live && owner.current===binding,[binding]);
  const journey=usable && control.storageConsented && loaded?.binding===binding && loaded.store.isCurrent()?loaded.store:null;
  const frame=useMemo(()=>({binding,journey,ephemeral,busy,error,blocked,closed,usable,status:control.status,consentBusy:control.busy,consentError:control.error,refresh:control.refresh,choose:control.choose}),[binding,journey,ephemeral,busy,error,blocked,closed,usable,control.status,control.busy,control.error,control.refresh,control.choose]);
  const currentFrame=useRef<typeof frame|null>(null);
  const frameLive=useCallback(()=>live() && currentFrame.current===frame && !closed,[live,frame,closed]);
  const invalidateFrame=useCallback(()=>{if(currentFrame.current===frame)currentFrame.current=null;},[frame]);
  const clear=useCallback(()=>{
    if(!live())return;
    binding.pending?.abort();binding.pending=null;connection.closeJourney();setLoaded(null);setEphemeral(false);setBusy(false);
  },[binding,connection,live]);
  useLayoutEffect(()=>{
    if(previous.current && (previous.current.connection!==connection || previous.current.active && !active))previous.current.connection.invalidate();
    previous.current={connection,active};binding.live=true;owner.current=binding;setLoaded(null);setEphemeral(false);setBusy(false);setError(false);setBlocked(false);setClosed(false);
    const unsubscribe=connection.subscribeInvalidation(()=>{if(owner.current!==binding || !binding.live)return;if(currentFrame.current?.binding===binding)currentFrame.current=null;binding.pending?.abort();binding.pending=null;setLoaded(null);setEphemeral(false);setBusy(false);setBlocked(true);});
    try{assertConsentJourneyReviewOnly();}catch{connection.invalidate();setBlocked(true);}
    return()=>{unsubscribe();binding.live=false;binding.pending?.abort();binding.pending=null;if(owner.current===binding)owner.current=null;connection.closeJourney();};
  },[binding,connection,active]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{
    if(!usable || control.busy || control.error || !control.storageConsented){binding.pending?.abort();binding.pending=null;connection.closeJourney();setLoaded(null);setBusy(false);}
  },[binding,connection,usable,control.busy,control.error,control.storageConsented]);
  const open=async()=>{
    if(!frameLive() || !usable || !connection.isCurrent() || !control.storageConsented || !control.status || busy || binding.pending)return;
    const attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);setError(false);setEphemeral(false);
    try{const store=await connection.openJourney(structuredClone(control.status),attempt.signal);attempt.signal.throwIfAborted();if(!live() || !connection.isCurrent())return;assertConsentJourneyReviewOnly();if(!store.isCurrent())throw new Error("Expired journey");setLoaded({binding,store});}
    catch{if(!attempt.signal.aborted && live()){connection.closeJourney();setLoaded(null);setError(true);}}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  const close=()=>{if(!frameLive())return;invalidateFrame();clear();binding.live=false;owner.current=null;setClosed(true);connection.invalidate();onClose();};
  const openEphemeral=()=>{
    if(!frameLive() || !usable || !connection.isCurrent() || control.busy || busy || binding.pending)return;
    invalidateFrame();clear();setError(false);
    try{assertConsentJourneyReviewOnly();if(!connection.isCurrent())throw new Error("Expired connection");setEphemeral(true);}
    catch{connection.invalidate();setBlocked(true);}
  };
  const refresh=useCallback(()=>{if(!frameLive() || consentBusy)return;invalidateFrame();clear();setError(false);refreshConsent();},[frameLive,invalidateFrame,clear,consentBusy,refreshConsent]);
  const choose=useCallback((...args:Parameters<typeof chooseConsent>)=>{if(!frameLive() || consentBusy || consentError || !consentStatus)return;invalidateFrame();clear();setError(false);chooseConsent(...args);},[frameLive,invalidateFrame,clear,consentBusy,consentError,consentStatus,chooseConsent]);
  const leaveChild=()=>{if(!frameLive())return;invalidateFrame();clear();};
  const finishEphemeral=()=>{if(!frameLive() || !ephemeral)return;invalidateFrame();setEphemeral(false);};
  if(!usable)return <main className="miray-main"><h1>계정과 동의를 확인해 주세요</h1><p>확인한 계정으로 다시 연결해 주세요.</p><button disabled={closed} onClick={close}>닫기</button></main>;
  const panelControl={...control,refresh,choose};
  const Container=journey || ephemeral?"section":"main";
  return <>
    <Container className="miray-main" aria-label="상태·루틴 점검 연결">
      {!journey && !ephemeral && <h1>상태·루틴 점검</h1>}
      <button onClick={close}>닫기</button>
      {busy && <p role="status">점검 연결을 확인하고 있어요.</p>}
      {error && <p role="alert">점검 연결을 확인하지 못했어요. 이력 저장 동의를 다시 확인해 주세요.</p>}
      {!journey && !ephemeral && <>
        <button disabled={!control.storageConsented || busy} onClick={()=>void open()}>저장된 이력으로 점검 열기</button>
        <button disabled={control.busy || busy} onClick={openEphemeral}>이력 저장 없이 현재 상태 확인</button>
      </>}
      {journey || ephemeral?<details><summary>이력 저장 설정</summary><AppHistoryConsentPanel control={panelControl}/></details>:<AppHistoryConsentPanel control={panelControl}/>}
    </Container>
    {journey && <MirayClosedLoopJourneyReviewPanel store={journey} active onClose={leaveChild}/>}
    {ephemeral && <MiraySkinStateCheckin historyStorageConsented={false} continueToAnalysis={false} questionProfile="routine_state_and_safety" onComplete={finishEphemeral} onCancel={finishEphemeral}/>}
  </>;
}
