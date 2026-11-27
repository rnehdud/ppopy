import {Capacitor,registerPlugin} from "@capacitor/core";
import connectionPolicy from "../../skin_engine/config/app_withdrawal_test_connection_local.json";
import httpsPolicy from "../../skin_engine/config/app_provider_withdrawal_https_review.json";

/** TEST observations stay separate from AccountWithdrawalAcceptance. */
export type NativeWithdrawalTestObservation={accountClosed:boolean;providerAcknowledged:boolean;sdkMemoryCleared:boolean};
export type NativeWithdrawalTestState={attempted:boolean;phase:"idle"|"withdrawing"|"unconfirmed"|"observed"|"reading"|"status_failed"|"status_observed";observation:NativeWithdrawalTestObservation|null};
type NativePort={withdrawExplicit(options:Record<string,never>):Promise<unknown>;readOriginalStatusExplicit(options:Record<string,never>):Promise<unknown>};
const common={version:"1.0.0",scope:"isolated_native_invocation_review",operationally_eligible:false,whole_deletion_completed:false};
function object(value:unknown,fields:readonly string[]){
  if(!value || typeof value!=="object" || Array.isArray(value))throw new Error("Native TEST result unconfirmed");
  const r=value as Record<string,unknown>;
  if(Object.keys(r).sort().join("|")!==[...Object.keys(common),...fields].sort().join("|") ||
    Object.entries(common).some(([k,v])=>r[k]!==v) || new TextEncoder().encode(JSON.stringify(r)).byteLength>2048)throw new Error("Native TEST result unconfirmed");
  return r;
}
export function parseNativeWithdrawalTestObservation(value:unknown):NativeWithdrawalTestObservation {
  const r=object(value,["kind","account_closed_in_fixture","provider_acknowledged_in_fixture","SDK_memory_cleared_in_fixture","SDK_storage_erasure_confirmed","app_vault_erasure_confirmed"]);
  if(r.kind!=="withdrawal_fixture_observation" || r.account_closed_in_fixture!==true || typeof r.provider_acknowledged_in_fixture!=="boolean" ||
    typeof r.SDK_memory_cleared_in_fixture!=="boolean" || r.SDK_storage_erasure_confirmed!==false || r.app_vault_erasure_confirmed!==false)throw new Error("Native TEST result unconfirmed");
  return {accountClosed:true,providerAcknowledged:r.provider_acknowledged_in_fixture,sdkMemoryCleared:r.SDK_memory_cleared_in_fixture};
}
function parseStatus(value:unknown):NativeWithdrawalTestObservation {
  const r=object(value,["kind","title","account","connection","data_deletion","account_closed_in_record","provider_acknowledged_in_record","SDK_cleanup_confirmed"]);
  if(r.kind!=="withdrawal_record_observation" || typeof r.account_closed_in_record!=="boolean" || typeof r.provider_acknowledged_in_record!=="boolean" || r.SDK_cleanup_confirmed!==false ||
    r.title!=="탈퇴 처리 상태" || r.account!==(r.account_closed_in_record?"계정 이용 종료 기록을 확인했어요":"계정 이용 종료 기록이 아직 없어요") ||
    r.connection!==(r.provider_acknowledged_in_record?"연결 해제 응답이 기록돼 있어요. 기기 연결 상태는 아직 확인되지 않았어요.":"연결 해제 완료 여부를 아직 확인하지 못했어요.") ||
    r.data_deletion!=="전체 데이터 삭제 완료 여부는 아직 확인되지 않았어요.")throw new Error("Native TEST status unconfirmed");
  return {accountClosed:r.account_closed_in_record,providerAcknowledged:r.provider_acknowledged_in_record,sdkMemoryCleared:false};
}

async function boundedNativeReply(work:()=>Promise<unknown>,kind:"withdrawal"|"status"):Promise<unknown>{
  const requests=kind==="withdrawal"?connectionPolicy.maximum_original_session_requests:connectionPolicy.maximum_original_status_requests;
  const deadline=kind==="withdrawal"?connectionPolicy.native_reply_deadline_ms:connectionPolicy.status_reply_deadline_ms;
  if(!Number.isSafeInteger(deadline) || deadline<=0 || deadline!==requests*httpsPolicy.timeout_seconds*1000+connectionPolicy.completion_margin_ms)
    throw new Error("Native TEST deadline unconfirmed");
  let timer:ReturnType<typeof setTimeout>|undefined;
  try {
    return await Promise.race([work(),new Promise<never>((_resolve,reject)=>{
      timer=setTimeout(()=>reject(new Error("Native TEST result unconfirmed")),deadline);
    })]);
  }finally{if(timer!==undefined)clearTimeout(timer);}
}

/** Pure construction, explicit empty native calls only, no HTTP/vault fallback. */
export function createWithdrawalTestConnection(port:()=>NativePort,available:()=>boolean){
  let state:NativeWithdrawalTestState={attempted:false,phase:"idle",observation:null};
  let busy=false;const listeners=new Set<()=>void>();
  const publish=(value:NativeWithdrawalTestState)=>{state=Object.freeze(value);for(const f of [...listeners])f();};
  return {
    available,
    getSnapshot:()=>state,
    subscribe:(f:()=>void)=>{listeners.add(f);return()=>{listeners.delete(f);};},
    async withdraw(isCurrent:()=>boolean){
      if(state.attempted || busy || !listeners.size || !isCurrent())return;
      // Never recreate a dispatch after an error, navigation or panel remount.
      busy=true;publish({attempted:true,phase:"withdrawing",observation:null});
      try {
        if(!available())throw new Error("Native TEST unavailable");
        const observation=parseNativeWithdrawalTestObservation(await boundedNativeReply(()=>port().withdrawExplicit({}),"withdrawal"));
        publish({attempted:true,phase:"observed",observation});
      }catch{publish({attempted:true,phase:"unconfirmed",observation:null});}
      finally{busy=false;}
    },
    async readOriginalStatus(isCurrent:()=>boolean){
      if(!state.attempted || busy || !listeners.size || !isCurrent())return;
      // A previous observation does not describe this explicit read. In
      // particular, an expired/failed read must not keep the earlier pending
      // provider result on screen as though it had just been confirmed.
      busy=true;publish({attempted:true,phase:"reading",observation:null});
      try {
        if(!available())throw new Error("Native TEST unavailable");
        const observation=parseStatus(await boundedNativeReply(()=>port().readOriginalStatusExplicit({}),"status"));
        publish({attempted:true,phase:"status_observed",observation});
      }catch{publish({attempted:true,phase:"status_failed",observation:null});}
      finally{busy=false;}
    },
  };
}
export type WithdrawalTestConnection=ReturnType<typeof createWithdrawalTestConnection>;
export function createIOSWithdrawalTestConnection():WithdrawalTestConnection {
  let original:NativePort|null=null;
  return createWithdrawalTestConnection(()=>original??(original=registerPlugin<NativePort>("IOSWithdrawalInvocationReview")),
    ()=>{try{return Capacitor.isNativePlatform() && Capacitor.getPlatform()==="ios" && typeof Capacitor.isPluginAvailable==="function" && Capacitor.isPluginAvailable("IOSWithdrawalInvocationReview");}catch{return false;}});
}
