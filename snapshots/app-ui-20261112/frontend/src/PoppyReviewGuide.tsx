import type {ReactNode} from "react";
import {PoppyCompanion} from "./PoppyCompanion";
import "./poppyReviewGuide.css";

type Phase="intro"|"submitting"|"question"|"answered"|"result"|"saved";
const messages:Partial<Record<Phase,string>>={
  intro:"다르게 쓰는 부분만 고쳐 주세요.",
  submitting:"답변을 보내고 있어요. 잠시만 기다려 주세요.",
  answered:"답변을 반영했어요.",
  result:"확인된 내용으로 루틴 안내를 정리했어요.",
  saved:"저장된 점검이에요.",
};

/** Presentation of acknowledged app state; never an inference/progress claim. */
export function PoppyReviewGuide({phase,safety=false,children}:{phase:Phase;safety?:boolean;children?:ReactNode}){
  const message=messages[phase];
  return <div className={`kb-popo-guide${safety?" kb-popo-guide-safety":""}`} data-phase={phase}>
    {!safety&&<PoppyCompanion size={48} state={phase==="submitting"?"thinking":phase==="answered"?"greeting":"idle"} paused={phase!=="submitting"&&phase!=="answered"}/>}
    <div className="kb-popo-copy">
      <span className="kb-popo-name" aria-hidden="true">{safety?"점검 안내":"포포"}</span>
      {message&&<p role={phase==="submitting"||phase==="answered"||phase==="saved"?"status":undefined}>{message}</p>}
      {children}
    </div>
  </div>;
}
