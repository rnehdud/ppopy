import {useEffect, useRef, useState} from "react";
import {productPhotoAccessStore} from "./productPhotoAccessStore";
export default function ProductPhotoTestSettings() {
  const input = useRef<HTMLInputElement>(null);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);
  const [stored, setStored] = useState<boolean | null | undefined>(undefined);
  useEffect(() => {
    let active = true;
    productPhotoAccessStore.isStored().then(value => { if (active) setStored(value); }).catch(() => {
      if (active) { setStored(null); setMessage("기기 저장 여부를 확인하지 못했습니다. 앱을 다시 열어 주세요."); }
    });
    return () => { active = false; };
  }, []);
  return <details className="photo-test-settings">
    <summary>비공개 TEST 연결 설정 <span className="photo-test-storage-status">{stored === true ? "코드 저장됨" : stored === false ? "코드 없음" : stored === undefined ? "저장 확인 중" : "저장 미확인"}</span></summary>
    <p>사진 검색 전용 연결 코드를 입력하세요. OpenAI API key는 앱에 저장하지 않습니다.</p>
    {message && <p role="status" aria-live="polite">{message}</p>}
    <form onSubmit={async event => {
      event.preventDefault(); setBusy(true); setMessage("");
      try {
        await productPhotoAccessStore.set((input.current?.value ?? "").trim());
        if (!await productPhotoAccessStore.isStored()) throw new Error("missing_saved_code");
        setStored(true); input.current?.blur();
        setMessage("저장 완료. 이 기기에 연결 코드가 저장된 것을 확인했습니다. 사진 검색으로 서버 연결을 확인해 주세요.");
      } catch {
        setMessage("저장을 확인하지 못했습니다. 사진 검색 전용 연결 코드를 확인한 뒤 다시 저장해 주세요.");
      } finally { if (input.current) input.current.value = ""; setBusy(false); }
    }}>
      <label htmlFor="photo-test-access">사진 TEST 연결 코드</label>
      <input ref={input} id="photo-test-access" type="password" autoComplete="off" autoCapitalize="none" spellCheck={false} maxLength={128} disabled={busy} required />
      <button className="app-secondary" type="submit" disabled={busy}>{busy ? "처리 중…" : "기기에 저장"}</button>
      <button className="app-inline-action" type="button" disabled={busy} onClick={async () => {
        setBusy(true);
        try { await productPhotoAccessStore.remove(); setStored(false); setMessage("사진 TEST 연결 코드를 삭제했습니다."); }
        catch { setMessage("연결 코드 삭제를 완료하지 못했습니다."); }
        finally { setBusy(false); }
      }}>연결 코드 삭제</button>
    </form>
  </details>;
}
