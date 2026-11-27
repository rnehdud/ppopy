import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
/**
 * Account-bound saved exploration candidates.
 *
 * This contract deliberately contains only the product candidate and the
 * evidence returned for it. It does not store skin state, an inferred fit,
 * purchase intent, ingredients, or a recommendation decision.
 */

export type MiraySavedCandidate = {
  id: string;
  title: string;
  detail: string;
  source: "catalog" | "web";
  evidence_status: "owner_verified" | "automation_verified" | "review_required";
  source_url: string | null;
  provenance_hash: string | null;
};

export type MiraySavedCandidates = {
  version: "1.0.0";
  candidates: MiraySavedCandidate[];
};

export type MiraySavedCandidatesEnvelope = {revision: number; candidates: MiraySavedCandidates};
export type MiraySavedCandidatesStore = {
  read(): Promise<MiraySavedCandidatesEnvelope>;
  save(candidates: MiraySavedCandidates, expectedRevision: number): Promise<MiraySavedCandidatesEnvelope>;
};

export class MiraySavedCandidatesRevisionConflict extends Error {
  constructor() {
    super("다른 기기에서 변경된 내용이 있어 다시 불러와야 해요.");
    this.name = "MiraySavedCandidatesRevisionConflict";
  }
}

export type MiraySavedCandidatesHttpOptions = {
  baseUrl?: string;
  allowedBaseUrls?: readonly string[];
  loadSessionToken: () => Promise<string | null>;
  /** Explicit UI lifecycle notification; never clears credentials or retries HTTP. */
  onSessionChanged?: () => void;
};

export const emptyMiraySavedCandidates = (): MiraySavedCandidates => ({version:"1.0.0",candidates:[]});

const object = (value: unknown): value is Record<string, unknown> => Boolean(value) && typeof value === "object" && !Array.isArray(value);
const exact = (value: Record<string,unknown>, keys: readonly string[]) => Object.keys(value).sort().join("|") === [...keys].sort().join("|");
const evidence = new Set(["owner_verified","automation_verified","review_required"]);
const candidateKeys = ["id","title","detail","source","evidence_status","source_url","provenance_hash"];
const hash = /^[a-f0-9]{64}$/i;

/**
 * A catalog source may use the public Olive Young `goodsNo` product identifier.
 * No other query field is permitted: it prevents a saved candidate from carrying
 * tracking, account, token, or other user-specific query data.
 */
export function validateMirayCandidateSourceUrl(value: string): string {
  const url = new URL(value);
  const query = [...url.searchParams.entries()];
  const permittedProductQuery = query.length === 1
    && query[0][0] === "goodsNo"
    && /^[A-Za-z0-9_-]{3,128}$/.test(query[0][1]);
  if (url.protocol !== "https:" || !url.hostname || url.username || url.password || url.hash
    || (query.length > 0 && !permittedProductQuery)) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  return value;
}

export const isMirayCandidateProvenanceHash = (value: string): boolean => hash.test(value);

function parseCandidate(value: unknown): MiraySavedCandidate {
  if (!object(value) || !exact(value,candidateKeys) || candidateKeys.slice(0,5).some(key => typeof value[key] !== "string")) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  const item = value as Record<string, string | null>;
  if (!item.id || [item.id,item.title,item.detail].some(text => !text || text.length > 300) || !["catalog","web"].includes(String(item.source)) || !evidence.has(String(item.evidence_status))) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  const hasSourceUrl = item.source_url !== null;
  const hasHash = item.provenance_hash !== null;
  if ((hasSourceUrl && typeof item.source_url !== "string") || (hasHash && typeof item.provenance_hash !== "string") || hasSourceUrl !== hasHash) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  if (hasSourceUrl) validateMirayCandidateSourceUrl(item.source_url!);
  if (hasHash && !isMirayCandidateProvenanceHash(item.provenance_hash!)) throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  if (item.source === "web" && (!hasSourceUrl || !hasHash || item.evidence_status !== "review_required")) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  return item as MiraySavedCandidate;
}

export function parseMiraySavedCandidatesEnvelope(value: unknown): MiraySavedCandidatesEnvelope {
  if (!object(value) || !exact(value,["revision","candidates"]) || !Number.isSafeInteger(value.revision) || Number(value.revision) < 0 || !object(value.candidates)) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  const candidates = value.candidates;
  if (!exact(candidates,["version","candidates"]) || candidates.version !== "1.0.0" || !Array.isArray(candidates.candidates) || candidates.candidates.length > 60) {
    throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  }
  const items = candidates.candidates.map(parseCandidate);
  if (new Set(items.map(item => item.id)).size !== items.length) throw new Error("저장한 후보 응답 형식을 확인하지 못했습니다.");
  return {revision:Number(value.revision),candidates:{version:"1.0.0",candidates:items}};
}

function httpsBase(value: string): string {
  const url = new URL(value);
  if (url.protocol !== "https:" || url.username || url.password || url.search || url.hash) throw new Error("앱 API 주소를 확인해 주세요.");
  return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
}

export function createHttpMiraySavedCandidatesStore(fetcher: typeof fetch, options: MiraySavedCandidatesHttpOptions): MiraySavedCandidatesStore {
  const loadSessionToken=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  const requested = options.baseUrl?.trim() || "";
  const base = requested ? httpsBase(requested) : "";
  if (base && !(options.allowedBaseUrls || []).map(httpsBase).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const request = async (method: "GET" | "PUT", candidates?: MiraySavedCandidates, expectedRevision?: number) => {
    const body = method === "PUT"
      ? JSON.stringify({expected_revision:expectedRevision,candidates:parseMiraySavedCandidatesEnvelope({revision:expectedRevision,candidates}).candidates})
      : undefined;
    const token = await loadSessionToken();
    if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new Error("로그인 세션을 다시 확인해 주세요.");
    const response = await fetcher(`${base}/api/v1/app/saved-candidates`, {
      method, cache:"no-store", redirect:"error", credentials:"omit",
      headers:{"Authorization":`Bearer ${token}`,...(method === "PUT" ? {"Content-Type":"application/json"} : {})},
      ...(method === "PUT" ? {body} : {}),
    });
    await assertCurrentMemberResponseSession(loadSessionToken, token, options.onSessionChanged);
    if (!response.ok) {
      if (response.status === 409) throw new MiraySavedCandidatesRevisionConflict();
      throw new Error("저장한 후보를 계정에 저장하지 못했습니다.");
    }
    const payload: unknown = await response.json();
    await assertCurrentMemberResponseSession(loadSessionToken, token, options.onSessionChanged);
    return parseMiraySavedCandidatesEnvelope(payload);
  };
  return {read:() => request("GET"),save:(candidates, expectedRevision) => request("PUT",candidates,expectedRevision)};
}
