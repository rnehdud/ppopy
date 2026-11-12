import { ChangeEvent, useEffect, useState } from "react";

import { isProductPhotoWebPreviewable, prepareProductPhoto, validateProductPhotoFile } from "./productPhoto";
import type {ProductPhotoIdentity} from "./testProductPhotoTransport";
type Props = {
  onProductIdentity?: (identity: ProductPhotoIdentity) => Promise<void>;
  onPhotoSelected?: (file: File) => Promise<void>;
  onCaptureStart?: () => () => boolean;
  onAnnouncement: (message: string) => void;
  extractText?: (photo: Blob) => Promise<string[]>;
  onRecognizedLines?: (lines: string[]) => Promise<number>;
};

export default function ProductPhotoInput({ onAnnouncement, extractText, onRecognizedLines, onCaptureStart, onPhotoSelected }: Props) {
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [message, setMessage] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => () => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  const handlePhoto = async (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;
    setMessage("");
    let isCurrentCapture = () => true;
    try {
      const validationError = validateProductPhotoFile(file);
      if (validationError) throw new Error(validationError);
      if (onPhotoSelected) {
        setBusy(true);
        await onPhotoSelected(file);
        setMessage("사진을 준비했습니다. 제품 영역을 확인해 주세요.");
        onAnnouncement("사진을 준비했습니다. 제품 영역을 확인해 주세요.");
        return;
      }
      let next = "사진을 준비했습니다.";
      if (extractText) {
        setBusy(true);
        isCurrentCapture = onCaptureStart?.() ?? (() => true);
        // iPhone HEIC는 WebView/canvas가 읽지 못할 수 있다. 원본을 먼저
        // native Vision에 넘기고, 미리보기 변환 실패가 OCR을 막지 않게 한다.
        const lines = await extractText(file);
        if (!isCurrentCapture()) throw new DOMException("Capture superseded", "AbortError");
        if (!lines.length) throw new Error("제품명을 읽지 못했습니다. 검색창에 직접 입력해 주세요.");
        // The candidate matcher owns cancellation once it starts a new search generation.
        isCurrentCapture = () => true;
        const candidateCount = onRecognizedLines ? await onRecognizedLines(lines) : 0;
        next = candidateCount
          ? `사진에서 카탈로그 후보 ${candidateCount}개를 찾았습니다. 아래에서 제품명과 용량을 확인해 주세요.`
          : "사진에서 확인된 카탈로그 후보가 없습니다. 제품명을 직접 검색해 주세요.";
      }
      if (isProductPhotoWebPreviewable(file)) {
        try {
          const prepared = await prepareProductPhoto(file, false);
          if (previewUrl) URL.revokeObjectURL(previewUrl);
          setPreviewUrl(prepared.previewUrl);
        } catch {
          // native OCR 성공 여부와 장식용 WebView 미리보기 성공 여부를 분리한다.
          if (!extractText) throw new Error("사진을 읽지 못했습니다.");
        }
      } else if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
        setPreviewUrl(null);
      }
      setMessage(next);
      onAnnouncement(next);
    } catch (error) {
      if (!isCurrentCapture() || (error instanceof DOMException && error.name === "AbortError")) {
        setMessage("");
        return;
      }
      const next = error instanceof Error ? error.message : "사진을 처리하지 못했습니다.";
      setMessage(next);
      onAnnouncement(next);
    } finally {
      setBusy(false);
      event.target.value = "";
    }
  };

  return (
    <div className="product-camera">
      <label className="photo-button" htmlFor="product-photo">
        <svg aria-hidden="true" viewBox="0 0 24 24"><path d="M8.4 5.5 9.7 3.8h4.6l1.3 1.7H19a2 2 0 0 1 2 2v10.2a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V7.5a2 2 0 0 1 2-2h3.4ZM12 16.8a4.1 4.1 0 1 0 0-8.2 4.1 4.1 0 0 0 0 8.2Zm0-2a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2Z"/></svg>{busy ? "사진 처리 중" : "제품 촬영"}
      </label>
      <input
        className="sr-only"
        id="product-photo"
        aria-label="제품 촬영"
        type="file"
        accept="image/jpeg,image/png,image/webp,image/heic,image/heif"
        capture="environment"
        disabled={busy}
        onChange={handlePhoto}
      />
      <label className="photo-button" htmlFor="product-photo-library">사진 선택</label>
      <input className="sr-only" id="product-photo-library" aria-label="사진 선택" type="file"
        accept="image/jpeg,image/png,image/webp,image/heic,image/heif" disabled={busy} onChange={handlePhoto} />
      <small>{onPhotoSelected ? "제품 영역과 전송 안내를 확인한 뒤 제품명 후보를 찾습니다. 선택만으로는 전송하지 않아요." : "촬영한 사진이나 제품 캡처를 선택할 수 있어요. 사진은 기기에서만 글자를 읽고 저장하지 않아요."}</small>
      {message && <p role="status">{message}</p>}
      {previewUrl && <div className="product-photo-chip"><img src={previewUrl} alt="선택한 제품 사진 미리보기" /><button type="button" onClick={() => { setPreviewUrl(null); setMessage(""); }}>지우기</button></div>}
    </div>
  );
}
