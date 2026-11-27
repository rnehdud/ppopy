import type { ProductCandidate } from "./productCatalog";

export type CatalogSearcher = (query: string) => Promise<ProductCandidate[]>;

export function photoCatalogQueries(
  lines: readonly string[],
  maximumQueryCharacters = 180,
): string[] {
  const cleaned = lines
    .map(line => line.normalize("NFKC").trim().replace(/\s+/g, " "))
    .filter(line => line.length > 0 && line.length <= 120);
  const adjacent = cleaned.slice(0, -1).map((line, index) => `${line} ${cleaned[index + 1]}`);
  return [...new Set([...cleaned, ...adjacent].filter(query => query.length <= maximumQueryCharacters))];
}

/**
 * Reconnects the P1-A03 strategy to the app runtime: search each OCR line and
 * adjacent line pair independently, then combine candidate support. The photo
 * never leaves the device and no candidate is selected automatically.
 */
export async function rankPhotoCatalogCandidates(
  lines: readonly string[],
  search: CatalogSearcher,
  limit = 5,
  concurrency = 3,
  isCurrent: () => boolean = () => true,
): Promise<ProductCandidate[]> {
  const queries = photoCatalogQueries(lines);
  if (!queries.length) return [];

  const responses: ProductCandidate[][] = new Array(queries.length);
  let cursor = 0;
  let failed = false;
  const worker = async () => {
    while (!failed && isCurrent() && cursor < queries.length) {
      const index = cursor++;
      try {
        responses[index] = await search(queries[index]);
      } catch {
        failed = true;
      }
    }
  };
  await Promise.all(Array.from({length: Math.min(Math.max(1, concurrency), queries.length)}, worker));

  if (!isCurrent()) throw new DOMException("Search superseded", "AbortError");
  if (failed) throw new Error("사진 후보 검색에 실패했습니다. 연결을 확인한 뒤 다시 검색해 주세요.");

  const scores = new Map<string, {
    candidate: ProductCandidate;
    bestRank: number;
    support: number;
    firstSeen: number;
  }>();
  let seenSequence = 0;
  for (const candidates of responses) {
    candidates.slice(0, limit).forEach((candidate, rank) => {
      const current = scores.get(candidate.id);
      if (current) {
        current.bestRank = Math.min(current.bestRank, rank);
        current.support += 1;
      } else {
        scores.set(candidate.id, {
          candidate,
          bestRank: rank,
          support: 1,
          firstSeen: seenSequence++,
        });
      }
    });
  }

  return [...scores.values()]
    .sort((left, right) =>
      left.bestRank - right.bestRank
      || right.support - left.support
      || left.firstSeen - right.firstSeen
      || left.candidate.id.localeCompare(right.candidate.id),
    )
    .slice(0, limit)
    .map(value => value.candidate);
}
