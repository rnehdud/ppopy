import config from "../../skin_engine/config/app_routine_result.json";
import consumer from "../../skin_engine/config/consumer_api.json";
import type {CareAnalysisEnvelope} from "./careApi";
import {isConsumerCareDelivery} from "./careDeliveryBoundary";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

export type MirayRoutineDelivery = {state:"unavailable";completed_at:null;result:null}
  | {state:"available";completed_at:string;result:CareAnalysisEnvelope};
export type MirayRoutineResultStore = {read(options?:MemberStatusReadOptions):Promise<MirayRoutineDelivery>};
const object=(v:unknown):v is Record<string,unknown>=>Boolean(v)&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");

/** Strict synthetic TEST contract. No historic wire is promoted into current advice. */
export function parseMirayRoutineDelivery(value:unknown):MirayRoutineDelivery {
  const invalid=():never=>{throw new Error("저장된 결과 응답 형식을 확인하지 못했습니다.");};
  if(!object(value)||!exact(value,["state","completed_at","result"]))return invalid();
  if(value.state==="unavailable") {
    if(value.completed_at!==null||value.result!==null)return invalid();
    return {state:"unavailable",completed_at:null,result:null};
  }
  if(value.state!=="available"||typeof value.completed_at!=="string"||!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$/.test(value.completed_at)||!Number.isFinite(Date.parse(value.completed_at))||new Date(value.completed_at).toISOString().slice(0,19)!==value.completed_at.slice(0,19))return invalid();
  const envelope=value.result;
  if(!object(envelope)||!exact(envelope,["api_schema_version","deployment_context","persistence","result"])||envelope.api_schema_version!==consumer.request_schema_version||envelope.deployment_context!=="synthetic_test"||envelope.persistence!=="none"||!object(envelope.result)||!exact(envelope.result,["schema_version","sections","safety"])||envelope.result.schema_version!==consumer.care_response_schema_version)return invalid();
  if(!isConsumerCareDelivery(envelope.result)||new TextEncoder().encode(JSON.stringify(envelope)).length>config.max_plaintext_bytes)return invalid();
  // Snapshot injected responses so caller mutation cannot replace approved display data.
  return structuredClone(value) as MirayRoutineDelivery;
}

export function createHttpMirayRoutineResultStore(fetcher:typeof fetch,options:{
  baseUrl:string;allowedBaseUrls:readonly string[];loadSessionToken:()=>Promise<string|null>;onSessionChanged?:()=>void;
}):MirayRoutineResultStore {
  const normalize=(value:string)=>{const url=new URL(value);if(url.protocol!=="https:"||url.username||url.password||url.search||url.hash)throw new Error("앱 API 주소를 확인해 주세요.");return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;};
  const base=normalize(options.baseUrl);
  if(!options.allowedBaseUrls.map(normalize).includes(base))throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const bound=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  return {read:async consumer=>{
    const {gate,load,wait,fetch}=memberStatusReadScope(bound,consumer);
    const token=await wait(load);if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response=await wait(()=>fetch(fetcher)(`${base}${config.http.path}`,{method:"GET",cache:"no-store",redirect:"error",credentials:"omit",headers:{Authorization:`Bearer ${token}`},signal:consumer?.signal}));
    await wait(()=>assertCurrentMemberResponseSession(load,token,options.onSessionChanged));
    let payload:unknown=null;try{payload=await wait(()=>response.json());}catch{gate();/* fail closed */}
    await wait(()=>assertCurrentMemberResponseSession(load,token,options.onSessionChanged));
    if(!response.ok)throw new Error("저장된 점검 결과를 불러오지 못했어요.");
    return parseMirayRoutineDelivery(payload);
  }};
}
