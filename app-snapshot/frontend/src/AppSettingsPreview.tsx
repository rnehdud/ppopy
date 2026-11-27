import AppSettingsScreen from "./AppSettingsScreen";
import { createAppExternalLinkRouter } from "./appExternalLinks";

const previewLinks = createAppExternalLinkRouter({
  firstPartyOrigins:["https://legal.skinanalysis.test", "https://support.skinanalysis.test"],
  links:[
    {purpose:"service_terms", ownership:"first_party", url:"https://legal.skinanalysis.test/terms"},
    {purpose:"privacy_policy", ownership:"first_party", url:"https://legal.skinanalysis.test/privacy"},
    {purpose:"support", ownership:"first_party", url:"https://support.skinanalysis.test/help"},
    {purpose:"account_deletion", ownership:"first_party", url:"https://support.skinanalysis.test/delete-account"},
    {purpose:"subscription_terms", ownership:"first_party", url:"https://legal.skinanalysis.test/subscription"},
    {purpose:"manage_subscription", ownership:"apple_store", url:"https://apps.apple.com/account/subscriptions"},
  ],
});

export default function AppSettingsPreview() {
  return <div className="app-settings-preview">
    <p className="app-preview-banner" role="status">LOCAL PREVIEW · 합성 구독 상태 · 외부 연결 없음</p>
    <AppSettingsScreen
      showPlanPreview
      subscription={{serverVerified:true, state:"ACTIVE"}}
      linkRouter={previewLinks}
      linkOpener={{openExternal:async () => undefined}}
      retrySubscription={() => undefined}
      logout={async () => ({state:"logged_out"})}
      withdrawAndDelete={async () => ({state:"signed_out"})}
    />
  </div>;
}
