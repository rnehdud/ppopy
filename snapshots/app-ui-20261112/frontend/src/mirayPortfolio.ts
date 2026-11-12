import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import type {ProductCandidate} from "./productCatalog";
import {isMirayCandidateProvenanceHash, validateMirayCandidateSourceUrl} from "./miraySavedCandidates";

export type MirayPortfolio = {
  version: "1.2.0";
  products: Array<{
    id: string;
    brand: string;
    name: string;
    option: string;
    evidence_status: ProductCandidate["evidenceStatus"];
    match_source: "catalog" | "public_web" | "manual";
    frequency: string;
    depletion_status: MirayProductDepletionStatus;
    /** Public product-source and ingredient-version proof only; never a member URL or a recommendation. */
    source_url: string | null;
    provenance_hash: string | null;
  }>;
  periods: {am: string[]; pm: string[]};
};

/** Member-declared availability only; never an inferred depletion date. */
export type MirayProductDepletionStatus = "not_tracking" | "enough" | "running_low" | "empty";

export type MirayRoutineOrder = MirayPortfolio["periods"];

export type MirayPortfolioEnvelope = {revision: number; portfolio: MirayPortfolio};
export type MirayPortfolioStore = {
  read(): Promise<MirayPortfolioEnvelope>;
  save(portfolio: MirayPortfolio, expectedRevision: number): Promise<MirayPortfolioEnvelope>;
};

export type MirayPortfolioHttpOptions = {
  baseUrl?: string;
  allowedBaseUrls?: readonly string[];
  loadSessionToken: () => Promise<string | null>;
  /** Explicit UI lifecycle notification; never clears credentials or retries HTTP. */
  onSessionChanged?: () => void;
};

export const emptyMirayPortfolio = (): MirayPortfolio => ({
  version:"1.2.0", products:[], periods:{am:[],pm:[]},
});

function stable(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === "object") return Object.fromEntries(
    Object.entries(value as Record<string,unknown>).sort(([left],[right]) => left.localeCompare(right)).map(([key,item]) => [key,stable(item)]),
  );
  return value;
}

export const portfolioFingerprint = (portfolio: MirayPortfolio) => JSON.stringify(stable(portfolio));

const object = (value: unknown): value is Record<string,unknown> => Boolean(value) && typeof value === "object" && !Array.isArray(value);
const exact = (value: Record<string,unknown>, keys: readonly string[]) => Object.keys(value).sort().join("|") === [...keys].sort().join("|");

export function parseMirayPortfolioEnvelope(value: unknown): MirayPortfolioEnvelope {
  if (!object(value) || !exact(value,["revision","portfolio"]) || !Number.isSafeInteger(value.revision) || Number(value.revision) < 0 || !object(value.portfolio)) {
    throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
  }
  const portfolio = value.portfolio;
  const version = portfolio.version;
  if (!exact(portfolio,["version","products","periods"]) || !["1.0.0","1.1.0","1.2.0"].includes(String(version)) || !Array.isArray(portfolio.products) || portfolio.products.length > 40 || !object(portfolio.periods) || !exact(portfolio.periods,["am","pm"])) {
    throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
  }
  const evidence = new Set(["owner_verified","automation_verified","review_required","fixture_only"]);
  const sources = new Set(["catalog","public_web","manual"]);
  const frequencies = new Set([...Array.from({length:8},(_,index) => String(index)),"unknown","user_does_not_remember","user_refused"]);
  const depletion = new Set<MirayProductDepletionStatus>(["not_tracking","enough","running_low","empty"]);
  const v10Keys = ["id","brand","name","option","evidence_status","match_source","frequency"];
  const v11Keys = [...v10Keys,"depletion_status"];
  const currentKeys = [...v11Keys,"source_url","provenance_hash"];
  const products = portfolio.products.map(item => {
    const productKeys = version === "1.0.0" ? v10Keys : version === "1.1.0" ? v11Keys : currentKeys;
    if (!object(item) || !exact(item,productKeys) || v10Keys.some(key => typeof item[key] !== "string")) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    if (!item.id || String(item.id).length > 300 || [item.brand,item.name,item.option].some(text => String(text).length > 300) || !evidence.has(String(item.evidence_status)) || !sources.has(String(item.match_source)) || !frequencies.has(String(item.frequency))) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    if (version !== "1.0.0" && !depletion.has(item.depletion_status as MirayProductDepletionStatus)) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    const sourceUrl = version === "1.2.0" ? item.source_url : null;
    const provenanceHash = version === "1.2.0" ? item.provenance_hash : null;
    if ((sourceUrl === null) !== (provenanceHash === null)) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    if (sourceUrl !== null) {
      if (typeof sourceUrl !== "string" || typeof provenanceHash !== "string") throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
      try { validateMirayCandidateSourceUrl(sourceUrl); }
      catch { throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다."); }
      if (!isMirayCandidateProvenanceHash(provenanceHash)) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    }
    if (item.match_source === "manual" && sourceUrl !== null) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    if (item.match_source === "public_web" && (sourceUrl === null || provenanceHash === null || item.evidence_status !== "review_required")) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    return {
      id:item.id as string, brand:item.brand as string, name:item.name as string, option:item.option as string,
      evidence_status:item.evidence_status as ProductCandidate["evidenceStatus"],
      match_source:item.match_source as MirayPortfolio["products"][number]["match_source"],
      frequency:item.frequency as string,
      depletion_status:version === "1.0.0" ? "not_tracking" : item.depletion_status as MirayProductDepletionStatus,
      source_url:sourceUrl as string | null,
      provenance_hash:provenanceHash as string | null,
    };
  });
  const ids = products.map(item => item.id);
  if (new Set(ids).size !== ids.length) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
  const readPeriod = (period: unknown) => {
    if (!Array.isArray(period) || period.some(id => typeof id !== "string" || !ids.includes(id)) || new Set(period).size !== period.length) throw new Error("계정 화장품 응답 형식을 확인하지 못했습니다.");
    return [...period] as string[];
  };
  return {revision:Number(value.revision),portfolio:{version:"1.2.0",products,periods:{am:readPeriod(portfolio.periods.am),pm:readPeriod(portfolio.periods.pm)}}};
}

function httpsBase(value: string): string {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
}

export function createHttpMirayPortfolioStore(fetcher: typeof fetch, options: MirayPortfolioHttpOptions): MirayPortfolioStore {
  const loadSessionToken=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  const requested = options.baseUrl?.trim() || "";
  const base = requested ? httpsBase(requested) : "";
  if (base && !(options.allowedBaseUrls || []).map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const request = async (method: "GET" | "PUT", portfolio?: MirayPortfolio, expectedRevision?: number) => {
    // Validate and serialize before asynchronous credential loading so callers
    // cannot mutate a queued request into a different product/routine update.
    let body: string | undefined;
    if (method === "PUT") {
      if (!Number.isSafeInteger(expectedRevision) || Number(expectedRevision) < 0
          || Number(expectedRevision) >= Number.MAX_SAFE_INTEGER) throw new Error("저장 버전을 확인해 주세요.");
      const snapshot = parseMirayPortfolioEnvelope({revision:expectedRevision,portfolio}).portfolio;
      body = JSON.stringify({expected_revision:expectedRevision,portfolio:snapshot});
    }
    const token = await loadSessionToken();
    if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response = await fetcher(`${base}/api/v1/app/portfolio`, {
      method, cache:"no-store", redirect:"error", credentials:"omit",
      headers:{"Authorization":`Bearer ${token}`,...(method === "PUT" ? {"Content-Type":"application/json"} : {})},
      ...(method === "PUT" ? {body} : {}),
    });
    await assertCurrentMemberResponseSession(loadSessionToken, token, options.onSessionChanged);
    const payload: unknown = await response.json();
    await assertCurrentMemberResponseSession(loadSessionToken, token, options.onSessionChanged);
    if (!response.ok) throw new Error(response.status === 409 ? "다른 기기에서 변경된 내용이 있어 다시 불러와야 해요." : "계정 화장품을 저장하지 못했습니다.");
    return parseMirayPortfolioEnvelope(payload);
  };
  return {read:() => request("GET"),save:(portfolio, expectedRevision) => request("PUT",portfolio,expectedRevision)};
}

export function portfolioFromWorkspace(
  products: ProductCandidate[],
  frequencies: Record<string,string>,
  periods: Record<string,string>,
  routineOrder: MirayRoutineOrder = {am:[],pm:[]},
  depletionStatuses: Record<string,MirayProductDepletionStatus> = {},
): MirayPortfolio {
  const orderedPeriod = (period: "am" | "pm") => {
    const applicable = products
      .filter(product => periods[product.id] === period || periods[product.id] === "both")
      .map(product => product.id);
    const remaining = new Set(applicable);
    const restored = routineOrder[period].filter(id => remaining.delete(id));
    return [...restored,...applicable.filter(id => remaining.has(id))];
  };
  return {
    version:"1.2.0",
    products:products.map(product => ({
      id:product.id, brand:product.brand, name:product.name, option:product.option,
      evidence_status:product.evidenceStatus,
      match_source:product.matchSource ?? (product.evidenceStatus === "fixture_only" ? "manual" : "catalog"),
      frequency:frequencies[product.id] || "unknown",
      depletion_status:depletionStatuses[product.id] || "not_tracking",
      source_url:product.sourceUrl ?? null,
      provenance_hash:product.provenanceHash ?? null,
    })),
    periods:{
      am:orderedPeriod("am"),
      pm:orderedPeriod("pm"),
    },
  };
}

export function workspaceFromPortfolio(portfolio: MirayPortfolio) {
  const products: ProductCandidate[] = portfolio.products.map(product => ({
    id:product.id, brand:product.brand, name:product.name, option:product.option,
    evidenceStatus:product.evidence_status, matchSource:product.match_source,
    sourceUrl:product.source_url ?? undefined, provenanceHash:product.provenance_hash ?? undefined,
  }));
  const frequencies = Object.fromEntries(portfolio.products.map(product => [product.id, product.frequency]));
  const depletionStatuses = Object.fromEntries(portfolio.products.map(product => [product.id, product.depletion_status]));
  const periods: Record<string,string> = {};
  for (const product of portfolio.products) {
    const am = portfolio.periods.am.includes(product.id);
    const pm = portfolio.periods.pm.includes(product.id);
    periods[product.id] = am && pm ? "both" : am ? "am" : pm ? "pm" : "";
  }
  return {products, frequencies, periods, routineOrder:{am:[...portfolio.periods.am],pm:[...portfolio.periods.pm]}, depletionStatuses};
}
