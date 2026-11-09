import {AppMemberResponseSessionChanged,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {awaitSearchRequest} from "./searchRequestLifetime";

/** Local view ownership only; never authentication or server settlement. */
export type MemberStatusReadOptions={signal?:AbortSignal;isCurrent?:()=>boolean};
export function memberStatusReadScope(bound:ReturnType<typeof createBoundMemberResponseSessionLoader>,options?:MemberStatusReadOptions){
  const live=()=>{
    try{return !options?.signal?.aborted && (!options?.isCurrent || options.isCurrent()===true);}catch{return false;}
  };
  const gate=()=>{options?.signal?.throwIfAborted();if(!live())throw new AppMemberResponseSessionChanged();};
  const load=bound.within(live);
  const wait=async<T,>(operation:()=>Promise<T>)=>{
    gate();const value=await awaitSearchRequest(async()=>{gate();const value=await operation();gate();return value;},async()=>{},options?.signal);
    gate();return value;
  };
  // Explicit local transports may perform their own nested credential awaits.
  // Preserve the same consumer fence there, before they can retire siblings.
  const fetch=(fetcher:typeof globalThis.fetch)=>
    (fetcher as typeof globalThis.fetch & {within?:(live:()=>boolean,prepare?:()=>Promise<void>)=>typeof globalThis.fetch})
      .within?.(live,async()=>{await wait(load);})??fetcher;
  return {gate,load,wait,fetch};
}
