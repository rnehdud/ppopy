import {useContext,useEffect,useLayoutEffect,useMemo,useRef,useState} from "react";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import config from "../../skin_engine/config/app_history_consent.json";
import loginPlan from "../../skin_engine/config/app_login_plan.json";
import type {useAppHistoryConsent} from "./useAppHistoryConsent";
import "./appHistoryConsent.css";

export default function AppHistoryConsentPanel({control}: {control:Omit<ReturnType<typeof useAppHistoryConsent>,"storageLifetime">}) {
  const lifetime=useContext(AppSettingsLifetimeContext);
  const {status,busy,error,choose,refresh}=control;
  const binding=useMemo(()=>({lifetime,status,busy,error,choose,refresh,live:false,checked:false,confirmation:false}),[lifetime,status,busy,error,choose,refresh]);
  const currentBinding=useRef<typeof binding|null>(null);
  const [selection,setSelection]=useState<{binding:typeof binding;checked:boolean;confirmation:boolean}|null>(null);
  const current=selection?.binding===binding?selection:null;
  const checked=current?.checked??false,confirmWithdrawal=current?.confirmation??false;
  const [actionEpoch,setActionEpoch]=useState(0);
  const frame=useMemo(()=>({binding,current,actionEpoch}),[binding,current,actionEpoch]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const isLive=()=>binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding && currentFrame.current===frame;
  const isCurrent=()=>isLive() && !binding.busy && !binding.error;
  const consume=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const reset=()=>{consume();binding.checked=false;binding.confirmation=false;setSelection(null);setActionEpoch(value=>value+1);};
  useLayoutEffect(()=>{
    binding.live=true;currentBinding.current=binding;
    binding.checked=false;binding.confirmation=false;setSelection(null);
    return()=>{binding.live=false;binding.checked=false;binding.confirmation=false;if(currentBinding.current===binding)currentBinding.current=null;};
  },[binding]);
  const confirmButton=useRef<HTMLButtonElement>(null);
  const withdrawButton=useRef<HTMLButtonElement>(null);
  useEffect(()=>{if(confirmWithdrawal)confirmButton.current?.focus();},[confirmWithdrawal]);
  const notice=config.notice;
  const mergedBasis=(config as {signup_storage_basis?:{accepted_notice_key?:string}}).signup_storage_basis;
  const mergedSensitive=mergedBasis?.accepted_notice_key==="sensitive_information";
  const requiredAtSignup=loginPlan.protection_session.required_notice_keys.includes("history_storage") || mergedSensitive;
  return <section className="app-history-consent" aria-labelledby="app-history-consent-title" aria-busy={control.busy}>
    <h2 id="app-history-consent-title">{notice.title}</h2>
    <div className="app-history-consent-notice"><p>{notice.purpose}</p><p>{notice.items}</p><p>{notice.retention}</p><p>{notice.choice}</p></div>
    {control.busy && <p className="app-history-consent-status" role="status">이력 저장 동의를 확인하고 있어요.</p>}
    {control.error && <p role="alert">{control.failedChoice==="withdraw"
      ?"철회 처리 결과를 확인하지 못했어요. 자동으로 다시 요청하지 않아요. 이력 저장 동의를 다시 확인해 주세요."
      :"이력 저장 동의를 확인하지 못했어요. 확인 전에는 답변을 계정 이력에 저장하지 않아요."}</p>}
    {!control.busy && control.status?.state==="not_consented" && <>
      <p className="app-history-consent-status" role="status">이력 저장에 동의하지 않은 상태예요.</p>
      <label><input type="checkbox" checked={checked} onChange={event=>{if(!isCurrent())return;consume();binding.checked=event.target.checked;setSelection({binding,checked:binding.checked,confirmation:false});}}/> {mergedSensitive ? "위 내용을 확인하고 민감정보 수집·이용에 동의해요" : "위 내용을 확인하고 상태·루틴 이력 저장에 동의해요"}{!requiredAtSignup && " (선택)"}</label>
      <button className="app-history-consent-primary" type="button" disabled={!checked} onClick={()=>{if(!isCurrent() || !binding.checked || status?.state!=="not_consented")return;reset();choose("grant");}}>{mergedSensitive ? "민감정보 동의" : requiredAtSignup ? "이력 저장 동의" : "선택 동의 저장"}</button>
    </>}
    {!control.busy && control.status?.state==="consented" && <p className="app-history-consent-status app-history-consent-status-consented" role="status">상태·루틴 이력 저장에 동의했어요.</p>}
    {!control.busy && control.status?.state==="review_required" && <p className="app-history-consent-status" role="status">기존 동의 내용을 다시 확인해야 해요. 확인 전에는 새 이력을 저장하지 않아요.</p>}
    {!control.busy && control.status && control.status.state!=="not_consented" && !confirmWithdrawal &&
      <button ref={withdrawButton} type="button" onClick={()=>{if(!isCurrent())return;consume();binding.confirmation=true;setSelection({binding,checked:false,confirmation:true});}}>{mergedSensitive ? "민감정보 동의 철회" : "이력 저장 동의 철회"}</button>}
    {!control.busy && control.status && confirmWithdrawal && <div role="group" aria-label="이력 저장 동의 철회 확인">
      <p>{notice.withdrawal}</p>
      <button className="app-history-consent-primary app-history-consent-danger" ref={confirmButton} type="button" onClick={()=>{if(!isCurrent() || !binding.confirmation || !status || status.state==="not_consented")return;reset();choose("withdraw");}}>{mergedSensitive ? "철회하고 민감정보 파기 시작" : "철회하고 이력 파기 시작"}</button>
      <button type="button" onClick={()=>{if(!isCurrent())return;reset();queueMicrotask(()=>{
        // The consumed cancel frame cannot authorize another action. Focus
        // belongs to the still-current receipt and only its closed confirmation.
        if(binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding && !binding.busy && !binding.error && !binding.confirmation)withdrawButton.current?.focus();
      });}}>취소</button>
    </div>}
    {!control.busy && <button className={control.error?"app-history-consent-primary":undefined} type="button" onClick={()=>{if(!isLive())return;reset();refresh();}}>이력 저장 동의 다시 확인</button>}
  </section>;
}
