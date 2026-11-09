import policy from "../../skin_engine/config/app_freemium.json";
import navigation from "../../skin_engine/config/miray_navigation.json";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

export type QuotaFeature = "ai_product_lookup" | "routine_review";
export type MirayQuotaStatus = {
  policy_version: string;
  plan: "free" | "plus";
  features: Array<{feature:QuotaFeature;limit:number|null;used:number;pending:number;remaining:number|null;period_ends_at:string}>;
};
export type MirayQuotaStatusStore = {read(options?:MemberStatusReadOptions):Promise<MirayQuotaStatus>};

const object=(v:unknown):v is Record<string,unknown>=>Boolean(v)&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const count=(v:unknown):v is number=>typeof v==="number"&&Number.isSafeInteger(v)&&v>=0;

export function parseMirayQuotaStatus(value:unknown):MirayQuotaStatus {
  const invalid=()=>{throw new Error("이용 횟수 응답 형식을 확인하지 못했습니다.");};
  if(!object(value)||!exact(value,["policy_version","plan","features"])||value.policy_version!==policy.version||!(value.plan==="free"||value.plan==="plus")||!Array.isArray(value.features)||value.features.length!==2)return invalid();
  const plan=value.plan;
  const features=value.features.map((item:unknown,index:number)=>{
    const feature:QuotaFeature=index===0?"ai_product_lookup":"routine_review";
    const maximum=policy.plans[plan][feature];
    if(!object(item)||!exact(item,["feature","limit","used","pending","remaining","period_ends_at"])||item.feature!==feature||item.limit!==maximum||!count(item.used)||!count(item.pending)||item.pending>item.used)return invalid();
    const remaining=maximum===null?null:Math.max(0,maximum-item.used);
    if(item.remaining!==remaining||typeof item.period_ends_at!=="string"||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(item.period_ends_at)||!Number.isFinite(Date.parse(item.period_ends_at))||new Date(item.period_ends_at).toISOString().slice(0,19)!==item.period_ends_at.slice(0,19))return invalid();
    return {feature,limit:maximum,used:item.used,pending:item.pending,remaining,period_ends_at:item.period_ends_at};
  });
  return {policy_version:policy.version,plan,features};
}

export function createHttpMirayQuotaStatusStore(fetcher:typeof fetch,options:{
  baseUrl:string;allowedBaseUrls:readonly string[];loadSessionToken:()=>Promise<string|null>;onSessionChanged?:()=>void;
}):MirayQuotaStatusStore {
  const normalize=(value:string)=>{
    const url=new URL(value);
    if(url.protocol!=="https:"||url.username||url.password||url.search||url.hash)throw new Error("앱 API 주소를 확인해 주세요.");
    return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
  };
  const base=normalize(options.baseUrl);
  if(!options.allowedBaseUrls.map(normalize).includes(base))throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const bound=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  return {read:async consumer=>{
    const {gate,load,wait,fetch}=memberStatusReadScope(bound,consumer);
    const token=await wait(load);
    if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response=await wait(()=>fetch(fetcher)(`${base}${navigation.quota_status_http.path}`,{
      method:"GET",cache:"no-store",redirect:"error",credentials:"omit",headers:{Authorization:`Bearer ${token}`},signal:consumer?.signal,
    }));
    await wait(()=>assertCurrentMemberResponseSession(load,token,options.onSessionChanged));
    let payload:unknown=null;
    try{payload=await wait(()=>response.json());}catch{gate();/* fail closed below */}
    await wait(()=>assertCurrentMemberResponseSession(load,token,options.onSessionChanged));
    if(!response.ok)throw new Error("이용 횟수를 확인하지 못했습니다.");
    return parseMirayQuotaStatus(payload);
  }};
}
