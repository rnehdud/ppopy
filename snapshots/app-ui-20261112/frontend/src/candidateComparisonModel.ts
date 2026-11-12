import config from "../../skin_engine/config/app_candidate_comparison.json";
import palette from "../../skin_engine/config/ingredient_palette.json";
import type {MirayExploreCandidate} from "./mirayExploreSearch";
import {isMirayCandidateProvenanceHash,validateMirayCandidateSourceUrl} from "./miraySavedCandidates";

export type CandidateComparisonRequest = {
  schema_version:string; deployment_context:"synthetic_test";
  candidates:Array<{product_id:string;source_url:string;provenance_hash:string}>;
};
export type CandidateComparisonProduct = {
  product_id:string;name:string;source_url:string;provenance_hash:string;
  evidence_status:"owner_verified"|"automation_verified";ingredients:string[];
  palette:Array<{key:string;label:string;present:boolean|null}>;
};
export type CandidateComparison = {
  schema_version:string;deployment_context:"synthetic_test";status:"ready"|"unavailable";
  products:CandidateComparisonProduct[];message:string;presence_note:string;persistence:"none";
};
/** Explicit TEST reader only; this module does not create HTTP or fixture fallback. */
export type CandidateComparisonReader = (request:CandidateComparisonRequest)=>Promise<unknown>;

export function candidateComparisonRequest(candidates:readonly MirayExploreCandidate[]):CandidateComparisonRequest|null {
  if(candidates.length!==config.candidate_count||new Set(candidates.map(c=>c.id)).size!==candidates.length)return null;
  const refs=[];
  for(const c of candidates){
    if(c.source!=="catalog"||!["owner_verified","automation_verified"].includes(c.evidenceStatus)||!c.sourceUrl||!isMirayCandidateProvenanceHash(c.provenanceHash??""))return null;
    try{validateMirayCandidateSourceUrl(c.sourceUrl);}catch{return null;}
    refs.push({product_id:c.id,source_url:c.sourceUrl,provenance_hash:c.provenanceHash!});
  }
  return{schema_version:config.version,deployment_context:"synthetic_test",candidates:refs};
}
const object=(v:unknown):v is Record<string,unknown>=>Boolean(v)&&typeof v==="object"&&!Array.isArray(v);
const exact=(v:Record<string,unknown>,keys:string[])=>Object.keys(v).sort().join("|")===keys.sort().join("|");
export function parseCandidateComparison(value:unknown,request:CandidateComparisonRequest):CandidateComparison {
  const invalid=()=>new Error("제품 비교 응답을 확인하지 못했어요.");
  if(!object(value)||!exact(value,["schema_version","deployment_context","status","products","message","presence_note","persistence"])||value.schema_version!==config.version||value.deployment_context!=="synthetic_test"||value.persistence!=="none"||!["ready","unavailable"].includes(String(value.status))||!Array.isArray(value.products)||value.presence_note!==config.copy.presence_only||value.message!==config.copy[value.status as "ready"|"unavailable"])throw invalid();
  if(value.status==="unavailable"){if(value.products.length)throw invalid();return structuredClone(value) as CandidateComparison;}
  if(value.products.length!==request.candidates.length||value.products.length!==config.candidate_count)throw invalid();
  const keys=Object.keys(palette.ingredients);
  for(let i=0;i<value.products.length;i++){
    const p:unknown=value.products[i];const expected=request.candidates[i];
    if(!object(p)||!exact(p,["product_id","name","source_url","provenance_hash","evidence_status","ingredients","palette"])||p.product_id!==expected.product_id||p.source_url!==expected.source_url||p.provenance_hash!==expected.provenance_hash||typeof p.name!=="string"||!p.name.trim()||!["owner_verified","automation_verified"].includes(String(p.evidence_status))||!Array.isArray(p.ingredients)||!p.ingredients.length||p.ingredients.some(x=>typeof x!=="string"||!x.trim())||!Array.isArray(p.palette)||p.palette.length!==keys.length)throw invalid();
    for(let j=0;j<keys.length;j++){
      const row:unknown=p.palette[j];const key=keys[j] as keyof typeof palette.ingredients;
      if(!object(row)||!exact(row,["key","label","present"])||row.key!==key||row.label!==palette.ingredients[key].display||(row.present!==null&&typeof row.present!=="boolean"))throw invalid();
    }
  }
  return structuredClone(value) as CandidateComparison;
}
