import type { ProductCandidate } from "./productCatalog";
import { CATALOG_COMPONENT_NAMES, CATALOG_SINGLE_PRODUCT_NAMES } from "./catalogSingleProductNames";

// Display only: never change the catalog identity or evidence.
export function productNamePresentation(originalName: string) {
  const evidencedName = CATALOG_SINGLE_PRODUCT_NAMES[originalName];
  if (evidencedName) return {name: evidencedName, originalName};
  // Only remove a terminal sales offer. A '+' in a formula or in a
  // multi-product name is not enough evidence of a free gift.
  const offer = /\s+(?:단품\s*\/\s*)?(?:더블\s+)?기획(?:\s*세트)?(?:\s*[（(][^()（）]*[)）])?\s*$/u;
  let name = originalName.replace(offer, "");
  if(name===originalName){
    // A catalog alias may itself contain the offer (e.g. the Avène cream).
    const alias = /^(.*?)[(（]([^()（）]+기획(?:\s*세트)?\s*[(（][^()（）]*[)）])[)）]$/u.exec(originalName);
    if(alias && alias[1].trim() && offer.test(alias[2]))
      name=alias[1]+"("+alias[2].replace(offer,"")+")";
  }
  if(name!==originalName && /(?:세트|[0-9]+\s*종|\s[+&]\s|[+&](?:크림|토너|앰플|세럼|로션))/.test(name))
    name=originalName; // No evidence identifies a single primary product.
  return {name, originalName: name !== originalName ? originalName : null};
}

export function productPresentation(product: ProductCandidate) {
  const shown = productNamePresentation(product.name);
  const component = CATALOG_COMPONENT_NAMES[product.id];
  const name = component?.original === product.name ? component.name : shown.name;
  const {originalName} = shown;
  const brand = name.includes(product.brand) ? "" : product.brand;
  const options = product.option.split("·").map(value => value.trim())
    .filter(value => value && !new Set(["크림제", "액제", "로션제", "겔제", "젤제", "밤", "폼"]).has(value))
    .filter(value => !name.toLowerCase().replace(/\s/g, "").includes(value.toLowerCase().replace(/\s/g, "")));
  return {name, subtitle: [brand, ...options].filter(Boolean).join(" · "), originalName};
}
