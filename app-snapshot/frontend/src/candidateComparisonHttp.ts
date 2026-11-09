/** Explicit synthetic TEST transport. Importing this module activates nothing. */
import config from "../../skin_engine/config/app_candidate_comparison.json";
import {parseCandidateComparison,type CandidateComparisonReader,type CandidateComparisonRequest} from "./candidateComparisonModel";
import {isMirayCandidateProvenanceHash,validateMirayCandidateSourceUrl} from "./miraySavedCandidates";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";

export type CandidateComparisonHttpOptions = {
  baseUrl:string; allowedBaseUrls:readonly string[];
  loadSessionToken:()=>Promise<string|null>;
  onSessionChanged?:()=>void;
};

function httpsBase(value:string):string {
  const url=new URL(value);
  if(url.protocol!=="https:"||url.username||url.password||url.search||url.hash)throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
}
const object=(v:unknown):v is Record<string,unknown>=>Boolean(v)&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:readonly string[])=>Object.keys(v).sort().join("|")===[...keys].sort().join("|");

function validate(request:unknown):asserts request is CandidateComparisonRequest {
  const invalid=()=>{throw new Error("비교할 제품 버전을 다시 확인해 주세요.");};
  if(!object(request)||!exact(request,config.request_fields)||request.schema_version!==config.version||request.deployment_context!==config.deployment_context||!Array.isArray(request.candidates)||request.candidates.length!==config.candidate_count)return invalid();
  const ids=[];
  for(const ref of request.candidates){
    if(!object(ref)||!exact(ref,config.candidate_fields)||typeof ref.product_id!=="string"||!ref.product_id.trim()||typeof ref.source_url!=="string"||typeof ref.provenance_hash!=="string"||!isMirayCandidateProvenanceHash(ref.provenance_hash))return invalid();
    try{validateMirayCandidateSourceUrl(ref.source_url);}catch{return invalid();}
    ids.push(ref.product_id);
  }
  if(new Set(ids).size!==ids.length)return invalid();
}

export function createHttpCandidateComparisonReader(fetcher:typeof fetch,options:CandidateComparisonHttpOptions):CandidateComparisonReader {
  if(!options.baseUrl.trim())throw new Error("앱 API 주소를 확인해 주세요.");
  const base=httpsBase(options.baseUrl.trim());
  if(!options.allowedBaseUrls.map(httpsBase).includes(base))throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const loadSessionToken=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  return async request=>{
    validate(request);
    // Freeze both transmitted evidence and response matching before awaiting a
    // phone token; caller mutation cannot replace either column mid-request.
    const snapshot=structuredClone(request);
    const body=JSON.stringify(snapshot);
    if(new TextEncoder().encode(body).byteLength>config.http.max_request_bytes)throw new Error("제품 비교 입력이 허용 크기를 넘었습니다.");
    const token=await loadSessionToken();
    if(!token||!/^[A-Za-z0-9_-]{32,200}$/.test(token))throw new Error("로그인 세션을 다시 확인해 주세요.");
    await assertCurrentMemberResponseSession(loadSessionToken,token,options.onSessionChanged);
    let response:Response;
    try {
      response=await fetcher(`${base}${config.http.path}`,{
        method:config.http.method,cache:"no-store",redirect:"error",credentials:"omit",
        headers:{Authorization:`Bearer ${token}`,"Content-Type":"application/json"},body,
      });
    } catch (error) {
      await assertCurrentMemberResponseSession(loadSessionToken,token,options.onSessionChanged);
      throw error;
    }
    await assertCurrentMemberResponseSession(loadSessionToken,token,options.onSessionChanged);
    if(!response.ok)throw new Error("제품 비교를 완료하지 못했어요.");
    let payload:unknown;
    try{payload=await response.json();}catch{
      await assertCurrentMemberResponseSession(loadSessionToken,token,options.onSessionChanged);
      throw new Error("제품 비교 응답을 확인하지 못했어요.");
    }
    await assertCurrentMemberResponseSession(loadSessionToken,token,options.onSessionChanged);
    return parseCandidateComparison(payload,snapshot);
  };
}
