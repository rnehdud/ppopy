export type AppExternalLinkPurpose =
  | "service_terms"
  | "privacy_policy"
  | "support"
  | "account_deletion"
  | "subscription_terms"
  | "manage_subscription";

export type AppExternalLink = {
  purpose: AppExternalLinkPurpose;
  ownership: "first_party" | "apple_store" | "google_play";
  url: string;
};

export interface AppExternalLinkOpener {
  openExternal(url: string): Promise<void>;
}

export type AppExternalLinkResult =
  | { state: "opened" }
  | { state: "not_configured" }
  | { state: "open_failed" };

function validateLink(link: AppExternalLink, firstPartyOrigins: ReadonlySet<string>): AppExternalLink {
  let parsed: URL;
  try { parsed = new URL(link.url); }
  catch { throw new Error(`외부 링크 ${link.purpose} URL 형식이 올바르지 않습니다.`); }
  if (parsed.protocol !== "https:" || parsed.username || parsed.password || parsed.hash) {
    throw new Error(`외부 링크 ${link.purpose}는 HTTPS이며 자격정보와 fragment가 없어야 합니다.`);
  }

  if (link.ownership === "first_party") {
    if (!firstPartyOrigins.has(parsed.origin)) throw new Error(`외부 링크 ${link.purpose} origin이 허용되지 않았습니다.`);
    return {...link, url: parsed.href};
  }
  if (link.purpose !== "manage_subscription") {
    throw new Error("스토어 링크는 구독 관리 목적으로만 사용할 수 있습니다.");
  }
  if (link.ownership === "apple_store") {
    if (parsed.origin !== "https://apps.apple.com" || parsed.pathname !== "/account/subscriptions" || parsed.search) {
      throw new Error("Apple 구독 관리 링크가 정확한 시스템 경로가 아닙니다.");
    }
  }
  if (link.ownership === "google_play") {
    if (parsed.origin !== "https://play.google.com" || parsed.pathname !== "/store/account/subscriptions") {
      throw new Error("Google Play 구독 관리 링크가 정확한 시스템 경로가 아닙니다.");
    }
    const allowedQueryKeys = new Set(["package", "sku"]);
    for (const key of parsed.searchParams.keys()) {
      if (!allowedQueryKeys.has(key)) throw new Error("Google Play 구독 관리 링크에 허용되지 않은 query가 있습니다.");
    }
  }
  return {...link, url: parsed.href};
}

export function createAppExternalLinkRouter({
  firstPartyOrigins,
  links,
}: {
  firstPartyOrigins: readonly string[];
  links: readonly AppExternalLink[];
}) {
  const origins = new Set(firstPartyOrigins.map(value => {
    const parsed = new URL(value);
    if (parsed.protocol !== "https:" || parsed.href !== `${parsed.origin}/`) throw new Error("first-party allowlist는 HTTPS origin만 허용합니다.");
    return parsed.origin;
  }));
  const byPurpose = new Map<AppExternalLinkPurpose, AppExternalLink>();
  for (const candidate of links) {
    if (byPurpose.has(candidate.purpose)) throw new Error(`외부 링크 목적 ${candidate.purpose}가 중복됐습니다.`);
    byPurpose.set(candidate.purpose, validateLink(candidate, origins));
  }

  return {
    configured(purpose: AppExternalLinkPurpose) { return byPurpose.has(purpose); },
    async open(purpose: AppExternalLinkPurpose, opener: AppExternalLinkOpener): Promise<AppExternalLinkResult> {
      const link = byPurpose.get(purpose);
      if (!link) return {state:"not_configured"};
      try {
        await opener.openExternal(link.url);
        return {state:"opened"};
      } catch {
        return {state:"open_failed"};
      }
    },
  };
}

export type AppExternalLinkRouter = ReturnType<typeof createAppExternalLinkRouter>;
