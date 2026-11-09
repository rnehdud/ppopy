import policy from "../../skin_engine/config/app_freemium.json";
import "./freemiumPlans.css";

/** Planning preview only. It cannot grant entitlement, count usage or buy. */
export default function FreemiumPlanComparison() {
  const [free, plus] = [policy.plans.free, policy.plans.plus];
  return <section className="freemium-plans" aria-labelledby="freemium-title">
    <h2 id="freemium-title">무료와 플러스 이용 범위</h2>
    <p>플러스는 월 {policy.price_krw.toLocaleString("ko-KR")}원으로 준비 중이에요. 별도 유료 구독 무료체험 없이 무료 기능부터 이용할 수 있어요.</p>
    <p className="freemium-age-note">{policy.copy.minor_purchase_detail}</p>
    <dl className="freemium-common">
      <dt>누구나 이용할 수 있어요</dt>
      <dd>제품명 검색·직접 입력, 확인된 전성분과 출처, 내 제품 등록</dd>
      <dt>언제나 무료예요</dt>
      <dd>안전 안내·불편 신고, 보관 중인 내 결과 열람, 정보 삭제·동의 철회·구독 관리</dd>
    </dl>
    <div className="freemium-grid">
      <article aria-labelledby="freemium-free-title">
        <h3 id="freemium-free-title">{free.label}</h3>
        <p>내 제품과 현재 루틴을 점검해요</p>
        <ul>
          <li>AI 제품 찾기 월 {free.ai_product_lookup}회</li>
          <li>전체 루틴 점검 월 {free.routine_review}회</li>
          <li>완전한 성분안과 안전 안내</li>
        </ul>
      </article>
      <article aria-labelledby="freemium-plus-title">
        <h3 id="freemium-plus-title">{plus.label}</h3>
        <p>제품이 바뀔 때 다시 점검하고 관리해요</p>
        <ul>
          <li>AI 제품 찾기 결제주기당 {plus.ai_product_lookup}회</li>
          <li>전체 루틴 점검 횟수 제한 없음</li>
          <li>제품 변경 전후 루틴 비교</li>
          <li>정기 체크인·다음 관리 안내</li>
        </ul>
      </article>
    </div>
    <details>
      <summary>이용 횟수와 보관기간 안내</summary>
      <p>{policy.copy.lookup_detail}</p>
      <p>실패·취소나 기존 결과 다시 보기에는 횟수를 차감하지 않아요.</p>
      <p>{policy.copy.reset_detail}</p>
      <p>{policy.copy.fallback_detail}</p>
      <p>{policy.copy.retention_detail}</p>
    </details>
  </section>;
}
