export type ProductCandidate = {
  id: string;
  brand: string;
  name: string;
  option: string;
  category?: import("./routineProductGroups").RoutineProductCategory;
  evidenceStatus: "owner_verified" | "automation_verified" | "review_required" | "fixture_only";
  matchSource?: "catalog" | "public_web" | "manual";
  sourceUrl?: string;
  provenanceHash?: string;
  /** Original text and its observation date, supplied only by a verified product source. */
  ingredientDisclosure?: {text: string; observedAt: string};
};

export type WebProductCandidate = {
  candidateId: string;
  title: string;
  sourceDomain: string;
  sourceUrl: string;
  snippet: string;
  provenanceHash: string;
};

// P2-A01은 실제 카탈로그를 노출하지 않는다. P1-J01 뒤 API로 교체할 고정 데모 후보다.
export const DEMO_PRODUCTS: ProductCandidate[] = [
  {
    id: "fixture-cleanser-01",
    brand: "데모 브랜드",
    name: "약산성 젤 클렌저",
    option: "150 mL",
    evidenceStatus: "fixture_only",
  },
  {
    id: "fixture-cream-01",
    brand: "데모 브랜드",
    name: "장벽 보습 크림",
    option: "50 mL",
    evidenceStatus: "fixture_only",
  },
  {
    id: "fixture-sun-01",
    brand: "샘플 랩",
    name: "데일리 선 로션",
    option: "40 mL",
    evidenceStatus: "fixture_only",
  },
];

const normalize = (value: string) => value.normalize("NFKC").toLocaleLowerCase("ko-KR").replace(/\s+/g, "");

export function searchDemoProducts(query: string): ProductCandidate[] {
  const normalized = normalize(query.trim());
  if (!normalized) return [];
  return DEMO_PRODUCTS.filter((product) =>
    normalize(`${product.brand}${product.name}${product.option}`).includes(normalized),
  );
}
