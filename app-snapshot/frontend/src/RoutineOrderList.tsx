import {useEffect, useId, useRef, useState, type PointerEvent} from "react";
import type {ProductCandidate} from "./productCatalog";
import {productPresentation} from "./productPresentation";

type Drag = {pointerId:number; id:string; from:number; to:number; startY:number; y:number; scroll:HTMLElement; initialScroll:number; centers:number[]; stride:number; offset:number};

function scrollContainer(element: HTMLElement): HTMLElement {
  for (let parent = element.parentElement; parent; parent = parent.parentElement) {
    if (/(auto|scroll)/.test(getComputedStyle(parent).overflowY) && parent.scrollHeight > parent.clientHeight) return parent;
  }
  return document.scrollingElement as HTMLElement || document.documentElement;
}

function moved(ids: string[], from: number, to: number): string[] {
  const next = [...ids];
  next.splice(to, 0, ...next.splice(from, 1));
  return next;
}

/** Pointer movement is a local preview; only a completed drop changes the portfolio. */
export default function RoutineOrderList({products, label, onReorder}: {products:ProductCandidate[]; label:string; onReorder:(ids:string[]) => void}) {
  const helpId = useId();
  const rows = useRef(new Map<string, HTMLLIElement>());
  const current = useRef<Drag | null>(null);
  const frame = useRef<number | null>(null);
  const [drag, setDrag] = useState<Drag | null>(null);
  const [announcement, setAnnouncement] = useState("");
  const ids = products.map(product => product.id);
  const stop = () => {
    current.current = null;
    if (frame.current !== null) cancelAnimationFrame(frame.current);
    frame.current = null;
    setDrag(null);
  };
  useEffect(() => () => {
    if (frame.current !== null) cancelAnimationFrame(frame.current);
  }, []);

  const preview = () => {
    const state = current.current;
    if (!state) return;
    const position = state.y + state.scroll.scrollTop;
    const to = state.centers.reduce((best, center, index) => Math.abs(center - position) < Math.abs(state.centers[best] - position) ? index : best, state.from);
    const next = {...state, to, offset:state.y - state.startY + state.scroll.scrollTop - state.initialScroll};
    current.current = next;
    setDrag(next);
  };

  const autoScroll = () => {
    const state = current.current;
    if (!state) return;
    const documentScroll = state.scroll === document.scrollingElement;
    const rect = state.scroll.getBoundingClientRect();
    const top = (documentScroll ? 0 : rect.top) + 88;
    const bottom = (documentScroll ? window.innerHeight : rect.bottom) - 100;
    const delta = state.y < top ? -Math.min(10, (top - state.y) / 5) : state.y > bottom ? Math.min(10, (state.y - bottom) / 5) : 0;
    if (delta) {state.scroll.scrollTop += delta; preview();}
    frame.current = requestAnimationFrame(autoScroll);
  };

  const begin = (event: PointerEvent<HTMLButtonElement>, id:string, from:number) => {
    if (!event.isPrimary || event.button !== 0 || current.current) return;
    const scroll = scrollContainer(event.currentTarget);
    const rects = ids.map(value => rows.current.get(value)!.getBoundingClientRect());
    const state:Drag = {pointerId:event.pointerId,id,from,to:from,startY:event.clientY,y:event.clientY,scroll,initialScroll:scroll.scrollTop,
      centers:rects.map(rect => rect.top + rect.height / 2 + scroll.scrollTop), stride:rects[from].height + 8,offset:0};
    event.currentTarget.setPointerCapture(event.pointerId);
    current.current = state; setDrag(state);
    frame.current = requestAnimationFrame(autoScroll);
  };

  const finish = (event: PointerEvent<HTMLButtonElement>, commit:boolean) => {
    const state = current.current;
    if (!state || state.pointerId !== event.pointerId) return;
    if (commit && state.from !== state.to) {
      onReorder(moved(ids,state.from,state.to));
      setAnnouncement(`${productPresentation(products[state.from]).name}, ${label} ${state.to + 1}번째로 옮겼어요.`);
    }
    stop();
    if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId);
  };

  return <>
    {products.length > 1 && <p className="miray-order-help" id={helpId}>오른쪽 손잡이를 끌어 순서를 바꿔요.<span className="sr-only">키보드는 위·아래 화살표, 처음은 Home, 마지막은 End 키를 사용하세요.</span></p>}
    <ol className="miray-order-list" aria-label={`${label}${label.endsWith("제품") ? "" : " 제품"} 순서`}>{products.map((product,index) => {
      let offset = 0;
      if (drag) {
        if (index === drag.from) offset = drag.offset;
        else if (drag.from < index && index <= drag.to) offset = -drag.stride;
        else if (drag.to <= index && index < drag.from) offset = drag.stride;
      }
      return <li key={product.id} ref={element => {if (element) rows.current.set(product.id,element);else rows.current.delete(product.id);}}
        className={drag?.id === product.id ? "miray-order-row dragging" : "miray-order-row"}
        style={{transform:`translateY(${offset}px)`}}>
        <span className="miray-order-number" aria-hidden="true">{index + 1}</span><span>{productPresentation(product).name}</span>
        {products.length > 1 && <button type="button" className="miray-order-handle" aria-label={`${productPresentation(product).name} ${label} 순서 옮기기`} aria-describedby={helpId}
          onPointerDown={event => begin(event,product.id,index)}
          onPointerMove={event => {if (current.current?.pointerId === event.pointerId) {current.current.y = event.clientY;preview();}}}
          onPointerUp={event => finish(event,true)} onPointerCancel={event => finish(event,false)} onLostPointerCapture={event => finish(event,false)}
          onKeyDown={event => {
            if (event.key === "Escape" && current.current) {stop();return;}
            if (current.current) return;
            const destination = event.key === "ArrowUp" ? index - 1 : event.key === "ArrowDown" ? index + 1 : event.key === "Home" ? 0 : event.key === "End" ? ids.length - 1 : null;
            if (destination === null) return;
            event.preventDefault();
            if (destination < 0 || destination >= ids.length || destination === index) return;
            onReorder(moved(ids,index,destination));
            setAnnouncement(`${productPresentation(product).name}, ${label} ${destination + 1}번째로 옮겼어요.`);
          }}><svg aria-hidden="true" width="20" height="20" viewBox="0 0 20 20"><path d="M3 5h14M3 10h14M3 15h14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/></svg></button>}
      </li>;
    })}</ol>
    <span role="status" className="sr-only">{announcement}</span>
  </>;
}
