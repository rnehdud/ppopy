/** Explicit local withdrawal seam; runtime supplies no default connection. */
import publicConfig from "../../skin_engine/config/app_public_account_withdrawal_contract.json";
import config from "../../skin_engine/config/app_account_withdrawal.json";
import clientPolicy from "../../skin_engine/config/app_account_withdrawal_client.json";
import loginPolicy from "../../skin_engine/config/app_login_plan.json";
import {clearSessionCredential,type SessionVault} from "./appSessionVault";

export type AccountWithdrawalAcceptance={schema_version:string;account_closed:true;history_deletion_scheduled:boolean;deletion_completed:false};
export type AccountWithdrawalClient=((token:string)=>Promise<unknown>) & {readonly acceptanceSchemaVersion?:string};
function checkedWithdrawalSchema(version:string):string {
  if(![config.version,publicConfig.version].includes(version))throw new Error("탈퇴 응답 계약을 확인해 주세요.");return version;
}
export function bindAccountWithdrawalClient(original:AccountWithdrawalClient,wrapped:AccountWithdrawalClient):AccountWithdrawalClient {
  Object.defineProperty(wrapped,"acceptanceSchemaVersion",{value:checkedWithdrawalSchema(original.acceptanceSchemaVersion??config.version),writable:false,configurable:false});return wrapped;
}
export class AccountWithdrawalError extends Error {
  constructor(public readonly status:number){super("탈퇴 접수 결과를 확인하지 못했어요.");}
}
export class AccountWithdrawalNotStartedError extends Error {}
export function accountWithdrawalNotStarted(status:number,headers:Headers,body:string):boolean {
  const policy=loginPolicy.client_database_resume_retry;
  if(policy.route_dispatch_performed!==false || status!==policy.retryable_status ||
    headers.get(policy.not_started_header)!==policy.not_started_header_value)return false;
  // Require a single code field. The independent server header remains required
  // even when a native JSON transport has already normalized the body.
  const match=body.match(/^\s*\{\s*"code"\s*:\s*("(?:[^"\\]|\\.)*")\s*\}\s*$/);
  if(!match)return false;
  try{return JSON.parse(match[1])===policy.retryable_error_code;}catch{return false;}
}
export function parseAccountWithdrawalAcceptance(value:unknown,schemaVersion:string=config.version):AccountWithdrawalAcceptance {
  checkedWithdrawalSchema(schemaVersion);
  if(!value||typeof value!=="object"||Array.isArray(value))throw new Error("탈퇴 응답을 확인해 주세요.");
  const record=value as Record<string,unknown>;
  if(Object.keys(record).sort().join("|")!==[...config.response_fields].sort().join("|")||record.schema_version!==schemaVersion||record.account_closed!==true||typeof record.history_deletion_scheduled!=="boolean"||record.deletion_completed!==false)throw new Error("탈퇴 응답을 확인해 주세요.");
  return record as AccountWithdrawalAcceptance;
}
function httpsBase(value:string):string {
  const url=new URL(value);
  if(url.protocol!=="https:"||url.username||url.password||url.search||url.hash)throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
}
export function createHttpAccountWithdrawalClient(fetcher:typeof fetch,options:{baseUrl:string;allowedBaseUrls:readonly string[];responseSchemaVersion?:string}):AccountWithdrawalClient {
  const base=httpsBase(options.baseUrl);
  if(!options.allowedBaseUrls.map(httpsBase).includes(base))throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  if(clientPolicy.version!=="1.0.0" || !Number.isSafeInteger(clientPolicy.reply_deadline_ms) || clientPolicy.reply_deadline_ms<=0 ||
    clientPolicy.automatic_retry!==false || clientPolicy.accept_late_response!==false)throw new Error("탈퇴 요청 시간 설정을 확인해 주세요.");
  const schemaVersion=checkedWithdrawalSchema(options.responseSchemaVersion??config.version);
  const client:AccountWithdrawalClient=async token=>{
    if(!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new Error("로그인 세션을 확인해 주세요.");
    const controller=new AbortController();
    let timer:ReturnType<typeof setTimeout>|undefined;
    // Native transports may ignore abort. The race also bounds response-body
    // reading and abandons late acceptance; the original dispatch fence stays.
    const deadline=new Promise<never>((_resolve,reject)=>{
      timer=setTimeout(()=>{controller.abort();reject(new AccountWithdrawalError(0));},clientPolicy.reply_deadline_ms);
    });
    try {
      return await Promise.race([deadline,(async()=>{
        const response=await fetcher(`${base}${config.http.path}`,{
          method:config.http.method,headers:{Authorization:`Bearer ${token}`},cache:"no-store",redirect:"error",credentials:"omit",signal:controller.signal,
        });
        if(controller.signal.aborted)throw new AccountWithdrawalError(0);
        if(response.status!==202){
          const body=await response.text();
          if(controller.signal.aborted)throw new AccountWithdrawalError(0);
          if(accountWithdrawalNotStarted(response.status,response.headers,body))throw new AccountWithdrawalNotStartedError();
          throw new AccountWithdrawalError(response.status);
        }
        const body=await response.json();
        if(controller.signal.aborted)throw new AccountWithdrawalError(0);
        return parseAccountWithdrawalAcceptance(body,schemaVersion);
      })()]);
    }finally{if(timer!==undefined)clearTimeout(timer);}
  };
  Object.defineProperty(client,"acceptanceSchemaVersion",{value:schemaVersion,writable:false,configurable:false});return client;
}
export type AccountWithdrawalResult=
  |{state:"signed_out"|"vault_unavailable"|"withdrawal_not_started"|"withdrawal_unconfirmed"|"retryable_error"}
  |{state:"account_closed"|"account_closed_local_cleanup_required"|"account_closed_session_changed";acceptance:AccountWithdrawalAcceptance};

export function confirmedAccountWithdrawal(result:AccountWithdrawalResult):AccountWithdrawalAcceptance|null {
  if(["account_closed","account_closed_local_cleanup_required","account_closed_session_changed"].includes(result.state)) {
    if(!("acceptance" in result))throw new Error("탈퇴 접수 결과를 확인해 주세요.");
    return parseAccountWithdrawalAcceptance(result.acceptance,result.acceptance.schema_version);
  }
  return null;
}

// This is a dispatch fence for the original credential in this JS process,
// never an authentication or deletion receipt. Keep it on the original vault
// when a screen supplies a shorter-lived scoped wrapper. A lost ACK must not
// become another DELETE merely because a screen or client was replaced.
type WithdrawalAttempt={acceptance:AccountWithdrawalAcceptance|null};
const withdrawalAttempts=new WeakMap<SessionVault,Map<string,WithdrawalAttempt>>();

export async function requestAppAccountWithdrawal(vault:SessionVault,client:AccountWithdrawalClient,attemptScope:SessionVault=vault,
  beforeLocalCleanup?:(acceptance:AccountWithdrawalAcceptance)=>void):Promise<AccountWithdrawalResult> {
  let credential;
  try{credential=await vault.load();}catch{return {state:"vault_unavailable"};}
  if(!credential)return {state:"signed_out"};
  let attempts=withdrawalAttempts.get(attemptScope);
  if(!attempts){attempts=new Map();withdrawalAttempts.set(attemptScope,attempts);}
  let attempt=attempts.get(credential.session_token);
  if(!attempt){
    attempt={acceptance:null};
    // Admission is synchronous and precedes the client call, including throws.
    attempts.set(credential.session_token,attempt);
    try{attempt.acceptance=Object.freeze({...parseAccountWithdrawalAcceptance(await client(credential.session_token),client.acceptanceSchemaVersion)});}
    catch(error){
      if(error instanceof AccountWithdrawalNotStartedError && attempts.get(credential.session_token)===attempt){
        attempts.delete(credential.session_token);
        return {state:"withdrawal_not_started"};
      }
      return {state:"withdrawal_unconfirmed"};
    }
  }
  // A pending or ambiguous attempt cannot authorize resubmission. Only a
  // complete cached receipt can authorize another original-value local cleanup.
  const acceptance=attempt.acceptance;
  if(!acceptance)return {state:"withdrawal_unconfirmed"};
  // A fresh view using the original credential must also retire its siblings
  // before delayed cleanup, even when acceptance came from the dispatch fence.
  try{beforeLocalCleanup?.(acceptance);}catch{/* Known acceptance cannot reopen or authorize another DELETE. */}
  const cleanup=await clearSessionCredential(vault,credential.session_token);
  return {state:cleanup === "cleared" ? "account_closed" : cleanup === "changed" ? "account_closed_session_changed" : "account_closed_local_cleanup_required",acceptance};
}
