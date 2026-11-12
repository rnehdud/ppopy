import consumerCopy from "./memberKbConsumerCopy.json";
import {productNamePresentation} from "./productPresentation";

// Consumer headings only. The engine's card IDs, versions, comparisons and
// original evidence remain untouched in the server's saved result.
const headings:Record<string,string>={
  "B-C01":"세안할 때 물 온도","B-C02":"세안 도구와 문지르는 정도","B-C03":"세안제를 사용하는 시간",
  "B-C04":"세안제 선택","B-C05":"세안 횟수와 단계","B-C06":"세안 후 헹구기",
  "B-M01":"세안 후 보습 시점","B-M02":"보습제 사용량과 횟수","B-M03":"현재 제품의 보습 역할",
  "B-M04":"손 보습과 사용감","B-M05":"면도 후 보습",
  "B-P01":"야외 활동에 맞는 자외선 차단","B-P02":"선크림 사용량과 바르는 부위","B-P03":"선크림 다시 바르기",
  "B-P04":"그늘과 옷을 이용한 자외선 차단","B-P05":"선크림 성분 정보","B-P06":"선크림 사용 후 눈의 불편감",
  "B-P07":"선크림 제품 정보","B-P08":"선크림 사용기한과 보관","B-P09":"분사형 선크림 사용 방법",
  "B-G01":"향료와 사용감","B-G02":"제품별 사용량과 횟수","B-G03":"제품에 안내된 사용법",
  "B-G04":"제품을 섞어 쓰는 방법","B-G05":"추가 관리 제품의 사용법","B-G06":"미용기기와 함께 쓰는 방법",
  "B-G07":"불편할 때 추가 관리 조정","B-G08":"제품 유형과 사용 방법","B-G09":"면도 전 준비",
  "B-G10":"면도 방향과 압력","B-G11":"새 제품의 작은 부위 사용","B-G12":"새 제품을 도입하는 순서",
  "B-G13":"레티노이드와 각질관리 제품","B-G14":"레티노이드와 각질관리 제품","B-G15":"각질관리 제품을 함께 쓰는 방법",
  "B-G16":"제품 표시와 사용하는 부위","B-G17":"알레르기와 제품 표시","B-G18":"비타민 C와 카퍼펩타이드 함께 쓰기","B-B01":"진료 지시와 지속되는 불편감",
  "B-S01":"보관 온도와 햇빛","B-S02":"사용기한과 개봉 시점","B-S03":"용기와 위생적인 사용",
  "B-S04":"제품 상태 변화","B-S05":"피부에 닿는 도구 관리","B-S06":"면도기 상태","B-S07":"제품 공유와 리필",
  "B-I01":"선크림 사용과 세안","B-I02":"겹쳐 바르는 방법과 불편감","B-I03":"관리 전후의 변화",
  "B-I04":"각질관리 중 보습과 자외선 차단","B-H01":"주기적인 피부 변화","B-H02":"최근 치료·관리·생활 변화",
  "B-Q01":"필요한 제품과 보유 제품","B-Q02":"제품 구매 경로","B-Q03":"사용 중인 제품 확인",
  "B-Q04":"개봉 전 제품 상태","B-Q05":"제품 회수 안내","B-Q06":"제품 품질 문의",
  "B-L01":"다른 부위 제품과의 접촉","B-L02":"세제·물 사용과 손 관리","B-L03":"마찰·땀·장비 접촉",
};
export const evidenceHeading=(card:string)=>headings[card]??"루틴 점검 항목";

// Replace only names explicitly attached to the displayed result, never general
// questionnaire text or a product ID/formulation reference.
export function scopedProductText(text:string,names:readonly string[]){
  for(const name of [...new Set(names)].filter(Boolean).sort((a,b)=>b.length-a.length)){
    const shown=productNamePresentation(name).name;
    if(shown!==name)text=text.split(name).join(shown);
  }
  return text;
}

// Source registry U rows are design input, not this member's observations.
// D rows describe service defaults; neither is external clinical evidence.
export function evidenceSourceLabel(id:string,title?:string){
  if(/^D\d+$/.test(id))return "뽀피의 루틴 점검 기준";
  if(/^U\d+$/.test(id))return "점검 기준을 정할 때 참고한 사용 의견";
  if(!title || /\.(md|json|ya?ml)$|^(?:KB|B-[A-Z]\d+)/i.test(title))return "참고 자료";
  return title;
}

// Exact source matching keeps historical decisions and stored wording intact.
// This is presentation only, never a new condition or a clinical endorsement.
export function consumerGuidanceText(card:string,status:string,source:string){
  const row=(consumerCopy.cards as Record<string,Record<string,{source:string;text:string}>>)[card]?.[status];
  if(row?.source===source)return row.text;
  const extra=(consumerCopy.exact_additional_text as Record<string,string>)[source];
  if(extra)return extra;
  if(status==="conflicting")return "답변이 서로 달라 이 부분은 아직 정하지 않았어요.";
  if(status==="unknown")return "이 항목은 아직 확인하지 않았어요.";
  if(/판단을 바꿀 때만|일반 원칙만 안내|기본값을 강제|미확인을 정상|기준으로 연결|근거 조회|가설|on_known|source_blind|서비스 기본값/.test(source)
      || /(?:안내한다|검토한다|판단한다|보류한다|선언하지 않는다|자동 확정하지 않는다)\.?$/.test(source))
    return "이 항목의 자세한 안내는 아직 정리 중이에요. 참고한 자료를 함께 확인해 주세요.";
  return source;
}

export const consumerBodyText=(source:string)=>(consumerCopy.exact_additional_text as Record<string,string>)[source]??source;
