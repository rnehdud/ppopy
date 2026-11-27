import {useContext,useLayoutEffect,useRef,useState,useSyncExternalStore} from "react";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import {NativeTestAccountActionContext} from "./AppSessionControls";
import type {WithdrawalTestConnection} from "./iosWithdrawalTestConnection";
import "./appSessionControls.css";

/** Explicit TEST display: never manufactures the operating deletion receipt. */
export default function NativeWithdrawalTestControl({connection}:{connection:WithdrawalTestConnection}){
  const state=useSyncExternalStore(connection.subscribe,connection.getSnapshot),parent=useContext(AppSettingsLifetimeContext);
  const sibling=useContext(NativeTestAccountActionContext);
  const [confirming,setConfirming]=useState(false),live=useRef(false),confirmation=useRef(false);
  useLayoutEffect(()=>{live.current=true;return()=>{live.current=false;confirmation.current=false;};},[connection]);
  useLayoutEffect(()=>{if(sibling?.blocked){confirmation.current=false;setConfirming(false);}},[sibling?.blocked]);
  const current=()=>live.current&&(!parent||parent.live)&&(!sibling||sibling.isCurrent());
  const busy=state.phase==="withdrawing"||state.phase==="reading";
  const observed=state.observation;
  return <section className="app-session-controls" aria-labelledby="native-test-withdrawal-title" aria-busy={busy}>
    <h2 id="native-test-withdrawal-title">{state.attempted?"TEST 탈퇴 처리 상태":"계정 탈퇴 요청"}</h2>
    {!state.attempted?<div className="app-session-control-row app-session-danger">
      <p>현재 로그인한 계정의 이용 중단과 데이터 삭제를 요청합니다. 전체 삭제 완료는 별도 확인이 필요합니다.</p>
      {!connection.available()&&<p role="alert">탈퇴 요청 연결을 준비하지 못했어요. 요청을 보내지 않았어요.</p>}
      {!confirming?<button type="button" disabled={!connection.available()||sibling?.blocked} onClick={()=>{if(current()){confirmation.current=true;setConfirming(true);}}}>탈퇴 확인</button>:
        <div className="app-session-confirm" role="group" aria-label="계정 탈퇴 최종 확인">
          <h3>탈퇴 전 확인해 주세요</h3><p>계정 이용을 중단하고 데이터 삭제를 요청합니다. 현재 로그인 상태로 요청하며, 추가 로그인은 필요하지 않습니다.</p>
          <button type="button" disabled={!connection.available()||sibling?.blocked} onClick={()=>{if(!current()||!confirmation.current)return;confirmation.current=false;void connection.withdraw(current);}}>탈퇴 요청</button>
          <button type="button" onClick={()=>{if(current()){confirmation.current=false;setConfirming(false);}}}>취소</button>
        </div>}
    </div>:<>
      {state.phase==="withdrawing"&&<p role="status">탈퇴 접수 결과를 확인하고 있어요. 같은 요청은 다시 보내지 않아요.</p>}
      {state.phase==="unconfirmed"&&<p role="alert">탈퇴 접수를 확인하지 못했어요. 같은 요청을 다시 보내지 않고 기존 처리 상태만 확인할 수 있어요.</p>}
      {state.phase==="reading"&&<p role="status">기존 탈퇴 처리 상태를 확인하고 있어요.</p>}
      {state.phase==="status_failed"&&<p role="alert">상태를 확인하지 못했어요. 탈퇴 요청을 다시 보내지 않았어요.</p>}
      {observed&&<div role="status"><h3>{observed.accountClosed?"TEST 계정 이용 종료 기록을 확인했어요":"계정 이용 종료 기록이 아직 없어요"}</h3>
        <p>{observed.providerAcknowledged?"연결 해제 응답이 기록돼 있어요.":"연결 해제 완료 여부는 아직 확인되지 않았어요."}</p></div>}
      <p>전체 데이터 삭제 완료는 아직 확인되지 않았어요. 이 기기의 로그인 정보 정리 완료도 아직 확인되지 않았어요.</p>
      <button type="button" disabled={busy} onClick={()=>void connection.readOriginalStatus(current)}>탈퇴 처리 상태 확인</button>
    </>}
  </section>;
}
