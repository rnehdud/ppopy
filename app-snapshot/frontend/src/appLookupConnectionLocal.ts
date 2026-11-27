import policy from "../../skin_engine/config/app_lookup_connection_local.json";
import {createReviewLookupRequestClient} from "./appLookupRequestLocal";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader,AppMemberResponseSessionChanged} from "./appMemberResponseSession";
import {awaitSearchRequest} from "./searchRequestLifetime";
import {bindBrowserAppLifecycle} from "./appLifecycle";
import {bindIOSNativeLifecycle,type IOSAppLifecycleBridge} from "./iosNativeLifecycle";

type Client=ReturnType<typeof createReviewLookupRequestClient>;
type Options=Parameters<typeof createReviewLookupRequestClient>[1]&{isCurrent:()=>boolean};
type RequestOptions={signal?:AbortSignal};
export class LookupConnectionUnavailable extends Error {
  constructor(){super("이전 검색 화면의 연결은 사용할 수 없어요.");this.name="LookupConnectionUnavailable";}
}
export class LookupConnectionBusy extends Error {
  constructor(){super("이전 검색 요청의 연결이 닫히기를 기다리고 있어요.");this.name="LookupConnectionBusy";}
}
export type LookupViewInvalidation={lifecycle:"foreground"|"background"|"retired"};
function guard(){
  if(policy.version!=="1.0.0"||policy.scope!=="isolated_local_review"||[
    policy.runtime_registered,policy.public_enabled,policy.native_connection_enabled,policy.automatic_poll_or_retry,
    policy.request_key_persistence_enabled,policy.response_cache_enabled,
  ].some(v=>v!==false)||policy.owner!=="original_member_connection_in_one_js_runtime"
    ||policy.view!=="exclusive_revocable_lease"||policy.background!=="abort_local_transport_preserve_original_client"
    ||policy.foreground!=="recheck_session_no_http"||policy.retirement!=="clear_client_ids_no_server_cancel"
    ||policy.unsettled_transport!=="hold_until_original_transport_settles"||policy.recovery!=="explicit_original_request_only")throw new LookupConnectionUnavailable();
}

/** Review owner above a search view. Keep this owner only for the original member
 * connection. View replacement/background retain its original client in memory;
 * member retirement destroys it. No export/adoption, persistence or HTTP on resume. */
export function createReviewLookupConnection(fetcher:typeof fetch,options:Options){
  return createReviewLookupConnectionWithClient(fetcher,options,createReviewLookupRequestClient);
}

/** Explicit synthetic-only injection for reviewing another guarded request port.
 * The registered/default connection retains its original in-memory client. */
export function createReviewLookupConnectionWithClient(fetcher:typeof fetch,options:Options,createClient:(fetcher:typeof fetch,options:Options)=>Client){
  guard();if(options.deploymentContext!=="synthetic_test"||typeof options.isCurrent!=="function")throw new LookupConnectionUnavailable();
  let lifecycle:"foreground"|"background"|"retired"="foreground",epoch=0,notified=false;
  let pending:Promise<unknown>|null=null;
  const active=new Set<AbortController>();
  const listeners=new Set<(event:LookupViewInvalidation)=>void>();
  type Registration={live:boolean;ready:Promise<()=>Promise<void>>;removed?:Promise<void>};
  let registration:Registration|null=null;
  const abortViews=(reason:Error=new LookupConnectionUnavailable())=>{
    epoch++;active.forEach(c=>c.abort(reason));active.clear();
    for(const notify of [...listeners])try{notify({lifecycle});}catch{/* A view cannot block retirement. */}
  };
  const remove=(entry:Registration)=>{
    entry.live=false;
    entry.removed??=entry.ready.then(dispose=>dispose()).finally(()=>{if(registration===entry)registration=null;});
    return entry.removed;
  };
  const retire=(reason:Error=new LookupConnectionUnavailable())=>{
    if(lifecycle==="retired")return;
    lifecycle="retired";abortViews(reason);listeners.clear();client?.dispose();
    if(registration)void remove(registration).catch(()=>{});
  };
  const changed=()=>{
    retire(new AppMemberResponseSessionChanged());if(notified)return;notified=true;
    try{options.onSessionChanged?.();}catch{/* Notification is not session authority. */}
  };
  const retired=()=>lifecycle==="retired";
  const load=createBoundMemberResponseSessionLoader(options.loadSessionToken,changed,()=>!retired()&&options.isCurrent());
  const client:Client=createClient(fetcher,{...options,loadSessionToken:load,isCurrent:()=>!retired()&&options.isCurrent(),onSessionChanged:changed});
  const transport=client;
  const member=async(isConsumerCurrent:()=>boolean)=>{
    guard();if(retired())throw new AppMemberResponseSessionChanged();
    try{
      const scoped=load.within(isConsumerCurrent),token=await scoped();
      if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token)){changed();throw new AppMemberResponseSessionChanged();}
      await assertCurrentMemberResponseSession(scoped,token,changed);
    }catch(error){
      let consumerCurrent=false;try{consumerCurrent=isConsumerCurrent();}catch{/* Uncertain view stays closed. */}
      if(!retired()&&!consumerCurrent)throw new LookupConnectionUnavailable();
      throw error;
    }
  };
  const foreground=()=>{if(retired())throw new AppMemberResponseSessionChanged();if(lifecycle!=="foreground")throw new LookupConnectionUnavailable();};
  const view=(own:number)=>{foreground();if(epoch!==own)throw new LookupConnectionUnavailable();};
  const coordinator={
    async toBackground(){
      if(retired())return;
      lifecycle="background";abortViews();
    },
    async toForeground(){
      if(retired()||lifecycle==="foreground")return;
      const own=epoch;
      const live=()=>!retired()&&lifecycle==="background"&&epoch===own;
      try{await member(live);if(live())lifecycle="foreground";}catch{if(live())retire();}
    },
    async settled(){await pending?.catch(()=>{});},
  };
  const register=(start:(entry:Registration)=>Promise<()=>Promise<void>>)=>{
    guard();foreground();if(registration)throw new LookupConnectionUnavailable();
    const entry:Registration={live:true,ready:Promise.resolve(async()=>{})};registration=entry;
    // Defer registration so this entry is visible before a synchronous bridge callback.
    entry.ready=Promise.resolve().then(()=>start(entry));
    void entry.ready.catch(()=>{entry.live=false;retire();});
    return entry;
  };
  const observer=(entry:Registration)=>({
    toBackground:()=>entry.live?coordinator.toBackground():Promise.resolve(),
    toForeground:()=>entry.live?coordinator.toForeground():Promise.resolve(),
    settled:()=>coordinator.settled(),
  });
  return {
    ...coordinator,
    subscribeInvalidation(notify:(event:LookupViewInvalidation)=>void){
      guard();if(retired())throw new AppMemberResponseSessionChanged();listeners.add(notify);
      return ()=>{listeners.delete(notify);};
    },
    async openView(){
      foreground();abortViews();const own=epoch;
      const live=()=>!retired()&&lifecycle==="foreground"&&epoch===own;
      await member(live);view(own);
      let detached=false;
      const consumerCurrent=()=>!detached&&live();
      const current=()=>{if(detached)throw new LookupConnectionUnavailable();view(own);};
      const run=async<T>(operation:(opts:RequestOptions)=>Promise<T>,opts?:RequestOptions):Promise<T>=>{
        current();opts?.signal?.throwIfAborted();
        const controller=new AbortController(),abort=()=>controller.abort(opts?.signal?.reason);
        active.add(controller);opts?.signal?.addEventListener("abort",abort,{once:true});
        try{
          const requestCurrent=()=>consumerCurrent()&&!controller.signal.aborted;
          await member(requestCurrent);current();controller.signal.throwIfAborted();
          if(pending)throw new LookupConnectionBusy();
          const wire=operation({signal:controller.signal});pending=wire;
          // Keep the hold until the actual transport finishes, even if a bridge
          // ignores abort. The abandoned view is released promptly without retry.
          void wire.then(()=>{if(pending===wire)pending=null;},()=>{if(pending===wire)pending=null;});
          const value=await awaitSearchRequest(()=>wire,async()=>{controller.abort();},controller.signal);
          await member(requestCurrent);current();return value;
        }finally{opts?.signal?.removeEventListener("abort",abort);active.delete(controller);}
      };
      return {
        begin:(query:string,opts?:RequestOptions)=>run(o=>transport.begin(query,o),opts),
        retryStart:(query:string,opts?:RequestOptions)=>run(o=>transport.retryStart(query,o),opts),
        recover:(opts?:RequestOptions)=>run(o=>transport.recover(o),opts),
        read:(opts?:RequestOptions)=>run(o=>transport.read(o),opts),
        cancel:(opts?:RequestOptions)=>run(o=>transport.cancel(o),opts),
        async state(){current();await member(consumerCurrent);current();return {lifecycle,phase:transport.state().phase,transport_pending:pending!==null};},
        detach(){if(detached)return;detached=true;if(epoch===own)abortViews();},
      };
    },
    async bindIOSLifecycle(bridge:IOSAppLifecycleBridge){
      const entry=register(e=>bindIOSNativeLifecycle(bridge,observer(e),()=>true));
      await entry.ready;
      if(!entry.live||retired()){await remove(entry);throw new LookupConnectionUnavailable();}
      return ()=>remove(entry);
    },
    async bindBrowserLifecycle(documentSource:Parameters<typeof bindBrowserAppLifecycle>[0],windowSource:Parameters<typeof bindBrowserAppLifecycle>[1]){
      const entry=register(async e=>{const dispose=bindBrowserAppLifecycle(documentSource,windowSource,observer(e));return async()=>{dispose();};});
      await entry.ready;
      if(!entry.live||retired()){await remove(entry);throw new LookupConnectionUnavailable();}
      return ()=>remove(entry);
    },
    async dispose(){retire();if(registration)await remove(registration);},
  };
}

export type ReviewLookupConnection=ReturnType<typeof createReviewLookupConnection>;
export type ReviewLookupView=Awaited<ReturnType<ReviewLookupConnection["openView"]>>;
