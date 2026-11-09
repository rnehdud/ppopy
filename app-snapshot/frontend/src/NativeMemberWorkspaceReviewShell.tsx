import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import {useCallback,useLayoutEffect,useMemo,useRef,useState} from "react";
import policy from "../../skin_engine/config/app_native_member_shell_local.json";
import type {createNativeMemberWorkspaceLocal} from "./nativeMemberWorkspaceLocal";
import {confirmedAccountWithdrawal,type AccountWithdrawalResult} from "./appAccountWithdrawal";
import type {AppDeletionResult,AppLogoutResult} from "./appSessionTermination";
import {createAppExternalLinkRouter} from "./appExternalLinks";
import AppSettingsScreen from "./AppSettingsScreen";
import AppHistoryConsentPanel from "./AppHistoryConsentPanel";
import {useAppHistoryConsent} from "./useAppHistoryConsent";
import MirayClosedLoopConsentJourneyReviewPanel from "./MirayClosedLoopConsentJourneyReviewPanel";
import {useReviewLookupConnection} from "./useReviewLookupConnection";
import "./nativeMemberWorkspaceReviewShell.css";

type Workspace=Awaited<ReturnType<typeof createNativeMemberWorkspaceLocal>>;
type Screen="home"|"routine"|"explore"|"settings";
const links=createAppExternalLinkRouter({firstPartyOrigins:[],links:[]});
const noExternalLinks={async openExternal(){throw new Error("Local review has no external links");}};
const noServerDeletion=async ():Promise<AppDeletionResult>=>({state:"retryable_error"});
function admitted(context:string,verified:boolean){
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
    initial_screen:"home",admission:"external_original_workspace_and_separate_sensitive_consent_no_UI_proxy",
    retirement:"mask_all_screens_before_cleanup_receipt_no_revive",navigation:"detach_view_preserve_owner_no_automatic_lookup_save_or_actual_use",
    account:"explicit_confirmation_withdrawal_original_workspace_only",unmount:"detach_UI_only_external_owner_disposal_required",
    questions:"routine_state_and_safety_2_plus_conditional_1"};
  return context==="synthetic_test"&&verified===true&&Object.keys(policy).sort().join("|")===Object.keys(expected).sort().join("|")
    &&Object.entries(expected).every(([k,v])=>policy[k as keyof typeof policy]===v);
}

/** Unregistered UI host. The caller owns the native authority and disposes it
 * when leaving the account. React StrictMode effect cleanup only detaches UI;
 * a mount, navigation or boolean prop never authenticates/adopts a native owner. */
export default function NativeMemberWorkspaceReviewShell({workspace,deploymentContext,memberAndSensitiveConsentVerified,logout}:{
  workspace:Workspace;deploymentContext:"synthetic_test";memberAndSensitiveConsentVerified:boolean;
  logout:()=>Promise<AppLogoutResult>;
}){
  const [frame,setFrame]=useState(()=>({workspace,current:true,screen:policy.initial_screen as Screen,withdrawing:false,result:null as AccountWithdrawalResult|null}));
  const previous=useRef<{workspace:Workspace;admitted:boolean}|null>(null),mounted=useRef(false),owner=useRef(workspace);
  const allowed=admitted(deploymentContext,memberAndSensitiveConsentVerified);
  // Mask a replaced owner's complete subtree during render, before effects run.
  const current=frame.workspace===workspace&&frame.current&&allowed&&workspace.isCurrent();
  const viewLifetime=useMemo(()=>({workspace,allowed,current,screen:frame.screen,live:false}),[workspace,allowed,current,frame.screen]);
  const currentView=useRef<typeof viewLifetime|null>(null);
  useLayoutEffect(()=>{
    viewLifetime.live=current;currentView.current=viewLifetime;
    return()=>{viewLifetime.live=false;if(currentView.current===viewLifetime)currentView.current=null;};
  },[viewLifetime,current]);
  useLayoutEffect(()=>{
    mounted.current=true;owner.current=workspace;
    if(previous.current&&(previous.current.workspace!==workspace||previous.current.admitted&&!allowed))previous.current.workspace.invalidate();
    previous.current={workspace,admitted:allowed};
    setFrame(f=>f.workspace===workspace?{...f,current:f.current&&allowed&&workspace.isCurrent()}:
      {workspace,current:allowed&&workspace.isCurrent(),screen:"home",withdrawing:false,result:null});
    let unsubscribe=()=>{};
    if(allowed)try{unsubscribe=workspace.subscribeInvalidation(()=>{if(currentView.current)currentView.current.live=false;setFrame(f=>f.workspace===workspace?{...f,current:false}:f);});}
    catch{setFrame(f=>f.workspace===workspace?{...f,current:false}:f);}
    return()=>{mounted.current=false;unsubscribe();};
  },[workspace,allowed]);
  const go=(screen:Screen)=>{
    if(!viewLifetime.live || currentView.current!==viewLifetime || !current || !workspace.isCurrent() || screen===frame.screen)return;
    viewLifetime.live=false;setFrame(f=>({...f,screen}));
  };
  const withdraw=useCallback(async():Promise<AccountWithdrawalResult>=>{
    if(!viewLifetime.live || currentView.current!==viewLifetime || !mounted.current || owner.current!==workspace || !current || !workspace.isCurrent())return {state:"retryable_error"};
    setFrame(f=>({...f,withdrawing:true,result:null}));
    let result:AccountWithdrawalResult;
    try{result=await workspace.withdrawAccount();}catch{result={state:"retryable_error"};}
    if(mounted.current&&owner.current===workspace)setFrame(f=>f.workspace===workspace?{...f,withdrawing:false,result}:f);
    return result;
  },[workspace,current,viewLifetime]);
  const endSession=useCallback(async():Promise<AppLogoutResult>=>{
    if(!viewLifetime.live || currentView.current!==viewLifetime || !mounted.current || owner.current!==workspace || !current || !workspace.isCurrent())return {state:"retryable_error"};
    const result=await logout();
    if(["logged_out","server_revoked_local_cleanup_required","server_revoked_session_changed"].includes(result.state))workspace.invalidate();
    return result;
  },[workspace,current,logout,viewLifetime]);
  if(!current){
    const result=frame.workspace===workspace?frame.result:null,accepted=result&&confirmedAccountWithdrawal(result);
    return <main className="miray-main">
      <h1>{accepted?"탈퇴 요청을 접수했어요":"계정 연결을 다시 확인해 주세요"}</h1>
      {accepted?<>
        <p>계정 이용 중단은 확인됐어요. 전체 데이터 삭제 완료는 아직 확인되지 않았어요. 구독은 앱 스토어에서 별도로 확인해 주세요.</p>
        <p>{result.state==="account_closed"?"이 기기의 원 로그인 정보를 정리했어요.":result.state==="account_closed_session_changed"?"변경된 로그인 정보는 보존했어요. 앱을 다시 열어 확인해 주세요.":"기기 로그인 정보 정리가 필요해요. 앱을 다시 열어 확인해 주세요."}</p>
      </>:<p>이전 계정의 화면을 닫았어요. 확인한 계정으로 다시 연결해 주세요.</p>}
      {frame.workspace===workspace&&frame.withdrawing&&<p role="status">탈퇴 접수 결과와 기기 정리 상태를 확인하고 있어요.</p>}
      {result&&!accepted&&<p role="alert">탈퇴 접수를 확인하지 못했어요. 자동으로 다시 요청하지 않습니다.</p>}
    </main>;
  }
  return <>
    <nav className="native-member-review-nav" aria-label="로컬 계정 검토 화면">
      {([ ["home","홈"],["routine","루틴"],["explore","탐색"],["settings","마이"] ] as const).map(([screen,label])=>
        <button key={screen} type="button" disabled={frame.withdrawing} aria-current={frame.screen===screen?"page":undefined} onClick={()=>go(screen)}>{label}</button>)}
    </nav>
    {frame.screen==="home"&&<main className="miray-main"><h1>내 루틴을 이어서 확인해요</h1><p>현재 상태와 실제 사용 기록은 직접 확인해 주세요.</p></main>}
    {frame.screen==="routine"&&<MirayClosedLoopConsentJourneyReviewPanel connection={workspace.journey} active onClose={()=>go("home")}/>}
    {frame.screen==="explore"&&<LookupScreen connection={workspace.lookup}/>}
    {frame.screen==="settings"&&<AppSettingsLifetimeContext.Provider value={viewLifetime}><AppSettingsScreen subscription={{serverVerified:false}} subscriptionStatusStore={workspace.subscription} quotaStatusStore={workspace.quota}
      historyConsentControl={<HistorySettings connection={workspace.journey}/>}
      linkRouter={links} linkOpener={noExternalLinks} logout={endSession} withdrawAndDelete={noServerDeletion} withdrawAccount={withdraw}/></AppSettingsLifetimeContext.Provider>}
  </>;
}

function HistorySettings({connection}:{connection:Workspace["journey"]}){
  // Exclusive screen mounting reads the current server choice. Reading or
  // changing it retires prior journeys through the shared connection, while
  // preserving the separate account, lookup and subscription authorities.
  const control=useAppHistoryConsent(connection.consent,connection.isCurrent());
  return <AppHistoryConsentPanel control={control}/>;
}

function LookupScreen({connection}:{connection:Workspace["lookup"]}){
  const {state,...actions}=useReviewLookupConnection(connection),[query,setQuery]=useState("");
  const ready=state.status==="ready"&&!state.busy,phase=state.view?.phase;
  const result=state.response&&"result" in state.response?state.response.result:null;
  const start=state.response&&"start" in state.response?state.response.start:null;
  return <main className="miray-main"><h1>제품 탐색</h1>
    <form onSubmit={e=>{e.preventDefault();void actions.begin(query);}}>
      <label htmlFor="native-review-product-query">제품명과 용량</label>
      <input id="native-review-product-query" value={query} onChange={e=>setQuery(e.target.value)} disabled={!ready}/>
      <button type="submit" disabled={!ready||!["idle","terminal","uncertain"].includes(phase??"")||query.trim().length<2}>검색 시작</button>
    </form>
    <button type="button" disabled={!ready||phase!=="uncertain"} onClick={()=>void actions.recover()}>이전 검색 상태 확인</button>
    <button type="button" disabled={!ready||!["active","terminal"].includes(phase??"")} onClick={()=>void actions.read()}>검색 결과 확인</button>
    <button type="button" disabled={!ready||phase!=="active"} onClick={()=>void actions.cancel()}>검색 취소 요청</button>
    {state.status==="connecting"&&<p role="status">검색 연결을 확인하고 있어요.</p>}
    {state.busy&&<p role="status">요청 결과를 확인하고 있어요.</p>}
    {state.notice&&<p role="alert">{state.notice}</p>}
    {start?.allowed&&<p role="status">검색 요청을 접수했어요. 결과는 직접 확인해 주세요.</p>}
    {start?.allowed===false&&<p role="status">{start.status==="limit_reached"?"현재 이용 횟수를 모두 사용했어요.":"이미 진행 중인 검색을 확인해 주세요."}</p>}
    {result&&<section aria-label="확인이 필요한 검색 후보"><h2>제품 정보 확인이 필요해요</h2>
      <p>검색 결과를 제품 등록이나 실제 사용으로 기록하지 않아요.</p>
      <ul>{result.kind==="candidates"?result.data.candidates.map(c=><li key={c.id}>{c.title} {c.detail}</li>):result.data.map((d,i)=><li key={i}>{d.product_name} {d.option}</li>)}</ul>
    </section>}
  </main>;
}
