import {expect, it} from "vitest";
import {productPresentation,productNamePresentation} from "./productPresentation";
import {CATALOG_COMPONENT_NAMES,CATALOG_SINGLE_PRODUCT_NAMES} from "./catalogSingleProductNames";

it("uses the source-linked single name only for the exact sales name",()=>{
 for (const [originalName, name] of Object.entries(CATALOG_SINGLE_PRODUCT_NAMES)) {
  expect(productNamePresentation(originalName)).toEqual({name, originalName});
 }
 const unresolved="풀리 토마토 팩클렌저 기획 2 종 택 1 ( 그린 / 레드 )";
 expect(productNamePresentation(unresolved)).toEqual({name:unresolved,originalName:null});
});

it("uses a component name only with its exact original identity and label",()=>{
 for(const [id, record] of Object.entries(CATALOG_COMPONENT_NAMES)) {
  const p={id,name:record.original,brand:"",option:"",evidenceStatus:"review_required" as const};
  expect(productPresentation(p).name).toBe(record.name);
  expect(productPresentation({...p,id:"different-id"}).name).toBe(record.original);
  expect(productPresentation({...p,name:"다른 제품"}).name).toBe("다른 제품");
 }
});
it("separates the promotion label without changing catalog evidence", () => {
 const product = {id:"sample",name:"라운드랩 자작나무 수분 선크림 50ml 더블 기획",brand:"라운드랩",option:"크림제 · 50mL",evidenceStatus:"owner_verified" as const};
 const before=JSON.stringify(product);
 expect(productPresentation(product)).toEqual({name:"라운드랩 자작나무 수분 선크림 50ml",subtitle:"",originalName:product.name});
 expect(JSON.stringify(product)).toBe(before);
});
it("preserves shade and set identity instead of guessing a single component", () => {
 const p={id:"set",name:"토너+크림 세트",brand:"브랜드",option:"21호 · 50mL",evidenceStatus:"review_required" as const};
 expect(productPresentation(p)).toEqual({name:p.name,subtitle:"브랜드 · 21호 · 50mL",originalName:null});
});
it("hides liquid classification and separates the gift promotion", () => {
 const p={id:"t",name:"토리든 세럼 50ml 기획 (+ 멀티 패드 10 매 )",brand:"토리든",option:"액제 · 50mL",evidenceStatus:"owner_verified" as const};
 expect(productPresentation(p)).toEqual({name:"토리든 세럼 50ml",subtitle:"",originalName:p.name});
});
it("separates numeric promotional contents and optional single-item labels without rewriting the original",()=>{
 for(const [raw,name] of [
  ["웰라쥬 리얼 히알루로닉 블루 100 앰플 100ml 기획 (+60ml 리필 + 수딩크림 30ml)","웰라쥬 리얼 히알루로닉 블루 100 앰플 100ml"],
  ["닥터엘시아 345 릴리프 크림 50ml 기획 (+10ml*2ea+ 튜브링거)","닥터엘시아 345 릴리프 크림 50ml"],
  ["크림 50ml 단품 / 기획 (본품+증정품)","크림 50ml"],
 ])expect(productNamePresentation(raw)).toEqual({name,originalName:raw});
 for(const raw of ["토너+크림 세트","크림 (향료 무첨가) 50ml","크림 2종"])
  expect(productNamePresentation(raw)).toEqual({name:raw,originalName:null});
});

it("handles a promotion inside an alias and full-width gift brackets without trimming formula or unlabelled kits",()=>{
  for(const [raw,shown] of [
    ["아벤느 크렘(시칼파트 플러스 SOS 리페어 크림 100ml 기획 (+40ml))","아벤느 크렘(시칼파트 플러스 SOS 리페어 크림 100ml)"],
    ["토너+크림 기획세트","토너+크림 기획세트"],
    ["수분크림 50ml 기획세트 （미니 10ml 증정）","수분크림 50ml"],
    ["조선미녀 맑은쌀 선크림 (Relief Sun : Rice + Probiotics)","조선미녀 맑은쌀 선크림 (Relief Sun : Rice + Probiotics)"],
  ])expect(productNamePresentation(raw).name).toBe(shown);
});
