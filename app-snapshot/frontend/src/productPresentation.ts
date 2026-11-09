import type { ProductCandidate } from "./productCatalog";

// Display only: never change the catalog identity or evidence.
export function productNamePresentation(originalName: string) {
  const name = originalName.replace(/\s+(?:더블\s+)?기획(?:\s*\(\s*\+[^)]*\))?\s*$/, "");
  return {name, originalName: name !== originalName ? originalName : null};
}

export function productPresentation(product: ProductCandidate) {
  const {name, originalName} = productNamePresentation(product.name);
  const brand = name.includes(product.brand) ? "" : product.brand;
  const options = product.option.split("·").map(value => value.trim())
    .filter(value => value && !new Set(["크림제", "액제", "로션제", "겔제", "젤제", "밤", "폼"]).has(value))
    .filter(value => !name.toLowerCase().replace(/\s/g, "").includes(value.toLowerCase().replace(/\s/g, "")));
  return {name, subtitle: [brand, ...options].filter(Boolean).join(" · "), originalName};
}
