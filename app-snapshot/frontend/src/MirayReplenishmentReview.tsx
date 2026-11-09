import {useLayoutEffect, useRef} from "react";
import type {ProductCandidate} from "./productCatalog";
import type {MirayProductDepletionStatus} from "./mirayPortfolio";
import {productPresentation} from "./productPresentation";
import {isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl} from "./miraySavedCandidates";
import {resetAppScroll} from "./appScroll";

export type ReplenishmentCheck = "ready" | "consent" | "history_consent" | "unsettled" | "routine_incomplete" | "unavailable";
const labels:Record<ReplenishmentCheck,string>={ready:"현재 상태로 전체 루틴 점검",consent:"민감정보 동의 확인",history_consent:"이력 저장 선택 동의 확인",unsettled:"현재 상태로 전체 루틴 점검",routine_incomplete:"사용 시간 먼저 확인",unavailable:"루틴 점검 연결 준비 중"};
const frequencyLabels:Record<string,string>={unknown:"모름",user_refused:"응답 거부",user_does_not_remember:"기억하지 못함","0":"사용하지 않음"};
const periodLabels:Record<string,string>={am:"아침",pm:"저녁",both:"아침·저녁"};
const statusLabels:Record<MirayProductDepletionStatus,string>={empty:"소진됐어요",running_low:"거의 다 썼어요",enough:"여유 있어요",not_tracking:"기록하지 않음"};

/** Declared availability is reference data, never purchase or actual-use evidence. */
export default function MirayReplenishmentReview({product,status,frequency,period,total,check,portfolioMessage,requiredConsent=false,onClose,onCheck}:{
  product:ProductCandidate;status:MirayProductDepletionStatus;frequency:string;period:string;total:number;check:ReplenishmentCheck;portfolioMessage:string;requiredConsent?:boolean;onClose():void;onCheck():void;
}) {
  const heading=useRef<HTMLHeadingElement|null>(null);
  useLayoutEffect(()=>{resetAppScroll();heading.current?.focus({preventScroll:true});},[product.id]);
  const display=productPresentation(product);
  let source:string|null=null;
  if(product.evidenceStatus!=="fixture_only" && product.sourceUrl && typeof product.provenanceHash==="string" && isMirayCandidateProvenanceHash(product.provenanceHash)){
    try{validateMirayCandidateSourceUrl(product.sourceUrl);source=product.sourceUrl;}catch{/* No guessed or incomplete product reference. */}
  }
  const frequencyLabel=frequencyLabels[frequency] ?? (/^[1-7]$/.test(frequency)?`주 ${frequency}일`:"기록하지 않음");
  return <main className="miray-main">
    <button type="button" onClick={onClose}>‹ 내 화장품으로</button>
    <h1 ref={heading} tabIndex={-1}>재구매 전에 확인해요</h1>
    <section className="miray-card">
      <h2>{display.name}</h2>{display.subtitle && <p>{display.subtitle}</p>}
      <p>{statusLabels[status] ?? "기록하지 않음"} · 직접 기록한 상태</p>
      <p>{frequencyLabel} · {periodLabels[period] ?? "사용 시간 미기록"}</p>
      <p>남은 양과 소진 날짜는 이 기록으로 추정하지 않아요.</p>
      {source?<><a href={source} target="_blank" rel="noreferrer">제품 출처 다시 확인</a><p>용량과 전성분이 지금 쓰는 제품과 같은지 확인해 주세요. 저장된 출처는 최신 처방이나 판매처 검증을 보장하지 않아요.</p></>:<p>제품 출처와 전성분 버전 근거를 아직 확인하지 못했어요.</p>}
    </section>
    <section className="miray-card">
      <h2>현재 상태와 루틴 함께 살피기</h2>
      <p>등록한 전체 {total}개 제품을 함께 점검해요.</p>
      <p>소진 기록만으로 재구매를 권하거나 제품·사용 빈도를 바꾸지 않아요. 새 용기를 실제로 쓰기 시작한 뒤에는 점검 이력에서 직접 기록할 수 있어요.</p>
      <p role="status">{portfolioMessage}</p>
      {check==="unsettled" && <p>화장품 저장 결과를 먼저 확인해 주세요.</p>}
      {check==="unavailable" && <p>전체 루틴 점검 연결을 준비 중이에요. 제품 정보는 계속 확인할 수 있어요.</p>}
      <button type="button" className="miray-primary" disabled={check==="unsettled" || check==="unavailable"} onClick={onCheck}>{requiredConsent && ["consent","history_consent"].includes(check)?"필수 동의 확인":labels[check]}</button>
    </section>
  </main>;
}
