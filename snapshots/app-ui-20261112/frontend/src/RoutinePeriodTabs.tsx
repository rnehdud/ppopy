import {useId,type ReactNode} from "react";
import "./routinePeriodTabs.css";
export type RoutinePeriod="am"|"pm";
/** Same morning/evening navigation for the saved routine and its review snapshot. */
export default function RoutinePeriodTabs({period,change,children}:{period:RoutinePeriod;change:(p:RoutinePeriod)=>void;children:ReactNode}){
 const id=useId();
 return <div className="routine-period-view">
  <div className="routine-period-tabs" role="tablist" aria-label="루틴 시간">
   {([['am','아침'],['pm','저녁']] as const).map(([p,label])=><button id={`${id}-${p}`} key={p} type="button" role="tab" aria-selected={period===p} tabIndex={period===p?0:-1} aria-controls={`${id}-panel`} onClick={()=>change(p)} onKeyDown={e=>{
    if(e.key!=="ArrowLeft"&&e.key!=="ArrowRight")return;e.preventDefault();const next=p==="am"?"pm":"am";change(next);document.getElementById(`${id}-${next}`)?.focus();
   }}>{label}</button>)}
  </div>
  <div id={`${id}-panel`} role="tabpanel" aria-labelledby={`${id}-${period}`}>{children}</div>
 </div>;
}
