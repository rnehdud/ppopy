import { createAppExternalLinkRouter } from "./appExternalLinks";

export const PUBLIC_APP_ORIGIN = "https://miraylab.com";

export const PUBLIC_APP_URLS = Object.freeze({
  serviceTerms: `${PUBLIC_APP_ORIGIN}/terms/`,
  privacyPolicy: `${PUBLIC_APP_ORIGIN}/privacy/`,
  support: `${PUBLIC_APP_ORIGIN}/support/`,
  accountDeletion: `${PUBLIC_APP_ORIGIN}/account-deletion/`,
  subscriptionTerms: `${PUBLIC_APP_ORIGIN}/subscription/`,
  manageAppleSubscription: "https://apps.apple.com/account/subscriptions",
});

/**
 * 공개 페이지의 실제 HTTPS 검증과 owner publication review 뒤에만 runtime에 주입한다.
 * 이 factory를 만든 것만으로 링크·public app·결제를 활성화하지 않는다.
 */
export function createProductionAppExternalLinkRouter() {
  return createAppExternalLinkRouter({
    firstPartyOrigins: [PUBLIC_APP_ORIGIN],
    links: [
      {purpose: "service_terms", ownership: "first_party", url: PUBLIC_APP_URLS.serviceTerms},
      {purpose: "privacy_policy", ownership: "first_party", url: PUBLIC_APP_URLS.privacyPolicy},
      {purpose: "support", ownership: "first_party", url: PUBLIC_APP_URLS.support},
      {purpose: "account_deletion", ownership: "first_party", url: PUBLIC_APP_URLS.accountDeletion},
      {purpose: "subscription_terms", ownership: "first_party", url: PUBLIC_APP_URLS.subscriptionTerms},
      {purpose: "manage_subscription", ownership: "apple_store", url: PUBLIC_APP_URLS.manageAppleSubscription},
    ],
  });
}
