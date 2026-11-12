/** Presentation-only names backed by the same public listing and ordered formula.
 * The catalog record, its version, price, and ownership evidence remain unchanged.
 */
export const CATALOG_SINGLE_PRODUCT_NAMES: Readonly<Record<string, string>> = {
  "브링그린 징크테카 트러블 세럼 대용량 기획": "브링그린 징크테카 트러블 세럼",
  "풀리 쌀 세라 수분 선크림 50ml ( 단품 / 기획 )": "풀리 쌀 세라 수분 선크림 50ml",
  "닥터지 그린 마일드 업 선 플러스 50ml 기획 2 종 (50+20/50+50+10) ( 선크림 )": "닥터지 그린 마일드 업 선 플러스 50ml",
  "닥터지 브라이트닝 업 선 플러스 50ml 기획 2 종 (50+20/50+50+10) ( 선크림 )": "닥터지 브라이트닝 업 선 플러스 50ml",
  "프롬리에 EGF 워터 화잘먹 선앰플 56ml+30ml 기획 / 단품": "프롬리에 EGF 워터 화잘먹 선앰플 56ml",
  "한율 보들은행잎 모공핏 세럼 기획 40ml 기획": "한율 보들은행잎 모공핏 세럼 40ml",
  "라운드랩 1025 독도 토너 500ml 기획 (+100ml)": "라운드랩 1025 독도 토너 500ml",
  "파티온 노스카나인 트러블 세럼 50ml 리필 기획 (+ 리필 40ml+ 크림 10ml)": "파티온 노스카나인 트러블 세럼 50ml",
  "토리든 다이브인 저분자 히알루론산 세럼 50ml 기획 (+ 멀티 패드 10 매 )": "토리든 다이브인 저분자 히알루론산 세럼 50ml",
  "에스트라 아토베리어 365 크림 80ml 기획 (+ 토너 25ml+ 클렌징폼 3g*3EA)": "에스트라 아토베리어 365 크림 80ml",
  "비플레인 녹두 약산성 클렌징폼 160ml 더블 기획": "비플레인 녹두 약산성 클렌징폼 160ml",
  "제로이드 핌프로브 젤 클렌저 180ml 기획 (+ 핌프로브 크림 10ml)": "제로이드 핌프로브 젤 클렌저 180ml",
  "에스네이처 아쿠아 라이스 약산성 클렌징폼 160ml 기획 (+ 클렌징폼 20ml)": "에스네이처 아쿠아 라이스 약산성 클렌징폼 160ml",
  "구달 맑은 어성초 진정 수분 선크림 50ml 1+1 기획": "구달 맑은 어성초 진정 수분 선크림 50ml",
  "[ 민감피부 추천 무기자차 ] 제로이드 데일리 선크림 기획 (50ml+50ml)": "제로이드 데일리 선크림 50ml",
  "달바 퍼플 톤업 선크림 듀오 기획 (50ml+50ml)": "달바 퍼플 톤업 선크림 50ml",
  "비플레인 녹두 쿨링 수분 선크림 50ml 1+1 기획 (+10ml)": "비플레인 녹두 쿨링 수분 선크림 50ml",
  "닥터지 레드블레미쉬 클리어 수딩크림 EX 70ml 기획 (+30ml+ 세럼 10ml*2ea)": "닥터지 레드블레미쉬 클리어 수딩크림 EX 70ml",
  "넘버즈인 5 번 글루타치온 C 흔적 앰플 30ml+30ml 듀오기획": "넘버즈인 5번 글루타치온 C 흔적 앰플 30ml",
  "썸바이미 아하 바하 파하 30 데이즈 미라클 토너 기획세트 (150ml+30ml)": "썸바이미 아하 바하 파하 30 데이즈 미라클 토너 150ml",
  "넘버즈인 1 번 판토텐산 액티브업 수딩세럼 50ml 리필기획 (50ml+50ml)": "넘버즈인 1번 판토텐산 액티브업 수딩세럼 50ml",
};

/** Names of existing child records whose parent transcription was reassembled
 * exactly and whose component tokens match. The original IDs and evidence stay. */
export const CATALOG_COMPONENT_NAMES: Readonly<Record<string, {original: string; name: string}>> = {
  "웰라쥬-히알루로닉블루100앰플-01--component-01": {
    original: "웰라쥬 앰플", name: "웰라쥬 리얼 히알루로닉 블루 100 앰플 100ml",
  },
  "에스네이처-213171--component-01": {
    original: "에스네이처 토너", name: "에스네이처 아쿠아 오아시스 토너 300ml",
  },
  "에스네이처-202893--component-01": {
    original: "에스네이처 수분 젤크림 (원문 헤더 없음)", name: "에스네이처 아쿠아 오아시스 수분 젤크림 90ml",
  },
};
