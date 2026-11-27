import {createReviewIOSStoreKitCapacitorBridge,type IOSStoreKitReviewCapacitorPlugin} from "./iosStoreKitCapacitorBridgeLocal";
import {createReviewIOSStoreKitSessionConnection,type IOSStoreKitSessionReviewConnection} from "./iosStoreKitSessionConnectionLocal";

export type StoreKitSessionReviewFactory=(owner:{loadToken:()=>Promise<string|null>;isCurrent:()=>boolean})=>IOSStoreKitSessionReviewConnection;

/** Explicit local app composition. Neither construction nor registration reads
 * credentials or calls native bootstrap. No default plugin or server reader is
 * supplied; the original member lifetime belongs to AppLaunchShell. */
export function createReviewIOSStoreKitSessionFactory(plugin:IOSStoreKitReviewCapacitorPlugin,now:()=>number=Date.now):StoreKitSessionReviewFactory{
  const bridge=createReviewIOSStoreKitCapacitorBridge(plugin);
  return owner=>createReviewIOSStoreKitSessionConnection(bridge,{
    deploymentContext:"synthetic_test",loadToken:owner.loadToken,isCurrent:owner.isCurrent,now,
  });
}
