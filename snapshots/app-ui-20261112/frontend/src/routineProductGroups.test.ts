import catalog from "../../skin_engine/config/routine_display_catalog.json";
import {groupRoutineProducts, reorderRoutineSubset, routineProductCategory, isRoutineSunscreen} from "./routineProductGroups";
import type {ProductCandidate} from "./productCatalog";

const cleanser = catalog.products.find(p => p.id === "PKG-20260815-010")!;
const serum = catalog.products.find(p => p.id === "토리든-258297")!;
const candidate = (record: typeof cleanser): ProductCandidate => ({...record, category:undefined, evidenceStatus:"review_required", matchSource:"catalog"});

it("recognizes explicit sunscreen names without treating cleansers or sets as sunscreen",()=>{
  expect(isRoutineSunscreen({...candidate(serum),id:"manual-sun",name:"촉촉 선크림",matchSource:"manual"})).toBe(true);
  expect(isRoutineSunscreen({...candidate(serum),id:"manual-cleanser",name:"선크림 클렌저",matchSource:"manual"})).toBe(false);
  expect(isRoutineSunscreen({...candidate(serum),id:"manual-set",name:"선크림 세트",matchSource:"manual"})).toBe(false);
  expect(isRoutineSunscreen({...candidate(serum),id:"manual-bundle",name:"선크림 + 패드",matchSource:"manual"})).toBe(false);
});

it("separates restored exact TEST identities without changing portfolio evidence or sale names", () => {
  const wash = candidate(cleanser), leave = candidate(serum);
  const before = JSON.stringify([leave,wash]);
  expect(groupRoutineProducts([leave,wash]).map(g => [g.label,g.products.map(p=>p.id)])).toEqual([
    ["세안",[wash.id]],["바르는 제품",[leave.id]],
  ]);
  expect(JSON.stringify([leave,wash])).toBe(before);
});

it("does not infer cleansing from a name or reuse metadata from a different option or manual source", () => {
  const wash = candidate(cleanser);
  for (const product of [{...wash,option:"999mL"},{...wash,id:"unknown"},{...wash,matchSource:"manual" as const},{...wash,name:"different"}]) {
    expect(routineProductCategory(product)).toBeUndefined();
    expect(groupRoutineProducts([product])[0].key).toBe("unclassified");
  }
});

it("uses a supported explicit live catalog category even for an identity outside the frozen display set", () => {
  expect(routineProductCategory({...candidate(cleanser),id:"new-catalog",category:"cleanser"})).toBe("cleanser");
  expect(routineProductCategory({...candidate(cleanser),id:"new-catalog",category:undefined})).toBeUndefined();
});

it("reorders only a group's slots, preserving interleaving and every other product", () => {
  const full=["c1","s1","unknown","s2","c2"];
  expect(reorderRoutineSubset(full,["s2","s1"])).toEqual(["c1","s2","unknown","s1","c2"]);
  expect(reorderRoutineSubset(full,["s2","s2"])).toBe(full);
  expect(reorderRoutineSubset(full,["other","s1"])).toBe(full);
  expect(full).toEqual(["c1","s1","unknown","s2","c2"]);
});
