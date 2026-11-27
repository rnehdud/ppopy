import {useContext,useCallback,useLayoutEffect,useMemo,useRef,useState} from "react";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import policy from "../../skin_engine/config/app_freemium.json";
import CareResult from "./CareResult";
import {parseMirayRoutineDelivery,type MirayRoutineDelivery,type MirayRoutineResultStore} from "./mirayRoutineResult";

/** Explicit sensitive read. Never automatically fetch, recalculate or persist in browser storage. */
export default function AppRoutineResult({store}:{store:MirayRoutineResultStore}) {
  const lifetime=useContext(AppSettingsLifetimeContext);
  const binding=useMemo(()=>({store,lifetime,live:false,controller:null as AbortController|null}),[store,lifetime]);
  const currentBinding=useRef<typeof binding|null>(null);
  const [resolved,setResolved]=useState<{binding:typeof binding;delivery:MirayRoutineDelivery|null;loading:boolean}|null>(null);
  const attempt=useRef(0);const pending=useRef<object|null>(null);
  const current=resolved?.binding===binding?resolved:null;
  const frame=useMemo(()=>({binding,current}),[binding,current]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const clear=useCallback(()=>{
    if(!binding.live || (lifetime && !lifetime.live) || currentBinding.current!==binding || currentFrame.current!==frame)return;
    currentFrame.current=null;attempt.current+=1;binding.controller?.abort();binding.controller=null;pending.current=null;setResolved(null);
  },[binding,lifetime,frame]);
  useLayoutEffect(()=>{
    binding.live=true;currentBinding.current=binding;
    attempt.current+=1;pending.current=null;setResolved(null);
    return()=>{
      binding.live=false;
      binding.controller?.abort();binding.controller=null;
      if(currentBinding.current===binding){currentBinding.current=null;attempt.current+=1;pending.current=null;}
    };
  },[binding]);
  const refresh=()=>{
    if(!binding.live || (lifetime && !lifetime.live) || currentBinding.current!==binding || currentFrame.current!==frame || pending.current)return;
    currentFrame.current=null;
    const id=++attempt.current;const request={};pending.current=request;
    const controller=new AbortController();binding.controller=controller;
    const isCurrent=()=>binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding && id===attempt.current;
    setResolved({binding,delivery:null,loading:true});
    // A screen/account can retire the queued read before it reaches the store.
    void Promise.resolve().then(()=>isCurrent()?store.read({signal:controller.signal,isCurrent}):null).then(
      value=>{if(isCurrent())setResolved({binding,delivery:parseMirayRoutineDelivery(value),loading:false});},
    ).catch(
      ()=>{if(isCurrent())setResolved({binding,delivery:null,loading:false});},
    ).finally(()=>{if(pending.current===request)pending.current=null;if(binding.controller===controller)binding.controller=null;});
  };
  return <section className="app-routine-result" aria-label="최근 저장된 점검 결과">
    <h2>최근 저장된 점검 결과</h2>
    <p>마지막으로 완료해 저장한 결과예요. 현재 제품이나 피부 상태로 다시 계산한 결과가 아니에요.</p>
    <p>결과를 다시 불러오는 데에는 이용 횟수를 사용하지 않아요.</p>
    <button type="button" disabled={current?.loading} onClick={refresh}>{current?.loading?"결과를 불러오고 있어요":"최근 결과 불러오기"}</button>
    {current&&!current.loading&&!current.delivery&&<p role="status">저장된 점검 결과를 불러오지 못했어요. 로그인과 기록 보관 동의 상태를 확인한 뒤 다시 시도해 주세요.</p>}
    {current?.delivery?.state==="unavailable"&&<p role="status">지금 불러올 수 있는 저장된 결과가 없어요.</p>}
    {current?.delivery?.state==="available"&&<>
      <p>점검 완료: {new Date(current.delivery.completed_at).toLocaleString("ko-KR",{timeZone:policy.timezone})} (한국 시간)</p>
      <button type="button" onClick={clear}>결과 닫기</button>
      <CareResult envelope={current.delivery.result} label="저장한 과거 점검 결과"/>
    </>}
  </section>;
}
