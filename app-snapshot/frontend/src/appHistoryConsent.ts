import config from "../../skin_engine/config/app_history_consent.json";
import {assertCurrentMemberResponseSession,createBoundMemberResponseSessionLoader} from "./appMemberResponseSession";
import {memberStatusReadScope,type MemberStatusReadOptions} from "./memberStatusReadScope";

export type AppHistoryConsentStatus = {
  state: "not_consented" | "consented" | "review_required";
  notice_version: string;
  revision: string;
};
export type AppHistoryConsentChoice = "grant" | "withdraw";
export type AppHistoryConsentStore = {
  read(options?: MemberStatusReadOptions): Promise<AppHistoryConsentStatus>;
  choose(choice: AppHistoryConsentChoice, expected: AppHistoryConsentStatus, options?: MemberStatusReadOptions): Promise<AppHistoryConsentStatus>;
};

export function parseAppHistoryConsentStatus(value: unknown): AppHistoryConsentStatus {
  if (!value || typeof value!=="object" || Array.isArray(value)) throw new Error("이력 저장 동의를 다시 확인해 주세요.");
  const status=value as Record<string,unknown>;
  if (Object.keys(status).length!==3 || !config.states.includes(String(status.state))
      || status.notice_version!==config.notice.version || typeof status.revision!=="string"
      || !/^[0-9a-f]{64}$/.test(status.revision)) throw new Error("이력 저장 동의를 다시 확인해 주세요.");
  return {...status} as AppHistoryConsentStatus;
}

/** No URL defaults: reviewed composition must opt in to an exact HTTPS origin. */
export function createHttpAppHistoryConsentStore(fetcher: typeof fetch, options: {
  baseUrl: string; allowedBaseUrls: readonly string[];
  loadSessionToken: () => Promise<string | null>; onSessionChanged?: () => void;
}): AppHistoryConsentStore {
  const normalize=(value:string)=>{
    const url=new URL(value);
    if(url.protocol!=="https:" || url.username || url.password || url.search || url.hash) throw new Error("앱 API 주소를 확인해 주세요.");
    return `${url.origin}${url.pathname.replace(/\/+$/,"")}`;
  };
  const base=normalize(options.baseUrl);
  if(!options.allowedBaseUrls.map(normalize).includes(base)) throw new Error("앱 API 주소가 허용 목록에 없습니다.");
  const load=createBoundMemberResponseSessionLoader(options.loadSessionToken,options.onSessionChanged);
  const request=async (body?: string, consumer?: MemberStatusReadOptions)=>{
    const scope=memberStatusReadScope(load,consumer),member=scope.load;
    const token=await scope.wait(member);
    if(!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) throw new Error("로그인 상태를 다시 확인해 주세요.");
    const response=await scope.wait(()=>scope.fetch(fetcher)(`${base}${config.http.path}`,{
      method:body?config.http.choice_method:config.http.read_method,
      cache:"no-store",credentials:"omit",redirect:"error",signal:consumer?.signal,
      headers:{Authorization:`Bearer ${token}`,...(body?{"Content-Type":"application/json"}:{})},
      ...(body?{body}:{}),
    }));
    await scope.wait(()=>assertCurrentMemberResponseSession(member,token,options.onSessionChanged));
    let payload: unknown=null;
    try{payload=await scope.wait(()=>response.json());}catch{scope.gate();/* generic failure below */}
    await scope.wait(()=>assertCurrentMemberResponseSession(member,token,options.onSessionChanged));
    if(!response.ok) throw new Error(response.status===409?"동의 상태가 바뀌었어요. 다시 확인한 뒤 선택해 주세요.":"이력 저장 동의를 확인하지 못했어요.");
    return parseAppHistoryConsentStatus(payload);
  };
  return {
    read:options=>request(undefined,options),
    choose:(choice,expected,options)=>{
      if(choice!=="grant" && choice!=="withdraw") throw new Error("동의 선택을 확인해 주세요.");
      const status=parseAppHistoryConsentStatus(expected);
      if(choice==="grant" && status.state!=="not_consented") throw new Error("동의 상태를 먼저 확인해 주세요.");
      const body=JSON.stringify({choice,notice_version:status.notice_version,revision:status.revision});
      if(new TextEncoder().encode(body).byteLength>config.http.max_request_bytes) throw new Error("동의 선택을 확인해 주세요.");
      return request(body,options);
    },
  };
}
