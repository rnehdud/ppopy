import contract from "../../skin_engine/config/kb_choice_member_candidate.json";
import {createBoundMemberResponseSessionLoader, runWithVerifiedMemberToken} from "./appMemberResponseSession";
import {memberStatusReadScope} from "./memberStatusReadScope";
import {checkedPublicAppTransportBase} from "./publicAppTransport";

export type MemberBinding={loadToken:()=>Promise<string|null>;onMemberChanged:()=>void};
export class MemberKbConflict extends Error {}
export type MemberKbClient=((channel:"read"|"intake",body:Record<string,unknown>,signal:AbortSignal)=>Promise<unknown>) & {overview?:(signal:AbortSignal)=>Promise<unknown>};
export function createMemberKbClient(base:string, fetcher:typeof fetch, member:MemberBinding, options:{overview?:boolean}={}):MemberKbClient {
  const url=checkedPublicAppTransportBase(base,fetcher);
  const bound=createBoundMemberResponseSessionLoader(member.loadToken,member.onMemberChanged);
  const client:MemberKbClient=async(channel, body, signal)=>{
    const scope=memberStatusReadScope(bound,{signal});
    const route=contract.routes.find(r=>r.operation==="member_"+channel);
    if(!route)throw new Error("점검 경로를 확인하지 못했어요.");
    const wire=JSON.stringify({...body,version:contract.version});
    return scope.wait(()=>runWithVerifiedMemberToken(scope.load,member.onMemberChanged,async token=>{
      scope.gate();
      const resp=await fetcher(url.origin+route.path,{method:route.method,headers:{Authorization:"Bearer "+token,"Content-Type":"application/json"},
        body:wire,credentials:"omit",cache:"no-store",redirect:"error",signal});
      scope.gate();
      if(resp.status===401){member.onMemberChanged();throw new Error("로그인 상태를 확인해 주세요.");}
      if(resp.status===400)throw new Error("현재 화면에 표시된 선택지를 다시 확인해 주세요.");
      if(resp.status===409)throw new MemberKbConflict("루틴이나 답변이 바뀌었어요. 현재 상태를 확인해 주세요.");
      if(resp.status!==200)throw new Error("서버에서 점검 상태를 확인하지 못했어요.");
      return resp.json();
    }));
  };
  // Opt in only in an app paired with an overview-capable server receipt.
  if(options.overview)client.overview=signal=>client("read",{command:"overview"},signal);
  return client;
}

export type Row={id:string;product_id:string;temporary_name:string|null;schedule:string;site:string;
  frequency:string;order:number|null;period_orders?:Record<string,number>;stage_label:string};
export type PopulationScope={version:"poppy-kb-adult-scope-v1";accepted_value:"adult";question:string;choices:Record<string,string>;unavailable_message:string};
export type SignupScope={version:"poppy-kb-signup-scope-v1";account_gate:"over_or_equal_14";source:"authenticated_signup_gate";separate_population_answer:false};
export type Draft={portfolio_revision:number;portfolio_fingerprint:string;catalog_sha256:string;rows:Row[];morning_water_only:boolean;population_scope?:PopulationScope;member_scope?:SignupScope};
type Question={path:string;text:string;options:string[];labels?:Record<string,string>;current?:string};
type Action={kind:string;title:string;body:string;message:string|null;question:string|null;answer:string|null};
type SourceDetail={id:string;title?:string;url?:string|null};
type UseScope={id:string;product_id:string;session:string|null;site:string|null;temporary_name?:string|null};
export type Display={schema:string;questions:Question[];guidance:{text:string;bucket:string}[];cards:{card:string;title?:string|null;version:string;status:string;text:string;sources:string[];scope?:string[];source_details?:SourceDetail[]}[];uses?:UseScope[];action_review:Action|null};
export type Turn={status:"ready"|"completed";operation_ref:string;step:number;display:Display;
  answer_controls:Question[];action_controls:{can_revise:boolean;editing:boolean;allow_change:boolean}|null};
export type History={records:{operation_ref:string;collected_at?:string;started_at?:string}[];next_cursor?:Record<string,string>|null};
// Owned by one live workspace/account/consent/portfolio revision. Display-only
// product drafts are reusable; answers, results and authorization are not cached.
export type MemberKbNavigation={operation:string|null;draft?:Draft;active?:History};
export function object(x:unknown):x is Record<string,unknown>{return x!==null&&typeof x==="object"&&!Array.isArray(x);}
const strings=(x:unknown):x is string[]=>Array.isArray(x)&&x.every(v=>typeof v==="string");
const ref=(x:unknown)=>typeof x==="string"&&/^sha256:[a-f0-9]{64}$/.test(x);
const invalid=()=>new Error("점검 응답의 형식을 확인하지 못했어요.");
export function asDraft(x:unknown):Draft{
  if(!object(x)||!Number.isSafeInteger(x.portfolio_revision)||![x.portfolio_fingerprint,x.catalog_sha256].every(v=>typeof v==="string"&&/^[a-f0-9]{64}$/.test(v))||
    typeof x.morning_water_only!=="boolean"||!Array.isArray(x.rows)||!x.rows.every(r=>object(r)&&
      [r.id,r.product_id,r.schedule,r.frequency,r.site,r.stage_label].every(v=>typeof v==="string")&&(r.temporary_name===null||typeof r.temporary_name==="string")&&
      (r.order===null||Number.isSafeInteger(r.order))&&(!r.period_orders||object(r.period_orders)&&Object.values(r.period_orders).every(Number.isSafeInteger))))throw invalid();
  if(x.population_scope!==undefined){
    const p=x.population_scope;
    if(!object(p)||p.version!=="poppy-kb-adult-scope-v1"||p.accepted_value!=="adult"||typeof p.question!=="string"||
      typeof p.unavailable_message!=="string"||!object(p.choices)||
      Object.keys(p.choices).sort().join(",")!=="adult,outside_scope,skipped,unknown"||!Object.values(p.choices).every(v=>typeof v==="string"))throw invalid();
  }
  if(x.member_scope!==undefined){
    const p=x.member_scope;
    if(!object(p)||p.version!=="poppy-kb-signup-scope-v1"||p.account_gate!=="over_or_equal_14"||
      p.source!=="authenticated_signup_gate"||p.separate_population_answer!==false)throw invalid();
  }
  return x as unknown as Draft;
}
const question=(q:unknown)=>object(q)&&typeof q.path==="string"&&typeof q.text==="string"&&strings(q.options)&&(!q.labels||object(q.labels)&&Object.values(q.labels).every(v=>typeof v==="string"));
export function asDisplay(x:unknown):Display{
  if(!object(x)||x.schema!=="poppy-kb-choice-result-v1"||!Array.isArray(x.questions)||!x.questions.every(question)||
    !Array.isArray(x.guidance)||!x.guidance.every(g=>object(g)&&typeof g.text==="string"&&typeof g.bucket==="string")||
    !Array.isArray(x.cards)||!x.cards.every(c=>object(c)&&[c.card,c.text,c.status].every(v=>typeof v==="string")&&strings(c.sources)&&
      (c.title==null||typeof c.title==="string")&&(c.scope===undefined||strings(c.scope))&&(c.source_details===undefined||Array.isArray(c.source_details)&&c.source_details.every(s=>object(s)&&typeof s.id==="string"&&
        (s.title===undefined||typeof s.title==="string")&&(s.url==null||typeof s.url==="string"))))||
    (x.uses!==undefined&&(!Array.isArray(x.uses)||!x.uses.every(u=>object(u)&&[u.id,u.product_id].every(v=>typeof v==="string")&&[u.session,u.site].every(v=>v===null||typeof v==="string")&&
      (u.temporary_name==null||typeof u.temporary_name==="string"))))||
    !(x.action_review===null||object(x.action_review)&&["kind","title","body"].every(k=>typeof (x.action_review as Record<string,unknown>)[k]==="string")&&
      ["message","question","answer"].every(k=>{const v=(x.action_review as Record<string,unknown>)[k];return v===null||typeof v==="string";})))throw invalid();
  return x as unknown as Display;
}
export function asTurn(x:unknown):Turn{
  if(!object(x)||!["ready","completed"].includes(String(x.status))||!ref(x.operation_ref)||!Number.isSafeInteger(x.step)||
    !Array.isArray(x.answer_controls)||!x.answer_controls.every(question)||
    !(x.action_controls===null||object(x.action_controls)&&Object.values(x.action_controls).every(v=>typeof v==="boolean")))throw invalid();
  asDisplay(x.display);return x as unknown as Turn;
}
export function asHistory(x:unknown):History{
  if(!object(x)||!Array.isArray(x.records)||!x.records.every(y=>object(y)&&ref(y.operation_ref)&&typeof (y.started_at??y.collected_at)==="string")||
     (x.next_cursor!=null&&(!object(x.next_cursor)||typeof x.next_cursor.collected_at!=="string"||!ref(x.next_cursor.record_ref))))throw invalid();
  return x as unknown as History;
}

/** Display-only edits. The server replays and validates these against its
 * current portfolio/catalogue at start; this never creates confirmed facts. */
export function previewMemberDraft(base:Draft, edits:Record<string,unknown>):Draft {
  const next:Draft={...base,rows:base.rows.map(r=>({...r,period_orders:r.period_orders?{...r.period_orders}:undefined}))};
  const slots=(s:string)=>s==="both"?["morning","evening"]:["morning","evening"].includes(s)?[s]:[];
  for(const [path,value] of Object.entries(edits)){
    if(path.startsWith("period_orders."))continue;
    if(path==="morning_water_only"){
      if(typeof value!=="boolean")throw invalid();
      next.morning_water_only=value;
      if(value)for(const r of next.rows.filter(r=>r.stage_label==="세정")){
        r.schedule=r.schedule==="both"?"evening":r.schedule==="morning"?"not_used":r.schedule;
      }
      continue;
    }
    const [kind,id,field,...extra]=path.split(".");
    const row=next.rows.find(r=>r.id===id);
    if(kind!=="rows"||!row||extra.length||!["schedule","frequency","site","order"].includes(field))throw invalid();
    if(field==="order"){
      if(!Number.isInteger(value)||Number(value)<1||Number(value)>100)throw invalid();
      row.order=Number(value);delete row.period_orders;
    } else {
      if(typeof value!=="string")throw invalid();
      row[field as "schedule"|"frequency"|"site"]=value;
      if(field==="schedule"&&row.stage_label==="세정"&&next.morning_water_only&&slots(value).includes("morning"))
        throw new Error("아침에 클렌저를 사용하려면 물세안 선택을 먼저 해제해 주세요.");
    }
  }
  for(const r of next.rows)if(r.period_orders)r.period_orders=Object.fromEntries(Object.entries(r.period_orders).filter(([s])=>slots(r.schedule).includes(s)));
  for(const [path,value] of Object.entries(edits).filter(([p])=>p.startsWith("period_orders."))){
    const [kind,id,slot,...extra]=path.split(".");const row=next.rows.find(r=>r.id===id);
    if(kind!=="period_orders"||!row||extra.length||!slots(row.schedule).includes(slot)||!Number.isInteger(value)||Number(value)<1||Number(value)>100)throw invalid();
    row.period_orders={...row.period_orders,[slot]:Number(value)};
  }
  return next;
}
