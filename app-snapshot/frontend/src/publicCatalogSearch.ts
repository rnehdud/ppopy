import policy from "../../skin_engine/config/app_public_catalog_search_review.json";
import consumer from "../../skin_engine/config/consumer_api.json";
import {checkedPublicAppTransportBase} from "./publicAppTransport";
import {createBoundMemberResponseSessionLoader,runWithMemberResponseSession} from "./appMemberResponseSession";
import {memberStatusReadScope} from "./memberStatusReadScope";
import {isMirayCandidateProvenanceHash,validateMirayCandidateSourceUrl} from "./miraySavedCandidates";
import {isRoutineProductCategory} from "./routineProductGroups";
import type {CareApiClient,ProductSearchOptions} from "./careApi";
import type {ProductCandidate} from "./productCatalog";
const object=(v:unknown):v is Record<string,unknown>=>v!==null&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
const unavailable=()=>new Error("제품 후보를 확인하지 못했어요.");
export function parsePublicCatalogCandidates(value:unknown):ProductCandidate[]{
 if(!object(value)||!exact(value,["schema_version","auto_confirmed","candidates"])||value.schema_version!==consumer.request_schema_version||value.auto_confirmed!==false||!Array.isArray(value.candidates)||value.candidates.length>policy.maximum_candidates)throw unavailable();
 const seen=new Set<string>();
 return value.candidates.map(raw=>{
  if(!object(raw)||!(exact(raw,["product_id","brand","name","option","category","ingredient_evidence_status","recommendation_eligible","requires_user_confirmation","source_url","provenance_hash"])||exact(raw,["product_id","brand","name","option","category","ingredient_evidence_status","recommendation_eligible","requires_user_confirmation","source_url","provenance_hash","ingredient_disclosure"]))||
    !["product_id","brand","name","option","category"].every(k=>typeof raw[k]==="string"&&(raw[k] as string).length<=300)||!raw.product_id||!raw.name||seen.has(raw.product_id as string)||
    !["owner_verified","automation_verified","review_required"].includes(String(raw.ingredient_evidence_status))||typeof raw.recommendation_eligible!=="boolean"||raw.requires_user_confirmation!==true||
    (raw.source_url===null)!==(raw.provenance_hash===null))throw unavailable();
  if(raw.source_url!==null){if(typeof raw.source_url!=="string"||typeof raw.provenance_hash!=="string"||!isMirayCandidateProvenanceHash(raw.provenance_hash))throw unavailable();validateMirayCandidateSourceUrl(raw.source_url);}
  const disclosure=raw.ingredient_disclosure;
  if(disclosure!==undefined&&disclosure!==null&&(!object(disclosure)||!exact(disclosure,["text","observed_at"])||typeof disclosure.text!=="string"||!disclosure.text.trim()||new TextEncoder().encode(disclosure.text).length>8000||typeof disclosure.observed_at!=="string"||!/^\d{4}-\d{2}-\d{2}(?:T.*)?$/.test(disclosure.observed_at)||!Number.isFinite(Date.parse(disclosure.observed_at))||raw.source_url===null||!["owner_verified","automation_verified"].includes(String(raw.ingredient_evidence_status))))throw unavailable();
  seen.add(raw.product_id as string);
  return {id:raw.product_id as string,brand:raw.brand as string,name:raw.name as string,option:raw.option as string,evidenceStatus:raw.ingredient_evidence_status as ProductCandidate["evidenceStatus"],matchSource:"catalog" as const,
    ...(isRoutineProductCategory(raw.category)?{category:raw.category}:{}),...(raw.source_url!==null?{sourceUrl:raw.source_url as string,provenanceHash:raw.provenance_hash as string}:{}),
    ...(object(disclosure)?{ingredientDisclosure:{text:disclosure.text as string,observedAt:disclosure.observed_at as string}}:{})};
 });
}
export function createPublicCatalogSearchClient({baseUrl,fetcher,loadToken,onMemberChanged,includeIngredients=false}:{baseUrl:string;fetcher:typeof fetch;loadToken:()=>Promise<string|null>;onMemberChanged():void;includeIngredients?:boolean}):Pick<CareApiClient,"searchProducts">{
 const url=checkedPublicAppTransportBase(baseUrl,fetcher),baseline=JSON.stringify(policy),bound=createBoundMemberResponseSessionLoader(loadToken,onMemberChanged);
 const gate=()=>{checkedPublicAppTransportBase(baseUrl,fetcher);if(JSON.stringify(policy)!==baseline||policy.version!=="1.0.0-public-catalog-search-20261021"||policy.automatic_retry!==false||policy.automatic_confirmation!==false||policy.query_persistence!==false||policy.provider_calls!==false||policy.recommendation_bonus_from_search!==false)throw unavailable();};
 return {searchProducts:async(query:string,options?:ProductSearchOptions)=>{
  gate();options?.signal?.throwIfAborted();if(typeof query!=="string")throw unavailable();
  const normalized=query.normalize("NFKC").trim().replace(/\s+/g," ");
  if(!normalized||Array.from(normalized).length>policy.maximum_query_characters||/[\r\n@]/.test(query)||!/[0-9a-z가-힣]/i.test(normalized)||/(?:\+?82[- ]?)?0\d{1,2}[- ]?\d{3,4}[- ]?\d{4}/.test(normalized))throw unavailable();
  const body=JSON.stringify({version:policy.version,query:normalized,...(includeIngredients?{include_ingredients:true}:{})});if(new TextEncoder().encode(body).length>policy.max_request_bytes)throw unavailable();
  const scope=memberStatusReadScope(bound,options),current=()=>{scope.gate();gate();};current();
  return scope.wait(()=>runWithMemberResponseSession(scope.load,onMemberChanged,async()=>{
   const token=await scope.load();if(!token)throw unavailable();current();
   const response=await scope.fetch(fetcher)(url.origin+policy.routes.search.path,{method:policy.routes.search.method,headers:{Authorization:"Bearer "+token,"Content-Type":"application/json"},body,signal:options?.signal,credentials:"omit",cache:"no-store",redirect:"error"});current();
   if(response.status!==200||response.redirected||response.headers.get("content-type")?.split(";")[0]!=="application/json"||response.headers.get("cache-control")?.trim().toLowerCase()!=="no-store")throw unavailable();
   const text=await response.text();current();if(new TextEncoder().encode(text).length>policy.max_response_bytes)throw unavailable();return parsePublicCatalogCandidates(JSON.parse(text));
  }));
 }};
}
