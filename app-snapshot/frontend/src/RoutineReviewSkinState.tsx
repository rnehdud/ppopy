import {useLayoutEffect, useMemo, useRef, useState} from "react";
import questionsConfig from "../../skin_engine/config/miray_skin_state_questions.json";
import {resetAppScroll} from "./appScroll";
import {parseSkinStateHomeTasks,validateMiraySkinState,type MiraySkinState,type MiraySkinStateStore,type MiraySkinStateSaveResult} from "./miraySkinState";
import "./miraySkinStateCheckin.css";

type QuestionId = keyof typeof questionsConfig.questions;
type Answers = Pick<MiraySkinState, QuestionId>;
type Question = {title:string; accessibility_label:string; options:Array<{value:string;label:string}>; multiple?:boolean; show_when?:{field:keyof Answers;value:string}};
const questions: Record<QuestionId,Question> = questionsConfig.questions as Record<QuestionId,Question>;
const initialAnswers = (): Answers => ({concern_presence:"not_asked",persistence:"not_asked",recent_change:"not_asked",discomfort_presence:"not_asked",discomfort_types:[],sensitivity_history:"not_asked"});

export default function MiraySkinStateCheckin({kind = "baseline", historyStorageConsented, store, requestLifetime, continueToAnalysis = true, completionMode = "standalone", questionProfile = questionsConfig.default_profile as keyof typeof questionsConfig.profiles, onComplete, onCancel}: {
  kind?: MiraySkinState["kind"];
  historyStorageConsented: boolean;
  continueToAnalysis?: boolean;
  /** Collect locally for the separate final confirmation; never save twice. */
  completionMode?: "standalone" | "collect_for_followup" | "collect_for_entry";
  /** Extended context is opt-in only when a reviewed decision actually consumes it. */
  questionProfile?: keyof typeof questionsConfig.profiles;
  store?: MiraySkinStateStore;
  /** Parent navigation ownership only; never consent or server settlement. */
  requestLifetime?: {isCurrent(): boolean};
  onComplete(value: MiraySkinState, result?: MiraySkinStateSaveResult): void;
  onCancel(): void;
}) {
  const [answers,setAnswers] = useState<Answers>(initialAnswers);
  const [step,setStep] = useState(0);
  const [busy,setBusy] = useState(false);
  const [error,setError] = useState("");
  const [finished,setFinished] = useState(false);
  const inputScope = useMemo(() => ({store,kind,completionMode,questionProfile}), [store,kind,completionMode,questionProfile]);
  const binding = useMemo(() => ({inputScope,historyStorageConsented,continueToAnalysis,requestLifetime,live:false,pending:null as AbortController|null,submission:null as MiraySkinState|null}), [inputScope,historyStorageConsented,continueToAnalysis,requestLifetime]);
  const owner = useRef<typeof binding|null>(null);
  const frame = useMemo(() => ({binding,answers,step,busy,error,finished}), [binding,answers,step,busy,error,finished]);
  const currentFrame = useRef<typeof frame|null>(null);
  const live = () => {
    try{return binding.live && owner.current === binding && (!requestLifetime || requestLifetime.isCurrent()===true);}catch{return false;}
  };
  const frameLive = () => live() && currentFrame.current === frame && !finished;
  const invalidateFrame = () => {if(currentFrame.current === frame) currentFrame.current = null;};
  const heading = useRef<HTMLHeadingElement | null>(null);
  const visible = (questionsConfig.profiles[questionProfile] as QuestionId[]).filter(id => {
    const condition = questions[id].show_when;
    return !condition || answers[condition.field] === condition.value;
  });
  const current = visible[step];
  const question = current ? questions[current] : null;
  const reviewing = step >= visible.length;
  const answered = (id:QuestionId) => id === "discomfort_types" ? answers.discomfort_types.length > 0 : answers[id] !== "not_asked";
  const complete = visible.every(answered);
  useLayoutEffect(() => {
    resetAppScroll();
    heading.current?.focus({preventScroll:true});
  }, [current]);
  useLayoutEffect(() => {
    binding.live = true;owner.current = binding;setBusy(false);setError("");setFinished(false);
    return () => {
      binding.live = false;binding.pending?.abort();binding.pending = null;binding.submission = null;
      if(owner.current === binding) owner.current = null;
    };
  }, [binding]);
  // Consent/CTA changes retire IO but retain answers for a new explicit confirmation.
  // A different store, record kind, completion mode or question profile starts unasked.
  useLayoutEffect(() => {setAnswers(initialAnswers());setStep(0);}, [inputScope]);
  useLayoutEffect(() => {
    currentFrame.current = frame;
    return () => {if(currentFrame.current === frame) currentFrame.current = null;};
  }, [frame]);
  const cancel = () => {
    if(!frameLive()) return;
    invalidateFrame();binding.live = false;binding.pending?.abort();binding.pending = null;binding.submission = null;
    if(owner.current === binding) owner.current = null;
    setBusy(false);setFinished(true);onCancel();
  };
  const transition = (change:()=>void) => {
    if(!frameLive() || busy || binding.pending) return;
    invalidateFrame();binding.submission = null;setError("");change();
  };
  const previous = () => {if(step > 0) transition(() => setStep(value => Math.max(0,value - 1)));};
  const next = () => {if(current && answered(current)) transition(() => setStep(value => value + 1));};

  const choose = (value:string) => {
    if (!current || current === "discomfort_types" || !questions[current].options.some(option => option.value === value)) return;
    transition(() => {setAnswers(previous => ({...previous,[current]:value,
      ...(current === "concern_presence" && value !== "reported" ? {persistence:"not_asked",recent_change:"not_asked"} : {}),
      ...(current === "discomfort_presence" && value !== "reported" ? {discomfort_types:[]} : {}),
    } as Answers));setStep(value => value + 1);});
  };
  const toggleDetail = (value:string) => {
    if(current !== "discomfort_types" || !questions[current].options.some(option => option.value === value)) return;
    const detail = value as MiraySkinState["discomfort_types"][number];
    transition(() => setAnswers(previous => ({...previous,discomfort_types:previous.discomfort_types.includes(detail) ? previous.discomfort_types.filter(item => item !== detail) : [...previous.discomfort_types,detail]})));
  };
  useLayoutEffect(() => {
    const back = (event:Event) => {
      if(!frameLive()) return;
      event.stopImmediatePropagation();
      if(step > 0 && !busy && !binding.pending) previous();else cancel();
    };
    window.addEventListener("skinanalysis:native-back",back,{capture:true});
    return () => window.removeEventListener("skinanalysis:native-back",back,{capture:true});
    // Back uses the committed question frame, including its cancel/previous guards.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [frame]);

  const submit = async () => {
    if (!frameLive() || !reviewing || !complete || busy || binding.pending) return;
    const attempt = new AbortController();
    const value: MiraySkinState = binding.submission ?? {
      version:"1.0.0",kind,observed_at:new Date().toISOString(),...answers,
      persistence:answers.concern_presence === "reported" ? answers.persistence : answers.concern_presence === "none_reported" ? "not_applicable" : "not_asked",
      recent_change:answers.concern_presence === "reported" ? answers.recent_change : answers.concern_presence === "none_reported" ? "not_applicable" : "not_asked",
      discomfort_types:answers.discomfort_presence === "reported" ? [...answers.discomfort_types] : [],
    };
    binding.pending = attempt;binding.submission = structuredClone(value);invalidateFrame();setBusy(true);setError("");
    try {
      validateMiraySkinState(value);
      const result = completionMode === "standalone" && historyStorageConsented && store ? await store.save(structuredClone(value), {signal:attempt.signal,isCurrent:live}) : undefined;
      if(attempt.signal.aborted || !live()) return;
      let receipt: MiraySkinStateSaveResult|undefined;
      if(result !== undefined) {
        if(!result || typeof result !== "object" || Array.isArray(result) || Object.keys(result).length !== 1 || !Object.hasOwn(result,"homeTasks")) throw new Error("Invalid state receipt");
        receipt = {homeTasks:parseSkinStateHomeTasks(result.homeTasks)};
      }
      // Consume completion before notifying a parent that may keep this child mounted.
      binding.live = false;binding.submission = null;owner.current = null;invalidateFrame();setBusy(false);setFinished(true);
      if(receipt) onComplete(structuredClone(value),receipt);else onComplete(structuredClone(value));
    } catch {
      if (!attempt.signal.aborted && live()) setError("현재 상태를 저장하지 못했어요. 다시 시도해 주세요.");
    } finally {
      if (binding.pending === attempt) {binding.pending = null;if(live()) setBusy(false);}
    }
  };

  return <main className="miray-main miray-state-checkin">
    <button type="button" disabled={finished} onClick={cancel}>‹ {kind === "checkin" ? "홈으로" : "내 루틴으로"}</button>
    <p className="miray-eyebrow">{kind === "checkin" && completionMode !== "collect_for_entry" ? "정기 상태 확인" : "현재 상태 확인"}</p>
    <h1>{kind === "checkin" ? "최근 상태를 확인해요" : "지금 느끼는 상태를 알려 주세요"}</h1>
    <p>{kind === "checkin" ? "진단이나 이전 기록과의 비교를 하지 않고, 지금 직접 답한 내용만 선택해요." : "진단이나 원인을 판단하지 않고, 지금 직접 답한 내용을 확인해요."}</p>
    {!reviewing && question && <>
      <div className="miray-state-progress" role="progressbar" aria-label="질문 진행" aria-valuemin={0} aria-valuenow={step + 1} aria-valuemax={visible.length} aria-valuetext={`${visible.length}개 중 ${step + 1}번째 질문`}>
        <span aria-hidden="true">{`${step + 1} / ${visible.length}`}</span>
        <progress aria-hidden="true" value={step + 1} max={visible.length}/>
      </div>
      <section className="miray-card miray-state-question" aria-labelledby="miray-state-question">
        <h2 id="miray-state-question" ref={heading} tabIndex={-1}>{question.title}</h2>
        {question.multiple ? <>
          <p>해당하는 항목을 모두 고른 뒤 다음으로 넘어가세요.</p>
          <fieldset aria-label={question.accessibility_label} disabled={busy || finished}>
            {question.options.map(option => <label key={option.value}>
              <input type="checkbox" checked={answers.discomfort_types.includes(option.value as MiraySkinState["discomfort_types"][number])} onChange={() => toggleDetail(option.value)}/>{option.label}
            </label>)}
          </fieldset>
        </> : <>
          <p>답변을 선택하면 다음 질문으로 넘어가요.</p>
          <select aria-label={question.accessibility_label} disabled={busy || finished} value={answers[current] as string} onChange={event => choose(event.target.value)}>
            <option value="not_asked" disabled>선택해 주세요</option>
            {question.options.filter(option => !(questionProfile === "routine_state_and_safety" && (current === "concern_presence" || current === "discomfort_presence")) || ["reported", "none_reported"].includes(option.value)).map(option => <option key={option.value} value={option.value}>{questionProfile === "routine_state_and_safety" && current === "discomfort_presence" ? (option.value === "reported" ? "있어요" : "없어요") : option.label}</option>)}
          </select>
        </>}
      </section>
    </>}
    {reviewing && <section className="miray-card miray-state-review">
      <h2 ref={heading} tabIndex={-1}>입력 내용을 확인해 주세요</h2>
      <dl>{visible.map(id => <div key={id}><dt>{questions[id].title}</dt><dd>{questions[id].options.filter(option => id === "discomfort_types" ? answers.discomfort_types.includes(option.value as MiraySkinState["discomfort_types"][number]) : answers[id] === option.value).map(option => option.label).join(" · ")}</dd></div>)}</dl>
      <p>수정하려면 이전 질문으로 돌아갈 수 있어요.</p>
    </section>}
    <p role="note">{completionMode === "collect_for_entry"
      ? "답변은 다음 확인 화면에서 루틴 점검과 함께 저장할 수 있어요. 아직 이력에 저장하지 않았어요."
      : completionMode === "collect_for_followup"
      ? "답변은 마지막 확인 화면에서 지난 점검과 연결해 저장할 수 있어요. 아직 이력에 저장하지 않았어요."
      : historyStorageConsented && store
      ? "별도 동의에 따라 계정 이력에 암호화해 저장합니다."
      : historyStorageConsented
        ? "이력 저장 동의는 확인했지만 저장 연결을 준비 중이에요. 이 답변은 지금 계정 이력에 저장하지 않습니다."
        : "별도 이력 저장 동의가 확인되지 않아 이 답변은 계정 이력에 저장하지 않습니다."}</p>
    {error && <p role="alert">{error}</p>}
    <div className="miray-state-actions">
      {step > 0 && <button type="button" disabled={busy || finished} onClick={previous}>이전 질문</button>}
      {reviewing ? <button className="miray-primary" type="button" disabled={!complete || busy || finished} onClick={submit}>{busy ? "저장 중" : kind === "checkin" || !continueToAnalysis ? "확인 마치기" : "루틴 점검 계속"}</button>
        : <button className="miray-primary" type="button" disabled={!current || !answered(current) || busy || finished} onClick={next}>다음</button>}
    </div>
  </main>;
}
