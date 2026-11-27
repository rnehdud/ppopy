import {useLayoutEffect,useMemo,useRef,useState} from "react";
import { presentSubscriptionStatus, type SubscriptionDisplayState } from "./subscriptionPresentation";

export default function AppSubscriptionStatus({
  serverVerified,
  state,
  loading = false,
  onManage,
  onRetry,
}: {
  serverVerified: boolean;
  state?: SubscriptionDisplayState;
  loading?: boolean;
  onManage?: () => void;
  onRetry?: () => void;
}) {
  const [actionEpoch,setActionEpoch]=useState(0);
  const frame=useMemo(()=>({serverVerified,state,loading,onManage,onRetry,actionEpoch}),[serverVerified,state,loading,onManage,onRetry,actionEpoch]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  if (loading) return <section className="app-subscription-status app-subscription-neutral" aria-labelledby="app-subscription-status-title">
    <p className="app-subscription-label">구독 상태</p>
    <h2 id="app-subscription-status-title">구독 상태를 확인하고 있어요</h2>
    <p>계정에 연결된 구독 상태를 서버에서 확인합니다.</p>
  </section>;
  const presentation = presentSubscriptionStatus({server_verified:typeof serverVerified==="boolean" ? serverVerified : false, state:typeof serverVerified==="boolean" ? state : undefined});
  const action = presentation.action === "manage_subscription"
    ? {label:"구독 관리 열기", run:onManage}
    : presentation.action === "retry_status"
      ? {label:"상태 다시 확인", run:onRetry}
      : null;
  return <section className={`app-subscription-status app-subscription-${presentation.tone}`} aria-labelledby="app-subscription-status-title">
    <p className="app-subscription-label">구독 상태</p>
    <h2 id="app-subscription-status-title">{presentation.title}</h2>
    <p>{presentation.detail}</p>
    {action && <button type="button" disabled={!action.run} onClick={()=>{
      if(currentFrame.current!==frame || !action.run)return;
      currentFrame.current=null;setActionEpoch(value=>value+1);action.run();
    }}>{action.label}</button>}
  </section>;
}
