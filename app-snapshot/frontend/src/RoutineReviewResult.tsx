import {useState} from "react";
import fixture from "./fixtures/syntheticCareResponse.json";
import "./routineReviewResult.css";

type Row=Record<string,unknown>;
const sections=fixture.result.sections as Array<{type:string;items:Row[];outcome?:{headline?:string;reason?:string;guidance?:string[]}}>;
const section=(type:string)=>sections.find(item=>item.type===type);
const string=(x:unknown)=>typeof x==="string"?x:"";
const statuses:Record<string,string>={selected:"이번 케어",support:"피부 보호",excluded:"사용 제외",not_prioritized:"이번에는 제외"};

export default function RoutineReviewResult(){
 const [period,setPeriod]=useState<"AM"|"PM">("AM");
 const routine=(section("routine")?.items??[]).filter(item=>item.slot===period).sort((a,b)=>Number(a.order)-Number(b.order));
 return <main className="rr-result">
  <header className="rr-head"><span className="rr-kicker">ROUTINE CHECK</span><h1>나의 루틴 점검 결과</h1><p>현재 입력을 바탕으로 확인했어요.</p></header>
  <section className="rr-notice" aria-labelledby="rr-safety"><div><span className="rr-badge">먼저 확인해요</span><h2 id="rr-safety">안전 안내</h2></div>
   <p className="rr-strength">도입 강도 <strong>{fixture.result.safety.tolerance_level}</strong></p>
   <ul>{[...fixture.result.safety.warnings,...fixture.result.safety.excluded_combinations].map(text=><li key={text}>{text}</li>)}</ul>
  </section>
  <section className="rr-section" aria-labelledby="rr-routine"><div className="rr-heading"><div><span className="rr-overline">01</span><h2 id="rr-routine">이렇게 사용해요</h2></div><span>사용 순서</span></div>
   <div className="rr-tabs" role="group" aria-label="사용 시간"><button className={period==="AM"?"selected":""} aria-pressed={period==="AM"} onClick={()=>setPeriod("AM")}>아침</button><button className={period==="PM"?"selected":""} aria-pressed={period==="PM"} onClick={()=>setPeriod("PM")}>저녁</button></div>
   <ol className="rr-routine">{routine.map(item=><li key={`${item.slot}-${item.order}`}><span className="rr-index">{String(item.order).padStart(2,"0")}</span><div><strong>{string(item.ingredient)}</strong><p>{string(item.frequency)}{item.dose!=="미포함" && item.dose ? ` · ${string(item.dose)}` : ""}{item.gradual_introduction===true?" · 단계적으로 도입":""}</p></div></li>)}</ol>
  </section>
  <section className="rr-section" aria-labelledby="rr-habits"><div className="rr-heading"><div><span className="rr-overline">02</span><h2 id="rr-habits">먼저 살펴볼 습관</h2></div></div>
   <div className="rr-habits">{(section("aggravating_factors")?.items??[]).map(item=><div key={string(item.factor)}><strong>{string(item.factor)}</strong><p>{string(item.guidance)}</p></div>)}</div>
  </section>
  <section className="rr-section" aria-labelledby="rr-palette"><div className="rr-heading"><div><span className="rr-overline">03</span><h2 id="rr-palette">6가지 성분 방향</h2></div></div><p className="rr-caption">각 성분을 누르면 이번 점검의 판단을 볼 수 있어요.</p>
   <div className="rr-list">{(section("ingredient_plan")?.items??[]).map(item=><details key={string(item.ingredient)}><summary><span>{string(item.ingredient)}</span><span className={`rr-status ${string(item.status)}`}>{statuses[string(item.status)]??string(item.status)}</span></summary><p>{string(item.reason)} · {string(item.dose)}</p></details>)}</div>
  </section>
  <section className="rr-section" aria-labelledby="rr-products"><div className="rr-heading"><div><span className="rr-overline">04</span><h2 id="rr-products">제품 살펴보기</h2></div></div>
   {(section("current_products")?.items??[]).map(item=><article className="rr-product" key={string(item.product_id)}><span>내 화장품 · 유지 가능</span><h3>{string(item.brand)} {string(item.name)}</h3>{Array.isArray(item.covered_ingredients)&&item.covered_ingredients.length>0&&<p>충족 방향: {item.covered_ingredients.map(string).join(", ")}</p>}{Array.isArray(item.notes)&&item.notes.map(note=><p key={string(note)}>{string(note)}</p>)}</article>)}
   {section("product_matches")?.outcome&&<article className="rr-empty"><strong>{section("product_matches")?.outcome?.headline}</strong><p>{section("product_matches")?.outcome?.reason}</p><details><summary>안내 자세히 보기</summary>{section("product_matches")?.outcome?.guidance?.map(g=><p key={g}>{g}</p>)}</details></article>}
  </section>
  <section className="rr-section rr-last"><details><summary>아직 확인이 필요한 내용</summary>{(section("unmet_gaps")?.items??[]).map(item=><p key={string(item.ingredient)}><strong>{string(item.ingredient)}</strong> · {string(item.message)}</p>)}{(section("disclaimers")?.items??[]).map((item,i)=><p key={i}>{typeof item==="string"?item:JSON.stringify(item)}</p>)}</details></section>
 </main>;
}
