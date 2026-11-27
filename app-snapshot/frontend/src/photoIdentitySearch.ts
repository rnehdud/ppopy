import brands from "../../skin_engine/config/brand_aliases.json";
import type { CatalogSearcher } from "./photoCatalogMatch";

const normalize = (s: string) => s.normalize("NFKC").toLowerCase().replace(/[^a-z0-9가-힣]/g, "");
// Search alias read from the owner-supplied package photo; no catalog evidence promotion.
const packageAliases: Record<string, string[]> = {"라로슈포제": ["LA ROCHE-POSAY"]};
export async function searchPhotoIdentity(lines: readonly string[], search: CatalogSearcher, isCurrent: () => boolean) {
  const text = lines.map(normalize);
  const matched = Object.entries(brands.brands).filter(([brand, value]) => {
    const aliases = [brand, ...(packageAliases[brand] ?? []), ...value.aliases.filter(a => a.search_enabled).map(a => a.value)];
    return aliases.some(alias => text.some(line => line.includes(normalize(alias))));
  }).map(([brand]) => brand);
  if (matched.length !== 1) throw new Error("제품 브랜드를 하나로 확인하지 못했어요. 제품 앞면만 촬영하거나 제품명을 직접 검색해 주세요.");
  if (!isCurrent()) throw new DOMException("Search superseded", "AbortError");
  // One brand-scoped lookup replaces line-by-line volume/marketing searches.
  const candidates = await search(matched[0]);
  if (!isCurrent()) throw new DOMException("Search superseded", "AbortError");
  return candidates.filter(candidate => normalize(candidate.brand) === normalize(matched[0]));
}
