import policy from "../../skin_engine/config/app_native_test_request_queue.json";
import login from "../../skin_engine/config/app_login_plan.json";

type Pending={run():void;cancel(error:unknown):void};
const pending:Pending[]=[];
let active=false;
const baseline=JSON.stringify(policy);
const unavailable=()=>new Error("서버 연결을 확인하지 못했어요. 잠시 뒤 다시 확인해 주세요.");
function gate(){
  if(JSON.stringify(policy)!==baseline || policy.scope!=="existing_test_client_request_scheduling_only" ||
    policy.max_in_flight!==1 || !Number.isSafeInteger(policy.max_pending) || policy.max_pending<1 ||
    policy.max_queue_wait_milliseconds!==login.client_database_resume_retry.budget_milliseconds ||
    policy.automatic_retry!==false || policy.coalesce_requests!==false || policy.response_cache!==false)throw unavailable();
}
function next(){
  if(active)return;
  const job=pending.shift();if(!job)return;
  active=true;job.run();
}

/** The native operation owns the slot until it settles. Abandoning its JS
 * consumer does not cancel URLSession or free capacity for an overlapping write. */
export function serializeIOSAppTestRequest<T>(origin:string,operation:()=>Promise<T>,options:{signal?:AbortSignal|null;beforeDispatch():void}):Promise<T>{
  gate();if(origin!==policy.origin)throw unavailable();options.signal?.throwIfAborted();
  if(pending.length>=policy.max_pending)throw unavailable();
  return new Promise<T>((resolve,reject)=>{
    let waiting=true;
    const cleanup=()=>{clearTimeout(timer);options.signal?.removeEventListener("abort",abort);};
    const job:Pending={
      cancel(error){
        if(!waiting)return;waiting=false;cleanup();
        const index=pending.indexOf(job);if(index>=0)pending.splice(index,1);
        reject(error);
      },
      run(){
        waiting=false;cleanup();
        let result:Promise<T>;
        try{gate();options.signal?.throwIfAborted();options.beforeDispatch();result=operation();}
        catch(error){active=false;reject(error);next();return;}
        void Promise.resolve(result).then(resolve,reject).finally(()=>{active=false;next();});
      },
    };
    const abort=()=>job.cancel(options.signal?.reason??new DOMException("Aborted","AbortError"));
    const timer=setTimeout(()=>job.cancel(unavailable()),policy.max_queue_wait_milliseconds);
    options.signal?.addEventListener("abort",abort,{once:true});
    pending.push(job);next();
  });
}
