import {useLayoutEffect,useMemo,useRef,useState} from "react";
import {assertIntakeReviewOnly,completeIntake,emptyIntake,intakeSteps,intakeDecisionGaps,intakeDecisionLabels,parseIntakeAnswers,pendingIntakeStep,type IntakeAnswers} from "./mirayClosedLoopIntake";
import {resetAppScroll} from "./appScroll";
import "./mirayNextIntake.css";

export type IntakePanelView<T>={context:T;stored:boolean;answers:IntakeAnswers};
export interface IntakePanelStore<T>{read(options:{signal:AbortSignal;isCurrent?:()=>boolean}):Promise<IntakePanelView<T>>;save(context:T,answers:IntakeAnswers,options:{signal:AbortSignal;isCurrent?:()=>boolean}):Promise<IntakePanelView<T>>;}

function canonical(value:unknown):string {
  return JSON.stringify(value && typeof value==="object" && !Array.isArray(value)?Object.fromEntries(Object.entries(value).sort(([a],[b])=>a.localeCompare(b))):value);
}

/** Disabled injected review: one question per screen, no draft persistence. */
export default function MirayIntakePanel<T>({store,label,savedPurpose,onClose,onSaved,onReviewed,requestLifetime}:{store:IntakePanelStore<T>;label:string;savedPurpose:string;onClose():void;onSaved(context:T):void;onReviewed?(context:T,answers:IntakeAnswers):void;requestLifetime?:{isCurrent():boolean}}){
  const [draft,setDraft]=useState<IntakeAnswers>(emptyIntake),[stepId,setStepId]=useState<string|null>(null),[selected,setSelected]=useState<string[]>([]);
  const [phase,setPhase]=useState<"loading"|"question"|"review"|"stored"|"error">("loading"),[busy,setBusy]=useState(false);
  const binding=useMemo(()=>({store,requestLifetime,live:false,pending:null as AbortController|null,candidate:null as IntakeAnswers|null,target:null as T|null}),[store,requestLifetime]);
  const owner=useRef<typeof binding|null>(null);
  const frame=useMemo(()=>({binding,draft,stepId,selected,phase,busy}),[binding,draft,stepId,selected,phase,busy]);
  const currentFrame=useRef<typeof frame|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const frameLive=()=>live() && currentFrame.current===frame;
  const invalidateFrame=()=>{if(currentFrame.current===frame)currentFrame.current=null;};
  const retire=()=>{binding.live=false;binding.pending?.abort();binding.pending=null;binding.candidate=null;binding.target=null;if(owner.current===binding)owner.current=null;invalidateFrame();};
  const transition=(change:()=>void)=>{if(!frameLive() || busy)return;invalidateFrame();change();};
  const heading=useRef<HTMLHeadingElement|null>(null);
  const run=async(save=false)=>{
    if(!live() || binding.pending || (save && (!frameLive() || phase!=="review")))return;
    const c=new AbortController();binding.pending=c;invalidateFrame();setBusy(true);
    try{
      assertIntakeReviewOnly();const answers=parseIntakeAnswers(draft);
      if(save){if(!completeIntake(answers))throw new Error("Incomplete intake");binding.candidate=answers;}
      if(save && binding.target===null)throw new Error("Input target missing");
      const v=await (save?store.save(structuredClone(binding.target!),structuredClone(answers),{signal:c.signal,isCurrent:live}):store.read({signal:c.signal,isCurrent:live}));
      c.signal.throwIfAborted();if(!live())return;assertIntakeReviewOnly();
      // An injected port may return a borrowed or malformed receipt. Confirm
      // and copy answers before retaining them or exposing the saved handoff.
      if(typeof v.stored!=="boolean")throw new Error("Input receipt unconfirmed");
      const receivedAnswers=parseIntakeAnswers(v.answers);
      if(v.stored && !completeIntake(receivedAnswers))throw new Error("Saved complete input required");
      if(binding.target!==null && canonical(v.context)!==canonical(binding.target))throw new Error("Input target changed");
      binding.target=structuredClone(v.context);
      const sameAnswers=(left:IntakeAnswers,right:IntakeAnswers)=>Object.keys(left).every(k=>left[k].state===right[k].state && canonical(left[k].value)===canonical(right[k].value));
      if(v.stored){if(binding.candidate && !sameAnswers(receivedAnswers,binding.candidate))throw new Error("Saved original differs");setDraft(receivedAnswers);setStepId(null);setPhase("stored");}
      else if(save)throw new Error("Save not confirmed");
      else if(binding.candidate){setPhase("review");} // ACK recovery found no record; explicit resubmit only.
      else{const next=pendingIntakeStep(receivedAnswers);setDraft(receivedAnswers);setStepId(next?.id??null);setPhase(next?"question":"review");}
    }catch{if(live() && !c.signal.aborted)setPhase("error");}
    finally{if(binding.pending===c){binding.pending=null;if(live())setBusy(false);}}
  };
  useLayoutEffect(()=>{
    binding.live=true;owner.current=binding;setDraft(emptyIntake());setStepId(null);setSelected([]);binding.candidate=null;binding.target=null;setPhase("loading");setBusy(false);
    let attached=true;void Promise.resolve().then(()=>{if(attached)void run();});
    return()=>{attached=false;retire();};
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  useLayoutEffect(()=>{resetAppScroll();if(phase==="question")heading.current?.focus({preventScroll:true});},[phase,stepId]);
  const close=()=>{if(!frameLive())return;retire();setDraft(emptyIntake());setSelected([]);setStepId(null);setPhase("loading");setBusy(false);onClose();};
  const step=intakeSteps.find(s=>s.id===stepId);
  const answer=(patch:IntakeAnswers)=>{
    if(!frameLive() || busy || phase!=="question")return;invalidateFrame();
    const next=parseIntakeAnswers({...draft,...patch});setDraft(next);setSelected([]);binding.candidate=null;
    if(Object.values(patch).some(a=>a.state==="unknown" || a.state==="user_refused")){setPhase("review");return;}
    const pendingStep=pendingIntakeStep(next);setStepId(pendingStep?.id??stepId);setPhase(pendingStep?"question":"review");
  };
  const multi=(none=false)=>{
    if(!step || step.kind!=="multi" || (!none && !selected.length))return;
    const field=step.fields[0],value=field==="care_priorities"?(none?[]:selected):none?{}:Object.fromEntries(step.items!.map(i=>[i.value,selected.includes(i.value)]));
    answer({[field]:{state:none?"none_reported":"reported",value}});
  };
  const answerLabel=(s:typeof intakeSteps[number])=>{
    if(s.kind==="single")return s.choices!.find(c=>s.fields.every(f=>canonical((c.answers as IntakeAnswers)[f].value)===canonical(draft[f].value)))?.label??"답변을 확인하지 못했어요";
    const value=draft[s.fields[0]].value;
    const chosen=s.items!.filter(i=>s.id==="habits"?(value as Record<string,boolean>)[i.value]:(value as string[]).includes(i.value));
    return chosen.length?chosen.map(i=>i.label).join(", "):"해당하는 항목이 없어요";
  };
  const blockedAreas=phase==="review"? [...new Set(intakeDecisionGaps(draft).gaps.filter(g=>
    g.missing.some(a=>a.state==="unknown" || a.state==="user_refused") ||
    g.missing.length!==intakeSteps.find(s=>s.id===g.step_id)!.fields.length).flatMap(g=>g.decision_areas))]:[];
  return <section className="miray-card miray-intake" aria-label={label} aria-busy={busy}><button className="miray-intake-close" onClick={close}>입력 확인 닫기</button>
    <p className="miray-intake-intro">루틴 점검에 필요한 제품 사용 정보와 피부 반응을 확인해요. 모르는 내용은 추측하지 않아도 돼요.</p>
    {busy && <p role="status">저장된 입력을 확인하는 중이에요.</p>}
    {phase==="error"?<div role="alert" className="miray-intake-recovery"><p>입력 저장 여부를 확인하지 못했어요. 답변을 다시 보내기 전에 저장 상태를 확인해 주세요.</p><button className="miray-intake-primary" disabled={busy} onClick={()=>{if(frameLive())void run();}}>입력 저장 상태 확인</button></div>:
     phase==="stored"?<><h2>이번 상태에 연결된 입력을 확인했어요</h2><p>같은 입력을 다시 묻거나 덮어쓰지 않아요. 점검 시작은 다음 화면에서 직접 선택해 주세요.</p><button className="miray-intake-primary" disabled={busy} onClick={()=>{if(!frameLive() || busy || binding.target===null)return;const context=structuredClone(binding.target);retire();onSaved(context);}}>점검 요청 화면으로</button></>:
     phase==="review"?<><h2>{completeIntake(draft)?"점검 입력을 확인했어요":"정보가 부족해 점검을 보류해요"}</h2>
       <p>{completeIntake(draft)?onReviewed?"확인한 답변으로 루틴 점검 요청 화면으로 이동해요. 아직 답변을 저장하거나 점검을 시작하지 않았어요.":`명시한 답변만 ${savedPurpose}에 연결해 저장해요. 저장만으로 점검을 시작하거나 실제 제품 사용을 기록하지 않아요.`:"모름·답변 거부·아직 묻지 않은 항목을 구분해요. 남은 질문을 자동으로 이어 묻거나 답을 채우지 않아요. 이 불완전 입력은 계정에 저장하지 않아요."}</p>
       {blockedAreas.length>0 && <><p>답변을 확인하지 못해 다음 판단을 보류해요.</p><ul>{blockedAreas.map(area=><li key={area}>{intakeDecisionLabels[area as keyof typeof intakeDecisionLabels]}</li>)}</ul></>}
       {completeIntake(draft)?<><dl>{intakeSteps.map(s=><div key={s.id}><dt>{s.title}</dt><dd>{answerLabel(s)}</dd></div>)}</dl><button className="miray-intake-primary" disabled={busy} onClick={()=>{
         if(!onReviewed){void run(true);return;}
         if(!frameLive() || busy || binding.target===null)return;
         const context=structuredClone(binding.target),answers=parseIntakeAnswers(draft);if(!completeIntake(answers))return;retire();onReviewed(context,answers);
       }}>{onReviewed?"확인한 입력으로 점검 준비":"확인한 입력 저장"}</button>{intakeSteps.map(s=><button className="miray-intake-edit" key={s.id} disabled={busy} onClick={()=>transition(()=>{setStepId(s.id);const v=draft[s.fields[0]].value;setSelected(s.kind==="multi"?s.id==="habits"?Object.keys(v as object).filter(k=>(v as Record<string,boolean>)[k]):v as string[]:[]);setPhase("question");})}>수정: {s.title}</button>)}</>:<button className="miray-intake-primary" onClick={()=>transition(()=>{setSelected([]);setPhase("question");})}>방금 답변 다시 확인</button>}
       </>:
     phase==="question" && step?<><p className="miray-intake-progress">입력 확인 {intakeSteps.indexOf(step)+1} / {intakeSteps.length}</p><h2 tabIndex={-1} ref={heading}>{step.title}</h2><p>{step.decision}</p>
       {step.kind==="single"?step.choices!.map((choice,i)=><button className="miray-intake-choice" key={i} onClick={()=>answer(choice.answers as IntakeAnswers)}>{choice.label}</button>):<>
         <fieldset><legend>해당하는 항목을 모두 선택해 주세요</legend>{step.items!.map(item=><label key={item.value}><input type="checkbox" checked={selected.includes(item.value)} onChange={e=>{const checked=e.target.checked;transition(()=>setSelected(old=>checked?[...old,item.value]:old.filter(x=>x!==item.value)));}}/>{item.label}</label>)}</fieldset>
         <p>선택을 확인하면 선택하지 않은 항목은 해당하지 않는다는 답변으로 기록해요.</p>
         <button className="miray-intake-primary" disabled={!selected.length} onClick={()=>multi()}>선택한 답변 확인</button><button className="miray-intake-choice" onClick={()=>multi(true)}>해당하는 항목이 없어요</button>
       </>}
       <button className="miray-intake-missing" onClick={()=>answer(Object.fromEntries(step.fields.map(f=>[f,{state:"unknown",value:null}])))}>모르겠어요 — 점검 보류</button>
       <button className="miray-intake-missing" onClick={()=>answer(Object.fromEntries(step.fields.map(f=>[f,{state:"user_refused",value:null}])))}>답하지 않을게요 — 점검 보류</button>
     </>:null}
  </section>;
}
