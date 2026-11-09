import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {assertStoreKitPurchaseReviewOnly,bindMemberStoreKitPurchaseReviewPort} from "./storeKitPurchaseReviewContract";
import type {IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";

/** One injected connection is consumed by the shell's original member session.
 * Screen leases belong to this consumer; the injected native factory remains
 * parent-owned. No bootstrap on construction or authority from a JS token. */
export function bindMemberStoreKitSessionConnectionLocal(connection:IOSStoreKitSessionReviewConnection,
  load:()=>Promise<string|null>,changed:()=>void):IOSStoreKitSessionReviewConnection{
  assertStoreKitPurchaseReviewOnly();
  type Port=Awaited<ReturnType<typeof connection.connectExplicit>>;
  type Attempt={live:boolean;raw?:Port;disposed:boolean};
  let closed=false,busy=false;const attempts=new Set<Attempt>();
  const retire=(attempt:Attempt)=>{
    attempt.live=false;
    if(attempt.raw && !attempt.disposed){attempt.disposed=true;attempt.raw.dispose();}
    attempts.delete(attempt);
  };
  const dispose=()=>{closed=true;for(const attempt of attempts)retire(attempt);};
  const sessionChanged=()=>{if(closed)return;dispose();changed();};
  const bound=createBoundMemberResponseSessionLoader(load,sessionChanged,()=>!closed);
  return {dispose,connectExplicit:async(options)=>{
    const scope=memberStatusReadScope(bound,options);
    const gate=()=>{scope.gate();assertStoreKitPurchaseReviewOnly();if(closed)throw new Error("Store connection unavailable");};
    gate();if(busy)throw new Error("Store connection unavailable");busy=true;
    const attempt:Attempt={live:true,disposed:false};attempts.add(attempt);
    try{
      const result=await scope.wait(()=>runWithMemberResponseSession(scope.load,sessionChanged,async()=>{
        gate();
        // Keep the original promise observed after consumer abort so a late
        // lease is closed exactly once instead of attached to another screen.
        const pending=Promise.resolve().then(()=>{gate();return connection.connectExplicit(options);}).then(raw=>{
          attempt.raw=raw;
          try{gate();if(!attempt.live)throw new Error("Store connection unavailable");}
          catch(error){retire(attempt);throw error;}
          const port=bindMemberStoreKitPurchaseReviewPort(raw,bound,sessionChanged);
          const scoped=(o?:MemberStatusReadOptions)=>({...o,isCurrent:()=>attempt.live && !closed && (!o?.isCurrent || o.isCurrent())});
          return {readOffer:(o?:MemberStatusReadOptions)=>port.readOffer(scoped(o)),
            purchaseExplicit:(o?:MemberStatusReadOptions)=>port.purchaseExplicit(scoped(o)),
            restoreExplicit:(o?:MemberStatusReadOptions)=>port.restoreExplicit(scoped(o)),dispose:()=>retire(attempt)};
        });
        const port=await scope.wait(()=>pending);gate();return port;
      }));
      gate();return result;
    }catch(error){retire(attempt);throw error;}
    finally{busy=false;}
  }};
}
