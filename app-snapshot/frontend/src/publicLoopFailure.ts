// Public service UI diagnostic classification only. Never retain a response body, SDK error, member
// identifier, URL, header, credential or answer as diagnostic metadata.
type Stage="T"|"S"|"W";
type Kind="P"|"N"|"M"|"H"|"B"|"J"|"C";
const failures=new WeakMap<object,{kind:Kind;status?:number}>();
const codes=new WeakMap<object,string>();
export function publicLoopFailure(stage:Stage,kind:Kind,status?:number):Error{
  const safeStage=["T","S","W"].includes(stage)?stage:"T";
  const safeKind=["P","N","M","H","B","J","C"].includes(kind)?kind:"C";
  const checked=typeof status==="number" && Number.isInteger(status) && status>=200 && status<=599?status:undefined;
  const error=new Error("루틴 연결을 확인하지 못했어요.");
  failures.set(error,{kind:safeKind,status:checked});codes.set(error,`L-${safeStage}-${safeKind}${checked??""}`);return error;
}
export function publicLoopFailureAt(error:unknown,stage:Stage):Error{
  const known=error && typeof error==="object"?failures.get(error):undefined;
  const projected=publicLoopFailure(stage,known?.kind??"C",known?.status);
  if(!(error instanceof Error) && !(error instanceof DOMException))return projected;
  // Preserve abort/member-change identity for existing callers. Weak keys do
  // not retain the original error; only the fixed classification is stored.
  failures.set(error,failures.get(projected)!);codes.set(error,codes.get(projected)!);return error;
}
export function publicLoopFailureCode(error:unknown):string{
  return error && typeof error==="object"?codes.get(error)??"L-V-C":"L-V-C";
}
