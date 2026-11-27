import policy from "../../skin_engine/config/app_storekit_ui_bridge_local.json";
import {assertStoreKitPurchaseReviewOnly,parseStoreKitOfferReview,parseStoreKitInteractionReview,
  type StoreKitPurchaseReviewPort,type StoreKitOfferReview} from "./storeKitPurchaseReviewContract";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession,assertCurrentMemberResponseSession,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {readReviewLookupResponseJson} from "./appLookupRequestLocal";

type Method="readOffer"|"purchaseExplicit"|"restoreExplicit";
export type IOSStoreKitPurchaseReviewBridge={
  invoke:(args:{lease_id:string;method:Method;args_json:"{}"})=>Promise<unknown>;
  dispose:(args:{lease_id:string})=>Promise<void>;
};
type Options={deploymentContext:"synthetic_test";loadToken:()=>Promise<string|null>;isCurrent:()=>boolean;now:()=>number};
export class IOSStoreKitReviewUnavailable extends Error {
  constructor(){super("구매 내역 연결을 확인하지 못했어요.");this.name="IOSStoreKitReviewUnavailable";}
}
const fail=()=>new IOSStoreKitReviewUnavailable();
const uuid=(v:unknown):v is string=>typeof v==="string" && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/.test(v) && v!=="00000000-0000-0000-0000-000000000000";
function exact(value:unknown,keys:string[]):Record<string,unknown>{
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==keys.sort().join("|"))throw fail();
  return value as Record<string,unknown>;
}
export function assertReviewIOSStoreKitBridgePolicy(){
  assertStoreKitPurchaseReviewOnly();
  const expected={version:"1.0.0",scope:"isolated_local_review",runtime_registered:false,native_plugin_registered:false,
    public_enabled:false,real_charge_enabled:false,system_store_calls_enabled:false,automatic_purchase_or_restore:false,
    automatic_retry:false,client_access_or_quota_grant:false,maximum_argument_bytes:2,maximum_response_bytes:8192,
    argument_contract:"canonical_empty_object_no_client_authority",methods:"readOffer,purchaseExplicit,restoreExplicit",
    request_id:"native_minted_each_explicit_operation",owner:"original_native_account_session_generation_before_after_await",
    lease:"native_minted_routing_only_not_authentication",offer:"signed_current_member_observation_not_purchase_admission",
    member_binding:"sha256_native_lease_and_original_session_no_bearer_forwarding",
    purchase:"fresh_server_admission_required_hold_before_await",pending_release:"never_from_client_cancel_error_or_empty_restore",
    output:"safe_ui_dto_no_bearer_jws_signature_account_token_or_refs",
    native_policy_sha256:"a64fb7daa3aa52b7222cd9eb4f16f5000ad0ec470c48f12d3c0c0bea117c7d78",
    ui_policy_sha256:"a4d4ec7f04c76c73e14e232d8af67e443aa6215f612e791d1004c103445430c6"};
  const value=exact(policy,Object.keys(expected));
  if(Object.entries(expected).some(([k,v])=>value[k]!==v))throw fail();
}
export type IOSStoreKitReviewLease={version:"1.0.0";scope:"synthetic_store_review";lease_id:string;member_binding:string};
/** Routing parser only. It grants no identity, session, purchase or quota. */
export function parseReviewIOSStoreKitLease(value:unknown):IOSStoreKitReviewLease{
  const lease=exact(value,["version","scope","lease_id","member_binding"]);
  if(lease.version!=="1.0.0" || lease.scope!=="synthetic_store_review" || !uuid(lease.lease_id)
    || typeof lease.member_binding!=="string" || !/^[0-9a-f]{64}$/.test(lease.member_binding))throw fail();
  return lease as IOSStoreKitReviewLease;
}
/** Safe DTO transport only, explicitly injected into the existing review UI.
 * Native owns member generation, signatures, nonces and fresh authorization.
 * No runtime registration, SDK dispatch, token forwarding or call on binding. */
export function createReviewIOSStoreKitPurchasePort(bridge:IOSStoreKitPurchaseReviewBridge,leaseValue:unknown,options:Options):StoreKitPurchaseReviewPort&{dispose:()=>void}{
  assertReviewIOSStoreKitBridgePolicy();const lease=parseReviewIOSStoreKitLease(leaseValue);
  if(options.deploymentContext!=="synthetic_test" || [options.loadToken,options.isCurrent,options.now,bridge?.invoke,bridge?.dispose].some(v=>typeof v!=="function"))throw fail();
  const leaseID=lease.lease_id;let retired=false,busy=false,held=false,offer:StoreKitOfferReview|null=null;
  const retire=()=>{if(retired)return;retired=true;offer=null;
    // Exact original lease only. A delayed disposal cannot close a replacement.
    void Promise.resolve().then(()=>bridge.dispose({lease_id:leaseID})).catch(()=>{});
  };
  const live=()=>{
    try{assertReviewIOSStoreKitBridgePolicy();if(retired || options.isCurrent()!==true)throw new AppMemberResponseSessionChanged();}
    catch(error){retire();throw error;}
  };
  const bound=createBoundMemberResponseSessionLoader(options.loadToken,retire,()=>!retired && options.isCurrent());
  const digest=async(text:string)=>{
    const bytes=new TextEncoder().encode(text),result=await globalThis.crypto.subtle.digest("SHA-256",bytes);
    return Array.from(new Uint8Array(result),byte=>byte.toString(16).padStart(2,"0")).join("");
  };
  const json=async(raw:unknown,scope:ReturnType<typeof memberStatusReadScope>)=>{
    if(typeof raw!=="string" || new TextEncoder().encode(raw).length>policy.maximum_response_bytes)throw fail();
    return scope.wait(()=>readReviewLookupResponseJson(new Response(raw,{headers:{"Content-Type":"application/json"}}),new AbortController().signal));
  };
  const run=async(method:Method,o?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,o);scope.gate();live();if(busy)throw fail();
    if(method==="purchaseExplicit"){
      if(held || !offer || !parseStoreKitOfferReview(offer,options.now()).can_purchase)throw fail();
      held=true;offer=null;
    }else offer=null;
    busy=true;
    try{
      const data=await scope.wait(()=>runWithMemberResponseSession(scope.load,retire,async()=>{
        scope.gate();live();
        const token=await scope.load();scope.gate();live();if(!token)throw fail();
        const session="sha256:"+await scope.wait(()=>digest(token));scope.gate();live();
        const binding=await scope.wait(()=>digest("storekit-ui-lease-v1\n"+leaseID+"\n"+session));scope.gate();live();
        if(binding!==lease.member_binding){retire();throw new AppMemberResponseSessionChanged();}
        await scope.wait(()=>assertCurrentMemberResponseSession(scope.load,token,retire));scope.gate();live();
        const raw=await scope.wait(()=>bridge.invoke({lease_id:leaseID,method,args_json:"{}"}));
        scope.gate();live();const e=exact(await json(raw,scope),["version","lease_id","member_binding","data_json"]);
        if(e.version!=="1.0.0" || e.lease_id!==leaseID || e.member_binding!==lease.member_binding)throw fail();
        const result=await json(e.data_json,scope);scope.gate();live();return result;
      }));
      scope.gate();live();
      if(method==="readOffer"){
        const parsed=parseStoreKitOfferReview(data,options.now());
        if(held && parsed.can_purchase)throw fail();offer=parsed;return parsed;
      }
      return parseStoreKitInteractionReview(data,method==="purchaseExplicit"?"purchase":"restore");
    }finally{busy=false;}
  };
  return {readOffer:o=>run("readOffer",o) as ReturnType<StoreKitPurchaseReviewPort["readOffer"]>,
    purchaseExplicit:o=>run("purchaseExplicit",o) as ReturnType<StoreKitPurchaseReviewPort["purchaseExplicit"]>,
    restoreExplicit:o=>run("restoreExplicit",o) as ReturnType<StoreKitPurchaseReviewPort["restoreExplicit"]>,dispose:retire};
}
