import type {NativeAccountClosureSnapshot} from "./nativeRecoveryMemberWorkspaceLocal";
import releaseScope from "../../skin_engine/config/app_release_scope.json";
/** OFF receipt metadata only. Pending CAS does not prove cleanup, physical
 * history deletion, OS logout or subscription cancellation. No action/retry. */
export default function NativeAccountClosureReview({closure}:{closure:NativeAccountClosureSnapshot}){
  if(closure.state!=="accepted")return null;
  return <main className="miray-main"><h1>탈퇴 요청을 접수했어요</h1>
    <p>회원 계정은 종료됐어요.{releaseScope.paid_subscription_enabled && " 구독은 별도로 관리해 주세요."}</p>
    {closure.history_deletion_scheduled&&<p>이력 삭제가 예약됐어요. 삭제 완료를 뜻하지는 않아요.</p>}
    {closure.local_cleanup==="pending"&&<p role="status">이 기기의 로그인 정보를 정리하고 있어요.</p>}
    {closure.local_cleanup==="cleared"&&<p role="status">이 기기의 로그인 정보를 정리했어요.</p>}
    {closure.local_cleanup==="required"&&<p role="alert">탈퇴는 접수됐지만 이 기기의 로그인 정보 정리를 확인하지 못했어요.</p>}
    {closure.local_cleanup==="session_changed"&&<p role="status">이 기기의 계정 연결이 바뀌어 현재 로그인 정보는 유지했어요.</p>}
  </main>;
}
