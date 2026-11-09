import type {CareApiClient,ProductSearchOptions} from "./careApi";
import type {ProductCandidate, WebProductCandidate} from "./productCatalog";
import {productPresentation} from "./productPresentation";

export type MirayExploreCandidate = {
  id: string;
  title: string;
  detail: string;
  source: "catalog" | "web";
  evidenceStatus: ProductCandidate["evidenceStatus"];
  sourceUrl?: string;
  provenanceHash?: string;
  /**
   * Only a fresh catalog result has the structured product fields needed to
   * add it to a member's cosmetics list. Saved and web candidates deliberately
   * do not manufacture those fields from display text.
   */
  registrationProduct?: ProductCandidate;
};
export type MirayExploreSearchStage = "catalog" | "web";
export type MirayExploreSearch = (
  query: string,
  onStage?: (stage: MirayExploreSearchStage) => void,
  options?: ProductSearchOptions,
) => Promise<MirayExploreCandidate[]>;

/**
 * The member workspace must supply this from its authenticated composition.
 * Keeping the lookup construction outside the screen avoids a hidden fallback
 * to the fixture client, which is only appropriate for an owner preview.
 */
export function createMirayExploreSearch(client: Pick<CareApiClient, "searchProducts"> & Partial<Pick<CareApiClient, "searchWebProducts">>): MirayExploreSearch {
  return async (query, onStage, options): Promise<MirayExploreCandidate[]> => {
    options?.signal?.throwIfAborted();
    onStage?.("catalog");
    options?.signal?.throwIfAborted();
    // Native TEST adapters are explicitly injected by the app composition too,
    // so the Shell's member-lifetime guard encloses every stage on every platform.
    const catalog: ProductCandidate[] = await (options ? client.searchProducts(query,options) : client.searchProducts(query));
    options?.signal?.throwIfAborted();
    if (catalog.length) return catalog.map(p => {
      const display = productPresentation(p);
      return {
        id:p.id, title:display.name, detail:display.subtitle, source:"catalog",
        evidenceStatus:p.evidenceStatus, sourceUrl:p.sourceUrl, provenanceHash:p.provenanceHash,
        registrationProduct:{...p, matchSource:p.matchSource ?? "catalog"},
      };
    });
    if (!client.searchWebProducts) return [];
    onStage?.("web");
    options?.signal?.throwIfAborted();
    const web: WebProductCandidate[] = await (options ? client.searchWebProducts(query,options) : client.searchWebProducts(query));
    options?.signal?.throwIfAborted();
    return web.map(p => ({
      id:p.candidateId, title:p.title, detail:p.sourceDomain, source:"web",
      evidenceStatus:"review_required", sourceUrl:p.sourceUrl, provenanceHash:p.provenanceHash,
    }));
  };
}
