import {createReviewLookupConnectionWithClient} from "./appLookupConnectionLocal";
import {createReviewLookupRestartClient} from "./appLookupResumeLocal";
import {AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {loadLookupCredentialWithin} from "./lookupConsumerScopeLocal";
type Options=Parameters<typeof createReviewLookupRestartClient>[1];

/** Unregistered local integration. Original member/view lifetime is shared with
 * the reviewed owner; a recreated owner uses only its authenticated intent slot.
 * Mount, foreground and reconnect do not read the slot or perform HTTP. */
export function createReviewLookupRestartConnection(fetcher:typeof fetch,options:Options){
  const token=async(live:()=>boolean)=>(await loadLookupCredentialWithin(options.vault,live))?.session_token??null;
  return createReviewLookupConnectionWithClient(fetcher,{
    deploymentContext:options.deploymentContext,baseUrl:options.baseUrl,allowedBaseUrls:options.allowedBaseUrls,
    loadSessionToken:Object.assign(()=>token(()=>true),{within:(live:()=>boolean)=>()=>token(live)}),
    isCurrent:options.isCurrent,onSessionChanged:options.onSessionChanged,
  },(network,bound)=>{
    const credential=async(live:()=>boolean)=>{
      const scoped=bound.loadSessionToken as typeof bound.loadSessionToken & {within?:(live:()=>boolean)=>typeof bound.loadSessionToken};
      const token=await (scoped.within?.(live)??scoped)(),value=await loadLookupCredentialWithin(options.vault,live);
      if(!token||value?.session_token!==token)throw new AppMemberResponseSessionChanged();return value;
    };
    return createReviewLookupRestartClient(network,{
    ...options,isCurrent:bound.isCurrent,onSessionChanged:bound.onSessionChanged,
    vault:{...options.vault,load:Object.assign(()=>credential(()=>true),{within:(live:()=>boolean)=>()=>credential(live)})},
  });});
}
