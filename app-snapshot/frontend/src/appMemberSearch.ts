import type {CareApiClient, ProductSearchOptions} from "./careApi";
import {runWithMemberResponseSession} from "./appMemberResponseSession";
import {awaitSearchRequest} from "./searchRequestLifetime";

/** Track only in-flight work, with no query, bearer or quota/cost state. */
export async function runMemberProductSearch<T>(
  load: () => Promise<string | null>, changed: () => void,
  active: Set<AbortController>,
  search: (query: string, options?: ProductSearchOptions) => Promise<T>,
  query: string, options?: ProductSearchOptions,
): Promise<T> {
  options?.signal?.throwIfAborted();
  const controller = new AbortController();
  const abort = () => controller.abort(options?.signal?.reason);
  options?.signal?.addEventListener("abort", abort, {once:true});
  active.add(controller);
  try {
    return await awaitSearchRequest(() => runWithMemberResponseSession(load,changed,() => {
      controller.signal.throwIfAborted();
      return search(query,{signal:controller.signal});
    }), async () => { controller.abort(); }, controller.signal);
  } finally {
    options?.signal?.removeEventListener("abort", abort);
    active.delete(controller);
  }
}

export function abortMemberProductSearches(active: Set<AbortController>): void {
  for (const controller of active) controller.abort();
  active.clear();
}

export type MemberSearchClient = Pick<CareApiClient,"searchProducts"> & Partial<Pick<CareApiClient,"searchWebProducts">>;
