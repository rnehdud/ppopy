import config from "../../skin_engine/config/miray_closed_loop_admission.json";
import {assertLoopEntryReviewOnly} from "./mirayClosedLoopEntry";

/** No HTTP adapter, operation issuer or runtime activation. */
export function assertOriginalEntryResumeReviewOnly(entryRef:string){
  assertLoopEntryReviewOnly();
  if(!/^sha256:[0-9a-f]{64}$/.test(entryRef) || config.enabled!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false || config.persistent_queue_enabled!==false)throw new Error("Unapproved original entry recovery");
}
