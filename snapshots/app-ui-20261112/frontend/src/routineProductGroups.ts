import catalog from "../../skin_engine/config/routine_display_catalog.json";
import type {ProductCandidate} from "./productCatalog";

export type RoutineProductCategory = "cleanser" | "toner" | "serum" | "moisturizer" | "spot" | "sunscreen";
const categories = new Set<string>(["cleanser", "toner", "serum", "moisturizer", "spot", "sunscreen"]);
export const isRoutineProductCategory = (value: unknown): value is RoutineProductCategory => typeof value === "string" && categories.has(value);

/** Public display metadata only. Exact identity/option match survives portfolio v1.2 restoration. */
export function routineProductCategory(product: ProductCandidate): RoutineProductCategory | undefined {
  if (product.matchSource !== "catalog") return undefined;
  if (isRoutineProductCategory(product.category)) return product.category;
  const record = catalog.products.find(item => item.id === product.id && item.brand === product.brand
    && item.name === product.name && item.option === product.option);
  return isRoutineProductCategory(record?.category) ? record.category : undefined;
}

/** Only explicit sunscreen names or catalog classification trigger the morning default. */
export function isRoutineSunscreen(product: ProductCandidate): boolean {
  const category = routineProductCategory(product);
  if (category) return category === "sunscreen";
  const name = product.name.normalize("NFKC");
  if (/클렌징|클렌싱|클렌저|리무버|cleanser|remover|세트|[+＆&]/i.test(name)) return false;
  return /선크림|썬크림|선스틱|썬스틱|선로션|썬로션|선세럼|썬세럼|선쿠션|썬쿠션|자외선차단제|\bsunscreen\b/i.test(name);
}

export function groupRoutineProducts(products: ProductCandidate[]) {
  const groups = [
    {key:"cleansing", label:"세안", products:[] as ProductCandidate[]},
    {key:"leave_on", label:"바르는 제품", products:[] as ProductCandidate[]},
    {key:"unclassified", label:"용도 확인 필요", products:[] as ProductCandidate[]},
  ];
  for (const product of products) {
    const category = routineProductCategory(product);
    groups[category === "cleanser" ? 0 : category ? 1 : 2].products.push(product);
  }
  return groups.filter(group => group.products.length);
}

/** Replace only this group's slots; all other groups, membership and order remain intact. */
export function reorderRoutineSubset(fullOrder: string[], reordered: string[]): string[] {
  const ids = new Set(reordered);
  if (ids.size !== reordered.length || reordered.some(id => !fullOrder.includes(id))) return fullOrder;
  let index = 0;
  return fullOrder.map(id => ids.has(id) ? reordered[index++] : id);
}
