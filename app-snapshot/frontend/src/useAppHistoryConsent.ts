import {useContext,useCallback,useLayoutEffect,useMemo,useRef,useState} from "react";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import type {AppHistoryConsentChoice,AppHistoryConsentStatus,AppHistoryConsentStore} from "./appHistoryConsent";
import {parseAppHistoryConsentStatus} from "./appHistoryConsent";

/** Authority is withheld during mutations/errors and whenever a member changes. */
export function useAppHistoryConsent(store: AppHistoryConsentStore | undefined, active: boolean) {
  const lifetime=useContext(AppSettingsLifetimeContext);
  // A callback belongs to this committed screen/account lifetime. Reusing the
  // same store after deactivation must not revive callbacks from the old cycle.
  const binding=useMemo(()=>({store,active,lifetime,live:false,status:null as AppHistoryConsentStatus|null}),[store,active,lifetime]);
  const currentBinding=useRef<typeof binding|null>(null);
  const [result,setResult]=useState<{binding:typeof binding;status:AppHistoryConsentStatus}|null>(null);
  const [busy,setBusy]=useState(false);
  const [error,setError]=useState(false);
  const [failedChoice,setFailedChoice]=useState<{store:AppHistoryConsentStore;choice:AppHistoryConsentChoice}|null>(null);
  const attempt=useRef(0);
  const pending=useRef<AbortController|null>(null);
  const status=active && result && result.binding===binding?result.status:null;
  const run=useCallback((choice?: AppHistoryConsentChoice,automaticRead=false)=>{
    // Only the acknowledgement shown by the current control may be used.
    // An explicit reread invalidates prior callbacks even at the same revision.
    if(!binding.live || currentBinding.current!==binding || binding.status!==status || !store || !active || pending.current || (choice && !status) || ((!automaticRead || choice) && lifetime && !lifetime.live)) return;
    const expected=status;
    const controller=new AbortController(); pending.current=controller;
    const id=++attempt.current;
    binding.status=null;
    setBusy(true);setError(false);setResult(null);setFailedChoice(null);
    const isCurrent=()=>binding.live && (!lifetime || lifetime.live) && currentBinding.current===binding && id===attempt.current && !controller.signal.aborted;
    const operation=async()=>{
      if(!isCurrent())return null;
      return choice && expected ? store.choose(choice,expected,{signal:controller.signal,isCurrent}) : store.read({signal:controller.signal,isCurrent});
    };
    // Child layout effects precede parent layout effects. Reserve the read now,
    // then check the committed parent lifetime and own attempt before dispatch.
    void Promise.resolve().then(operation).then(value=>{
      if(!isCurrent()) return;
      const parsed=parseAppHistoryConsentStatus(value);
      // A successful HTTP code alone cannot manufacture the requested choice.
      if(choice && parsed.state!==(choice==="grant"?"consented":"not_consented")) throw new Error("choice not acknowledged");
      binding.status=parsed;
      setResult({binding,status:parsed});
    }).catch(()=>{
      if(isCurrent()){
        setResult(null);setError(true);
        if(choice)setFailedChoice({store,choice});
      }
    }).finally(()=>{
      if(pending.current===controller){pending.current=null;setBusy(false);}
    });
  },[binding,store,active,status,lifetime]);
  // A parent render must not turn the panel's current explicit choice into a
  // different action connection. A new binding/acknowledgement changes run.
  const refresh=useCallback(()=>run(),[run]);
  const choose=useCallback((choice:AppHistoryConsentChoice)=>run(choice),[run]);
  // This is a local request lifetime, not server permission. Starting any
  // reread/choice clears binding.status synchronously. Even an equal receipt
  // returned later must not revive an earlier storage operation or callable.
  const storageLifetime=useMemo(()=>({isCurrent:()=>Boolean(
    status?.state==="consented" && binding.live && currentBinding.current===binding
      && binding.status===status && (!lifetime || lifetime.live),
  )}),[status,binding,lifetime]);
  useLayoutEffect(()=>{
    binding.live=true;binding.status=null;currentBinding.current=binding;
    attempt.current+=1;pending.current?.abort();pending.current=null;
    setResult(null);setBusy(false);setError(false);setFailedChoice(null);
    if(store && active) run(undefined,true);
    return ()=>{
      binding.live=false;binding.status=null;
      if(currentBinding.current===binding){
        currentBinding.current=null;attempt.current+=1;pending.current?.abort();pending.current=null;
      }
    };
    // Connection identity/active lifecycle, not each response, triggers a read.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  return {status,busy:busy || Boolean(store && active && !status && !error),error,
    failedChoice:active && failedChoice && failedChoice.store===store?failedChoice.choice:null,
    storageConsented:Boolean(status?.state==="consented" && !busy && !error),
    storageLifetime,refresh,choose};
}
