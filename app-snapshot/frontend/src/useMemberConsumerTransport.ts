import {useLayoutEffect,useMemo,useRef} from "react";
import type {createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";

/** One committed adapter contract consumes the shared account bearer. */
export function useMemberConsumerTransport(
  shared:ReturnType<typeof createBoundMemberResponseSessionLoader>,
  onSessionChanged:()=>void,
  contract:object,
  lifetime?:{isCurrent:()=>boolean},
) {
  const binding=useMemo(()=>({contract,shared,onSessionChanged,lifetime,live:false}),[contract,shared,onSessionChanged,lifetime]);
  const owner=useRef<typeof binding|null>(null);
  useLayoutEffect(()=>{
    binding.live=true;owner.current=binding;
    return()=>{binding.live=false;if(owner.current===binding)owner.current=null;};
  },[binding]);
  return useMemo(()=>{
    const current=()=>binding.live && owner.current===binding && (!lifetime || lifetime.isCurrent());
    return {load:shared.within(current),changed:()=>{if(current())onSessionChanged();}};
  },[binding,shared,onSessionChanged,lifetime]);
}
