import AppAuthTest from "./AppAuthTest";
import appleLoginHandoff from "../../skin_engine/config/app_apple_login_handoff.json";
import googleLoginHandoff from "../../skin_engine/config/app_google_login_handoff.json";
import {kakaoOwnerHandoffSelected} from "./appKakaoLogin";
import releaseScope from "../../skin_engine/config/app_release_scope.json";
import {nativeReleaseCandidateHostAvailable} from "./nativeReleaseCandidateSelection";
import {useMemo} from "react";
import loopPolicy from "../../skin_engine/config/miray_closed_loop_native_test.json";
import {createOriginalLoopTestFactory} from "./mirayOriginalLoopTest";
import {createNativeLoopTestFetcher} from "./mirayLoopTestTransport";

/** Candidate uses the existing fixed TEST backend until deployment review is complete. */
export default function AppNativeReleaseCandidate() {
  const available=nativeReleaseCandidateHostAvailable() && appleLoginHandoff.selected === true
      && googleLoginHandoff.selected === true && kakaoOwnerHandoffSelected()
      && releaseScope.paid_subscription_enabled === false;
  const original=useMemo(()=>available ? createOriginalLoopTestFactory({baseUrl:loopPolicy.origin,
    fetcher:createNativeLoopTestFetcher({bootstrapResumeEnabled:true})}) : undefined,[available]);
  if (!original) {
    return <main className="account-start-screen"><p role="status">앱을 준비하고 있어요.</p></main>;
  }
  return <AppAuthTest routineReview={{original}}/>;
}
