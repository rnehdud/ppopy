import {useCallback,useEffect,useRef,useState} from "react";
import type {ReviewLookupConnection,ReviewLookupView} from "./appLookupConnectionLocal";
import type {LookupRequestConfirmation} from "./appLookupRequestLocal";
import type {LookupDelivery,LookupMetadata} from "./appLookupDeliveryLocal";

type ResponseValue=LookupRequestConfirmation|LookupDelivery|LookupMetadata;
type ViewState=Awaited<ReturnType<ReviewLookupView["state"]>>;
type State={status:"connecting"|"ready"|"closed";busy:boolean;view:ViewState|null;response:ResponseValue|null;notice:string|null};
const empty=(status:State["status"]):State=>({status,busy:false,view:null,response:null,notice:null});

/** Unregistered review hook. Mount/connect checks the member vault only. Every
 * network action is explicit; invalidation clears this view's response eagerly. */
export function useReviewLookupConnection(connection:ReviewLookupConnection){
  const [state,setState]=useState<State>(()=>empty("connecting"));
  const live=useRef(false),generation=useRef(0),lease=useRef<ReviewLookupView|null>(null);
  const owner=useRef(connection),running=useRef<number|null>(null);
  const connect=useCallback(async()=>{
    if(!live.current||owner.current!==connection)return;
    // openView invalidates the old lease synchronously, before vault awaits.
    const opening=connection.openView(),own=++generation.current;
    setState(empty("connecting"));
    try{
      const opened=await opening;
      if(!live.current||generation.current!==own){opened.detach();return;}
      lease.current=opened;const view=await opened.state();
      if(live.current&&generation.current===own)setState({...empty("ready"),view});
    }catch{
      if(live.current&&generation.current===own)setState({...empty("closed"),notice:"검색 연결을 다시 확인해 주세요."});
    }
  },[connection]);
  useEffect(()=>{
    const viewLifetime=generation;
    live.current=true;owner.current=connection;running.current=null;
    let unsubscribe=()=>{};
    try{
      unsubscribe=connection.subscribeInvalidation(()=>{
        generation.current++;lease.current=null;running.current=null;
        if(live.current)setState({...empty("closed"),notice:"이전 검색 화면을 닫았어요. 돌아오면 연결을 확인해 주세요."});
      });
      void connect();
    }catch{setState({...empty("closed"),notice:"검색 연결을 다시 확인해 주세요."});}
    return ()=>{live.current=false;viewLifetime.current++;running.current=null;unsubscribe();lease.current?.detach();lease.current=null;};
  },[connection,connect]);
  const run=useCallback(async(operation:(view:ReviewLookupView)=>Promise<ResponseValue>)=>{
    const current=lease.current,own=generation.current;
    if(!live.current||owner.current!==connection||!current||running.current===own)return;
    running.current=own;
    setState(s=>({...s,busy:true,response:null,notice:null}));
    try{
      const response=await operation(current),view=await current.state();
      if(live.current&&generation.current===own)setState({status:"ready",busy:false,view,response,notice:null});
    }catch{
      if(!live.current||generation.current!==own)return;
      try{
        const view=await current.state();
        if(live.current&&generation.current===own)setState({status:"ready",busy:false,view,response:null,notice:"검색 상태를 확인하지 못했어요. 자동으로 다시 요청하지 않습니다."});
      }catch{
        if(live.current&&generation.current===own)setState({...empty("closed"),notice:"검색 연결을 다시 확인해 주세요."});
      }
    }finally{if(running.current===own)running.current=null;}
  },[connection]);
  // A prop replacement can render before effects clean up the old lease. Never
  // publish its old member response during that first replacement render.
  return {state:owner.current===connection?state:empty("connecting"),connect,
    begin:(query:string)=>run(v=>v.begin(query)),retryStart:(query:string)=>run(v=>v.retryStart(query)),
    recover:()=>run(v=>v.recover()),read:()=>run(v=>v.read()),cancel:()=>run(v=>v.cancel()),
  };
}
