import {useLayoutEffect,useRef,useState,type ComponentProps} from "react";
import {nativeRecoveryUIConfigured,type createNativeRecoveryMemberWorkspaceLocal} from "./nativeRecoveryMemberWorkspaceLocal";
import NativeMemberWorkspaceReviewShell from "./NativeMemberWorkspaceReviewShell";
import NativeAccountClosureReview from "./NativeAccountClosureReview";
import {useNativeAccountClosure} from "./useNativeAccountClosure";

type ShellProps=ComponentProps<typeof NativeMemberWorkspaceReviewShell>;
type Workspace=ShellProps["workspace"];
type Connection=Awaited<ReturnType<typeof createNativeRecoveryMemberWorkspaceLocal>>;
async function closeCandidate(workspace:Workspace){workspace.invalidate();await workspace.dispose().catch(()=>{});}

/** OFF review UI. Explicit activation is bound to one private native host.
 * StrictMode mount cleanup detaches UI; the account caller owns disposal. */
export default function NativeRecoveryMemberWorkspaceReviewHost({connection,...props}:Omit<ShellProps,"workspace">&{connection:Connection}){
  const workspace=connection.workspace;
  const [frame,setFrame]=useState(()=>({source:workspace,workspace,busy:false,failed:false,current:workspace.isCurrent()}));
  const currentSource=useRef(workspace),mounted=useRef(false),request=useRef<AbortController|null>(null),adopted=useRef<Workspace|null>(null);
  const currentConnection=useRef(connection);
  // Prop replacement masks the old subtree during render, before cleanup.
  const shown=frame.source===workspace?frame.workspace:workspace;
  const allowed=nativeRecoveryUIConfigured()&&props.deploymentContext==="synthetic_test"&&props.memberAndSensitiveConsentVerified;
  const closure=useNativeAccountClosure(allowed?connection:null);
  const current=allowed&&frame.source===workspace&&frame.current&&shown.isCurrent();
  useLayoutEffect(()=>{
    if(currentConnection.current!==connection)currentConnection.current.invalidate();
    currentConnection.current=connection;
    mounted.current=true;currentSource.current=workspace;
    setFrame(f=>f.source===workspace?f:{source:workspace,workspace,busy:false,failed:false,current:workspace.isCurrent()});
    return()=>{
      mounted.current=false;request.current?.abort();request.current=null;
      const old=adopted.current;adopted.current=null;if(old)void closeCandidate(old);
    };
  },[workspace,connection]);
  useLayoutEffect(()=>{
    if(!allowed){void connection.dispose();request.current?.abort();request.current=null;shown.invalidate();
      const old=adopted.current;adopted.current=null;if(old)void closeCandidate(old);
      setFrame(f=>f.source===workspace?{...f,current:false,busy:false}:f);return;}
    try{return shown.subscribeInvalidation(()=>setFrame(f=>f.source===workspace&&f.workspace===shown?{...f,current:false}:f));}
    catch{setFrame(f=>f.source===workspace&&f.workspace===shown?{...f,current:false}:f);}
  },[workspace,shown,allowed,connection]);
  const recover=async()=>{
    if(!allowed||current||frame.failed||request.current||currentSource.current!==workspace)return;
    const controller=new AbortController();request.current=controller;
    workspace.invalidate();shown.invalidate();
    const prior=adopted.current;adopted.current=null;if(prior)await closeCandidate(prior);
    setFrame(f=>f.source===workspace?{...f,busy:true,failed:false,current:false}:f);
    let candidate:Workspace|null=null;
    try{
      if(controller.signal.aborted||!mounted.current||currentSource.current!==workspace)return;
      candidate=await connection.recoverOriginalWorkspace(controller.signal);
      if(candidate===workspace||candidate===shown||!candidate.isCurrent())throw new Error("Original native recovery unavailable");
      if(controller.signal.aborted||!mounted.current||currentSource.current!==workspace){await closeCandidate(candidate);return;}
      adopted.current=candidate;setFrame({source:workspace,workspace:candidate,busy:false,failed:false,current:true});
    }catch{
      if(candidate&&candidate!==workspace&&candidate!==shown)await closeCandidate(candidate);
      if(!controller.signal.aborted&&mounted.current&&currentSource.current===workspace)setFrame(f=>f.source===workspace?{...f,busy:false,failed:true,current:false}:f);
    }finally{if(request.current===controller)request.current=null;}
  };
  if(closure.state==="accepted")return <NativeAccountClosureReview closure={closure}/>;
  if(current)return <NativeMemberWorkspaceReviewShell {...props} workspace={shown}/>;
  return <main className="miray-main"><h1>계정 연결을 다시 확인해 주세요</h1>
    <p>이전 화면을 닫았어요. 저장된 검색을 확인한 뒤 다시 연결할 수 있어요.</p>
    {allowed&&<button type="button" disabled={frame.busy||frame.failed} onClick={()=>void recover()}>저장된 검색으로 다시 연결</button>}
    {frame.busy&&<p role="status">저장된 검색을 확인하고 있어요.</p>}
    {frame.failed&&<p role="alert">저장된 검색을 확인하지 못했어요. 새 검색을 시작하지 않았어요.</p>}
  </main>;
}
