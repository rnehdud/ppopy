import {useSyncExternalStore} from "react";
import {EMPTY_NATIVE_ACCOUNT_CLOSURE} from "./nativeAccountClosureProjectionLocal";
import type {NativeAccountClosureSnapshot} from "./nativeRecoveryMemberWorkspaceLocal";

type Source={accountClosureSnapshot:()=>NativeAccountClosureSnapshot;subscribeAccountClosure:(listener:()=>void)=>()=>void};
const snapshotNone=()=>EMPTY_NATIVE_ACCOUNT_CLOSURE,subscribeNone=()=>()=>{};
export function useNativeAccountClosure(source:Source|null){
  return useSyncExternalStore(source?.subscribeAccountClosure??subscribeNone,
    source?.accountClosureSnapshot??snapshotNone,source?.accountClosureSnapshot??snapshotNone);
}
