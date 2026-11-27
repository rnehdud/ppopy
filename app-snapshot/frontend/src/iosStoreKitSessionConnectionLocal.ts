import policy from "../../skin_engine/config/app_storekit_ui_bridge_local.json";
import {assertReviewIOSStoreKitBridgePolicy,createReviewIOSStoreKitPurchasePort,parseReviewIOSStoreKitLease,
  IOSStoreKitReviewUnavailable,type IOSStoreKitPurchaseReviewBridge,type IOSStoreKitReviewLease} from "./iosStoreKitPurchaseBridgeLocal";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";
import {readReviewLookupResponseJson} from "./appLookupRequestLocal";
import type {StoreKitPurchaseReviewPort} from "./storeKitPurchaseReviewContract";

export type IOSStoreKitSessionReviewBridge=IOSStoreKitPurchaseReviewBridge&{
  bootstrapExplicit:(args:{args_json:"{}"})=>Promise<unknown>;
};
type Options={deploymentContext:"synthetic_test";loadToken:()=>Promise<string|null>;isCurrent:()=>boolean;now:()=>number};
type Port=StoreKitPurchaseReviewPort&{dispose:()=>void};
export type IOSStoreKitSessionReviewConnection={connectExplicit:(options?:MemberStatusReadOptions)=>Promise<Port>;dispose:()=>void};
const fail=()=>new IOSStoreKitReviewUnavailable();
const digest=async(text:string)=>Array.from(new Uint8Array(await globalThis.crypto.subtle.digest("SHA-256",new TextEncoder().encode(text))),v=>v.toString(16).padStart(2,"0")).join("");

/** Prepared app connection, explicitly injected only. Native bootstrap gets
 * empty arguments; JS bearer binds safe consumption and is never forwarded.
 * Closing a screen discards late results and disposes only their exact lease.
 * Cancellation requests do not assert Apple ACK or release server purchases. */
export function createReviewIOSStoreKitSessionConnection(bridge:IOSStoreKitSessionReviewBridge,options:Options):IOSStoreKitSessionReviewConnection{
  assertReviewIOSStoreKitBridgePolicy();
  if(options.deploymentContext!=="synthetic_test" || [options.loadToken,options.isCurrent,options.now,
    bridge?.bootstrapExplicit,bridge?.invoke,bridge?.dispose].some(v=>typeof v!=="function"))throw fail();
  let closed=false,busy=false;
  type Attempt={live:boolean;port?:Port;lease?:IOSStoreKitReviewLease;disposed:boolean};
  let current:Attempt|undefined;
  const disposeLease=(attempt:Attempt)=>{
    if(attempt.disposed || !attempt.lease)return;attempt.disposed=true;
    if(attempt.port)attempt.port.dispose();
    else void Promise.resolve().then(()=>bridge.dispose({lease_id:attempt.lease!.lease_id})).catch(()=>{});
  };
  const retire=(attempt:Attempt|undefined)=>{if(!attempt)return;attempt.live=false;disposeLease(attempt);};
  const dispose=()=>{closed=true;retire(current);};
  const live=()=>{
    assertReviewIOSStoreKitBridgePolicy();
    let valid=false;try{valid=!closed && options.isCurrent()===true;}catch{/* uncertain owner stays closed */}
    if(!valid){dispose();throw fail();}
  };
  const bound=createBoundMemberResponseSessionLoader(options.loadToken,dispose,()=>!closed && options.isCurrent());
  const connectExplicit=async(o?:MemberStatusReadOptions):Promise<Port>=>{
    const scope=memberStatusReadScope(bound,o);scope.gate();live();if(busy)throw fail();
    const attempt:Attempt={live:true,disposed:false};retire(current);current=attempt;busy=true;
    const gate=()=>{scope.gate();live();if(!attempt.live || current!==attempt)throw fail();};
    try{
      gate();
      const result=await scope.wait(()=>runWithMemberResponseSession(scope.load,dispose,async()=>{
        const token=await scope.load();gate();if(!token)throw fail();
        // Observe completion independently of the UI await: even a late lease
        // after unmount/abort is parsed and retired by its original attempt.
        const pending=Promise.resolve().then(()=>{gate();return bridge.bootstrapExplicit({args_json:"{}"});})
          .then(async(raw)=>{
            if(typeof raw!=="string" || new TextEncoder().encode(raw).length>policy.maximum_response_bytes)throw fail();
            const value=await readReviewLookupResponseJson(new Response(raw,{headers:{"Content-Type":"application/json"}}),new AbortController().signal);
            attempt.lease=parseReviewIOSStoreKitLease(value);
            if(!attempt.live || closed || current!==attempt){disposeLease(attempt);throw fail();}
            gate();
            const session="sha256:"+await digest(token);gate();
            const expected=await digest("storekit-ui-lease-v1\n"+attempt.lease.lease_id+"\n"+session);gate();
            if(expected!==attempt.lease.member_binding)throw fail();
            attempt.port=createReviewIOSStoreKitPurchasePort(bridge,attempt.lease,{...options,loadToken:bound,
              isCurrent:()=>!closed && attempt.live && current===attempt && options.isCurrent()});
            gate();return attempt.port;
          }).catch(error=>{retire(attempt);throw error;});
        const result=await scope.wait(()=>pending);gate();return result;
      }));
      gate();return result;
    }catch(error){retire(attempt);throw error;}
    finally{busy=false;}
  };
  return {connectExplicit,dispose};
}
