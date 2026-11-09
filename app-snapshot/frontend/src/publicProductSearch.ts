import transfer from "../../skin_engine/config/app_public_product_transfer_review.json";
import policy from "../../skin_engine/config/app_public_product_lookup_http_review.json";
import care from "../../skin_engine/config/consumer_care_delivery.json";
import {checkedPublicAppTransportBase} from "./publicAppTransport";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope} from "./memberStatusReadScope";
import type {CareApiClient,ProductSearchOptions} from "./careApi";
import type {WebProductCandidate} from "./productCatalog";
const bad=()=>new Error("외부 제품 후보를 확인하지 못했어요. 같은 요청은 자동으로 다시 보내지 않아요.");
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
export async function parsePublicWebCandidates(value:unknown):Promise<WebProductCandidate[]>{
 if(!object(value)||!exact(value,["version","provider","auto_confirmed","candidates"])||value.version!==policy.version||value.provider!=="openai_responses"||value.auto_confirmed!==false||!Array.isArray(value.candidates)||value.candidates.length>policy.maximum_candidates)throw bad();
 const seen=new Set<string>(),out:WebProductCandidate[]=[];
 for(const row of value.candidates){
  if(!object(row)||!exact(row,["candidate_id","title","source_domain","source_url","snippet","provenance_hash","requires_user_confirmation"])||
    !["candidate_id","title","source_domain","source_url","snippet","provenance_hash"].every(k=>typeof row[k]==="string")||row.requires_user_confirmation!==true||
    !/^[a-f0-9]{24}$/.test(String(row.candidate_id))||!/^[a-f0-9]{64}$/.test(String(row.provenance_hash))||row.snippet!==policy.candidate_notice||
    !String(row.title).trim()||Array.from(String(row.title)).length>180||care.prohibited_terms.some(term=>String(row.title).toLowerCase().includes(term.toLowerCase())))throw bad();
  const url=new URL(String(row.source_url));
  if(url.protocol!=="https:"||url.username||url.password||url.hash||url.port||url.hostname!==row.source_domain||url.href!==row.source_url||!url.hostname.includes(".")||url.hostname==="localhost"||/\.(localhost|local|internal)$/.test(url.hostname)||/^\[|^[0-9.]+$/.test(url.hostname)||String(row.source_url).length>2048)throw bad();
  const digest=Array.from(new Uint8Array(await crypto.subtle.digest("SHA-256",new TextEncoder().encode(row.source_url+"\n"+row.title)))).map(x=>x.toString(16).padStart(2,"0")).join("");
  if(digest!==row.provenance_hash||digest.slice(0,24)!==row.candidate_id||seen.has(digest))throw bad();seen.add(digest);
  out.push({candidateId:row.candidate_id as string,title:row.title as string,sourceDomain:row.source_domain as string,sourceUrl:row.source_url as string,snippet:row.snippet as string,provenanceHash:row.provenance_hash as string});
 }
 return out;
}
export function createPublicWebProductSearchClient({baseUrl,fetcher,loadToken,onMemberChanged}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void}):Pick<CareApiClient,"searchWebProducts">{
 const base=checkedPublicAppTransportBase(baseUrl,fetcher),baseline=JSON.stringify(policy),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
 const gate=()=>{checkedPublicAppTransportBase(baseUrl,fetcher);if(JSON.stringify(policy)!==baseline||policy.automatic_retry!==false||policy.automatic_confirmation!==false||policy.query_persistence!==false)throw bad();};
 return {searchWebProducts:async(query:string,options?:ProductSearchOptions)=>{
  gate();options?.signal?.throwIfAborted();if(typeof query!=="string")throw bad();const normalized=query.normalize("NFKC").trim().replace(/\s+/g," ");
  if(Array.from(normalized).length<2||Array.from(normalized).length>policy.maximum_query_characters||/[\r\n@]/.test(query)||!/[a-z가-힣]/i.test(normalized)||/(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}/.test(normalized))throw bad();
  const bytes=crypto.getRandomValues(new Uint8Array(16));bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
  const hex=Array.from(bytes,x=>x.toString(16).padStart(2,"0")).join("");
  const requestId=hex.slice(0,8)+"-"+hex.slice(8,12)+"-"+hex.slice(12,16)+"-"+hex.slice(16,20)+"-"+hex.slice(20);
  const body=JSON.stringify({version:policy.version,query:normalized,request_id:requestId,transfer_consent:{version:transfer.version,accepted:true}});if(new TextEncoder().encode(body).length>policy.max_request_bytes)throw bad();
  const scope=memberStatusReadScope(bound,options),current=()=>{scope.gate();gate();};current();
  return scope.wait(()=>runWithMemberResponseSession(scope.load,onMemberChanged,async()=>{
   const token=await scope.load();if(!token)throw bad();current();
   if(!options?.confirmExternalTransfer || await scope.wait(()=>options.confirmExternalTransfer!(structuredClone(transfer),options.signal))!==true)throw new Error("인터넷 후보 찾기를 취소했어요. DB 검색은 계속 이용할 수 있어요.");current();
   const response=await scope.fetch(fetcher)(base.origin+policy.routes.search.path,{method:"POST",headers:{Authorization:"Bearer "+token,"Content-Type":"application/json"},body,signal:options?.signal,credentials:"omit",cache:"no-store",redirect:"error"});current();
   if(response.status!==200||response.redirected||response.headers.get("content-type")?.split(";")[0]!=="application/json"||response.headers.get("cache-control")?.trim().toLowerCase()!=="no-store")throw bad();
   const text=await response.text();current();if(new TextEncoder().encode(text).length>policy.max_response_bytes)throw bad();
   const candidates=await parsePublicWebCandidates(JSON.parse(text));current();return candidates;
  }));
 }};
}
