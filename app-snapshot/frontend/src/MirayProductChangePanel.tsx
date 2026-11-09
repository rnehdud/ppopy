import {useLayoutEffect,useMemo,useRef,useState} from "react";
import {resetAppScroll} from "./appScroll";
import {parseProductChangeAck,parseProductChangeView,productChangeRequest,type ProductChangeView,type ProductChangeReviewStore} from "./mirayClosedLoopTransitions";
import config from "../../skin_engine/config/miray_closed_loop_transitions.json";
const labels:Record<string,string>={product_added:"새 제품을 추가해 사용",product_replaced:"다른 제품으로 바꿔 사용",repurchased_same:"같은 제품을 재구매해 새 용기 사용",product_removed:"제품 사용을 끝냄"};
/** User-opened optional input. Never adds a default state question. */
export default function MirayProductChangePanel({store,active,decisionRef,onClose,requestLifetime}:{store:ProductChangeReviewStore;active:boolean;decisionRef:string;onClose():void;requestLifetime?:{isCurrent():boolean}}){
  const binding=useMemo(()=>({store,active,decisionRef,requestLifetime,live:false,pending:null as AbortController|null}),[store,active,decisionRef,requestLifetime]);
  const current=useRef<typeof binding|null>(null);
  const [loaded,setLoaded]=useState<{binding:typeof binding;view:ProductChangeView}|null>(null);
  const [action,setAction]=useState(""),[before,setBefore]=useState(""),[after,setAfter]=useState(""),[frequency,setFrequency]=useState(""),[effective,setEffective]=useState("");
  const [explicit,setExplicit]=useState(false),[busy,setBusy]=useState(false),[error,setError]=useState(""),[saved,setSaved]=useState(false);
  const heading=useRef<HTMLHeadingElement|null>(null);
  const view=active && loaded?.binding===binding?loaded.view:null;
  const frame=useMemo(()=>({binding,view,action,before,after,frequency,effective,explicit,busy,error,saved}),[binding,view,action,before,after,frequency,effective,explicit,busy,error,saved]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && current.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && currentFrame.current===frame;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;if(current.current===binding)current.current=null;if(currentFrame.current?.binding===binding)currentFrame.current=null;};
  const edit=(change:()=>void)=>{if(!frameLive() || binding.pending)return;invalidateFrame();change();setExplicit(false);};
  const reset=()=>{setLoaded(null);setAction("");setBefore("");setAfter("");setFrequency("");setEffective("");setExplicit(false);setError("");setSaved(false);};
  const read=async()=>{if(!live() || !binding.active || binding.pending)return;const c=new AbortController();binding.pending=c;invalidateFrame();reset();setBusy(true);
    try{const response=await binding.store.read({signal:c.signal,isCurrent:live});c.signal.throwIfAborted();if(!live())return;const v=parseProductChangeView(response);if(v.decision_ref!==binding.decisionRef)throw new Error("Different decision");setLoaded({binding,view:v});}
    catch{if(live() && !c.signal.aborted)setError("read");}finally{if(binding.pending===c){binding.pending=null;if(live())setBusy(false);}}};
  const refresh=()=>{if(frameLive())void read();};
  useLayoutEffect(()=>{binding.live=true;current.current=binding;reset();setBusy(false);
    // Wait for the parent frame to commit; cleanup also fences StrictMode replay.
    let attached=true;if(active)void Promise.resolve().then(()=>{if(attached)void read();});
    return()=>{attached=false;retire();};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[saved]);
  const close=()=>{if(!frameLive())return;retire();reset();onClose();};
  const save=async()=>{if(!frameLive() || !view || binding.pending || !explicit || !active || error || saved)return;
    let request;
    try{request=productChangeRequest(view,action,action==="product_added"?null:before,action==="product_removed"?null:action==="repurchased_same"?before:after,action==="product_removed"?null:frequency,new Date(effective).toISOString());}
    catch{setError("input");return;}
    const c=new AbortController();binding.pending=c;invalidateFrame();setBusy(true);
    try{const response=await binding.store.confirm(structuredClone(request),{signal:c.signal,isCurrent:live});c.signal.throwIfAborted();if(!live())return;const ack=parseProductChangeAck(response);const a=ack.view.actions.find(v=>v.ref===ack.saved_action_ref);
      if(ack.view.decision_ref!==view.decision_ref || view.actions.some(v=>v.ref===ack.saved_action_ref) || !a || a.action_type!==request.action_type || a.before_product_id!==request.before_product_id || a.after_product_id!==request.after_product_id || a.frequency!==request.frequency || a.effective_from!==request.effective_from)throw new Error("Mismatched actual change ACK");
      setLoaded({binding,view:ack.view});setSaved(true);
    }catch{if(live() && !c.signal.aborted)setError("save");}finally{if(binding.pending===c){binding.pending=null;if(live())setBusy(false);}}
  };
  const old=view?.baseline_products.filter(p=>!view.confirmed_product_ids.includes(p.id) && (action!=="repurchased_same" || view.current_products.some(v=>v.id===p.id)))??[];
  const added=view?.current_products.filter(p=>!view.baseline_products.some(v=>v.id===p.id) && !view.confirmed_product_ids.includes(p.id))??[];
  if(!active)return <main className="miray-main"><p>계정과 이력 저장 동의를 확인해 주세요.</p><button onClick={close}>닫기</button></main>;
  return <main className="miray-main miray-loop-panel"><button onClick={close}>‹ 실제 사용·상태 확인으로</button><h1 ref={heading} tabIndex={-1}>제품·용기 변경 직접 기록</h1>
    <p>직접 선택한 경우에만 기록해요. 제품 목록 편집이나 구매 클릭은 실제 사용 확인으로 처리하지 않아요.</p>
    {busy && <p role="status">이력을 확인하는 중이에요.</p>}
    {error && <section role="alert" className="miray-card"><p>{error==="input"?"제품과 실제 사용 빈도, 점검 이후의 시작 시점을 확인해 주세요.":"저장 여부를 확인하지 못했어요. 다시 저장하기 전에 최신 이력을 확인해 주세요."}</p><button disabled={busy} onClick={refresh}>최신 제품 변경 이력 확인</button></section>}
    {view && !error && (saved?<section className="miray-card" role="status"><h2>직접 확인한 제품 변경을 저장했어요</h2><p>실제 사용과 새 용기 이력에 연결했어요. 제품 목록과 사용 빈도는 자동 수정하지 않아요.</p><button onClick={close}>현재 상태 확인으로 돌아가기</button></section>:view.followup_completed?<p>이번 후속 상태 확인은 이미 완료했어요.</p>:<section className="miray-card">
      <label>직접 확인할 변경<select aria-label="직접 확인할 변경" disabled={busy} value={action} onChange={e=>edit(()=>{setAction(e.target.value);setBefore("");setAfter("");setFrequency("");setEffective("");})}><option value="" disabled>선택해 주세요</option>{config.supported_actions.map(v=><option key={v} value={v}>{labels[v]}</option>)}</select></label>
      {action && <>
        {action!=="product_added" && <label>이전 제품<select aria-label="이전 제품" disabled={busy} value={before} onChange={e=>edit(()=>setBefore(e.target.value))}><option value="" disabled>선택해 주세요</option>{old.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}</select></label>}
        {["product_added","product_replaced"].includes(action) && <label>현재 목록의 새 제품<select aria-label="현재 목록의 새 제품" disabled={busy} value={after} onChange={e=>edit(()=>setAfter(e.target.value))}><option value="" disabled>선택해 주세요</option>{added.map(p=><option key={p.id} value={p.id}>{p.name}</option>)}</select></label>}
        {["product_added","product_replaced"].includes(action) && !added.length && <p>새 제품을 화장품 목록에 등록한 뒤 다시 열어 주세요. 목록 등록만으로 사용했다고 기록하지 않아요.</p>}
        {action!=="product_added" && !old.length && <p>이번 점검에서 아직 확인하지 않은 이전 제품이 없어요. 이미 확인한 변경을 덮어쓰지 않아요.</p>}
        {action!=="product_removed" && <label>변경 후 실제 사용 빈도<select aria-label="변경 후 실제 사용 빈도" disabled={busy} value={frequency} onChange={e=>edit(()=>setFrequency(e.target.value))}><option value="" disabled>선택해 주세요</option>{config.frequency_values.filter(v=>v!=="0").map(v=><option key={v} value={v}>주 {v}일</option>)}</select></label>}
        {action==="repurchased_same" && <p>새로 구매했더라도 아직 사용하지 않았다면 기록하지 마세요. 새 용기를 실제로 사용하기 시작했을 때 확인해 주세요.</p>}
        <label>{action==="product_removed"?"사용을 끝낸 때":"새 제품·용기를 사용하기 시작한 때"}<input aria-label="제품 변경 시작 시점" type="datetime-local" disabled={busy} value={effective} onChange={e=>edit(()=>setEffective(e.target.value))}/></label>
        <label className="miray-product-change-confirmation"><input type="checkbox" checked={explicit} disabled={busy} onChange={e=>{if(frameLive() && !binding.pending){invalidateFrame();setExplicit(e.target.checked);}}}/>위 내용을 실제로 수행했음을 직접 확인해요</label>
        <button className="miray-primary" disabled={busy || !explicit || !effective || (action!=="product_added" && !before) || (["product_added","product_replaced"].includes(action) && !after) || (action!=="product_removed" && !frequency)} onClick={()=>void save()}>제품 변경 실제 사용 확인·저장</button>
      </>}
    </section>)}
    {view && !error && view.actions.length>0 && <section className="miray-card"><h2>저장된 실제 사용 기록</h2><p>이번 점검에 {view.actions.length}건을 직접 확인했어요. 같은 제품의 변경을 다시 덮어쓰지 않아요.</p></section>}
  </main>;
}
