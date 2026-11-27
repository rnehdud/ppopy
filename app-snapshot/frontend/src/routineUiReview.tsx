import {useState} from "react";
import {createRoot} from "react-dom/client";
import AppVisualFrame from "./AppVisualFrame";
import MiraySkinStateCheckin from "./RoutineReviewSkinState";
import MirayIntakePanel from "./RoutineReviewIntake";
import {emptyIntake} from "./mirayClosedLoopIntake";
import RoutineReviewResult from "./RoutineReviewResult";
import "./nativeShell.css";
import "./mirayExplore.css";

const store={read:async()=>({context:{preview:true},stored:false,answers:{...emptyIntake(),product_context_status:{state:"reported" as const,value:"registered"}}}),save:async()=>{throw new Error("검토 화면에서는 저장하지 않아요.");}};
function Review(){
 const [page,setPage]=useState<"menu"|"state"|"routine"|"routine-list"|"routine-add"|"intake"|"result">("menu");
 return <AppVisualFrame><div style={{maxWidth:520,margin:"0 auto",padding:"16px 20px 60px"}}>
 <div style={{padding:"12px",background:"#eef5ff",borderRadius:12,marginBottom:20,fontSize:14}}>화면 검토용 · 예시 데이터 · 저장 및 서버 요청 없음</div>
 {page!=="menu"&&<button onClick={()=>setPage("menu")} style={{padding:"10px",marginBottom:16}}>‹ 화면 목록으로</button>}
 {page==="menu"&&<main><h1>루틴 점검 화면 살펴보기</h1><p>실제 앱의 화면 구성 요소를 사용한 미리보기예요. 아래 항목에서 질문과 결과 화면을 각각 열 수 있어요.</p><div style={{display:"grid",gap:12,marginTop:24}}>
 <button onClick={()=>setPage("state")}>1. 현재 피부 상태 질문</button><button onClick={()=>setPage("routine")}>2. 현재 루틴 확인과 점검 질문</button><button onClick={()=>setPage("result")}>3. 점검 결과 예시</button></div><p style={{marginTop:28}}>저장 확인·처리 중·이용 한도·후속 확인 등 조건부 화면은 이 미리보기에 포함되지 않아요.</p></main>}
 {page==="state"&&<MiraySkinStateCheckin kind="baseline" questionProfile="routine_state_and_safety" historyStorageConsented={false} completionMode="collect_for_entry" continueToAnalysis={false} onCancel={()=>setPage("menu")} onComplete={()=>setPage("menu")}/>}
 {page==="routine"&&<main className="miray-main"><h1>현재 루틴 확인</h1><section className="miray-card miray-intake"><h2>현재 루틴을 확인할까요?</h2><p>점검할 제품 목록을 먼저 확인해 주세요.</p><button className="miray-intake-choice" onClick={()=>setPage("routine-list")}>현재 루틴 확인</button><button className="miray-intake-choice" onClick={()=>setPage("routine-add")}>루틴에 제품 추가</button></section></main>}
 {page==="routine-list"&&<main className="miray-main"><h1>현재 루틴 확인</h1><section className="miray-card"><p>예시 제품 · 보습 크림</p><p>예시 제품 · 세안제</p><p>사용 중인 제품이 모두 포함되어 있나요?</p><button className="miray-primary" onClick={()=>setPage("intake")}>네, 모두 확인했어요</button><button onClick={()=>setPage("routine-add")}>제품 추가하기</button></section></main>}
 {page==="routine-add"&&<main className="miray-main"><h1>루틴에 제품 추가</h1><p>실제 제품 추가 화면으로 이동하는 자리예요. 이 미리보기에는 연결되어 있지 않습니다.</p><button onClick={()=>setPage("routine")}>현재 루틴 확인으로</button></main>}
 {page==="intake"&&<main className="miray-main"><h1>현재 루틴 확인</h1><MirayIntakePanel store={store} label="현재 루틴 확인" savedPurpose="현재 상태의 점검" onClose={()=>setPage("menu")} onSaved={()=>setPage("menu")} onReviewed={()=>setPage("menu")}/></main>}
 {page==="result"&&<RoutineReviewResult/>}
 </div></AppVisualFrame>;
}
createRoot(document.getElementById("root")!).render(<Review/>);
