import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import config from "../../skin_engine/config/miray_closed_loop_transitions.json";
import loop from "../../skin_engine/config/miray_closed_loop.json";
import {loopTime} from "./mirayClosedLoop";
export type TransitionProduct={id:string;name:string;frequency:string};
export type ProductChange={ref:string;action_type:string;before_product_id:string|null;after_product_id:string|null;frequency:string|null;effective_from:string};
export type ProductChangeView={version:string;decision_ref:string;decision_at:string;portfolio_revision:number;baseline_products:TransitionProduct[];current_products:TransitionProduct[];recorded_products:TransitionProduct[];confirmed_product_ids:string[];unregistered_product_ids:string[];actions:ProductChange[];followup_completed:boolean};
export type ProductChangeRequest={version:string;decision_ref:string;request_id:string;expected_portfolio_revision:number;action_type:string;before_product_id:string|null;after_product_id:string|null;frequency:string|null;effective_from:string};
export interface ProductChangeReviewStore{read(options?:MemberStatusReadOptions):Promise<unknown>;confirm(request:ProductChangeRequest,options?:MemberStatusReadOptions):Promise<unknown>;}
function exact(v:unknown,keys:string[]):Record<string,unknown>{if(!v || typeof v!=="object" || Array.isArray(v) || Object.keys(v).sort().join("|")!==[...keys].sort().join("|"))throw new Error("Unexpected transition fields");return v as Record<string,unknown>;}
function text(v:unknown):asserts v is string{if(typeof v!=="string" || !v.trim() || v.length>300)throw new Error("Bounded product text required");}
function ref(v:unknown):asserts v is string{if(typeof v!=="string" || !/^sha256:[0-9a-f]{64}$/.test(v))throw new Error("Transition identity required");}
export function parseProductChangeView(value:unknown):ProductChangeView{
  if(new TextEncoder().encode(JSON.stringify(value)).length>config.max_response_bytes)throw new Error("Bounded transition view required");
  const v=exact(value,["version","decision_ref","decision_at","portfolio_revision","baseline_products","current_products","recorded_products","confirmed_product_ids","unregistered_product_ids","actions","followup_completed"]);
  if(v.version!==config.version || !Number.isSafeInteger(v.portfolio_revision) || (v.portfolio_revision as number)<0 || typeof v.followup_completed!=="boolean")throw new Error("Reviewed transition version required");
  ref(v.decision_ref);loopTime(v.decision_at);
  const productSets=[];
  for(const key of ["baseline_products","current_products","recorded_products"]){const list=v[key];if(!Array.isArray(list) || list.length>(key==="recorded_products"?config.max_recorded_products:loop.max_actual_actions))throw new Error("Bounded products required");const ids=new Set<string>();
    for(const item of list){const p=exact(item,["id","name","frequency"]);text(p.id);text(p.name);if(ids.has(p.id) || !loop.frequency_values.includes(p.frequency as string))throw new Error("Invalid product projection");ids.add(p.id);}productSets.push(ids);}
  const [baseline,current,all]=productSets;
  if([...baseline,...current].some(id=>!all.has(id)))throw new Error("Missing recorded product");
  for(const key of ["confirmed_product_ids","unregistered_product_ids"]){const list=v[key];if(!Array.isArray(list) || list.length>loop.max_actual_actions*2 || new Set(list).size!==list.length)throw new Error("Bounded distinct products required");
    for(const id of list){text(id);if(!(key==="unregistered_product_ids"?current:all).has(id))throw new Error("Unknown transition product");}}
  if(!Array.isArray(v.actions) || v.actions.length>loop.max_actual_actions)throw new Error("Bounded actual actions required");
  const refs=new Set<string>(),touched=new Set<string>();
  for(const item of v.actions){const a=exact(item,["ref","action_type","before_product_id","after_product_id","frequency","effective_from"]);ref(a.ref);loopTime(a.effective_from);
    if(refs.has(a.ref) || !loop.actual_action_types.includes(a.action_type as string) || Date.parse(a.effective_from)<Date.parse(v.decision_at))throw new Error("Invalid actual transition");refs.add(a.ref);
    if(a.before_product_id!==null){text(a.before_product_id);if(!baseline.has(a.before_product_id))throw new Error("Unknown old product");}
    if(a.after_product_id!==null){text(a.after_product_id);if(!all.has(a.after_product_id) || !loop.frequency_values.includes(a.frequency as string))throw new Error("Unknown actual product");}
    else if(a.frequency!==null || a.before_product_id===null)throw new Error("Invalid actual removal");
    const targets=new Set([a.before_product_id,a.after_product_id].filter((id):id is string=>typeof id==="string"));
    for(const id of targets){if(touched.has(id))throw new Error("Overlapping actual confirmations");touched.add(id);}
  }
  if(JSON.stringify([...touched].sort())!==JSON.stringify([...(v.confirmed_product_ids as string[])].sort()))throw new Error("Actual confirmation identities differ");
  return structuredClone(value) as ProductChangeView;
}
export function productChangeRequest(view:ProductChangeView,action:string,before:string|null,after:string|null,frequency:string|null,effectiveFrom:string,requestId=crypto.randomUUID()):ProductChangeRequest{
  const v=parseProductChangeView(view);const old=new Set(v.baseline_products.map(p=>p.id)),current=new Set(v.current_products.map(p=>p.id));
  const shape=action==="product_added"?before===null && after!==null && !old.has(after):action==="product_removed"?before!==null && after===null:action==="repurchased_same"?before!==null && after===before:action==="product_replaced"?before!==null && after!==null && before!==after && !old.has(after):false;
  if(v.followup_completed || !config.supported_actions.includes(action) || !shape || (before!==null && !old.has(before)) || (after!==null && !current.has(after)) || v.confirmed_product_ids.some(id=>id===before || id===after))throw new Error("Unconfirmed registered transition required");
  if(action==="product_removed"?frequency!==null:!config.frequency_values.includes(frequency as string) || frequency==="0")throw new Error("Explicit active use required");
  loopTime(effectiveFrom);if(Date.parse(effectiveFrom)<Date.parse(v.decision_at) || Date.parse(effectiveFrom)>Date.now())throw new Error("Invalid use interval");
  if(!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(requestId))throw new Error("Request UUID required");
  return {version:config.version,decision_ref:v.decision_ref,request_id:requestId,expected_portfolio_revision:v.portfolio_revision,action_type:action,before_product_id:before,after_product_id:after,frequency,effective_from:effectiveFrom};
}
export function parseProductChangeAck(value:unknown):{version:string;saved_action_ref:string;view:ProductChangeView}{
  const v=exact(value,["version","saved_action_ref","view"]);if(v.version!==config.version)throw new Error("Reviewed change ACK required");ref(v.saved_action_ref);const view=parseProductChangeView(v.view);
  if(!view.actions.some(a=>a.ref===v.saved_action_ref))throw new Error("Saved transition missing from ACK");return {version:v.version as string,saved_action_ref:v.saved_action_ref,view};
}
