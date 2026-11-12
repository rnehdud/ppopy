import {readFileSync} from "node:fs";
import {resolve} from "node:path";
import {expect,it} from "vitest";
import copy from "./memberKbConsumerCopy.json";
import {consumerGuidanceText} from "./memberKbPresentation";
it("matches the original 60 KB recommendation branches without changing source or decisions",()=>{
 const kb=JSON.parse(readFileSync(resolve(process.cwd(),"../KB/Poppy_KB_v0.6/Poppy_KB_seed_v0.6.json"),"utf8"));
 expect(Object.keys(copy.cards).sort()).toEqual(kb.baseline_cards.map((r:{id:string})=>r.id).sort());
 for(const card of kb.baseline_cards){
  const entry=(copy.cards as Record<string,Record<string,{source:string;text:string}>>)[card.id];
  for(const [status,key] of Object.entries({aligned:"on_aligned",difference:"on_known_difference",unknown:"on_unknown",exception:"on_exception"})){
   expect(entry[status].source).toBe(card.recommendation[key]);
   expect(consumerGuidanceText(card.id,status,entry[status].source)).toBe(entry[status].text);
  }
 }
 expect(copy.changes_decisions).toBe(false);
});
it("does not apply stale editorial text to a different recommendation",()=>{
 expect(consumerGuidanceText("B-C01","difference","제품을 쓰지 말아 주세요.")).toBe("제품을 쓰지 말아 주세요.");
 expect(consumerGuidanceText("B-C01","conflicting","internal reason")).toContain("답변이 서로 달라");
 expect(consumerGuidanceText("B-C01","difference","기본값을 강제하지 않고 안내한다.")).not.toContain("기본값");
});
it("retains prescription and urgent eye exceptions in consumer copy",()=>{
 expect(copy.cards["B-G13"].difference.text).toContain("처방약은 임의로 바꾸지");
 expect(copy.cards["B-P06"].difference.text).toContain("시야 변화");
 expect(copy.cards["B-P08"].difference.text).toContain("사용기한");
});
