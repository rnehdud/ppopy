/** Exact UTC identity across JavaScript millisecond and server microsecond
 * representations. Padding is not rounding and carries no time tolerance. */
export function canonicalUtcInstant(value:string):string{
  const m=/^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})(?:\.(\d{1,6}))?(?:Z|\+00:00)$/.exec(value);
  if(!m)throw new Error("Exact UTC timestamp required");
  const date=new Date(m[1]+"Z");
  if(!Number.isFinite(date.getTime()) || date.toISOString().slice(0,19)!==m[1])throw new Error("Valid UTC timestamp required");
  return m[1]+"."+(m[2]??"").padEnd(6,"0")+"Z";
}
export const sameUtcInstant=(left:string,right:string)=>canonicalUtcInstant(left)===canonicalUtcInstant(right);
