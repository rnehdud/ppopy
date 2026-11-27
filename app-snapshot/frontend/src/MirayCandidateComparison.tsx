import {useLayoutEffect,useMemo,useRef,useState} from "react";
import type {MirayExploreCandidate} from "./mirayExploreSearch";
import {candidateComparisonRequest,parseCandidateComparison,type CandidateComparison,type CandidateComparisonReader} from "./candidateComparisonModel";

export default function MirayCandidateComparison({candidates,reader,active=true,primaryAction=false}:{candidates:readonly MirayExploreCandidate[];reader:CandidateComparisonReader;active?:boolean;primaryAction?:boolean}){
  const request=candidateComparisonRequest(candidates);
  const signature=JSON.stringify(request);
  const binding=useMemo(()=>({signature,reader,active,live:false,pending:null as object|null}),[signature,reader,active]);
  const owner=useRef<typeof binding|null>(null);
  const [view,setView]=useState<{binding:typeof binding;value:CandidateComparison|null;busy:boolean;failed:boolean}|null>(null);
  const current=active && view?.binding===binding?view:null;
  const busy=current?.busy??false,failed=current?.failed??false,visible=current?.value??null;
  const frame=useMemo(()=>({binding,current}),[binding,current]);
  const currentFrame=useRef<typeof frame|null>(null);
  useLayoutEffect(()=>{currentFrame.current=frame;return()=>{if(currentFrame.current===frame)currentFrame.current=null;};},[frame]);
  const live=()=>active && binding.live && owner.current===binding;
  useLayoutEffect(()=>{binding.live=true;owner.current=binding;setView(null);return()=>{binding.live=false;binding.pending=null;if(owner.current===binding)owner.current=null;};},[binding]);
  const run=async()=>{
    if(!live() || currentFrame.current!==frame || !request || binding.pending)return;
    const attempt={};binding.pending=attempt;currentFrame.current=null;setView({binding,value:null,busy:true,failed:false});
    try{
      const fixed=structuredClone(request),response=await reader(structuredClone(fixed));
      if(!live() || binding.pending!==attempt)return;
      setView({binding,value:parseCandidateComparison(response,fixed),busy:false,failed:false});
    }catch{if(live() && binding.pending===attempt)setView({binding,value:null,busy:false,failed:true});}
    finally{if(binding.pending===attempt)binding.pending=null;}
  };
  return <section className="miray-card miray-candidate-comparison" aria-label="확인된 성분 비교">
    <h3>확인된 성분 나란히 보기</h3>
    {!request?<p>확인된 카탈로그 제품 두 개를 선택해야 성분을 비교할 수 있어요.</p>:<button className={primaryAction ? "miray-primary" : undefined} disabled={busy || !active} onClick={()=>void run()}>{busy?"성분 확인 중…":"성분 비교 확인"}</button>}
    {failed&&<p role="alert">성분 비교를 완료하지 못했어요. 제품 버전과 연결을 다시 확인해 주세요.</p>}
    {visible&&<><p>{visible.message}</p><p>{visible.presence_note}</p>{visible.products.map(product=><article key={product.product_id}><h4>{product.name}</h4><p>{product.ingredients.join(", ")}</p><dl>{product.palette.map(row=><div key={row.key}><dt>{row.label}</dt><dd>{row.present===null?"확인되지 않음":row.present?"포함 확인":"미포함 확인"}</dd></div>)}</dl></article>)}</>}
  </section>;
}
