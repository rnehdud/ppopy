import {useEffect,useMemo,useRef,useState} from "react";
import type {StoreKitSessionReviewFactory} from "./appStoreKitSessionFactoryLocal";
import type {IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";

/** A committed original member owns a factory-created connection. Settings
 * detach closes only its lease; account/root retirement closes this connection.
 * Each StrictMode setup gets a fresh attempt, never a revived closed owner. */
export function useStoreKitSessionFactoryLocal(factory:StoreKitSessionReviewFactory|undefined,
  loadToken:(()=>Promise<string|null>)|undefined,lifetime:{isCurrent:()=>boolean}){
  const binding=useMemo(()=>({factory,loadToken,lifetime}),[factory,loadToken,lifetime]);
  type Attempt={binding:typeof binding;live:boolean;connection?:IOSStoreKitSessionReviewConnection};
  const current=useRef<Attempt|null>(null);
  const [ready,setReady]=useState<Attempt|null>(null);
  useEffect(()=>{
    if(!binding.factory || !binding.loadToken)return;
    const attempt:Attempt={binding,live:true};current.current=attempt;
    const isCurrent=()=>attempt.live && current.current===attempt && binding.lifetime.isCurrent();
    const retire=()=>{
      if(!attempt.live)return;attempt.live=false;
      if(current.current===attempt)current.current=null;
      try{attempt.connection?.dispose();}catch{/* disposal is a request, not an Apple acknowledgement */}
    };
    try{
      if(isCurrent()){
        attempt.connection=binding.factory({loadToken:binding.loadToken,isCurrent});
        if(isCurrent())setReady(attempt);else retire();
      }
    }catch{retire();}
    return retire;
  },[binding]);
  return ready?.binding===binding && ready.live?ready.connection:undefined;
}
