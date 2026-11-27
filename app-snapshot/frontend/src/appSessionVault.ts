import googleOwnerPolicy from "../../skin_engine/config/app_google_sdk_owner_local.json";
import kakaoOwnerPolicy from "../../skin_engine/config/app_kakao_sdk_owner_local.json";

export const APP_SESSION_VAULT_KEY = "skinanalysis.app.session.v1";
export const APP_SESSION_VAULT_VERSION = "1.0.0-app-draft";
export const GOOGLE_OWNER_SESSION_VAULT_VERSION = "1.1.0-google-sdk-owner-review";
export const KAKAO_OWNER_SESSION_VAULT_VERSION = "1.2.0-kakao-sdk-owner-review";

export type AppSessionCredential = {
  contract_version: typeof APP_SESSION_VAULT_VERSION | typeof GOOGLE_OWNER_SESSION_VAULT_VERSION | typeof KAKAO_OWNER_SESSION_VAULT_VERSION
    | "1.0.0-public-session" | "1.0.0-public-google-session" | "1.0.0-public-kakao-session";
  session_token: string;
  expires_at: string;
  native_cleanup_proof?: string;
};

export interface SecureValueStore {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  remove(key: string): Promise<void>;
  /** Native stores compare the exact original bytes in their own serialized mutation path. */
  removeIfValueMatches?(key:string,expectedValue:string|null):Promise<boolean>;
}

export interface SessionVault {
  /** Explicit codec selection by the composed vault; TEST defaults stay unchanged. */
  readonly authenticationContracts?:Readonly<{plain:AppSessionCredential["contract_version"];google:AppSessionCredential["contract_version"];kakao:AppSessionCredential["contract_version"]}>;
  load(): Promise<AppSessionCredential | null>;
  save(value: AppSessionCredential): Promise<void>;
  clear(): Promise<void>;
  /** Serialized with this store's vault operations; false preserves a different credential. */
  clearIfCurrent?(expectedToken:string): Promise<boolean>;
}

export async function clearSessionCredential(vault:SessionVault,expectedToken:string):Promise<"cleared"|"changed"|"unavailable"> {
  if(!vault.clearIfCurrent)return "unavailable";
  try {
    const result=await vault.clearIfCurrent(expectedToken);
    return result===true ? "cleared" : result===false ? "changed" : "unavailable";
  } catch {return "unavailable";}
}

// Shares ordering only between adapters using the same store object in this JS
// runtime. It is not a native/cross-process Keychain compare-and-swap.
const storeQueues=new WeakMap<SecureValueStore,Promise<void>>();

function validate(value: unknown, now: number, allowExpired = false): AppSessionCredential | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const record = value as Record<string, unknown>;
  const googleOwner=record.contract_version===GOOGLE_OWNER_SESSION_VAULT_VERSION;
  const kakaoOwner=record.contract_version===KAKAO_OWNER_SESSION_VAULT_VERSION;
  const ownerPolicy=kakaoOwner ? kakaoOwnerPolicy : googleOwnerPolicy;
  const signedOwner=googleOwner || kakaoOwner;
  if (
    Object.keys(record).sort().join("|") !== (signedOwner
      ? "contract_version|expires_at|native_cleanup_proof|session_token" : "contract_version|expires_at|session_token")
    || (!signedOwner && record.contract_version !== APP_SESSION_VAULT_VERSION)
    || (signedOwner && (typeof record.native_cleanup_proof!=="string" || record.native_cleanup_proof.length===0
      || new TextEncoder().encode(record.native_cleanup_proof).length>ownerPolicy.maximum_envelope_bytes
      || new TextEncoder().encode(JSON.stringify(record)).length>ownerPolicy.maximum_vault_bytes))
    || typeof record.session_token !== "string"
    || record.session_token.length < 32
    || (signedOwner && !/^[A-Za-z0-9_-]{32,200}$/.test(record.session_token))
    || typeof record.expires_at !== "string"
    || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|\+00:00)$/.test(record.expires_at)
  ) return null;
  const expires = Date.parse(record.expires_at);
  if (!Number.isFinite(expires) || (!allowExpired && expires <= now)) return null;
  return {
    contract_version: kakaoOwner ? KAKAO_OWNER_SESSION_VAULT_VERSION : googleOwner ? GOOGLE_OWNER_SESSION_VAULT_VERSION : APP_SESSION_VAULT_VERSION,
    session_token: record.session_token,
    expires_at: new Date(expires).toISOString().replace(".000Z", "Z"),
    ...(signedOwner ? {native_cleanup_proof:record.native_cleanup_proof as string} : {}),
  };
}

export function createSessionVault(store: SecureValueStore, now: () => number = Date.now): SessionVault {
  function ordered<T>(work:()=>Promise<T>):Promise<T> {
    const result=(storeQueues.get(store) ?? Promise.resolve()).then(work);
    storeQueues.set(store,result.then(()=>undefined,()=>undefined));
    return result;
  }
  async function removeOriginal(raw:string|null):Promise<boolean> {
    if(store.removeIfValueMatches) {
      const removed=await store.removeIfValueMatches(APP_SESSION_VAULT_KEY,raw);
      if(typeof removed!=="boolean")throw new Error("보안 저장소의 조건부 정리를 확인하지 못했습니다.");
      return removed;
    }
    // Browser/synthetic stores retain the existing per-object JS queue scope.
    // The native iOS adapter always exposes the stronger operation and never
    // falls back to unconditional remove if an older plugin rejects it.
    if(raw!==null)await store.remove(APP_SESSION_VAULT_KEY);
    return true;
  }
  return {
    load:()=>ordered(async()=>{
      const raw = await store.get(APP_SESSION_VAULT_KEY);
      if (raw === null) return null;
      let parsed: unknown;
      try {
        parsed = JSON.parse(raw);
      } catch {
        await removeOriginal(raw);
        return null;
      }
      const credential = validate(parsed, now());
      if (!credential) await removeOriginal(raw);
      return credential;
    }),
    save:value=>ordered(async()=>{
      const credential = validate(value, now());
      if (!credential) throw new Error("유효한 앱 세션만 보안 저장소에 보관할 수 있습니다.");
      await store.set(APP_SESSION_VAULT_KEY, JSON.stringify(credential));
    }),
    clear:()=>ordered(async()=>{
      await removeOriginal(await store.get(APP_SESSION_VAULT_KEY));
    }),
    clearIfCurrent:expectedToken=>ordered(async()=>{
      const raw=await store.get(APP_SESSION_VAULT_KEY);
      if(raw === null)return removeOriginal(null);
      let parsed:unknown;
      try{parsed=JSON.parse(raw);}catch{return false;}
      // Signed provider formats can retire their expired original slot;
      // native verification still precedes any SDK or Keychain mutation.
      const signedRetirement=Boolean(parsed && typeof parsed==="object" && !Array.isArray(parsed)
        && [GOOGLE_OWNER_SESSION_VAULT_VERSION,KAKAO_OWNER_SESSION_VAULT_VERSION].includes((parsed as Record<string,unknown>).contract_version as string));
      const current=validate(parsed,now(),signedRetirement);
      if(!current || current.session_token!==expectedToken)return false;
      return removeOriginal(raw);
    }),
  };
}

export function createBrowserTestStore(storage: Storage): SecureValueStore {
  return {
    async get(key) { return storage.getItem(key); },
    async set(key, value) { storage.setItem(key, value); },
    async remove(key) { storage.removeItem(key); },
  };
}
