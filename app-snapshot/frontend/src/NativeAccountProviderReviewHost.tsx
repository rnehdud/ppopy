import {useLayoutEffect,useRef,useSyncExternalStore,type ComponentProps} from "react";
import {nativeAccountProviderConfigured,type createNativeAccountProviderLocal} from "./nativeAccountProviderLocal";
import NativeRecoveryMemberWorkspaceReviewHost from "./NativeRecoveryMemberWorkspaceReviewHost";
import NativeAccountClosureReview from "./NativeAccountClosureReview";
import {useNativeAccountClosure} from "./useNativeAccountClosure";

type Provider=Pick<ReturnType<typeof createNativeAccountProviderLocal>,"snapshot"|"subscribe"|"invalidate"|"accountClosureSnapshot"|"subscribeAccountClosure">;
type Props=Omit<ComponentProps<typeof NativeRecoveryMemberWorkspaceReviewHost>,"connection">&{provider:Provider};
/** OFF UI consumes an explicit provider or its serialized account owner;
 * mounting cannot create a channel/login/consent. The caller owns disposal. */
export default function NativeAccountProviderReviewHost({provider,...props}:Props){
  const previous=useRef(provider),frame=useSyncExternalStore(provider.subscribe,provider.snapshot,provider.snapshot);
  const allowed=nativeAccountProviderConfigured()&&props.deploymentContext==="synthetic_test"&&props.memberAndSensitiveConsentVerified;
  const connection=allowed&&frame.state==="ready"?frame.connection:null;
  // Owner projection survives UI detach without reopening a member/native
  // connection. Replacement/revocation masks the old provider during render.
  const closure=useNativeAccountClosure(allowed&&frame.state==="retired"?provider:null);
  useLayoutEffect(()=>{
    if(previous.current!==provider)previous.current.invalidate();previous.current=provider;
    if(!allowed)provider.invalidate();
    // StrictMode detach does not dispose the caller-owned account provider.
  },[provider,allowed]);
  if(allowed&&closure.state==="accepted")return <NativeAccountClosureReview closure={closure}/>;
  if(connection)return <NativeRecoveryMemberWorkspaceReviewHost {...props} connection={connection}/>;
  return <main className="miray-main"><h1>계정 연결을 확인해 주세요</h1>
    {allowed&&frame.state==="connecting"?<p role="status">계정 연결을 준비하고 있어요.</p>:
      <p>확인한 계정으로 연결한 뒤 루틴을 이어서 볼 수 있어요.</p>}
  </main>;
}
