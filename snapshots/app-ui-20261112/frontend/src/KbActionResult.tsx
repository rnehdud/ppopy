import {useEffect, useRef} from 'react';
type Card = {
  kind: string; scope: string[]; key: string; title: string; body: string; display_body?: string;
  message: string|null; question: string|null; answer: string|null;
  editing: boolean; allow_change: boolean; can_revise: boolean;
};
type Use = {id: string; name: string; schedule: string};

export default function KbActionResult({card, uses, busy, reply, revise, changeIntent, move}:
  {card: Card; uses: Use[]; busy: boolean; reply:(value:string)=>void; revise:()=>void; changeIntent:()=>void; move:(row:string,period:string)=>void}) {
  const panel=useRef<HTMLElement>(null);
  useEffect(()=>{panel.current?.scrollIntoView?.({block:'start'})},[card.key]);
  const eye=card.kind==='eye';
  return <section className="kb-action-result" ref={panel} data-testid="action-result" aria-live="polite">
    <div className="kb-action-heading">현재 루틴 안내</div>
    {eye&&card.answer==='yes'&&<p className="kb-action-message" role="status">{card.message}</p>}
    {!(eye&&card.answer==='yes')&&<article className="kb-action-card">
      <div className="kb-action-type">{card.kind==='maintain'?'유지할 점':'조정할 점'}</div>
      <h2>{card.title}</h2><p>{card.display_body??card.body}</p>
      <small>{uses.map(use=>use.name.replace(/^\[합성\]\s*/, '')).join(' · ')}</small>
    </article>}
    {card.question&&<div className="kb-action-question"><h3>{card.question}</h3>
      <div className="kb-action-options">{[['yes',eye?'하나라도 있어요':'있어요'],['no',eye?'모두 없어요':'없어요'],['skip','건너뛰기']].map(([v,label])=>
        <button key={v} disabled={busy} onClick={()=>reply(v)}>{label}</button>)}</div></div>}
    {card.message&&!(eye&&card.answer==='yes')&&<p className="kb-action-message">{card.message}</p>}
    {card.can_revise&&<button disabled={busy} onClick={revise}>답변 수정</button>}
    {card.kind==='pair'&&!card.editing&&<button disabled={busy} onClick={changeIntent}>두 세럼의 사용 회차 변경</button>}
    {card.allow_change&&<div className="kb-action-question"><h3>어느 세럼의 회차를 바꿀까요?</h3>{uses.map(u=>{
      const next=u.schedule==='evening'?'morning':'evening';
      return <button disabled={busy} key={u.id} onClick={()=>move(u.id,next)}>{u.name.replace(/^\[합성\]\s*/, '')} · {next==='morning'?'아침':'저녁'}으로 변경</button>
    })}</div>}
  </section>
}
