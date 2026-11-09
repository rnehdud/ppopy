import {useCallback,useEffect,useRef,useState} from "react";
import notice from "../../skin_engine/config/app_public_product_transfer_review.json";
export type ProductTransferNotice=typeof notice;
export type ConfirmProductTransfer=(value:ProductTransferNotice,signal?:AbortSignal)=>Promise<boolean>;

/** One affirmative choice per search. No remembered choice or signup substitution. */
export function useProductTransferConfirmation(owner:object){
 const [opened,setOpened]=useState(false),pending=useRef<null|((value:boolean)=>void)>(null),heading=useRef<HTMLHeadingElement>(null);
 useEffect(()=>()=>{pending.current?.(false);},[owner]);
 useEffect(()=>{if(opened)heading.current?.focus({preventScroll:true});},[opened]);
 const confirm=useCallback<ConfirmProductTransfer>((value,signal)=>{
  if(signal?.aborted||pending.current||JSON.stringify(value)!==JSON.stringify(notice))return Promise.resolve(false);
  return new Promise(resolve=>{
   const abort=()=>finish(false);
   const finish=(accepted:boolean)=>{if(pending.current!==finish)return;pending.current=null;signal?.removeEventListener("abort",abort);setOpened(false);resolve(accepted);};
   pending.current=finish;signal?.addEventListener("abort",abort,{once:true});setOpened(true);
  });
 },[]);
 const content=opened?<div className="product-transfer-backdrop"><section role="dialog" aria-modal="true" aria-labelledby="product-transfer-title" className="product-transfer-dialog" onKeyDown={event=>{
  if(event.key==="Escape"){event.preventDefault();pending.current?.(false);}
  if(event.key==="Tab") {const buttons=Array.from(event.currentTarget.querySelectorAll<HTMLElement>("button,a[href]"));const index=buttons.indexOf(document.activeElement as HTMLElement);event.preventDefault();buttons[index<0?(event.shiftKey?buttons.length-1:0):(index+(event.shiftKey?-1:1)+buttons.length)%buttons.length]?.focus();}
 }}><h2 id="product-transfer-title" ref={heading} tabIndex={-1}>인터넷 후보 찾기 전 확인해 주세요</h2>
 <p>{notice.items}를 {notice.country}의 {notice.recipient}로 보내 제품 후보와 공개 출처를 찾습니다. 동의한 이번 검색에만 전송합니다.</p>
 <p>{notice.retention_display}</p><p>{notice.refusal_effect}</p><p>피부 상태·알레르기·연락처는 검색어에 넣지 마세요.</p>
 <p><a href={notice.contact_url} target="_blank" rel="noopener noreferrer">OpenAI 개인정보 문의</a></p>
 <div><button type="button" onClick={()=>pending.current?.(false)}>DB 검색만 이용</button><button type="button" className="miray-primary" onClick={()=>pending.current?.(true)}>{notice.affirmative_label}</button></div>
 </section></div>:null;
 return {confirm,content};
}
