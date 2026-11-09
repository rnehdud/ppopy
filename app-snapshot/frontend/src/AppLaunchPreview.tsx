import AppLaunchShell from "./AppLaunchShell";
import {careApiClient} from "./careApi";

export default function AppLaunchPreview() {
  // This is the deliberately marked local owner preview. Member composition
  // receives no fixture product or analysis client by default.
  return <AppLaunchShell allowOwnerTestSession memberCareClient={careApiClient} newNavigationEnabled={import.meta.env.VITE_MIRAY_NAV_PREVIEW === "true"} />;
}
