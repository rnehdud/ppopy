import {useLayoutEffect,useMemo,useRef,useState} from "react";
import MirayClosedLoopEntryPanel from "./MirayClosedLoopEntryPanel";
import MirayClosedLoopPanel from "./MirayClosedLoopPanel";
import MirayTerminalNextReviewPanel from "./MirayTerminalNextReviewPanel";
import {assertJourneyReviewOnly,type ClosedLoopJourneyReviewStore} from "./mirayClosedLoopJourneyReview";
import type {ClosedLoopReviewStore} from "./mirayClosedLoop";
import type {TerminalUiReviewStore} from "./mirayClosedLoopTerminalUiReview";
import {nextRef,type NextDecisionContext} from "./mirayClosedLoopNext";

type Page={kind:"entry"}|{kind:"episode";store:ClosedLoopReviewStore;decisionRef?:string}|{kind:"terminal";store:TerminalUiReviewStore;context:NextDecisionContext};
/** Unregistered optional host. The caller verifies both consents; this does not
 * record consent, answer questions, or silently choose a new work item. */
export default function MirayClosedLoopJourneyReviewPanel({store,active,onClose,requestLifetime,expectedPortfolioRevision,initialPage="entry"}:{store:ClosedLoopJourneyReviewStore;active:boolean;onClose():void;requestLifetime?:{isCurrent():boolean};expectedPortfolioRevision?:number;initialPage?:"entry"|"episode"}){
  const binding=useMemo(()=>({store,active,requestLifetime,initialPage,expectedPortfolioRevision,live:false,pending:null as AbortController|null,lifetime:null as AbortController|null}),[store,active,requestLifetime,initialPage,expectedPortfolioRevision]);
  const owner=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;page:Page}|null>(null);
  const [blocked,setBlocked]=useState(false),[busy,setBusy]=useState(false);
  const [closed,setClosed]=useState(false);
  const previous=useRef<{store:ClosedLoopJourneyReviewStore;active:boolean}|null>(null);
  const page=active && !blocked && !closed && store.isCurrent() && loaded?.binding===binding?loaded.page:null;
  const frame=useMemo(()=>({binding,page,busy,blocked,closed}),[binding,page,busy,blocked,closed]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  // The selected page owns the child binding. A navigation busy frame retires
  // access immediately without rebinding the old page and starting another read.
  const pageLifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true) && !binding.lifetime?.signal.aborted && store.isCurrent() && loaded?.binding===binding && loaded.page===page && currentFrame.current?.binding===binding && currentFrame.current.page===page && !currentFrame.current.busy && !currentFrame.current.blocked && !currentFrame.current.closed;}catch{return false;}}}),[binding,store,loaded,page]);
  const frameLive=()=>live() && currentFrame.current===frame && !closed;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  useLayoutEffect(()=>{
    if(previous.current && (previous.current.store!==store || previous.current.active && !active))previous.current.store.invalidate();
    previous.current={store,active};
    const lifetime=new AbortController();binding.lifetime=lifetime;binding.live=true;owner.current=binding;setLoaded(null);setBusy(false);setBlocked(false);setClosed(false);
    const unsubscribe=store.subscribeInvalidation(()=>{if(!live())return;if(currentFrame.current?.binding===binding)currentFrame.current=null;lifetime.abort();binding.pending?.abort();binding.pending=null;setLoaded(null);setBlocked(true);setBusy(false);});
    // The parent's consent/view frame commits after the child's layout effect.
    let attached=true;
    const open=()=>{if(!attached || !live())return;try{assertJourneyReviewOnly();if(!store.isCurrent())throw new Error("Expired journey");setLoaded({binding,page:initialPage==="episode"?{kind:"episode",store:store.episode()}: {kind:"entry"}});}catch{setBlocked(true);}};
    if(active){if(requestLifetime)void Promise.resolve().then(open);else open();}
    // Effect replay (StrictMode) aborts this render but must not revoke the
    // same member connection. Explicit close/consent/store changes revoke it.
    return()=>{attached=false;unsubscribe();binding.live=false;lifetime.abort();binding.pending?.abort();binding.pending=null;binding.lifetime=null;if(owner.current===binding)owner.current=null;};
    // The committed connection owns its lifetime, independent of child pages.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const close=()=>{if(!frameLive())return;invalidateFrame();binding.lifetime?.abort();binding.pending?.abort();binding.pending=null;setLoaded(null);setBusy(false);setClosed(true);binding.live=false;owner.current=null;store.invalidate();onClose();};
  const reject=()=>{if(!frameLive())return;invalidateFrame();store.invalidate();setLoaded(null);setBlocked(true);};
  const navigate=async(next:()=>Page)=>{
    if(!frameLive() || !active || !page || busy || !store.isCurrent() || binding.pending || !binding.lifetime || binding.lifetime.signal.aborted)return;
    const lifetime=binding.lifetime,attempt=new AbortController();binding.pending=attempt;invalidateFrame();setBusy(true);
    try{assertJourneyReviewOnly();await store.assertCurrent(attempt.signal);lifetime.signal.throwIfAborted();attempt.signal.throwIfAborted();if(!live() || !store.isCurrent())return;assertJourneyReviewOnly();setLoaded({binding,page:next()});}
    catch{if(live() && !attempt.signal.aborted && !lifetime.signal.aborted){store.invalidate();setLoaded(null);setBlocked(true);}}
    finally{if(binding.pending===attempt){binding.pending=null;if(live())setBusy(false);}}
  };
  const episode=(decisionRef?:string)=>{
    if(!frameLive() || !page)return;
    try{nextRef(decisionRef!);}catch{reject();return;}
    void navigate(()=>({kind:"episode",store:store.episode(decisionRef),decisionRef}));
  };
  const existingEpisode=()=>{if(frameLive() && page?.kind==="entry")void navigate(()=>({kind:"episode",store:store.episode(undefined)}));};
  const terminal=(context:NextDecisionContext)=>{
    if(!frameLive() || page?.kind!=="episode")return;
    try{
      const fixed=structuredClone(context);
      if(!fixed || Object.keys(fixed).length!==4 || !["next_ref","parent_decision_ref","snapshot_ref","portfolio_revision"].every(key=>Object.hasOwn(fixed,key)))throw new Error("Exact terminal context required");
      [fixed.next_ref,fixed.parent_decision_ref,fixed.snapshot_ref].forEach(nextRef);
      if(new Set([fixed.next_ref,fixed.parent_decision_ref,fixed.snapshot_ref]).size!==3 || !Number.isSafeInteger(fixed.portfolio_revision) || fixed.portfolio_revision<0)throw new Error("Invalid terminal context");
      void navigate(()=>({kind:"terminal",store:store.terminal(structuredClone(fixed)),context:fixed}));
    }catch{reject();}
  };
  if(!page)return <main className="miray-main"><h1>점검 연결 확인</h1><p>계정과 별도 이력 저장 동의를 확인한 뒤 새로 연결해 주세요.</p><button disabled={closed} onClick={close}>닫기</button></main>;
  return <>
    {busy && <p role="status">같은 계정과 이력 연결을 확인하고 있어요.</p>}
    <div inert={busy}>{page.kind==="entry"?<MirayClosedLoopEntryPanel expectedPortfolioRevision={expectedPortfolioRevision} requestLifetime={pageLifetime} store={store.entry} active onClose={close} onEpisode={episode} onExistingEpisode={existingEpisode}/>:
      page.kind==="episode"?<MirayClosedLoopPanel store={page.store} active expectedDecisionRef={page.decisionRef} requestLifetime={pageLifetime} onClose={close} onTerminal={terminal} onCompleted={episode}/>:
      <MirayTerminalNextReviewPanel requestLifetime={pageLifetime} store={page.store} terminalNextRef={page.context.next_ref} active onClose={close} onEpisode={episode}/>}</div>
  </>;
}
