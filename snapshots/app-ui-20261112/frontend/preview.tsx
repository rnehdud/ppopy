import {createRoot} from 'react-dom/client';
import MirayWorkspace from './src/MirayWorkspace';
import AppVisualFrame from './src/AppVisualFrame';
import MemberKbPanel from './src/MemberKbPanel';
import copy from './src/memberKbConsumerCopy.json';
import './src/mirayWorkspace.css';
import './src/nativeShell.css';
const products=[['demo-1','웰라쥬 리얼 히알루로닉 블루 100 앰플 100ml'],['demo-2','닥터엘시아 345 릴리프 크림 50ml'],['demo-3','예시 선크림']].map(([id,name])=>({id,name,brand:'화면 예시',option:'',evidence_status:'review_required' as const,match_source:'manual' as const,frequency:'unknown',depletion_status:'not_tracking' as const,source_url:null,provenance_hash:null}));
let portfolio={version:'1.2.0' as const,products,periods:{am:['demo-1','demo-2'],pm:['demo-2','demo-1']}};
let revision=1;
const store={read:async()=>({revision,portfolio}),save:async(p:typeof portfolio,expected:number)=>{if(expected!==revision)throw Error('합성 버전 충돌');portfolio=structuredClone(p);return {revision:++revision,portfolio};}};
const mode=new URLSearchParams(location.search).get('screen');
const op='sha256:'+'c'.repeat(64);
const question={path:'observations.r0~evening.method.water_temperature',text:'세안할 때 물이 뜨겁게 느껴지나요?',options:['warm','hot','skipped'],labels:{warm:'아니요, 미지근해요',hot:'네, 뜨겁게 느껴져요',skipped:'건너뛰기'}};
const baseDisplay={schema:'poppy-kb-choice-result-v1',questions:[],action_review:null,guidance:[{bucket:'adjust',text:copy.cards['B-C01'].difference.source}],cards:[{card:'B-C01',title:'원본 내부 기준',version:'0.6',status:'difference',text:copy.cards['B-C01'].difference.source,sources:[],scope:[]}],uses:[]};
let sendReply:undefined|(()=>void);
const client=async(_:unknown,p:Record<string,unknown>)=>{
 if(mode==='conversation'||mode==='result'){
  if(p.command==='active')return {records:[{operation_ref:op,started_at:'2026-11-12T12:00:00Z'}]};
  if(p.command==='session')return {operation_ref:op,status:'ready',step:0,answer_controls:[],action_controls:null,display:{...baseDisplay,questions:mode==='conversation'?[question]:[]}};
  if(p.command==='answer')return new Promise(resolve=>{sendReply=()=>resolve({operation_ref:op,status:'ready',step:1,answer_controls:[],action_controls:null,display:baseDisplay});});
  if(p.command==='finish')return {status:'completed',result:baseDisplay};
 }

 if(p.command==='active')return {records:[]};
 if(p.command!=='draft')throw Error('이 화면은 표시만 재현하며 실제 점검을 시작하지 않아요.');
 return {member_scope:{version:'poppy-kb-signup-scope-v1',account_gate:'over_or_equal_14',source:'authenticated_signup_gate',separate_population_answer:false},portfolio_revision:revision,portfolio_fingerprint:'a'.repeat(64),catalog_sha256:'b'.repeat(64),morning_water_only:false,rows:products.map((product,index)=>({id:'r'+index,product_id:product.id,temporary_name:product.name,stage_label:index===0?'세럼':'보습',schedule:index===2?'not_used':'both',site:'face',frequency:'unknown',order:null,period_orders:index===0?{morning:1,evening:2}:index===1?{morning:2,evening:1}:{}}))};
};
if(import.meta.env.DEV&&['127.0.0.1','localhost'].includes(location.hostname)){

 createRoot(document.getElementById('root')!).render(<AppVisualFrame><aside style={{fontSize:12,padding:8,background:'#f5f7fa',color:'#53677e'}}>합성 표시 검토·실제 컴포넌트 · 서버/유료 API 요청 없음</aside>{(mode==='draft'||mode==='conversation'||mode==='result')?<MemberKbPanel client={client} close={()=>{}} editRoutine={()=>{}}/>:<MirayWorkspace settings={<p>합성 검토 화면</p>} portfolioStore={store}/>}{mode==='conversation'&&<button onClick={()=>sendReply?.()}>합성 서버 응답 보내기</button>}</AppVisualFrame>);
}
