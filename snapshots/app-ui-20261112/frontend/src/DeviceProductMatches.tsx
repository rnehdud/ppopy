import catalog from "./devicePublicCatalog.json";
import {productNamePresentation} from "./productPresentation";

const normalize=(s:string)=>s.normalize("NFKC").toLowerCase().replace(/\s+/g,"");

// These are public, versioned facts shipped with the app, never member search history.
export default function DeviceProductMatches({query}:{query:string}){
  const key=normalize(query);
  if(!key)return null;
  const matches=catalog.products.filter(p=>normalize(p.brand+" "+p.name).includes(key));
  if(!matches.length)return null;
  return <section aria-label="제품 바로 보기"><h2>제품 바로 보기</h2>
    {matches.map(p=><details key={p.id} className="miray-card">
      <summary>{productNamePresentation(p.name).name}</summary>
      <p>{p.ingredients ? "전성분: "+p.ingredients : "제품 용기의 전성분 표시를 확인해 주세요."}</p>
      <a href={p.url} target="_blank" rel="noopener noreferrer">제품 출처 보기</a>
    </details>)}
  </section>;
}
