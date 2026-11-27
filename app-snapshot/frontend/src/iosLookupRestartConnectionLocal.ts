import {createReviewIOSLookupRestartPorts,type IOSLookupRestartBridge} from "./iosLookupRestartPortsLocal";
import {createReviewLookupRestartConnection} from "./appLookupRestartConnectionLocal";
type Options=Parameters<typeof createReviewIOSLookupRestartPorts>[1]&{onSessionChanged?:()=>void};

/** Unregistered factory candidate. No Capacitor registerPlugin, native URLSession,
 * Keychain key creation/provisioning, native project edit or default shell import. */
export function createReviewIOSLookupRestartConnection(fetcher:typeof fetch,bridge:IOSLookupRestartBridge,options:Options){
  const ports=createReviewIOSLookupRestartPorts(bridge,options);
  const connection=createReviewLookupRestartConnection(fetcher,{...options,store:ports.store,mac:ports.mac});
  return {...connection,async dispose(){ports.dispose();await connection.dispose();}};
}
