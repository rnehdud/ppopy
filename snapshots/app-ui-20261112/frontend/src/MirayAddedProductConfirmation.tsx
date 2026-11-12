import {useLayoutEffect,useRef,useState} from "react";
import {resetAppScroll} from "./appScroll";
import {productNamePresentation} from "./productPresentation";
import type {TestLoopStateView} from "./mirayClosedLoopStateTest";

/** A user-opened form; no registration, edit or recommendation confirms use. */
export default function MirayAddedProductConfirmation({products,decisionAt,allowCurrentUse=false,busy,onConfirm,onClose,onEditFrequency}:{decisionAt:string;products:NonNullable<TestLoopStateView["unregistered_products"]>["products"];allowCurrentUse?:boolean;busy:boolean;onConfirm(productId:string,frequency:string,effectiveFrom:string|null,mode?:"current_use"):void;onClose():void;onEditFrequency?(productId:string):void}){
  const [product,setProduct]=useState(""),[effective,setEffective]=useState(""),[explicit,setExplicit]=useState<string|null>(null);
  const [mode,setMode]=useState<""|"newly_started"|"current_use">(allowCurrentUse?"":"newly_started");
  const heading=useRef<HTMLHeadingElement|null>(null);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[]);
  const selected=products.find(p=>p.id===product);
  const frequency=selected?.frequency??"";
  const registeredFrequency=selected && (/^[1-7]$/.test(selected.frequency)?`주 ${selected.frequency}일`:selected.frequency==="0"?"사용하지 않음":selected.frequency==="unknown"?"모름":selected.frequency==="user_refused"?"답변하지 않음":selected.frequency==="user_does_not_remember"?"기억나지 않음":"아직 확인하지 않음");
  const instant=new Date(effective).getTime(),earliest=new Date(decisionAt).getTime();
  const confirmationKey=JSON.stringify([product,frequency,mode,effective]);
  const valid=!!selected && /^[1-7]$/.test(frequency) && explicit===confirmationKey && (mode==="current_use"?allowCurrentUse:mode==="newly_started" && !!effective && Number.isFinite(instant) && instant>=earliest && instant<=Date.now());
  const edit=(change:()=>void)=>{if(busy)return;change();setExplicit(null);};
  return <section className="miray-card miray-added-product-panel" aria-busy={busy}><h2 ref={heading} tabIndex={-1}>새 제품의 실제 사용 확인</h2>
    <p>제품을 목록에 추가한 것과 실제로 사용한 것은 따로 기록해요. 이전 기록은 유지해요.</p>
    {allowCurrentUse?<><p>이전부터 쓰던 제품을 늦게 등록했거나 시작일을 모르면 현재 사용만 확인할 수 있어요. 과거 사용 시작일이나 변경 이력을 만들지 않아요.</p><label>사용 확인 방법<select aria-label="사용 확인 방법" disabled={busy} value={mode} onChange={e=>edit(()=>{setMode(e.target.value as "newly_started"|"current_use");setEffective("");})}><option value="" disabled>선택해 주세요</option><option value="current_use">지금 사용 중이에요 · 시작일은 기록하지 않음</option><option value="newly_started">지난 점검 이후 사용을 시작했어요</option></select></label></>:<p>지난 점검 이후 실제로 사용하기 시작한 별도 제품만 직접 확인해 주세요.</p>}
    <label>현재 목록의 새 제품<select aria-label="현재 목록의 새 제품" disabled={busy} value={product} onChange={e=>edit(()=>{setProduct(e.target.value);setEffective("");})}><option value="" disabled>선택해 주세요</option>{products.map(p=><option key={p.id} value={p.id}>{productNamePresentation(p.name).name}</option>)}</select></label>
    {selected && <div><p><strong>사용 빈도: {registeredFrequency}</strong></p><p>내 화장품에 저장한 빈도예요. 맞으면 아래에서 실제 사용을 직접 확인해 주세요. 빈도가 다르면 먼저 수정할 수 있어요.</p>
      {!/^[1-7]$/.test(frequency) && <p role="status">사용 중인 빈도가 아직 확인되지 않았어요. 실제로 사용하는 경우에만 내 화장품의 빈도를 수정하고 돌아와 확인해 주세요. 모르는 내용은 채우지 않아도 돼요.</p>}
      {onEditFrequency && <button disabled={busy} onClick={()=>{if(!busy)onEditFrequency(selected.id);}}>사용 빈도 수정하기</button>}</div>}
    {mode==="newly_started" && <><label>사용하기 시작한 때<input aria-label="사용하기 시작한 때" type="datetime-local" disabled={busy} value={effective} onChange={e=>edit(()=>setEffective(e.target.value))}/></label>
    {effective && (instant<earliest || instant>Date.now()) && <p role="status">지난 점검 이후부터 현재까지 직접 확인한 시점이 필요해요. 이전부터 사용한 제품이거나 시점을 모르면 추측해서 저장하지 않아도 돼요.</p>}</>}
    <label className="miray-added-product-confirmation"><input type="checkbox" disabled={busy || !selected || !/^[1-7]$/.test(frequency)} checked={explicit===confirmationKey} onChange={e=>{if(!busy)setExplicit(e.target.checked?confirmationKey:null);}}/>{mode==="current_use"?"지금 위 제품을 이 빈도로 실제 사용하고 있음을 직접 확인해요":"위 제품을 이 빈도로 실제 사용했음을 직접 확인해요"}</label>
    <button className="miray-primary" disabled={busy || !valid} onClick={()=>{if(!busy && valid){if(mode==="current_use")onConfirm(product,frequency,null,"current_use");else onConfirm(product,frequency,new Date(effective).toISOString());}}}>{mode==="current_use"?"현재 사용 확인·저장":"새 제품 실제 사용 확인·저장"}</button>
    <p>모르거나 아직 사용하지 않았다면 확인하지 않아도 돼요. 연결 정보가 부족한 동안 새 점검을 보류하고 이용 횟수는 사용하지 않아요.</p>
    <button disabled={busy} onClick={onClose}>확인하지 않고 돌아가기</button>
  </section>;
}
