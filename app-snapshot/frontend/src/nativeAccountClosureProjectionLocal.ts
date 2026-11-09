import type {NativeAccountClosureSnapshot} from "./nativeRecoveryMemberWorkspaceLocal";

type Source={accountClosureSnapshot:()=>NativeAccountClosureSnapshot;subscribeAccountClosure:(listener:()=>void)=>()=>void};
export const EMPTY_NATIVE_ACCOUNT_CLOSURE:NativeAccountClosureSnapshot=Object.freeze({state:"none"});
/** Private OFF owner metadata. Following a new source masks its predecessor
 * immediately. Retirement retains only an accepted pending cleanup observer;
 * final settlement detaches it. No token, vault, network or native API here. */
export function createNativeAccountClosureProjectionLocal(){
  let value=EMPTY_NATIVE_ACCOUNT_CLOSURE,origin:Source|null=null,unbind:(()=>void)|null=null;
  const listeners=new Set<()=>void>();
  const detach=()=>{origin=null;unbind?.();unbind=null;};
  const publish=(next:NativeAccountClosureSnapshot)=>{
    if(value===next)return;value=next;
    for(const listener of [...listeners])try{listener();}catch{/* Safe status must reach other observers. */}
  };
  return {
    snapshot:()=>value,
    subscribe(listener:()=>void){listeners.add(listener);return()=>{listeners.delete(listener);};},
    reset(){detach();publish(EMPTY_NATIVE_ACCOUNT_CLOSURE);},
    follow(source:Source){
      detach();publish(EMPTY_NATIVE_ACCOUNT_CLOSURE);origin=source;
      const update=()=>{
        if(origin!==source)return;
        const next=source.accountClosureSnapshot();publish(next);
        if(origin===source&&next.state==="accepted"&&next.local_cleanup!=="pending")detach();
      };
      unbind=source.subscribeAccountClosure(update);update();
    },
    retire(){if(value.state!=="accepted"||value.local_cleanup!=="pending")detach();},
  };
}
