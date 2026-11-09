import {Capacitor,registerPlugin} from "@capacitor/core";
import {createPublicAppTransport,type PublicClientTransportBinding,type PublicNativeRequestPort,type PublicNativeResponse} from "./publicAppTransport";
import {createPublicSessionVault,PUBLIC_SESSION_KEY,type PublicOwnerBindings,type PublicSessionStore} from "./publicSessionVault";
import routes from "../../skin_engine/config/app_public_auth_routes_review.json";

/** Final entry must obtain this plugin only from the explicit native public
 * registration. No browser/TEST/CapacitorHttp fallback is supplied here. */
export interface PublicRuntimePlugin {
  bootstrap():Promise<unknown>;
  readSession():Promise<unknown>;
  compareAndSwapSession(options:{expectedValue:string|null;nextValue:string|null}):Promise<unknown>;
  request(options:{id:string;url:string;method:string;headers:Record<string,string>;body:string|null;timeoutMilliseconds:number;maximumResponseBytes:number}):Promise<PublicNativeResponse>;
  cancel(options:{id:string}):Promise<unknown>;
}
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const unavailable=()=>new Error("공개 앱 연결 결과를 확인하지 못했어요.");
type InitializationCode="P01"|"P02"|"P03"|"P04"|"P05"|"P06"|"P07";
class InitializationFailure extends Error{
  constructor(readonly initializationCode:InitializationCode){super("공개 앱 연결 결과를 확인하지 못했어요.");}
}
/** Only a fixed stage code may leave initialization; never bridge error text. */
export const publicInitializationCode=(error:unknown)=>error instanceof InitializationFailure?error.initializationCode:"P08";

export async function createPublicNativeConnection(plugin:PublicRuntimePlugin,options:{crypto?:Crypto;now?:()=>number}={}){
  let stage:InitializationCode="P03";
  try{
    const crypto=options.crypto??globalThis.crypto;
    if(!crypto?.randomUUID||!crypto.subtle)throw unavailable();
    stage="P04";const bootstrap=await plugin.bootstrap();stage="P05";
    if(!object(bootstrap)||!exact(bootstrap,["version","binding","ownerBindings"])||bootstrap.version!=="1.0.0-public-native-bootstrap"||
      !object(bootstrap.binding)||!object(bootstrap.ownerBindings))throw unavailable();
    // Snapshot bridge output. Caller/native-object mutation cannot rebind an
    // already constructed connection to different keys, endpoints or versions.
    const binding=JSON.parse(JSON.stringify(bootstrap.binding)) as PublicClientTransportBinding;
    const ownerBindings=JSON.parse(JSON.stringify(bootstrap.ownerBindings)) as PublicOwnerBindings;
    // Native storage and HTTP share one exclusive authentication lease. A
    // sibling vault read must wait for HTTP settlement, not be mistaken for
    // a changed account. Cancellation may still drain the current HTTP call.
    let nativeTail:Promise<void>=Promise.resolve();
    const orderedNative=<T,>(work:()=>Promise<T>):Promise<T>=>{
      const task=nativeTail.then(work);
      nativeTail=task.then(()=>{},()=>{});
      return task;
    };
    const store:PublicSessionStore={
      get:async key=>{
        if(key!==PUBLIC_SESSION_KEY)throw unavailable();
        const reply=await orderedNative(()=>plugin.readSession());
        if(!object(reply)||!exact(reply,["value"])||reply.value!==null&&typeof reply.value!=="string")throw unavailable();
        return reply.value as string|null;
      },
      compareAndSwap:async(key,expectedValue,nextValue)=>{
        if(key!==PUBLIC_SESSION_KEY)throw unavailable();
        const reply=await orderedNative(()=>plugin.compareAndSwapSession({expectedValue,nextValue}));
        if(!object(reply)||!exact(reply,["changed"])||typeof reply.changed!=="boolean")throw unavailable();return reply.changed;
      }
    };
    stage="P06";const vault=await createPublicSessionVault(store,{ownerBindings,crypto,now:options.now});
    const port:PublicNativeRequestPort=async request=>{
      request.signal.throwIfAborted();const id=crypto.randomUUID();let settled=false;
      const abort=()=>{if(!settled)try{void plugin.cancel({id}).catch(()=>{});}catch{/* Native completion still owns the pending slot. */}};
      request.signal.addEventListener("abort",abort,{once:true});
      try{
        request.signal.throwIfAborted();
        const deadline=Date.now()+request.timeoutMilliseconds;
        const response=await orderedNative(()=>{
          request.signal.throwIfAborted();
          const remaining=deadline-Date.now();
          if(remaining<=0)throw unavailable();
          return plugin.request({id,url:request.url,method:request.method,headers:{...request.headers},body:request.body,
            timeoutMilliseconds:remaining,maximumResponseBytes:request.maximumResponseBytes});
        });
        request.signal.throwIfAborted();return response;
      }finally{settled=true;request.signal.removeEventListener("abort",abort);}
    };
    stage="P07";const transport=createPublicAppTransport(binding,port,async request=>{
      const path=new URL(request.url).pathname;
      if(routes.routes.some(r=>r.path===path&&r.method===request.method&&r.operation==="new_login"))return;
      const member=await vault.load();if(!member||request.headers.authorization!=="Bearer "+member.session_token)throw unavailable();
    });
    return Object.freeze({vault,transport});
  }catch{throw new InitializationFailure(stage);}
}

export async function connectBundledPublicNativeRuntime(){
  if(!Capacitor.isNativePlatform()||Capacitor.getPlatform()!=="ios")throw new InitializationFailure("P01");
  if(!Capacitor.isPluginAvailable("PoppyPublicRuntime"))throw new InitializationFailure("P02");
  return createPublicNativeConnection(registerPlugin<PublicRuntimePlugin>("PoppyPublicRuntime"));
}
