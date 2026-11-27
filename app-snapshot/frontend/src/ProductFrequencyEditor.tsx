import {forwardRef, useId, useLayoutEffect, useRef, useState} from "react";
import "./productFrequencyEditor.css";

const choices = ["0", "1", "2", "3", "4", "5", "6", "7", "unknown"];
function frequencyLabel(value:string) {
  if (value === "0") return "사용하지 않음";
  if (/^[1-7]$/.test(value)) return `주 ${value}일`;
  if (value === "unknown") return "모름";
  if (value === "user_refused") return "답변하지 않았어요";
  if (value === "user_does_not_remember") return "기억나지 않아요";
  return "선택해 주세요";
}

/** Inline native radio choices avoid requiring an iOS select popup to open. */
const ProductFrequencyEditor = forwardRef<HTMLButtonElement, {label:string;value:string;disabled?:boolean;onChange(value:string):void}>(function ProductFrequencyEditor({label,value,disabled=false,onChange},ref) {
  const [open,setOpen] = useState(false);
  const id = useId(),trigger = useRef<HTMLButtonElement|null>(null),panel = useRef<HTMLFieldSetElement|null>(null);
  const restoreFocus = useRef(false);
  useLayoutEffect(()=>{
    if (open && !disabled) {
      const target=panel.current?.querySelector<HTMLInputElement>('input:checked') ?? panel.current?.querySelector<HTMLInputElement>('input');
      target?.focus({preventScroll:true});
    } else if (restoreFocus.current) {restoreFocus.current=false;trigger.current?.focus({preventScroll:true});}
  },[open,disabled]);
  const close=()=>{restoreFocus.current=true;setOpen(false);};
  return <div className="product-frequency-editor">
    <button ref={element=>{trigger.current=element;if(typeof ref==="function")ref(element);else if(ref)ref.current=element;}}
      type="button" data-frequency-trigger aria-label={label} value={value}
      aria-expanded={open && !disabled} aria-controls={id} aria-describedby={`${id}-value`} disabled={disabled}
      onClick={()=>{if(!disabled){if(open)close();else setOpen(true);}}}>
      <span id={`${id}-value`}>{frequencyLabel(value)}</span><span aria-hidden="true">{open?"⌃":"⌄"}</span>
    </button>
    {open && !disabled && <fieldset id={id} ref={panel} onKeyDown={event=>{if(event.key==="Escape"){event.preventDefault();close();}}}>
      <legend>사용 빈도 선택</legend>
      <p>최근 7일 동안 실제로 사용한 빈도를 선택해 주세요.</p>
      <div className="product-frequency-options">{choices.map(option=><label key={option}>
        <input type="radio" name={id} value={option} checked={value===option} onClick={close} onChange={()=>{if(!disabled){onChange(option);close();}}}/>
        <span>{frequencyLabel(option)}</span>
      </label>)}</div>
      <button type="button" onClick={close}>선택하지 않고 닫기</button>
    </fieldset>}
  </div>;
});
export default ProductFrequencyEditor;
