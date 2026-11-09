import policy from "../../skin_engine/config/app_storekit_purchase_ui_local.json";
import nativePolicy from "../../skin_engine/config/app_storekit_native_local.json";
import freemium from "../../skin_engine/config/app_freemium.json";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

/** Safe local-review UI data only. No bearer, JWS, signature or account token. */
export type StoreKitOfferReview={scope:"synthetic_store_review";product_id:string;currency:"KRW";price:number;
  period_unit:"month";period_value:1;can_purchase:boolean;expires_ms:number};
export type StoreKitInteractionReview={scope:"synthetic_store_review";action:"purchase"|"restore";
  state:"pending"|"user_cancelled"|"awaiting_server_status";recorded_count:number};
/** Native remains responsible for signed admission/fulfillment, member fences,
 * SDK verification and finish. UI results never grant access or reissue intent.
 * No installed runtime factory constructs this explicit, isolated review seam. */
export type StoreKitPurchaseReviewPort={
  readOffer(options?:MemberStatusReadOptions):Promise<StoreKitOfferReview>;
  purchaseExplicit(options?:MemberStatusReadOptions):Promise<StoreKitInteractionReview>;
  restoreExplicit(options?:MemberStatusReadOptions):Promise<StoreKitInteractionReview>;
};
export function assertStoreKitPurchaseReviewOnly(){
  if(policy.scope!=="isolated_local_review" || policy.runtime_registered!==false || policy.native_plugin_registered!==false
    || policy.public_enabled!==false || policy.real_charge_enabled!==false || policy.automatic_purchase_or_restore!==false
    || policy.automatic_status_retry!==false || policy.client_access_grant!==false || policy.transaction_payload_in_js!==false
    || policy.purchase_admission_authority!=="native_signed_server_only"
    || policy.pending_purchase_release!=="never_from_client_cancel_error_or_empty_restore"
    || !Number.isSafeInteger(policy.offer_maximum_age_seconds) || policy.offer_maximum_age_seconds<=0
    || nativePolicy.system_store_calls_enabled!==false || nativePolicy.runtime_registered!==false
    || nativePolicy.native_plugin_registered!==false || nativePolicy.real_charge_enabled!==false
    || nativePolicy.public_enabled!==false || nativePolicy.product_registration_verified!==false
    || nativePolicy.scope!=="isolated_local_review" || nativePolicy.introductory_offer_allowed!==false
    || nativePolicy.family_shared_allowed!==false || nativePolicy.automatic_purchase_or_restore!==false
    || nativePolicy.automatic_retry!==false || nativePolicy.native_access_grant!==false
    || nativePolicy.version!=="1.1.0" || nativePolicy.purchase_uncertainty_latch!=="before_server_authorization"
    || nativePolicy.pending_purchase_release!==policy.pending_purchase_release
    || nativePolicy.currency!=="KRW" || nativePolicy.price!==freemium.price_krw
    || nativePolicy.period_unit!=="month" || nativePolicy.period_value!==1
    || freemium.runtime_enabled!==false || freemium.public_enabled!==false || freemium.real_charge_enabled!==false
    || freemium.introductory_trial!==false || freemium.purchase_eligibility.client_boolean_can_authorize_purchase!==false
    || policy.offer_maximum_age_seconds!==nativePolicy.maximum_authorization_seconds
    || policy.offer_maximum_age_seconds!==freemium.purchase_eligibility.server_context_max_age_seconds)throw new Error("Store review unavailable");
}
function record(value:unknown,keys:string[]):Record<string,unknown>{
  if(!value || typeof value!=="object" || Array.isArray(value) || Object.keys(value).sort().join("|")!==keys.sort().join("|"))throw new Error("Unconfirmed store review");
  return value as Record<string,unknown>;
}
export function parseStoreKitOfferReview(value:unknown,now=Date.now()):StoreKitOfferReview{
  assertStoreKitPurchaseReviewOnly();const r=record(value,["scope","product_id","currency","price","period_unit","period_value","can_purchase","expires_ms"]);
  if(r.scope!=="synthetic_store_review" || r.product_id!==nativePolicy.product_id || r.currency!==nativePolicy.currency
    || r.price!==nativePolicy.price || r.period_unit!==nativePolicy.period_unit || r.period_value!==nativePolicy.period_value
    || typeof r.can_purchase!=="boolean" || !Number.isSafeInteger(now) || !Number.isSafeInteger(r.expires_ms)
    || (r.expires_ms as number)<=now || (r.expires_ms as number)>now+policy.offer_maximum_age_seconds*1000)throw new Error("Unconfirmed product review");
  return {...r} as StoreKitOfferReview;
}
export function parseStoreKitInteractionReview(value:unknown,action:"purchase"|"restore"):StoreKitInteractionReview{
  assertStoreKitPurchaseReviewOnly();const r=record(value,["scope","action","state","recorded_count"]);
  if(r.scope!=="synthetic_store_review" || r.action!==action || !Number.isSafeInteger(r.recorded_count)
    || (r.recorded_count as number)<0 || (r.recorded_count as number)>nativePolicy.maximum_restore_transactions
    || !["pending","user_cancelled","awaiting_server_status"].includes(r.state as string)
    || (r.state!=="awaiting_server_status" && r.recorded_count!==0)
    || (action==="restore" && r.state!=="awaiting_server_status")
    || (action==="purchase" && r.state==="awaiting_server_status" && r.recorded_count!==1))throw new Error("Unconfirmed store outcome");
  return {...r} as StoreKitInteractionReview;
}
export function bindMemberStoreKitPurchaseReviewPort(port:StoreKitPurchaseReviewPort,
  load:()=>Promise<string|null>,changed:()=>void):StoreKitPurchaseReviewPort{
  const bound=createBoundMemberResponseSessionLoader(load,changed);
  const run=async<T,>(operation:()=>Promise<unknown>,parse:(value:unknown)=>T,options?:MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(bound,options);scope.gate();assertStoreKitPurchaseReviewOnly();
    const result=await scope.wait(()=>runWithMemberResponseSession(scope.load,changed,async()=>{
      scope.gate();assertStoreKitPurchaseReviewOnly();const result=parse(await scope.wait(operation));
      scope.gate();assertStoreKitPurchaseReviewOnly();return result;
    }));
    scope.gate();assertStoreKitPurchaseReviewOnly();return parse(result);
  };
  return {readOffer:o=>run(()=>port.readOffer(o),parseStoreKitOfferReview,o),
    purchaseExplicit:o=>run(()=>port.purchaseExplicit(o),v=>parseStoreKitInteractionReview(v,"purchase"),o),
    restoreExplicit:o=>run(()=>port.restoreExplicit(o),v=>parseStoreKitInteractionReview(v,"restore"),o)};
}
