import type { RoutineObservation } from "./careApi";
import { followupQuestions, missingOptions } from "./routineObservation";

const questions: Record<string, {label: string; values: Array<[string, string]>}> = {
  timing: {label: "불편감을 느낀 시점", values: [["recent", "최근 7일"], ["earlier", "그 이전"]]},
  ongoing: {label: "현재도 지속되나요?", values: [["yes", "예"], ["no", "아니요"]]},
  duration: {label: "불편감은 얼마나 이어졌나요?", values: [["brief", "잠시 후 사라짐"], ["persistent", "한동안 이어짐"]]},
  other_recent_changes: {label: "다른 제품을 최근 2주에 새로 쓰거나 사용 빈도를 바꿨나요?", values: [["none", "변화 없음"], ["new_product", "새 제품 사용"], ["frequency_changed", "사용 빈도 변경"], ["both", "둘 다"]]},
  application_site: {label: "제품을 바른 부위", values: [["whole_face", "얼굴 전체"], ["localized", "일부 부위"], ["other", "그 외"]]},
  amount: {label: "평소와 비교한 사용량", values: [["less_than_usual", "평소보다 적게"], ["usual", "평소대로"], ["more_than_usual", "평소보다 많이"]]},
};

export default function RoutineFollowup({observation, onAnswer}: {
  observation: RoutineObservation; onAnswer: (question: string, value: string) => void;
}) {
  const next = followupQuestions(observation)[0];
  return <div className="routine-followup">
    <p>제품과 불편감의 인과관계는 아직 확인되지 않았습니다. 기억나지 않거나 답하고 싶지 않은 항목은 다시 묻지 않습니다.</p>
    {next && <label>{questions[next].label}<select aria-label={questions[next].label} value="not_asked" onChange={e => onAnswer(next, e.target.value)}>
      <option value="not_asked" disabled>선택해 주세요</option>
      {questions[next].values.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
      {missingOptions.filter(([value]) => value !== "not_asked").map(([value, label]) => <option key={value} value={value}>{label}</option>)}
    </select></label>}
    {!!observation.context?.answered.length && <p role="status">답한 항목은 보존했습니다. 남은 확인 질문 {followupQuestions(observation).length}개</p>}
    <dl aria-label="보존한 사용 경험 답변">{observation.context?.answered.map(q => {
      const values: Record<string, unknown> = {...observation.context, ...observation.details};
      const label = [...questions[q].values, ...missingOptions, ["refused", "응답하지 않음"]].find(([value]) => value === values[q])?.[1] || String(values[q]);
      return <div key={q}><dt>{questions[q].label}</dt><dd>{label}</dd></div>;
    })}</dl>
  </div>;
}
