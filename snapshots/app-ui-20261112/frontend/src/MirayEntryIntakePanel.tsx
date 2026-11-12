import type {MemberStatusReadOptions} from "./memberStatusReadScope";
import {useLayoutEffect,useMemo,useRef} from "react";
import MirayIntakePanel,{type IntakePanelStore} from "./MirayIntakePanel";
import {assertEntryIntakeReviewOnly,parseEntryIntakeView,type EntryIntakeReviewStore} from "./mirayClosedLoopEntryIntake";
import {parseLoopEntryContext,type LoopEntryContext} from "./mirayClosedLoopEntry";
import MirayEntryStateFirstPanel from "./MirayEntryStateFirstPanel";
import type {MiraySkinState} from "./miraySkinState";

/** Disabled initial/fresh input; only server-selected current targets are accepted. */
export default function MirayEntryIntakePanel({store,originalContext,onClose,onSaved,collectStateFirst=false,requestLifetime,expectedPortfolioRevision}:{store:EntryIntakeReviewStore;originalContext:LoopEntryContext|null;collectStateFirst?:boolean;onClose():void;onSaved(context:LoopEntryContext,state?:MiraySkinState):void;requestLifetime?:{isCurrent():boolean};expectedPortfolioRevision?:number}){
  const binding=useMemo(()=>({store,original:originalContext===null?null:parseLoopEntryContext(originalContext),requestLifetime,expectedPortfolioRevision,live:false}),
    // Equal copies of the four exact correlation fields preserve current input.
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [store,collectStateFirst,requestLifetime,expectedPortfolioRevision,originalContext?.entry_ref,originalContext?.mode,originalContext?.previous_snapshot_ref,originalContext?.portfolio_revision]);
  const owner=useRef<typeof binding|null>(null);
  const live=()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}};
  const lifetime=useMemo(()=>({isCurrent:()=>{try{return binding.live && owner.current===binding && (!binding.requestLifetime || binding.requestLifetime.isCurrent()===true);}catch{return false;}}}),[binding]);
  const retire=()=>{binding.live=false;if(owner.current===binding)owner.current=null;};
  useLayoutEffect(()=>{binding.live=true;owner.current=binding;return retire;
    // Exact original correlation and state-first mode own the child port.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  },[binding]);
  const bound=useMemo<IntakePanelStore<LoopEntryContext>>(()=>{
    const original=binding.original;
    const consumer=(o:MemberStatusReadOptions)=>({signal:o.signal,isCurrent:()=>{try{return lifetime.isCurrent() && (!o.isCurrent || o.isCurrent()===true);}catch{return false;}}});
    const gate=(o:MemberStatusReadOptions)=>{o.signal?.throwIfAborted();if(!lifetime.isCurrent() || o.isCurrent?.()!==true)throw new Error("Entry input connection retired");assertEntryIntakeReviewOnly();};
    const target=(c:LoopEntryContext)=>{
      parseLoopEntryContext(c);
      if(binding.expectedPortfolioRevision!==undefined && c.portfolio_revision!==binding.expectedPortfolioRevision)throw new Error("Visible portfolio changed before input");
      if(original?(c.mode!=="fresh" || c.entry_ref===original.entry_ref || c.portfolio_revision!==original.portfolio_revision):c.mode!=="initial")throw new Error("Unconfirmed entry input target");
    };
    const parse=(v:unknown,o:MemberStatusReadOptions)=>{
      gate(o);const value=parseEntryIntakeView(v);target(value.context);
      return value;
    };
    // Child layout reads wait for this parent's binding commit.
    return {read:async options=>{const o=consumer(options);await Promise.resolve();gate(o);const value=await (original?binding.store.readFresh(original.entry_ref,o):binding.store.read(o));gate(o);return parse(value,o);},save:async(c,a,options)=>{const o=consumer(options);await Promise.resolve();gate(o);target(c);const value=await binding.store.save(c.entry_ref,a,o);gate(o);return parse(value,o);}};
  },[binding,lifetime]);
  const close=()=>{if(!live())return;retire();onClose();};
  const saved=(context:LoopEntryContext,state?:MiraySkinState)=>{if(!live())return;retire();if(collectStateFirst)onSaved(structuredClone(context),state?structuredClone(state):undefined);else onSaved(structuredClone(context));};
  if(collectStateFirst)return <MirayEntryStateFirstPanel requestLifetime={lifetime} store={bound} onClose={close} onSaved={saved}/>;
  return <MirayIntakePanel requestLifetime={lifetime} store={bound} label="현재 점검 입력 확인" savedPurpose={originalContext?"새로 확인할 현재 상태":"첫 점검"} onClose={close} onSaved={saved}/>;
}
