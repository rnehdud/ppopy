import {useEffect,useLayoutEffect,useRef,useState,type ReactNode} from "react";
import {asDisplay,asDraft,asHistory,asTurn,object,previewMemberDraft,MemberKbConflict,type Display,type Draft,type History,type MemberKbClient,type MemberKbNavigation,type Row,type Turn} from "./memberKbReview";
import {choiceLabels} from "./kbChoiceLabels";
import {productNamePresentation} from "./productPresentation";
import {consumerBodyText,consumerGuidanceText,evidenceHeading,evidenceSourceLabel,scopedProductText} from "./memberKbPresentation";
import RoutinePeriodTabs,{type RoutinePeriod} from "./RoutinePeriodTabs";
import {PoppyReviewGuide} from "./PoppyReviewGuide";
import "./memberKbPanel.css";

const labels:Record<string,string>={...choiceLabels,unknown:"잘 모르겠어요",skipped:"건너뛰기"};
const contextFields=[["discomfort","지금 피부에 불편감이 있나요?",["none","current","unknown","skipped"]],
  ["concern","어떤 점을 살펴볼까요?",["none","dryness","friction","pilling","other","unknown","skipped"]]] as const;
function ConversationQuestion({text,options,answer,busy=false,acknowledged=false,safety=false}:{text:string;options:{value:string;label:string}[];answer:(value:string)=>void;busy?:boolean;acknowledged?:boolean;safety?:boolean}){
  const heading=useRef<HTMLHeadingElement>(null);
  const [selected,setSelected]=useState<string|null>(null);
  useEffect(()=>{heading.current?.focus({preventScroll:true});},[text]);
  // A conflict is an engine state, not a meaningful routine answer to ask a
  // member to invent. Existing conflicts remain untouched in the server record.
  const visible=options.filter(option=>option.value!=="conflicting");
  const optional=new Set(["unknown","skipped","skip"]);
  return <section className="kb-conversation-question" aria-label="현재 질문">
    <PoppyReviewGuide phase={busy?"submitting":acknowledged?"answered":"question"} safety={safety}><h2 ref={heading} tabIndex={-1}>{text}</h2></PoppyReviewGuide>
    {busy&&selected&&<p className="kb-member-answer" aria-label="보내는 답변">{selected}</p>}
    <div className="kb-conversation-options">{visible.filter(option=>!optional.has(option.value)).map(option=><button type="button" key={option.value} disabled={busy} onClick={()=>{setSelected(option.label);answer(option.value);}}>{option.label}</button>)}</div>
    <div className="kb-conversation-optional">{visible.filter(option=>optional.has(option.value)).map(option=><button type="button" key={option.value} disabled={busy} onClick={()=>{setSelected(option.label);answer(option.value);}}>{option.value==="unknown"?"잘 모르겠어요":"건너뛰기"}</button>)}</div>
  </section>;
}
const periods=(r:Row)=>r.schedule==="both"?["morning","evening"]:["morning","evening"].includes(r.schedule)?[r.schedule]:[];
function Choice({label,value,options,change}:{label:string;value:string;options:readonly string[];change:(v:string)=>void}){
  return <label>{label}<select value={value} onChange={e=>change(e.target.value)}>{options.map(v=><option key={v} value={v}>{labels[v]??v}</option>)}</select></label>;
}
// Defer the controls themselves (including order options), not just their CSS.
function DeferredDetails({label,children}:{label:string;children:()=>ReactNode}){
  const [expanded,setExpanded]=useState(false);
  return <details onToggle={event=>setExpanded(event.currentTarget.open)}>
    <summary>{label}</summary>{expanded&&children()}</details>;
}
function evidenceLink(value:unknown){
  if(typeof value!=="string")return null;
  try{const url=new URL(value);return url.protocol==="https:"&&!url.username&&!url.password?url.href:null;}
  catch{return null;}
}
function Guidance({display}:{display:Display}){
  const [showEvidence,setShowEvidence]=useState(false);
  const names=(display.uses??[]).flatMap(u=>u.temporary_name?[u.temporary_name]:[]);
  const text=(value:string)=>scopedProductText(value,names);
  const card=display.action_review;
  const groups=(["maintain","adjust","check"] as const).map(key=>{
    const statuses={maintain:["aligned","difference"],adjust:["difference"],check:["exception","conflicting"]}[key];
    const evidence=new Set(display.cards.filter(c=>statuses.includes(c.status)).map(c=>c.text));
    const texts=[...new Set(display.guidance.filter(g=>g.bucket===key&&evidence.has(g.text)).map(g=>{
      const row=display.cards.find(c=>statuses.includes(c.status)&&c.text===g.text);
      return row?consumerGuidanceText(row.card,row.status,g.text):g.text;
    }))];
    return {key,texts};
  });
  const hasGuidance=groups.some(g=>g.texts.length>0);
  return <>{(card||hasGuidance||!display.questions.length)&&<h2>{card?text(card.title):"현재 루틴 안내"}</h2>}{card&&<><p>{text(consumerBodyText(card.body))}</p>{card.message&&<p role="status">{text(card.message)}</p>}</>}
    {!card&&groups.map(({key,texts})=>texts.length>0&&<section key={key}><h3>{{maintain:"유지할 점",adjust:"조정할 점",check:"추가 확인"}[key]}</h3>
      <ul>{texts.map(t=><li key={t}>{text(t)}</li>)}</ul></section>)}
    {!card&&!groups.some(g=>g.texts.length)&&!display.questions.length&&<p>확인한 내용만으로는 지금 루틴에서 바꿀 점을 정하기 어려워요.</p>}
    <details onToggle={e=>setShowEvidence(e.currentTarget.open)}><summary>안내에 참고한 내용</summary>{showEvidence&&display.cards.filter(r=>r.status!=="not_applicable").map((r,i)=><section key={i}>
      <p><strong>{evidenceHeading(r.card)}</strong> · {({aligned:"지금 방식으로 이어가도 좋아요",difference:"사용 방식을 조정할 수 있어요",unknown:"아직 확인하지 않은 부분이에요",conflicting:"답변이 서로 달라 확인이 필요해요",exception:"개별 상황을 먼저 확인해요"} as Record<string,string>)[r.status]??"현재 정보로는 판단하기 어려워요"}</p>
      {r.scope?.map(id=>{const use=display.uses?.find(u=>u.id===id);return use&&<p key={id}>
        {productNamePresentation(use.temporary_name??"등록한 제품").name} · {({morning:"아침",evening:"저녁"} as Record<string,string>)[use.session??""]??"사용 시간 미확인"} · {({face:"얼굴",neck:"목",body:"몸",hands:"손"} as Record<string,string>)[use.site??""]??"사용 부위 미확인"}
      </p>;})}
      {r.source_details?.map((source,index)=>{const href=evidenceLink(source.url);return <p key={index}>
        {href?<a href={href} target="_blank" rel="noopener noreferrer">{evidenceSourceLabel(source.id,source.title)}</a>:evidenceSourceLabel(source.id,source.title)}
      </p>;})}
    </section>)}</details></>;
}

function orderIn(r:Row,p:string){
  return r.period_orders&&Object.keys(r.period_orders).length?r.period_orders[p]:r.order;
}
function rowSummary(r:Row){
  const use=periods(r).map(p=>labels[p]+" "+(orderIn(r,p)?orderIn(r,p)+"번째":"순서 미확인"));
  return [...(use.length?use:[labels[r.schedule]]),labels[r.site],labels[r.frequency]].join(" · ");
}

export default function MemberKbPanel({client,close,editRoutine,loadingOrder,loadingProductNames=[],navigation,openedAt}:{navigation?:MemberKbNavigation;openedAt?:number;client:MemberKbClient;close:()=>void;editRoutine:()=>void;loadingOrder?:{am:readonly string[];pm:readonly string[]};loadingProductNames?:readonly string[]}){
  const [summaryPeriod,setSummaryPeriod]=useState<RoutinePeriod>("am");
  const [draft,setDraft]=useState<Draft|null>(()=>navigation?.draft?structuredClone(navigation.draft):null);
  const cachedDraft=useRef(draft);
  const [edits,setEdits]=useState<Record<string,unknown>>({});
  const [context,setContext]=useState<Record<string,string>>({discomfort:"unknown",concern:"unknown",goal:"review"});
  // Optional context stays on this mounted/account-owned screen. It is never
  // inferred from registration, remembered as a default fact or sent alone.
  const [contextQuestion,setContextQuestion]=useState<0|1|null>(null);
  const [contextAnswered,setContextAnswered]=useState(false);
  const [editingAnswer,setEditingAnswer]=useState<string|null>(null);
  const [editingSafety,setEditingSafety]=useState(false);
  const [answerAcknowledged,setAnswerAcknowledged]=useState(false);
  const [population,setPopulation]=useState("");
  const [turn,setTurn]=useState<Turn|null>(null),[saved,setSaved]=useState<Display|null>(null);
  const [active,setActive]=useState<History|null>(()=>cachedDraft.current&&navigation?.active?structuredClone(navigation.active):null),[history,setHistory]=useState<History|null>(null);
  const [busy,setBusy]=useState(false),[error,setError]=useState(""),[notice,setNotice]=useState("");
  const [recover,setRecover]=useState<Record<string,unknown>|null>(null);
  const originalDraft=useRef<Draft|null>(cachedDraft.current);
  const originalStart=useRef<{fingerprint:string;id:string}|null>(null);
  const [unfinished,setUnfinished]=useState<string|null>(null);
  const [saving,setSaving]=useState<{op:string;step:number}|null>(null);
  const [stale,setStale]=useState<string|null>(null);
  const [pending,setPending]=useState<{op:string;step:number}|null>(null);
  const controller=useRef<AbortController|null>(null),inFlight=useRef(false);
  const [recent,setRecent]=useState(()=>navigation?.operation??null);
  const measured=useRef(new Set<string>());
  const summaryVisible=(!draft||!!recent)&&!turn&&!saved&&!error&&(loadingOrder!==undefined||loadingProductNames.length>0);
  useLayoutEffect(()=>{
    if(openedAt===undefined || !performance.measure || !performance.clearMeasures)return;
    function record(name:string){
      if(measured.current.has(name))return;
      measured.current.add(name);
      const key="ppopy.kb."+name;
      performance.clearMeasures(key);
      performance.measure(key,{start:openedAt});
    }
    if(summaryVisible || draft)record("routine-visible");
    if(!busy && !recover && (recent || active?.records.length))record("resume-available");
  },[openedAt,summaryVisible,draft,busy,recover,recent,active]);
  function forgetNavigation(){
    if(navigation)navigation.operation=null;
    setRecent(null);
  }
  async function run(task:(signal:AbortSignal)=>Promise<void>){
    const c=controller.current;
    if(!c||c.signal.aborted||inFlight.current)return;
    inFlight.current=true;setBusy(true);setError("");setNotice("");setAnswerAcknowledged(false);
    try{await task(c.signal);}catch(e){if(!c.signal.aborted)setError(e instanceof Error?e.message:"점검 상태를 확인해 주세요.");}
    finally{if(controller.current===c&&!c.signal.aborted){inFlight.current=false;setBusy(false);}}
  }
  function load(){return run(async signal=>{
    forgetNavigation();
    let d:Draft,a:History;
    if(client.overview){
      const response=await client.overview(signal);
      if(!object(response))throw new Error("루틴 응답을 확인하지 못했어요.");
      d=asDraft(response.draft);a=asHistory(response.active);
    }else{
      d=asDraft(await client("read",{command:"draft"},signal));
      a=asHistory(await client("read",{command:"active"},signal));
    }
    signal.throwIfAborted();
    if(navigation && a.records.length===1 && !a.next_cursor)navigation.operation=a.records[0].operation_ref;
    originalDraft.current=d;setDraft(d);setEdits({});setActive(a);setPopulation("");
    if(navigation){navigation.draft=structuredClone(d);navigation.active=structuredClone(a);}
  });}
  useEffect(()=>{
    const c=new AbortController();controller.current=c;inFlight.current=false;
    if(!navigation?.operation&&!cachedDraft.current)void load();
    return ()=>{c.abort();controller.current=null;};
  },[client]);
  const initial=draft&&{portfolio_revision:draft.portfolio_revision,portfolio_hash:draft.portfolio_fingerprint,catalog_hash:draft.catalog_sha256};
  function edit(path:string,value:unknown){
    if(!initial)return;
    const changes={...edits,[path]:value};
    if(path.endsWith(".schedule")){
      const id=path.split(".")[1];
      for(const slot of ["morning","evening"])if(value!=="both"&&value!==slot)delete changes["period_orders."+id+"."+slot];
    }
    if(path==="morning_water_only"&&value===true)for(const r of draft!.rows.filter(r=>r.stage_label==="세정")){
      const schedule=changes["rows."+r.id+".schedule"];
      if(schedule==="morning"||schedule==="both")changes["rows."+r.id+".schedule"]=schedule==="morning"?"not_used":"evening";
      delete changes["period_orders."+r.id+".morning"];
    }
    if(!originalDraft.current)return;
    try{
      const next=previewMemberDraft(originalDraft.current,changes);
      setDraft(next);setEdits(changes);setError("");
    }catch(e){setError(e instanceof Error?e.message:"사용 방식을 확인해 주세요.");}

  }
  function accept(x:unknown){
    if(!object(x))throw new Error("점검 응답을 확인하지 못했어요.");
    setEditingAnswer(null);setEditingSafety(false);
    if(x.status==="save_pending"&&typeof x.operation_ref==="string"&&typeof x.step==="number"){
      setSaving({op:x.operation_ref,step:x.step});setPending(null);setTurn(null);setUnfinished(null);setRecover(null);
      setNotice("저장 요청이 접수됐어요. 저장 결과를 확인해 주세요.");return;
    }
    setSaving(null);
    if(x.status==="selection_pending"&&typeof x.operation_ref==="string"&&typeof x.pending_step==="number"){
      setPending({op:x.operation_ref,step:x.pending_step});setTurn(null);setUnfinished(null);setRecover(null);
      setNotice("답변이 접수됐어요. 결과를 다시 확인할 수 있어요.");return;
    }
    setPending(null);
    if(x.status==="cancelled"){
      setStale(null);setTurn(null);setSaved(null);setRecover(null);setUnfinished(null);setActive(null);setDraft(null);originalStart.current=null;
      setNotice("미완료 점검을 종료했어요. 점검 횟수는 차감되지 않았어요.");return;
    }
    if(x.status==="scope_confirmation_required"&&typeof x.operation_ref==="string"){
      setStale(x.operation_ref);setTurn(null);setSaved(null);setDraft(null);setUnfinished(null);setActive(null);setRecover(null);
      originalStart.current=null;setPopulation("");
      setNotice("이전 점검에는 대상 범위 확인이 없어요. 이전 점검을 종료한 뒤 대상 범위를 확인하고 다시 시작해 주세요.");return;
    }
    if((x.status==="portfolio_changed"||x.status==="requires_new_draft")&&typeof x.operation_ref==="string"){
      if(navigation){delete navigation.draft;delete navigation.active;}
      setStale(x.status==="portfolio_changed"?x.operation_ref:null);
      setTurn(null);setSaved(null);setDraft(null);setUnfinished(null);setActive(null);setRecover(null);
      originalStart.current=null;setNotice(x.status==="portfolio_changed"?"등록 제품이 바뀌었어요. 이전 점검을 종료한 뒤 현재 루틴으로 다시 시작할 수 있어요.":"등록 제품이 바뀌었어요. 현재 루틴을 다시 불러와 주세요.");return;
    }
    if(x.status==="quota_unavailable"){setRecover(null);setNotice("사용 가능한 점검 횟수가 없거나 이미 진행 중인 점검이 있어요.");return;}
    if(x.status==="not_started"||x.status==="start_unconfirmed"){
      setNotice(x.status==="not_started"?"접수된 점검을 찾지 못했어요.":"서버에서 접수와 첫 결과를 아직 확인하지 못했어요.");
      if(x.status==="start_unconfirmed"&&typeof x.operation_ref==="string")setUnfinished(x.operation_ref);
      setRecover(null);
      return;
    }
    setUnfinished(null);
    if(x.status==="completed"&&x.result){setSaved(asDisplay(x.result));setTurn(null);}
    else{const t=asTurn(x);if(t.status==="completed"){setSaved(t.display);setTurn(null);}else{if(navigation)navigation.operation=t.operation_ref;setTurn(t);setSaved(null);}}
    setRecover(null);
  }
  function mutate(payload:Record<string,unknown>,lookup:Record<string,unknown>){
    return run(async signal=>{
      const started=performance.now();
      const phase=["start","answer","safety_answer","finish"].includes(String(payload.command))?String(payload.command):"other";
      forgetNavigation();
      if(navigation){delete navigation.draft;delete navigation.active;}
      setRecover(lookup);
      let reply:unknown;
      try{reply=await client("intake",payload,signal);}
      catch(e){
        if(payload.command==="start"&&e instanceof MemberKbConflict){
          cachedDraft.current=null;originalDraft.current=null;setDraft(null);setActive(null);setEdits({});
        }
        throw e;
      }
      signal.throwIfAborted();
      performance.measure("ppopy.kb."+phase+".response",{start:started,end:performance.now()});
      accept(reply);
      if((payload.command==="answer"||payload.command==="safety_answer")&&object(reply)
          &&reply.status==="ready"&&typeof reply.step==="number"&&typeof payload.step==="number"
          &&reply.step>payload.step)setAnswerAcknowledged(true);
      if(navigation && originalDraft.current && object(reply) && (reply.status==="ready"||reply.status==="completed")){
        navigation.draft=structuredClone(originalDraft.current);
        // A successful finish ends this operation, but does not prove there are
        // no other active reviews. Refresh that list on explicit request.
      }
    });
  }
  function command(name:string,data:Record<string,unknown>={}){
    if(!turn)return;
    return mutate({command:name,step:turn.step,operation_ref:turn.operation_ref,...data},{command:"session",operation_ref:turn.operation_ref});
  }
  function check(payload:Record<string,unknown>){
    return run(async s=>{
      if(payload.command==="session"){
        forgetNavigation();
        // A fresh server lookup owns the next view; never keep an old draft
        // actionable after login/consent denial or a missing operation.
        if(navigation){delete navigation.draft;delete navigation.active;}
        setActive(null);setDraft(null);originalDraft.current=null;
      }
      const x=await client("read",payload,s);s.throwIfAborted();accept(x);
    });
  }
  function records(before?:Record<string,string>){
    return run(async s=>{
      const x=asHistory(await client("read",{command:"list",...(before?{before}:{})},s));s.throwIfAborted();
      setHistory(old=>before&&old?{...x,records:[...old.records,...x.records]}:x);
    });
  }
  const shown=saved??turn?.display,card=turn?.display.action_review;
  const scopedNames=[...(shown?.uses??[]).flatMap(u=>u.temporary_name?[u.temporary_name]:[]),...(draft?.rows??[]).flatMap(r=>r.temporary_name?[r.temporary_name]:[])];
  // The server owns relevance and re-evaluates after every acknowledged answer.
  // Do not ask a second server candidate or a revision beside the current one.
  const safetyQuestion=!!card?.question||!!editingSafety;
  const currentQuestion=!safetyQuestion?(turn?.answer_controls.find(q=>q.path===editingAnswer)??turn?.display.questions[0]):undefined;
  const waitingForAnswer=safetyQuestion||!!currentQuestion;
  return <main className="miray-main member-kb"><header><h1>루틴 점검</h1><button onClick={close}>닫기</button></header>
    {busy&&!waitingForAnswer&&<p role="status" aria-live="polite">루틴 점검을 처리하고 있어요.</p>}
    {summaryVisible&&<section aria-label="등록한 화장품"><h2>등록한 화장품</h2>{loadingOrder&&(loadingOrder.am.length||loadingOrder.pm.length)?<>{(["am","pm"] as const).map(period=><p key={period}>{period==="am"?"아침":"저녁"}: {loadingOrder[period].join(" → ")||"등록한 순서 없음"}</p>)}</>:loadingProductNames.length>0?<ul>{loadingProductNames.map((name,i)=><li key={i}>{name}</li>)}</ul>:<p>등록한 화장품이 아직 없어요.</p>}</section>}
    {error&&<p role="alert">{error}</p>}{notice&&<p role="status">{notice}</p>}
    {recover&&!busy&&<button disabled={busy} onClick={()=>void check(recover)}>접수 상태 확인</button>}
    {recent&&draft&&!shown&&!summaryVisible&&<section aria-label="등록한 화장품"><h2>등록한 화장품</h2>{draft.rows.map(r=><p key={r.id}>{productNamePresentation(r.temporary_name||"등록한 제품").name}</p>)}</section>}
    {recent&&!busy&&!shown&&<button onClick={()=>void check({command:"session",operation_ref:recent})}>최근 점검 이어서 확인</button>}
    {!draft&&!shown&&!busy&&!stale&&!unfinished&&!pending&&!saving&&!recover&&<button onClick={()=>void load()}>현재 루틴 불러오기</button>}
    <fieldset disabled={busy||!!recover}>
      {draft&&!active&&!recent&&!shown&&!unfinished&&!pending&&!saving&&!recover&&<button onClick={()=>void load()}>진행 중인 점검 확인</button>}
      {!recent&&!shown&&!saving&&!pending&&!unfinished&&active?.records.map(r=><button key={r.operation_ref} onClick={()=>void check({command:"session",operation_ref:r.operation_ref})}>진행 중인 점검 이어서 보기</button>)}
      {saving&&<button onClick={()=>void mutate({command:"finish",operation_ref:saving.op,step:saving.step},{command:"session",operation_ref:saving.op})}>접수된 점검 저장 마치기</button>}
      {stale&&<button onClick={()=>void mutate({command:"cancel",operation_ref:stale},{command:"session",operation_ref:stale})}>이전 점검 종료</button>}
      {pending&&<section><button onClick={()=>void check({command:"session",operation_ref:pending.op})}>점검 결과 확인</button>
        <button onClick={()=>void mutate({command:"recover_selection",operation_ref:pending.op,step:pending.step},{command:"session",operation_ref:pending.op})}>기본 점검 기준으로 계속하기</button></section>}
      {unfinished&&<button onClick={()=>void mutate({command:"recover_start",operation_ref:unfinished},{command:"session",operation_ref:unfinished})}>접수된 점검 계속하기</button>}
      {!recent&&!shown&&!unfinished&&!pending&&!saving&&draft&&<>
        {contextQuestion===null?<>
        <h2>현재 루틴 확인</h2><PoppyReviewGuide phase="intro"/>
        <p className="kb-routine-scope">{draft.rows.every(r=>r.site==="face")?"얼굴 루틴":"부위별 현재 루틴"}</p>
        <RoutinePeriodTabs period={summaryPeriod} change={setSummaryPeriod}>
          {summaryPeriod==="am"&&(draft.morning_water_only||draft.rows.some(r=>r.stage_label==="세정"))&&<label className="kb-water"><input type="checkbox" checked={draft.morning_water_only} onChange={e=>void edit("morning_water_only",e.target.checked)}/>아침에는 물로만 세안해요</label>}
          <ol className="routine-snapshot-list" aria-label={`${summaryPeriod==="am"?"아침":"저녁"} 현재 루틴`}>{draft.rows.filter(r=>periods(r).includes(summaryPeriod==="am"?"morning":"evening")).sort((a,b)=>(orderIn(a,summaryPeriod==="am"?"morning":"evening")??Number.MAX_SAFE_INTEGER)-(orderIn(b,summaryPeriod==="am"?"morning":"evening")??Number.MAX_SAFE_INTEGER)).map(r=><li key={r.id}><span className="routine-snapshot-number" aria-hidden="true">{orderIn(r,summaryPeriod==="am"?"morning":"evening")??"–"}</span><div><h3>{productNamePresentation(r.temporary_name||"등록한 제품").name}</h3>{r.frequency==="occasional"&&<small>가끔 사용</small>}{!draft.rows.every(row=>row.site==="face")&&<small>{labels[r.site]??"부위 미확인"}</small>}</div></li>)}</ol>
          {!draft.rows.some(r=>periods(r).includes(summaryPeriod==="am"?"morning":"evening"))&&<p>이 루틴에 담긴 제품이 없어요.</p>}
        </RoutinePeriodTabs>
        {draft.rows.some(r=>r.schedule==="unassigned")&&<p>사용 회차가 정해지지 않은 제품이 있어요. 루틴 수정에서 확인할 수 있어요.</p>}
        <DeferredDetails label="루틴 수정">{()=><>{draft.rows.map(r=><section className="miray-card" key={r.id}><h3>{productNamePresentation(r.temporary_name||"등록한 제품").name}</h3><p className="kb-row-summary">{rowSummary(r)}</p>
          <DeferredDetails label="사용 방식 수정">{()=><>
          <Choice label={"사용 회차"} value={r.schedule} options={["morning","evening","both","unassigned","not_used"]} change={v=>void edit("rows."+r.id+".schedule",v)}/>
          <Choice label="사용 빈도" value={r.frequency} options={["regular","occasional","unknown"]} change={v=>void edit("rows."+r.id+".frequency",v)}/>
          <Choice label="부위" value={r.site} options={["face","neck","body","hands","unknown"]} change={v=>void edit("rows."+r.id+".site",v)}/>
          {periods(r).map(p=><label key={p}>{labels[p]} 순서<select value={orderIn(r,p)??""} onChange={e=>void edit("period_orders."+r.id+"."+p,Number(e.target.value))}>
            <option value="" disabled>미확인</option>{Array.from({length:Math.max(draft.rows.length, r.period_orders?.[p]??r.order??1)},(_,i)=><option key={i} value={i+1}>{i+1}</option>)}</select></label>)}</>}</DeferredDetails></section>)}</>}</DeferredDetails>
        <div className="kb-context-summary">{contextAnswered&&<p>불편감: {labels[context.discomfort]} · 살펴볼 점: {labels[context.concern]}</p>}
          <button type="button" className="kb-text-action" onClick={()=>setContextQuestion(0)}>{contextAnswered?"피부 상태 답변 수정":"피부 상태도 알려주기"}</button>
        </div>
        {!draft.member_scope&&(draft.population_scope?<label>{draft.population_scope.question}<select value={population} onChange={e=>setPopulation(e.target.value)}>
          <option value="">선택해 주세요</option>{Object.entries(draft.population_scope.choices).map(([v,label])=><option key={v} value={v}>{label}</option>)}
        </select></label>:<p role="status">점검 대상 확인 기능을 준비 중이에요. 새 점검은 아직 시작할 수 없어요.</p>)}
        {!draft.member_scope&&population&&population!=="adult"&&draft.population_scope&&<p role="status">{draft.population_scope.unavailable_message}</p>}
        {draft.rows.length===0?<p>먼저 화장품 탭에서 사용하는 제품을 등록해 주세요.</p>:<button className="miray-primary" disabled={!draft.member_scope&&(!draft.population_scope||population!=="adult")} onClick={()=>{
          if(!draft.member_scope&&(!draft.population_scope||population!=="adult"))return;
          const scopedContext=draft.member_scope?context:{...context,population};
          const fingerprint=JSON.stringify([initial,scopedContext,edits]);
          if(originalStart.current?.fingerprint!==fingerprint)originalStart.current={fingerprint,id:crypto.randomUUID()};
          const request_id=originalStart.current.id;void mutate({command:"start",confirmed:true,...initial,request_id,context:scopedContext,edits},{command:"lookup_start",request_id});
        }}>현재 루틴 확인하고 점검</button>}
        </>:<>
          <ConversationQuestion text={contextFields[contextQuestion][1]} options={contextFields[contextQuestion][2].map(value=>({value,label:labels[value]??value}))} busy={busy} answer={value=>{
            setContext(previous=>({...previous,[contextFields[contextQuestion][0]]:value}));
            setContextAnswered(true);
            if(contextQuestion===0)setContextQuestion(1);else{setContextQuestion(null);setContextAnswered(true);}
          }}/>
          <button type="button" className="kb-text-action" onClick={()=>setContextQuestion(null)}>루틴으로 돌아가기</button>
        </>}
      </>}
      {shown&&!waitingForAnswer&&<>
        {!busy&&!error&&<PoppyReviewGuide phase={saved?"saved":answerAcknowledged?"answered":"result"} safety={shown.action_review?.kind==="eye"}/>}
        <Guidance display={shown}/>
      </>}
      {turn&&<>
        {safetyQuestion&&card&&<>
          <div className="kb-conversation-safety"><p>{scopedProductText(card.body,scopedNames)}</p>{card.message&&<p>{scopedProductText(card.message,scopedNames)}</p>}</div>
          <ConversationQuestion text={card.question??"안전·사용 지침 답변 수정"} options={["yes","no","skip"].map((value,i)=>({value,label:(card.kind==="eye"?["하나라도 있어요","모두 없어요","건너뛰기"]:["있어요","없어요","건너뛰기"])[i]}))} busy={busy} safety acknowledged={answerAcknowledged&&!busy&&!error} answer={value=>void command("safety_answer",{value})}/>
        </>}
        {currentQuestion&&<ConversationQuestion key={currentQuestion.path} text={scopedProductText(currentQuestion.text,scopedNames)} options={currentQuestion.options.map(value=>({value,label:currentQuestion.labels?.[value]??labels[value]??value}))} busy={busy} acknowledged={answerAcknowledged&&!busy&&!error} answer={value=>void command("answer",{path:currentQuestion.path,value})}/>}
        {waitingForAnswer&&!safetyQuestion&&<DeferredDetails label="확인된 안내 보기">{()=> <Guidance display={turn.display}/>}</DeferredDetails>}
        {card?.kind==="pair"&&!waitingForAnswer&&!turn.action_controls?.editing&&<button onClick={()=>void command("change_intent")}>두 세럼의 사용 회차 변경</button>}
        {!waitingForAnswer&&turn.action_controls?.allow_change&&<button onClick={()=>void run(async s=>{
          forgetNavigation();
          const payload={command:"finish",operation_ref:turn.operation_ref,step:turn.step};
          setRecover({command:"session",operation_ref:turn.operation_ref});
          const reply=await client("intake",payload,s);s.throwIfAborted();accept(reply);
          if(object(reply)&&reply.status==="completed")editRoutine();
        })}>점검 저장하고 루틴에서 회차 수정</button>}
        {(turn.answer_controls.length>0||turn.action_controls?.can_revise)&&!editingAnswer&&!editingSafety&&<DeferredDetails label="이전 답변 수정">{()=> <div className="kb-answer-history">{turn.answer_controls.map(q=><button type="button" key={q.path} onClick={()=>setEditingAnswer(q.path)}>{scopedProductText(q.text,scopedNames)}{q.current?" · "+(q.labels?.[q.current]??labels[q.current]??q.current):""}</button>)}
          {turn.action_controls?.can_revise&&<button type="button" onClick={()=>setEditingSafety(true)}>안전·사용 지침 답변 수정</button>}</div>}</DeferredDetails>}
        {(editingAnswer||editingSafety)&&<button type="button" className="kb-text-action" onClick={()=>{setEditingAnswer(null);setEditingSafety(false);}}>답변 수정 닫기</button>}
        {!waitingForAnswer&&<button className="miray-primary" onClick={()=>void command("finish")}>이 점검 저장</button>}
      </>}
      {!turn&&<button onClick={()=>void records()}>저장한 점검 보기</button>}
      {!turn&&history&&<section><h2>저장한 점검</h2>{history.records.length===0&&<p>저장한 점검이 아직 없어요.</p>}
        {history.records.map(r=><button key={r.operation_ref} onClick={()=>void check({command:"read",operation_ref:r.operation_ref})}>{new Date(r.collected_at!).toLocaleString("ko-KR")} 점검</button>)}
        {history.next_cursor&&<button onClick={()=>void records(history.next_cursor!)}>이전 점검 더 보기</button>}
      </section>}
    </fieldset>
  </main>;
}
