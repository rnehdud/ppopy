import {useContext,useLayoutEffect,useMemo,useRef,useState} from "react";
import AppStoreKitPurchaseReview from "./AppStoreKitPurchaseReview";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import type {IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";

/** Explicit local integration screen. No installed app/native registration. */
export default function AppStoreKitSessionReview({connection,onInteractionStart}:{connection:IOSStoreKitSessionReviewConnection;onInteractionStart:()=>void}){
  const lifetime=useContext(AppSettingsLifetimeContext);
  const owner=useMemo(()=>({connection,lifetime,live:false,busy:false,controller:null as AbortController|null,port:null as Awaited<ReturnType<typeof connection.connectExplicit>>|null}),[connection,lifetime]);
  const current=useRef<typeof owner|null>(null);
  const [view,setView]=useState<{owner:typeof owner;state:"connecting"|"connected"|"error"}|null>(null);
  const frame=useMemo(()=>({owner,view}),[owner,view]);const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>owner.live && current.current===owner && (!owner.lifetime || owner.lifetime.live);
  useLayoutEffect(()=>{owner.live=true;current.current=owner;return()=>{
    owner.live=false;owner.controller?.abort();owner.port?.dispose();owner.port=null;
    if(current.current===owner)current.current=null;
  };},[owner]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const connect=()=>{
    if(!live() || currentFrame.current!==frame || owner.busy)return;
    currentFrame.current=null;
    owner.busy=true;owner.port?.dispose();owner.port=null;
    const controller=new AbortController();owner.controller=controller;
    const isCurrent=()=>live() && owner.controller===controller && !controller.signal.aborted;
    setView({owner,state:"connecting"});
    void Promise.resolve().then(async()=>{
      if(!isCurrent())return;
      const port=await owner.connection.connectExplicit({signal:controller.signal,isCurrent});
      if(!isCurrent()){port.dispose();return;}
      owner.port=port;setView({owner,state:"connected"});
    }).catch(()=>{if(isCurrent())setView({owner,state:"error"});}).finally(()=>{
      if(owner.controller===controller){owner.controller=null;owner.busy=false;}
    });
  };
  const active=view?.owner===owner?view:null;
  return <div className="app-store-purchase-review">
    {active?.state==="connected" && owner.port
      ?<AppStoreKitPurchaseReview port={owner.port} onInteractionStart={onInteractionStart}/>
      :<section className="app-subscription-status" aria-labelledby="app-store-connection-title" aria-busy={active?.state==="connecting"}>
        <h2 id="app-store-connection-title">플러스 구독</h2>
        <p>현재 로그인 상태로 구매 내역 연결을 확인해 주세요. 연결 확인만으로 구매나 복원을 진행하지 않아요.</p>
        {active?.state==="connecting" && <p role="status">구매 내역 연결을 확인하고 있어요.</p>}
        {active?.state==="error" && <p role="alert">연결을 확인하지 못했어요. 로그인 상태를 확인한 뒤 다시 시도해 주세요.</p>}
      </section>}
    <button type="button" className={active?.state==="connected"?"app-store-secondary":"app-store-primary"}
      disabled={active?.state==="connecting"} onClick={connect}>{active?.state==="connected"?"연결 다시 확인":"구독 연결 확인"}</button>
  </div>;
}
