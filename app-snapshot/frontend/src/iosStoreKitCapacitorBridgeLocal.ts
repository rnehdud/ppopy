import policy from "../../skin_engine/config/app_storekit_ui_bridge_local.json";
import {assertReviewIOSStoreKitBridgePolicy,IOSStoreKitReviewUnavailable,
  type IOSStoreKitPurchaseReviewBridge} from "./iosStoreKitPurchaseBridgeLocal";
import type {IOSStoreKitSessionReviewBridge} from "./iosStoreKitSessionConnectionLocal";

export type IOSStoreKitReviewCapacitorPlugin={
  bootstrapExplicit:(args:{args_json:"{}"})=>Promise<unknown>;
  invoke:IOSStoreKitPurchaseReviewBridge["invoke"];
  dispose:(args:{lease_id:string})=>Promise<unknown>;
};
const fail=()=>new IOSStoreKitReviewUnavailable();
const uuid=(v:unknown):v is string=>typeof v==="string" && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(v)
  && v!=="00000000-0000-0000-0000-000000000000";
function exact(value:unknown,keys:string[]):Record<string,unknown>{
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==[...keys].sort().join("|"))throw fail();
  return value as Record<string,unknown>;
}
function unwrap(value:unknown):string{
  const result=exact(value,["result_json"]).result_json;
  if(typeof result!=="string" || !result.length || new TextEncoder().encode(result).length>policy.maximum_response_bytes)throw fail();
  return result;
}
/** Explicitly injected Capacitor object-to-string transport only. Binding has
 * no IO or registerPlugin call. Identity, lease validation and safe DTO parsing
 * remain in the existing original-member session connection and purchase port.
 * Retirement stays there so late valid leases can still be exactly cleaned. */
export function createReviewIOSStoreKitCapacitorBridge(plugin:IOSStoreKitReviewCapacitorPlugin):IOSStoreKitSessionReviewBridge{
  assertReviewIOSStoreKitBridgePolicy();
  if([plugin?.bootstrapExplicit,plugin?.invoke,plugin?.dispose].some(v=>typeof v!=="function"))throw fail();
  const reply=async(run:()=>Promise<unknown>)=>{
    assertReviewIOSStoreKitBridgePolicy();
    try{const value=await run();assertReviewIOSStoreKitBridgePolicy();return unwrap(value);}catch{throw fail();}
  };
  return {
    bootstrapExplicit:args=>{
      if(exact(args,["args_json"]).args_json!=="{}")throw fail();
      return reply(()=>plugin.bootstrapExplicit({args_json:"{}"}));
    },
    invoke:args=>{
      const value=exact(args,["lease_id","method","args_json"]);
      if(!uuid(value.lease_id) || value.args_json!=="{}" || typeof value.method!=="string" || !["readOffer","purchaseExplicit","restoreExplicit"].includes(value.method))throw fail();
      // Copy canonical fields; never forward an arbitrary caller object.
      const method=value.method as Parameters<IOSStoreKitPurchaseReviewBridge["invoke"]>[0]["method"];
      return reply(()=>plugin.invoke({lease_id:value.lease_id as string,method,args_json:"{}"}));
    },
    dispose:async args=>{
      assertReviewIOSStoreKitBridgePolicy();const value=exact(args,["lease_id"]);if(!uuid(value.lease_id))throw fail();
      try{const result=await plugin.dispose({lease_id:value.lease_id});assertReviewIOSStoreKitBridgePolicy();exact(result,[]);}catch{throw fail();}
    },
  };
}
