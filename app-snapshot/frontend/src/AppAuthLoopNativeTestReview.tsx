import {useMemo} from "react";
import AppAuthTest from "./AppAuthTest";
import policy from "../../skin_engine/config/miray_closed_loop_native_test.json";
import {createOriginalLoopTestFactory} from "./mirayOriginalLoopTest";
import {createNativeLoopTestFetcher} from "./mirayLoopTestTransport";

/** Explicit TEST entry; the default main composition stays unchanged.
 * The original shell remains the sole owner of member and separate consent. */
export default function AppAuthLoopNativeTestReview(){
  const factory=useMemo(()=>{
    if(import.meta.env.VITE_APP_MODE!=="app_auth_test" || import.meta.env.VITE_APP_PORTFOLIO_TEST!=="true" ||
      import.meta.env.VITE_APP_SKIN_STATE_TEST!=="true" || import.meta.env.VITE_APP_HISTORY_CONSENT_TEST!=="true" ||
      import.meta.env.VITE_APP_LOOP_NATIVE_TEST_REVIEW!=="true")return undefined;
    return createOriginalLoopTestFactory({baseUrl:policy.origin,fetcher:createNativeLoopTestFetcher({
      bootstrapResumeEnabled:import.meta.env.VITE_APP_LOOP_BOOTSTRAP_RESUME_TEST==="true",
    })});
  },[]);
  return <AppAuthTest routineReview={factory?{original:factory}:undefined}/>;
}
