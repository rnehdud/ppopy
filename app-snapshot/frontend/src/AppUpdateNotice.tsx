import type { AppCompatibilityState } from "./appClientCompatibility";

export default function AppUpdateNotice({
  state,
  onUpdate,
  onRetry,
}: {
  state: AppCompatibilityState;
  onUpdate?: () => void;
  onRetry?: () => void;
}) {
  if (state === "supported") return null;
  if (state === "update_available") return <section className="app-update-notice" role="status">
    <strong>새 앱 버전을 사용할 수 있어요</strong>
    <p>현재 작업을 마친 뒤 업데이트할 수 있습니다.</p>
    {onUpdate && <button type="button" onClick={onUpdate}>업데이트 열기</button>}
  </section>;
  if (state === "update_required") return <section className="app-update-notice app-update-required" role="alert">
    <strong>계속하려면 앱 업데이트가 필요해요</strong>
    <p>새 입력과 구매는 잠시 멈춥니다. 제품 정보 확인, 로그아웃, 데이터 삭제, 고객지원과 구독 관리는 계속 이용할 수 있어요.</p>
    {onUpdate && <button type="button" onClick={onUpdate}>업데이트 열기</button>}
  </section>;
  return <section className="app-update-notice app-update-required" role="alert">
    <strong>앱 사용 가능 상태를 확인할 수 없어요</strong>
    <p>새 입력과 구매는 잠시 멈춥니다. 데이터 삭제, 고객지원과 구독 관리는 계속 이용할 수 있어요.</p>
    {onRetry && <button type="button" onClick={onRetry}>상태 다시 확인</button>}
  </section>;
}
