import type {SelectHTMLAttributes} from "react";

/** Older answers retain their stored provenance until the member changes them. */
export default function ProductFrequencySelect({value, ...props}: SelectHTMLAttributes<HTMLSelectElement>) {
  return <select {...props} value={value ?? ""}>
    <option value="" disabled>선택해 주세요</option>
    {value === "user_refused" && <option value="user_refused" disabled>답변하지 않았어요</option>}
    {value === "user_does_not_remember" && <option value="user_does_not_remember" disabled>기억나지 않아요</option>}
    {[0,1,2,3,4,5,6,7].map(days => <option key={days} value={String(days)}>{days === 0 ? "사용하지 않음" : `주 ${days}일`}</option>)}
    <option value="unknown">모름</option>
  </select>;
}
