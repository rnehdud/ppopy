import {useCallback,useLayoutEffect,useMemo,useRef,useState} from "react";
import policy from "../../skin_engine/config/app_freemium.json";
import releaseScope from "../../skin_engine/config/app_release_scope.json";
import {parseMirayQuotaStatus,type MirayQuotaStatus,type MirayQuotaStatusStore} from "./mirayQuotaStatus";
import "./appQuotaStatus.css";

/** Optional display reader; counts never authorize a workflow or a purchase. */
export default function AppQuotaStatus({store,lifetime,subscriptionEnabled=true}:{store:MirayQuotaStatusStore;lifetime?:{live:boolean};subscriptionEnabled?:boolean}) {
  const binding=useMemo(()=>({store,lifetime,live:false,controller:null as AbortController|null}),[store,lifetime]);
  const currentBinding=useRef<typeof binding|null>(null);
  const [resolved,setResolved]=useState<{binding:typeof binding;status:MirayQuotaStatus|null;loading:boolean}|null>(null);
  const attempt=useRef(0);
  const pending=useRef<object|null>(null);
  const refresh=useCallback(()=>{
    if(!binding.live || currentBinding.current!==binding || pending.current)return;
    const id=++attempt.current;
    const controller=new AbortController();binding.controller=controller;
    const request={};pending.current=request;
    const isCurrent=()=>binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding && id===attempt.current;
    setResolved({binding,status:null,loading:true});
    // Cleanup can retire a queued read before it reaches the provider. In
    // StrictMode the same binding may be replayed, so the attempt also matters.
    void Promise.resolve().then(()=>isCurrent()?store.read({signal:controller.signal,isCurrent}):null).then(
      value=>{
        if(!isCurrent())return;
        const status=parseMirayQuotaStatus(value);
        setResolved({binding,status,loading:false});
      },
    ).catch(
      ()=>{if(isCurrent())setResolved({binding,status:null,loading:false});},
    ).finally(()=>{if(pending.current===request)pending.current=null;if(binding.controller===controller)binding.controller=null;});
  },[binding,store,lifetime]);
  useLayoutEffect(()=>{
    binding.live=true;currentBinding.current=binding;
    attempt.current+=1;pending.current=null;
    refresh();
    return()=>{
      binding.live=false;
      binding.controller?.abort();binding.controller=null;
      if(currentBinding.current===binding){currentBinding.current=null;attempt.current+=1;pending.current=null;}
    };
  },[binding,refresh]);
  // Render masks an old member before the connection-change effect runs.
  const current=resolved?.binding===binding?resolved:null;
  const frame=useMemo(()=>({binding,current}),[binding,current]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const refreshCurrent=()=>{
    if(!binding.live || (lifetime && !lifetime.live) || currentBinding.current!==binding || currentFrame.current!==frame || pending.current)return;
    currentFrame.current=null;refresh();
  };
  if(!current||current.loading)return <section className="app-quota-status app-quota-state" aria-label="이용 횟수" aria-busy="true"><h2>이용 횟수를 확인하고 있어요</h2></section>;
  if(!current.status)return <section className="app-quota-status app-quota-state" aria-label="이용 횟수"><h2>이용 횟수를 확인할 수 없어요</h2><button className="app-quota-refresh" type="button" onClick={refreshCurrent}>횟수 다시 확인</button></section>;
  const status=current.status;
  return <section className="app-quota-status" aria-labelledby="app-quota-title">
    <header className="app-quota-header"><h2 id="app-quota-title">남은 이용 횟수</h2>
    <p>{policy.plans[status.plan].label} 이용 중</p></header>
    <ul>{status.features.map(item=><li className="app-quota-feature" key={item.feature}>
      <strong>{policy.features[item.feature].label}</strong>
      <p className="app-quota-balance">{item.remaining===null?"횟수 제한 없이 이용해요":`${item.limit}회 중 ${item.remaining}회 남았어요`}</p>
      {item.pending>0&&<p className="app-quota-pending">처리 중인 {item.pending}회가 예약되어 있어요.</p>}
      <small>{`현재 제공 구간 종료: ${new Date(item.period_ends_at).toLocaleString("ko-KR",{timeZone:policy.timezone})} (한국 시간)`}</small>
    </li>)}</ul>
    <div className="app-quota-notes"><p>조회는 횟수를 사용하지 않아요. 실패하거나 취소된 작업은 처리 결과 확인 뒤 횟수를 돌려드려요.</p>
    <p>{subscriptionEnabled ? policy.copy.reset_detail : releaseScope.quota_period_detail}</p>
    <p>{policy.copy.fallback_detail}</p></div>
    <button className="app-quota-refresh" type="button" onClick={refreshCurrent}>횟수 다시 확인</button>
  </section>;
}
