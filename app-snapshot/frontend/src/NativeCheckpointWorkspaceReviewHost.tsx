import {useLayoutEffect,useRef,useState,type ComponentProps} from "react";
import policy from "../../skin_engine/config/app_native_checkpoint_workspace_host_local.json";
import NativeMemberWorkspaceReviewShell from "./NativeMemberWorkspaceReviewShell";

type ShellProps=ComponentProps<typeof NativeMemberWorkspaceReviewShell>;
type Workspace=ShellProps["workspace"];
type Recovery=(signal:AbortSignal)=>Promise<Workspace>;
const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,public_enabled:false,native_plugin_registered:false,
  activation:"explicit_click_after_original_workspace_retirement",admission:"external_native_recovery_then_distinct_registered_workspace",
  mount:"no_recovery_no_storage_no_http",late_result:"retire_dispose_on_abort_unmount_or_original_replacement",
  failure:"hold_original_intent_no_reset_no_automatic_retry"};
const configured=Object.keys(policy).sort().join("|")===Object.keys(expected).sort().join("|")&&
  Object.entries(expected).every(([k,v])=>policy[k as keyof typeof policy]===v);
async function closeCandidate(workspace:Workspace){workspace.invalidate();await workspace.dispose().catch(()=>{});}

/** Unregistered synthetic host. Recovery belongs to the external native owner:
 * it must authenticate the same original context, settle only the exact stored
 * reservation, retire its recovery owner, and create a distinct observed owner.
 * This UI never creates storage, clears an intent, or proves native identity. */
export default function NativeCheckpointWorkspaceReviewHost({workspace,recoverOriginalWorkspace,...props}:ShellProps&{
  recoverOriginalWorkspace:Recovery;
}){
  const [frame,setFrame]=useState(()=>({source:workspace,workspace,busy:false,failed:false,current:workspace.isCurrent()}));
  const currentSource=useRef(workspace),mounted=useRef(false),request=useRef<AbortController|null>(null),adopted=useRef<Workspace|null>(null);
  // Prop replacement masks the old subtree during render, before cleanup.
  const shown=frame.source===workspace?frame.workspace:workspace;
  const allowed=configured&&props.deploymentContext==="synthetic_test"&&props.memberAndSensitiveConsentVerified;
  const current=allowed&&frame.source===workspace&&frame.current&&shown.isCurrent();
  useLayoutEffect(()=>{
    if(currentSource.current!==workspace)currentSource.current.invalidate();
    mounted.current=true;currentSource.current=workspace;
    setFrame(f=>f.source===workspace?f:{source:workspace,workspace,busy:false,failed:false,current:workspace.isCurrent()});
    return()=>{
      mounted.current=false;request.current?.abort();request.current=null;
      const old=adopted.current;adopted.current=null;if(old)void closeCandidate(old);
    };
  },[workspace]);
  useLayoutEffect(()=>{
    if(!allowed){request.current?.abort();request.current=null;shown.invalidate();
      const old=adopted.current;adopted.current=null;if(old)void closeCandidate(old);
      setFrame(f=>f.source===workspace?{...f,current:false,busy:false}:f);return;}
    try{return shown.subscribeInvalidation(()=>setFrame(f=>f.source===workspace&&f.workspace===shown?{...f,current:false}:f));}
    catch{setFrame(f=>f.source===workspace&&f.workspace===shown?{...f,current:false}:f);}
  },[workspace,shown,allowed]);
  const recover=async()=>{
    if(!allowed||current||request.current||currentSource.current!==workspace)return;
    const controller=new AbortController();request.current=controller;
    workspace.invalidate();shown.invalidate();
    const prior=adopted.current;adopted.current=null;if(prior)await closeCandidate(prior);
    setFrame(f=>f.source===workspace?{...f,busy:true,failed:false,current:false}:f);
    let candidate:Workspace|null=null;
    try{
      if(controller.signal.aborted||!mounted.current||currentSource.current!==workspace)return;
      candidate=await recoverOriginalWorkspace(controller.signal);
      if(candidate===workspace||candidate===shown||!candidate.isCurrent())throw new Error("Original native recovery unavailable");
      if(controller.signal.aborted||!mounted.current||currentSource.current!==workspace){await closeCandidate(candidate);return;}
      adopted.current=candidate;setFrame({source:workspace,workspace:candidate,busy:false,failed:false,current:true});
    }catch{
      if(candidate&&candidate!==workspace&&candidate!==shown)await closeCandidate(candidate);
      if(!controller.signal.aborted&&mounted.current&&currentSource.current===workspace)setFrame(f=>f.source===workspace?{...f,busy:false,failed:true,current:false}:f);
    }finally{if(request.current===controller)request.current=null;}
  };
  if(current)return <NativeMemberWorkspaceReviewShell {...props} workspace={shown}/>;
  return <main className="miray-main"><h1>계정 연결을 다시 확인해 주세요</h1>
    <p>이전 화면을 닫았어요. 저장된 검색을 확인한 뒤 다시 연결할 수 있어요.</p>
    {allowed&&<button type="button" disabled={frame.busy} onClick={()=>void recover()}>저장된 검색으로 다시 연결</button>}
    {frame.busy&&<p role="status">저장된 검색을 확인하고 있어요.</p>}
    {frame.failed&&<p role="alert">저장된 검색을 확인하지 못했어요. 새 검색을 시작하지 않았어요.</p>}
  </main>;
}
