import type {SessionVault,AppSessionCredential} from "./appSessionVault";
import {AppMemberResponseSessionChanged} from "./appMemberResponseSession";

export type LookupConsumerScope=()=>boolean;
export type ScopedLookupCredentialLoader=SessionVault["load"] & {
  within?: (live:LookupConsumerScope)=>SessionVault["load"];
};
/** A cancelled view/request cannot bind or retire a still-live original owner. */
export function assertLookupConsumerCurrent(live:LookupConsumerScope){
  let current=false;try{current=live();}catch{/* Uncertain consumers stay closed. */}
  if(!current)throw new AppMemberResponseSessionChanged();
}
/** Optional local scope propagation; plain vaults retain their no-argument call. */
export async function loadLookupCredentialWithin(vault:SessionVault,live:LookupConsumerScope):Promise<AppSessionCredential|null>{
  assertLookupConsumerCurrent(live);
  let value:AppSessionCredential|null;
  try{value=await ((vault.load as ScopedLookupCredentialLoader).within?.(live)??(()=>vault.load()))();}
  catch(error){assertLookupConsumerCurrent(live);throw error;}
  assertLookupConsumerCurrent(live);return value;
}
