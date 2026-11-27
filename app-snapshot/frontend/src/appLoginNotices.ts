import disclosure from "../../skin_engine/config/app_public_disclosure.json";
import privacy from "../../skin_engine/config/beta_privacy.json";

export type AppLoginNotice = {version:string; title:string; summary:string; url:string};
export type AppLoginNotices = {
  service_terms: AppLoginNotice;
  general_personal_information: AppLoginNotice;
  sensitive_information: AppLoginNotice;
  history_storage?: AppLoginNotice;
};
type PublicConfig = {
  publication_status:string;
  first_party_origin:string;
  public_urls:{service_terms:string | null; privacy_policy:string | null};
  required_notice_versions:{service_terms:string; general_personal_information:string; sensitive_information:string;history_storage?:string};
};
type PrivacyConfig = {
  notices:{service_terms:{version:string}; general_personal_information:{version:string}; sensitive_information:{version:string};history_storage?:{version:string}};
  public_copy:{service_terms:{title:string;summary:string}; general_personal_information:{title:string;summary:string}; sensitive_information:{title:string;summary:string};history_storage?:{title:string;summary:string}};
};

function fullTextUrl(value: unknown, origin: string): string | null {
  if (typeof value !== "string") return null;
  try {
    const url = new URL(value);
    if (url.protocol !== "https:" || url.origin !== origin || url.pathname === "/"
      || url.username || url.password || url.search || url.hash) return null;
    return url.href;
  } catch { return null; }
}

export function buildAppLoginNotices(
  publicConfig: PublicConfig,
  privacyConfig: PrivacyConfig,
): AppLoginNotices | null {
  if (publicConfig.publication_status !== "FINAL") return null;
  const origin = publicConfig.first_party_origin;
  if (typeof origin !== "string" || !/^https:\/\/[^/]+$/.test(origin)) return null;
  const termsUrl = fullTextUrl(publicConfig.public_urls.service_terms, origin);
  const privacyUrl = fullTextUrl(publicConfig.public_urls.privacy_policy, origin);
  const terms = privacyConfig.public_copy.service_terms;
  const general = privacyConfig.public_copy.general_personal_information;
  const sensitive = privacyConfig.public_copy.sensitive_information;
  if (!termsUrl || !privacyUrl
    || publicConfig.required_notice_versions.service_terms !== privacyConfig.notices.service_terms.version
    || publicConfig.required_notice_versions.general_personal_information !== privacyConfig.notices.general_personal_information.version
    || publicConfig.required_notice_versions.sensitive_information !== privacyConfig.notices.sensitive_information.version
    || !terms.title || !general.title || !sensitive.title || !terms.summary || !general.summary || !sensitive.summary) return null;
  const historyVersion=privacyConfig.notices.history_storage?.version;
  const historyCopy=privacyConfig.public_copy.history_storage;
  if ((historyVersion || historyCopy || publicConfig.required_notice_versions.history_storage)
    && (!historyVersion || !historyCopy?.title || !historyCopy.summary
      || publicConfig.required_notice_versions.history_storage!==historyVersion)) return null;
  return {
    ...(historyVersion && historyCopy ? {history_storage:{version:historyVersion,title:historyCopy.title,summary:historyCopy.summary,url:privacyUrl}} : {}),
    service_terms:{version:privacyConfig.notices.service_terms.version,title:terms.title,summary:terms.summary,url:termsUrl},
    general_personal_information:{version:privacyConfig.notices.general_personal_information.version,title:general.title,summary:general.summary,url:privacyUrl},
    sensitive_information:{version:privacyConfig.notices.sensitive_information.version,title:sensitive.title,summary:sensitive.summary,url:privacyUrl},
  };
}

export const appLoginNotices = buildAppLoginNotices(disclosure, privacy);
