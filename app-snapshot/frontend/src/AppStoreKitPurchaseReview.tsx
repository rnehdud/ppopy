import {useContext,useLayoutEffect,useMemo,useRef,useState} from "react";
import "./storeKitPurchaseReview.css";
import freemium from "../../skin_engine/config/app_freemium.json";
import {AppSettingsLifetimeContext} from "./appSettingsLifetime";
import {assertStoreKitPurchaseReviewOnly,parseStoreKitOfferReview,parseStoreKitInteractionReview,
  type StoreKitPurchaseReviewPort,type StoreKitOfferReview,type StoreKitInteractionReview} from "./storeKitPurchaseReviewContract";

/** Local UI integration only; the explicit port has no installed native bridge. */
export default function AppStoreKitPurchaseReview({port,onInteractionStart}:{port:StoreKitPurchaseReviewPort;onInteractionStart:()=>void}){
  const lifetime=useContext(AppSettingsLifetimeContext);
  const binding=useMemo(()=>({port,lifetime,onInteractionStart,live:false,busy:false,unsettled:false,controller:null as AbortController|null}),[port,lifetime,onInteractionStart]);
  const owner=useRef<typeof binding|null>(null);
  type View={binding:typeof binding;stage:"idle"|"loading"|"offer"|"working"|"outcome"|"error";offer?:StoreKitOfferReview;outcome?:StoreKitInteractionReview};
  const [view,setView]=useState<View|null>(null);
  const current=view?.binding===binding?view:null;
  const frame=useMemo(()=>({binding,current}),[binding,current]);const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>binding.live && owner.current===binding && (!lifetime || lifetime.live);
  useLayoutEffect(()=>{
    binding.live=true;owner.current=binding;
    return()=>{binding.live=false;binding.controller?.abort();if(owner.current===binding)owner.current=null;};
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const run=(action:"offer"|"purchase"|"restore")=>{
    if(!live() || currentFrame.current!==frame || binding.busy)return;
    try{
      assertStoreKitPurchaseReviewOnly();
      if(action==="purchase"){
        if(binding.unsettled || !current?.offer || !parseStoreKitOfferReview(current.offer).can_purchase)return;
        // A cancellation, throw or empty restore is never proof of no purchase.
        binding.unsettled=true;
      }
    }catch{if(live())setView({binding,stage:"error"});return;}
    currentFrame.current=null;binding.busy=true;
    const controller=new AbortController();binding.controller=controller;
    const isCurrent=()=>live() && binding.controller===controller && !controller.signal.aborted;
    setView({binding,stage:action==="offer"?"loading":"working"});
    void Promise.resolve().then(async()=>{
      if(!isCurrent())return;
      assertStoreKitPurchaseReviewOnly();
      if(action==="purchase" && (!current?.offer || !parseStoreKitOfferReview(current.offer).can_purchase))throw new Error("Product view expired");
      if(action!=="offer"){binding.onInteractionStart();if(!isCurrent())return;}
      const options={signal:controller.signal,isCurrent};
      const raw=await (action==="offer"?port.readOffer(options):action==="purchase"?port.purchaseExplicit(options):port.restoreExplicit(options));
      if(!isCurrent())return;
      assertStoreKitPurchaseReviewOnly();
      if(action==="offer")setView({binding,stage:"offer",offer:parseStoreKitOfferReview(raw)});
      else setView({binding,stage:"outcome",outcome:parseStoreKitInteractionReview(raw,action)});
    }).catch(()=>{if(isCurrent())setView({binding,stage:"error"});}).finally(()=>{
      if(binding.controller===controller){binding.controller=null;binding.busy=false;}
    });
  };
  const busy=current?.stage==="loading" || current?.stage==="working";
  const outcome=current?.outcome;
  const message=outcome?.state==="pending"?"App Store의 구매 확인을 기다리고 있어요. 다시 구매하지 말고 구매 내역을 복원해 주세요."
    :outcome?.state==="user_cancelled"?"구매 화면을 닫았어요. 처리 중인 구매가 있는지는 구매 내역 복원으로 확인해 주세요."
    :outcome?.state==="awaiting_server_status" && outcome.recorded_count===0?"복원에서 확인된 내역이 없어요. 구독 종료나 구매 취소가 확인된 것은 아닙니다."
    :outcome?"구매 내역 확인을 마쳤어요. 현재 구독 상태는 ‘상태 다시 확인’에서 확인해 주세요.":null;
  return <section className="app-subscription-status app-store-purchase-review" aria-labelledby="app-store-review-title" aria-busy={busy}>
    <h2 id="app-store-review-title">플러스 구독</h2>
    <p>구독은 매월 자동 갱신됩니다. 취소·관리는 App Store에서 할 수 있어요. 구독과 선택 이력 저장 동의·데이터 삭제는 별도로 처리됩니다.</p>
    <p>{freemium.copy.minor_purchase_detail}</p>
    {busy && <p role="status">{current.stage==="loading"?"상품을 확인하고 있어요.":"구매 내역을 확인하고 있어요."}</p>}
    {current?.offer && <>
      <p>월 {current.offer.price.toLocaleString("ko-KR")}원</p>
      <p>무료 체험은 제공하지 않아요. 구매 확정 금액은 App Store 결제 화면에서 확인해 주세요.</p>
      <p>{freemium.copy.reset_detail}</p>
      {!current.offer.can_purchase && <p role="status">지금은 새 구매를 진행할 수 없어요. 기존 구매 내역을 복원하거나 구독 상태를 확인해 주세요.</p>}
      <button className="app-store-primary" type="button" disabled={busy || binding.unsettled || !current.offer.can_purchase} onClick={()=>run("purchase")}>App Store에서 구매하기</button>
    </>}
    {message && <p role="status">{message}</p>}
    {current?.stage==="error" && <p role="alert">확인을 마치지 못했어요. 다시 구매하지 말고 구매 내역을 복원하거나 구독 상태를 확인해 주세요.</p>}
    {!busy && !binding.unsettled && <button className={current?.offer || outcome || current?.stage==="error"?"app-store-secondary":"app-store-primary"} type="button" onClick={()=>run("offer")}>구독 상품 확인</button>}
    <button className={outcome || current?.stage==="error" || current?.offer?.can_purchase===false?"app-store-primary":"app-store-secondary"} type="button" disabled={busy} onClick={()=>run("restore")}>구매 내역 복원</button>
  </section>;
}
