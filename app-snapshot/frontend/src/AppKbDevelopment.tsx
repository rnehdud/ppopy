import {useEffect,useMemo,useRef,useState} from 'react';
import AppLaunchShell from './AppLaunchShell';
import AppVisualFrame from './AppVisualFrame';
import {emptyMirayPortfolio,parseMirayPortfolioEnvelope,type MirayPortfolio} from './mirayPortfolio';
import type {ProductCandidate} from './productCatalog';
import './kbRoutineReview.css';
type Obj=Record<string,any>;
export default function AppKbDevelopment(){
 const [csrf,setCsrf]=useState(''),[session,setSession]=useState<Obj|null>(null),[error,setError]=useState(''),[generation,setGeneration]=useState(0),[busy,setBusy]=useState(false);
 const [localModel,setLocalModel]=useState(false);
 const epoch=useRef(0);
 useEffect(()=>{void fetch('/api/kb-app/bootstrap').then(r=>r.json()).then(x=>{setCsrf(x.csrf);setLocalModel(x.actual_llm_enabled===true)}).catch(e=>setError(String(e)))},[]);
 const ports=useMemo(()=>{
  if(!session)return null;const issued=epoch.current;
  const request=async(route:string,data:Obj)=>{if(issued!==epoch.current)throw Error('개발 계정이 바뀌었어요.');const r=await fetch('/api/kb-app/'+route,{method:'POST',headers:{'Content-Type':'application/json','X-KB-Token':csrf,'X-Dev-Session':session.token},body:JSON.stringify(data)});const value=await r.json();if(issued!==epoch.current)throw Error('이전 계정 응답을 닫았어요.');if(!r.ok)throw Error(value.error||'개발 연결 실패');return value};
  const loadCatalog=async()=>{const r=await fetch('/api/kb-app/catalog',{headers:{'X-Dev-Session':session.token}});if(issued!==epoch.current||!r.ok)throw Error('제품 자료 연결 실패');return r.json()};
  return {request,loadCatalog,portfolioStore:{read:async()=>parseMirayPortfolioEnvelope(await request('portfolio/read',{})),save:async(portfolio:MirayPortfolio,expectedRevision:number)=>parseMirayPortfolioEnvelope(await request('portfolio/save',{portfolio,expectedRevision}))},memberCareClient:{searchProducts:async(query:string):Promise<ProductCandidate[]>=>{const c=await loadCatalog();return c.products.filter((p:Obj)=>(p.name+' '+p.id).toLowerCase().includes(query.toLowerCase())).map((p:Obj)=>({id:p.id,brand:'',name:p.name,option:p.volume||'',evidenceStatus:p.kind==='synthetic'?'fixture_only':'review_required',matchSource:'catalog'}))}}};
 },[session,csrf]);
 async function login(account:string){if(busy)return;setBusy(true);setError('');try{if(ports)await ports.request('logout',{});epoch.current++;setSession(null);const r=await fetch('/api/kb-app/login',{method:'POST',headers:{'Content-Type':'application/json','X-KB-Token':csrf},body:JSON.stringify({account})});const x=await r.json();if(!r.ok)throw Error(x.error);setSession(x)}catch(e){setError(String(e))}finally{setBusy(false)}}
 async function example(){if(!ports||busy)return;setBusy(true);try{const old=await ports.portfolioStore.read();if(old.portfolio.products.length)throw Error('이미 제품이 있어요. 기존 화장품 화면에서 수정하세요.');const c=await ports.loadCatalog();const ids=['CLN-0001','official-lead-celimax-52','official-lead-celimax-65'];const p=emptyMirayPortfolio();p.products=ids.map(id=>{const x=c.products.find((p:Obj)=>p.id===id);if(!x)throw Error('실제 제품 스냅샷 없음');return {id,name:x.name,brand:'',option:x.volume||'',evidence_status:'review_required',match_source:'catalog',frequency:'7',depletion_status:'not_tracking',source_url:null,provenance_hash:null}});p.periods={am:ids,pm:ids.slice(0,2)};await ports.portfolioStore.save(p,old.revision);setGeneration(n=>n+1)}catch(e){setError(String(e))}finally{setBusy(false)}}
 if(!import.meta.env.DEV||import.meta.env.VITE_KB_APP_PREVIEW!=='true'||!['127.0.0.1','localhost'].includes(location.hostname))return <p>개발 환경에서만 열 수 있어요.</p>;
 return <AppVisualFrame><aside className="kb-panel"><strong>Poppy 기존 앱 · KB 개발 연결 / 연구 OFF</strong><p>합성 개발 계정 {session?.account||'미선택'} · 로컬 저장 · 실제 OAuth 없음 · {localModel?'로컬 Qwen 실제 추론 사용':'코드 기반 실행'} · 외부 모델 전송 없음</p><p>공개 제품과 합성 상태로 검토하세요. 실제 개인정보를 입력하지 마세요.</p><button disabled={!csrf||busy} onClick={()=>void login('developer-a')}>개발 계정 A</button><button disabled={!csrf||busy} onClick={()=>void login('developer-b')}>개발 계정 B</button>{ports&&<button disabled={busy} onClick={()=>void example()}>빈 계정에 실제 제품 3종 검토 목록 불러오기</button>}{error&&<p role="alert">{error}</p>}</aside>
 {ports&&<AppLaunchShell key={session!.token+':'+generation} allowOwnerTestSession newNavigationEnabled sensitiveConsentVerified historyStorageConsented skinStateEnabled={false} subscriptionEnabled={false} portfolioStore={ports.portfolioStore} memberCareClient={ports.memberCareClient} kbAppPort={{request:ports.request,loadCatalog:ports.loadCatalog}}/>}</AppVisualFrame>
}
