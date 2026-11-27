import config from "../../skin_engine/config/miray_closed_loop_entry_selector.json";
import {assertLoopEntryReviewOnly} from "./mirayClosedLoopEntry";

export function assertAccountEntrySelectorReviewOnly(entryRef:string){
  assertLoopEntryReviewOnly();
  if(!/^sha256:[0-9a-f]{64}$/.test(entryRef) || config.enabled!==false || config.deployment_context!=="synthetic_test" || config.automatic_retry!==false || config.automatic_poll!==false || config.persistent_selection_enabled!==false || config.fresh_entry_requires_explicit_request!==true)throw new Error("Unapproved account entry selection");
}
