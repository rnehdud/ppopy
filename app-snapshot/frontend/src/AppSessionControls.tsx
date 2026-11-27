import { createContext, useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
import type {ReactNode} from "react";

import type { AppDeletionResult, AppLogoutResult } from "./appSessionTermination";
import {confirmedAccountWithdrawal, type AccountWithdrawalResult} from "./appAccountWithdrawal";
import "./appSessionControls.css";

type Notice = { tone: "status" | "error"; title: string; detail: string };
export const NativeTestAccountActionContext=createContext<{blocked:boolean;isCurrent:()=>boolean}|null>(null);

function logoutNotice(result: AppLogoutResult): Notice {
  if (result.state === "logged_out") return {
    tone: "status",
    title: "이 기기에서 로그아웃했어요",
    detail: "서버 로그인 세션을 종료하고 기기의 세션을 제거했습니다. 서버 데이터는 삭제되지 않았습니다.",
  };
  if (result.state === "retryable_error") return {tone:"error", title:"로그아웃을 완료하지 못했어요", detail:"서버 확인에 실패해 기기 세션을 보존했습니다. 연결을 확인하고 다시 시도해 주세요."};
  if (result.state === "server_revoked_local_cleanup_required") return {tone:"error", title:"서버 세션은 종료됐지만 기기 정리가 필요해요", detail:"앱을 다시 시작한 뒤 기기 세션 제거를 다시 시도해 주세요."};
  if(result.state === "server_revoked_session_changed")return {tone:"error",title:"로그인 상태가 변경됐어요",detail:"요청에 사용한 서버 세션은 종료했습니다. 새 로그인 정보는 보존했으니 앱을 다시 열어 확인해 주세요."};
  return {tone:"error", title:"로그아웃을 완료하지 못했어요", detail:"기기 보안 저장소를 확인한 뒤 다시 시도해 주세요."};
}

function deletionNotice(result: AppDeletionResult): Notice {
  switch (result.state) {
    case "deleted": return {
      tone: "status",
      title: "데이터 삭제 요청을 처리했어요",
      detail: "서비스·연락처·민감정보 삭제 영수증을 확인하고 이 기기의 세션도 제거했습니다. 법정 거래 기록은 별도 기준에 따라 보관될 수 있습니다.",
    };
    case "signed_out": return {tone:"status", title:"로그인된 세션을 찾지 못했어요", detail:"서버 데이터 삭제 완료는 확인되지 않았습니다. 다시 인증하거나 보호 문의를 이용해 주세요."};
    case "deletion_unconfirmed": return {tone:"status", title:"삭제 완료를 확인하지 못했어요", detail:"세션 인증이 만료됐습니다. 다시 인증하거나 보호 문의에서 삭제 상태를 확인해 주세요."};
    case "deletion_unconfirmed_session_changed": return {tone:"error",title:"로그인 상태가 변경됐어요",detail:"새 로그인 정보를 보존했습니다. 이전 요청의 삭제 완료는 확인되지 않았습니다."};
    case "retryable_error": return {tone:"error", title:"삭제 요청을 완료하지 못했어요", detail:"기기 세션은 보존했습니다. 연결을 확인하고 다시 시도해 주세요."};
    case "server_deleted_local_cleanup_required": return {tone:"error", title:"서버 데이터는 삭제됐지만 기기 정리가 필요해요", detail:"삭제 영수증은 확인했습니다. 앱을 다시 시작한 뒤 기기 세션 제거를 다시 시도해 주세요."};
    case "server_deleted_session_changed": return {tone:"error",title:"삭제 영수증 확인 후 로그인 상태가 변경됐어요",detail:"이전 요청의 삭제 영수증은 확인했고 새 로그인 정보는 보존했습니다. 앱을 다시 열어 로그인 상태를 확인해 주세요."};
    case "vault_unavailable": return {tone:"error", title:"기기 보안 저장소를 확인할 수 없어요", detail:"앱을 다시 시작한 뒤 재시도해 주세요."};
  }
}

function withdrawalNotice(result:AccountWithdrawalResult,subscriptionEnabled:boolean):Notice {
  if(confirmedAccountWithdrawal(result))return {
    tone:result.state === "account_closed" ? "status" : "error",
    title:"탈퇴 요청을 접수했어요",
    detail:result.state === "account_closed" ? "계정 이용을 중단하고 이 기기의 세션을 정리했습니다. 전체 데이터 삭제 완료는 아직 확인되지 않았습니다." + (subscriptionEnabled ? " 구독은 앱 스토어에서 별도로 확인해 주세요." : "")
      : "계정 이용 중단은 확인됐지만 기기의 로그인 상태를 정리해야 합니다. 전체 데이터 삭제 완료는 아직 확인되지 않았습니다.",
  };
  if(result.state === "signed_out")return {tone:"error",title:"탈퇴 접수를 확인하지 못했어요",detail:"로그인 상태를 확인하거나 보호 문의를 이용해 주세요. 전체 데이터 삭제 완료는 확인되지 않았습니다."};
  if(result.state === "vault_unavailable")return {tone:"error",title:"탈퇴 접수를 확인하지 못했어요",detail:"기기 보안 저장소를 확인하지 못해 요청을 보내지 않았어요. 보안 저장소를 확인한 뒤 다시 시도해 주세요."};
  if(result.state === "withdrawal_not_started")return {tone:"error",title:"탈퇴 처리는 시작되지 않았어요",detail:"서버를 준비하고 있어요. 잠시 뒤 다시 시도해 주세요."};
  return {tone:"error",title:"탈퇴 접수를 확인하지 못했어요",detail:"이미 접수됐을 수 있어요. 같은 요청은 다시 보내지 않아요. 보호 문의에서 접수 여부를 확인해 주세요. 전체 데이터 삭제 완료는 확인되지 않았습니다."};
}

export default function AppSessionControls({
  logout,
  withdrawAndDelete,
  withdrawAccount,
  lifetime,
  subscriptionEnabled = true,
  withdrawalTestControl,
  dataConsentControl,
}: {
  dataConsentControl?: ReactNode;
  logout: () => Promise<AppLogoutResult>;
  withdrawAndDelete: () => Promise<AppDeletionResult>;
  /** Explicit account-closure acceptance, separate from a final deletion receipt. */
  withdrawAccount?: () => Promise<AccountWithdrawalResult>;
  /** Parent screen can retire issued actions before children unmount. */
  lifetime?: {live:boolean};
  subscriptionEnabled?: boolean;
  /** Explicit native TEST control; replaces legacy JS/HTTP deletion actions. */
  withdrawalTestControl?: ReactNode;
}) {
  // Function identities describe the supplied action contract, not proof of
  // authentication. A replaced contract requires its own final confirmation.
  const binding=useMemo(()=>({logout,withdrawAndDelete,withdrawAccount,lifetime,subscriptionEnabled,live:false,confirmation:null as object|null,withdrawalHeld:false}),[logout,withdrawAndDelete,withdrawAccount,lifetime,subscriptionEnabled]);
  const currentBinding=useRef<typeof binding|null>(null);
  type Frame={binding:typeof binding;confirmation:object|null;busy:"logout"|"delete"|null;notice:Notice|null;withdrawalHeld:boolean};
  const [frame,setFrame]=useState<Frame>(()=>({binding,confirmation:null,busy:null,notice:null,withdrawalHeld:false}));
  const visible=useMemo(()=>frame.binding===binding?frame:{binding,confirmation:null,busy:null,notice:null,withdrawalHeld:false},[frame,binding]);
  const {confirmation,busy,notice,withdrawalHeld}=visible;
  const confirmingDelete=Boolean(confirmation);
  const isCurrent=()=>binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding;
  const currentFrame=useRef<typeof visible|null>(null);
  useLayoutEffect(()=>{currentFrame.current=visible;return()=>{if(currentFrame.current===visible)currentFrame.current=null;};},[visible]);
  const frameLive=()=>isCurrent() && currentFrame.current===visible;
  const consume=()=>{if(currentFrame.current===visible)currentFrame.current=null;};
  const update=(changes:Partial<Omit<Frame,"binding">>)=>{
    if(isCurrent())setFrame(f=>f.binding===binding?{...f,...changes}:{binding,confirmation:null,busy:null,notice:null,withdrawalHeld:false,...changes});
  };
  const deleteTriggerRef = useRef<HTMLButtonElement>(null);
  const deleteConfirmRef = useRef<HTMLButtonElement>(null);
  const confirmationChanged = useRef(false);
  const pendingAction = useRef<object | null>(null);
  useLayoutEffect(()=>{
    binding.live=true;currentBinding.current=binding;pendingAction.current=null;
    setFrame({binding,confirmation:null,busy:null,notice:null,withdrawalHeld:false});
    return()=>{
      binding.live=false;binding.confirmation=null;
      if(currentBinding.current===binding){currentBinding.current=null;pendingAction.current=null;}
    };
  },[binding]);

  useEffect(() => {
    if (!confirmationChanged.current) return;
    (confirmingDelete ? deleteConfirmRef : deleteTriggerRef).current?.focus();
  }, [confirmingDelete]);

  const runLogout = async () => {
    if (!frameLive() || pendingAction.current) return;
    consume();
    const attempt = {}; pendingAction.current = attempt;
    update({busy:"logout",notice:null});
    try {
      const result = await logout();
      if (pendingAction.current === attempt) update({notice:logoutNotice(result)});
    }
    catch { if (pendingAction.current === attempt) update({notice:{tone:"error", title:"로그아웃을 완료하지 못했어요", detail:"잠시 뒤 다시 시도해 주세요."}}); }
    finally { if (pendingAction.current === attempt) {pendingAction.current = null; update({busy:null});} }
  };

  const runDelete = async () => {
    if (!frameLive() || pendingAction.current || !confirmation || binding.confirmation!==confirmation || withdrawAccount && binding.withdrawalHeld) return;
    consume();
    const attempt = {}; pendingAction.current = attempt;
    update({busy:"delete",notice:null});
    try {
      if(withdrawAccount) {
        binding.withdrawalHeld=true;update({withdrawalHeld:true});
        const result=await withdrawAccount();
        if(pendingAction.current !== attempt)return;
        if(result.state==="vault_unavailable" || result.state==="signed_out" || result.state==="withdrawal_not_started"){
          binding.withdrawalHeld=false;update({withdrawalHeld:false});
        }
        update({notice:withdrawalNotice(result,subscriptionEnabled)});
        if(confirmedAccountWithdrawal(result)){binding.confirmation=null;update({confirmation:null});}
        return;
      }
      const result = await withdrawAndDelete();
      if (pendingAction.current !== attempt) return;
      update({notice:deletionNotice(result)});
      if (["deleted","server_deleted_local_cleanup_required","server_deleted_session_changed"].includes(result.state)){binding.confirmation=null;update({confirmation:null});}
    } catch {
      if (pendingAction.current === attempt) update({notice:withdrawAccount ? withdrawalNotice({state:"withdrawal_unconfirmed"},subscriptionEnabled) : {tone:"error", title:"삭제 요청을 완료하지 못했어요", detail:"잠시 뒤 다시 시도하거나 보호 문의를 이용해 주세요."}});
    } finally { if (pendingAction.current === attempt) {pendingAction.current = null; update({busy:null});} }
  };

  return <section className="app-session-controls" aria-labelledby="app-session-controls-title" aria-busy={busy !== null}>
    <h2 id="app-session-controls-title">계정과 내 데이터</h2>
    {dataConsentControl && <details className="app-data-consent-management"><summary>저장 데이터·동의 관리</summary>{dataConsentControl}</details>}
    <div className="app-session-control-row">
      <div><h3>이 기기에서 로그아웃</h3><p>서버 로그인 세션과 기기 세션을 종료하고 계정 데이터는 유지합니다.</p></div>
      <button type="button" disabled={busy !== null} onClick={() => void runLogout()}>{busy === "logout" ? "로그아웃 중" : "로그아웃"}</button>
    </div>
    {withdrawalTestControl ? <NativeTestAccountActionContext.Provider value={{blocked:busy!==null,isCurrent:()=>frameLive()&&!pendingAction.current}}>{withdrawalTestControl}</NativeTestAccountActionContext.Provider> : <div className="app-session-control-row app-session-danger">
      <div><h3>{withdrawAccount ? "계정 탈퇴 요청" : "동의 철회 및 데이터 삭제"}</h3><p>서비스·연락처·민감정보 삭제를 서버에 요청합니다.{subscriptionEnabled && " 구독 관리는 앱 스토어에서 별도로 확인해야 합니다."}</p></div>
      {!confirmingDelete
        ? <button ref={deleteTriggerRef} type="button" disabled={busy !== null || withdrawalHeld} onClick={() => {
          if(!frameLive() || pendingAction.current || binding.withdrawalHeld)return;
          consume();
          confirmationChanged.current = true;const next={};binding.confirmation=next;update({confirmation:next,notice:null});
        }}>{withdrawAccount ? "탈퇴 확인" : "삭제 확인"}</button>
        : <div className="app-session-confirm" role="group" aria-label={withdrawAccount ? "계정 탈퇴 최종 확인" : "데이터 삭제 최종 확인"}>
          <h4>{withdrawAccount ? "탈퇴 전 확인해 주세요" : "삭제 전 확인해 주세요"}</h4>
          <p>{withdrawAccount ? "계정 이용을 중단하고 데이터 삭제를 요청합니다. 전체 삭제 완료는 별도 확인이 필요합니다." : "삭제 뒤 현재 문진과 결과는 복구할 수 없습니다."}</p>
          <button className="app-session-final-action" ref={deleteConfirmRef} type="button" disabled={busy !== null || withdrawalHeld} onClick={() => void runDelete()}>{busy === "delete" ? "요청 중" : withdrawAccount ? "탈퇴 요청" : "동의 철회하고 삭제"}</button>
          <button type="button" disabled={busy !== null} onClick={() => {
            if(!frameLive() || pendingAction.current || binding.confirmation!==confirmation)return;
            consume();
            confirmationChanged.current = true;binding.confirmation=null;update({confirmation:null});
          }}>취소</button>
        </div>}
    </div>}
    {notice && <div className={`app-session-notice ${notice.tone === "error" ? "app-session-notice-error" : ""}`} role={notice.tone === "error" ? "alert" : "status"}>
      <h3>{notice.title}</h3><p>{notice.detail}</p>
    </div>}
  </section>;
}
