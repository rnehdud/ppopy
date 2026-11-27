import {useEffect, useRef, useState} from "react";
import rules from "../../skin_engine/config/product_photo_client.json";
import type {PreparedProductPhoto} from "./productPhoto";
import {cropPhotoForTransmission, defaultPhotoCrop, type PhotoCrop} from "./productPhotoPreparation";
import {adjustPhotoCrop, type CropGesture} from "./productPhotoCropGesture";
import {ProductPhotoSearchError} from "./productPhotoErrors";
import type {ProductPhotoIdentity} from "./testProductPhotoTransport";

type Props = {
  photo: PreparedProductPhoto;
  search: (photo: Blob, confirmed: boolean, signal?: AbortSignal) => Promise<ProductPhotoIdentity>;
  onIdentity: (identity: ProductPhotoIdentity) => Promise<void>;
  onCancel: () => void;
  isCurrent?: () => boolean;
};
export default function ProductPhotoReview({photo, search, onIdentity, onCancel, isCurrent = () => true}: Props) {
  const [crop, setCrop] = useState<PhotoCrop>(defaultPhotoCrop);

  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const imageStage = useRef<HTMLDivElement>(null);
  const gesture = useRef<{id: number; mode: CropGesture; crop: PhotoCrop; x: number; y: number; width: number; height: number} | null>(null);
  const startGesture = (event: React.PointerEvent<HTMLElement>, mode: CropGesture) => {
    if (busy || gesture.current || !event.isPrimary || event.button !== 0) return;
    const rect = imageStage.current?.getBoundingClientRect();
    if (!rect || rect.width <= 0 || rect.height <= 0) return;
    event.preventDefault(); event.stopPropagation();
    event.currentTarget.setPointerCapture(event.pointerId);
    gesture.current = {id: event.pointerId, mode, crop, x: event.clientX, y: event.clientY, width: rect.width, height: rect.height};
  };
  const moveGesture = (event: React.PointerEvent<HTMLElement>) => {
    const value = gesture.current;
    if (busy || !value || value.id !== event.pointerId) return;
    event.preventDefault(); event.stopPropagation();
    setCrop(adjustPhotoCrop(value.crop, value.mode, (event.clientX - value.x) / value.width * 100, (event.clientY - value.y) / value.height * 100));
  };
  const endGesture = (event: React.PointerEvent<HTMLElement>) => {
    if (gesture.current?.id === event.pointerId) gesture.current = null;
  };
  const keyboardAdjust = (event: React.KeyboardEvent<HTMLElement>, mode: CropGesture) => {
    const delta: Record<string, [number, number]> = {ArrowLeft: [-1, 0], ArrowRight: [1, 0], ArrowUp: [0, -1], ArrowDown: [0, 1]};
    if (busy || !delta[event.key]) return;
    event.preventDefault(); event.stopPropagation();
    const [dx, dy] = delta[event.key]; setCrop(current => adjustPhotoCrop(current, mode, dx, dy));
  };
  const panel = useRef<HTMLDivElement>(null);
  const request = useRef<AbortController | null>(null);
  const active = useRef(true);
  useEffect(() => {
    active.current = true;
    const previous = document.activeElement as HTMLElement | null;
    const overflow = document.body.style.overflow; document.body.style.overflow = "hidden";
    panel.current?.focus();
    return () => { active.current = false; request.current?.abort(); document.body.style.overflow = overflow; previous?.focus(); };
  }, []);
  const cancel = () => { active.current = false; request.current?.abort(); onCancel(); };
  const send = async () => {
    if (busy || gesture.current) return;
    if (!isCurrent()) { cancel(); return; }
    setBusy(true); setMessage("");
    const controller = new AbortController(); request.current = controller;
    let prepared: PreparedProductPhoto | null = null;
    let stage: "preparing" | "identifying" | "matching" = "preparing";
    try {
      // The versioned disclosure and affirmative send button form one optional consent action.
      // Selection, opening the sheet, or region changes alone never dispatch a request.
      prepared = await cropPhotoForTransmission(photo, crop);
      if (!active.current || !isCurrent() || controller.signal.aborted) { if (active.current) cancel(); return; }
      stage = "identifying";
      const identity = await search(prepared.blob, true, controller.signal);
      if (!active.current || !isCurrent() || controller.signal.aborted) { if (active.current) cancel(); return; }
      if (!identity.brand || !identity.product_name) {
        setMessage("제품명을 확인하지 못했어요. 다른 사진을 선택하거나 제품명으로 검색해 주세요.");
        return;
      }
      stage = "matching";
      await onIdentity(identity);
      if (active.current) cancel();
    } catch (error) {
      if (active.current && isCurrent() && !controller.signal.aborted) setMessage(stage === "preparing"
        ? "제품 영역을 준비하지 못했어요. 영역을 조정하거나 다른 사진을 선택해 주세요."
        : stage === "identifying"
        ? error instanceof ProductPhotoSearchError ? error.message : "사진 검색을 완료하지 못했어요. 잠시 후 다시 시도하거나 제품명으로 검색해 주세요."
        : "사진에서 제품명을 읽었지만 제품 조회에 실패했어요. 제품명으로 다시 검색해 주세요.");
    } finally {
      if (prepared) URL.revokeObjectURL(prepared.previewUrl);
      if (active.current) setBusy(false);
    }
  };
  const controls: Array<[keyof PhotoCrop, string]> = [["x", "가로 위치"], ["y", "세로 위치"], ["width", "영역 너비"], ["height", "영역 높이"]];
  const update = (key: keyof PhotoCrop, value: number) => setCrop(current => {
    const next = {...current, [key]: value};
    next.x = Math.min(next.x, 100 - next.width); next.y = Math.min(next.y, 100 - next.height);
    return next;
  });
  return <div className="photo-review-backdrop"><div className="photo-review-panel" role="dialog" aria-modal="true" aria-labelledby="photo-review-title" tabIndex={-1} ref={panel} onKeyDown={event => {
    if (event.key === "Escape") { event.preventDefault(); cancel(); }
    if (event.key === "Tab") {
      const elements = Array.from(panel.current?.querySelectorAll<HTMLElement>('button:not(:disabled),input:not(:disabled),summary,[role="button"][tabindex="0"]') ?? []).filter(value => value.getClientRects().length > 0);
      const first = elements[0], last = elements[elements.length - 1];
      if (!first) { event.preventDefault(); return; }
      if (event.shiftKey && (document.activeElement === first || document.activeElement === panel.current)) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && (document.activeElement === last || document.activeElement === panel.current)) { event.preventDefault(); first.focus(); }
    }
  }}>
    <div className="photo-review-heading"><h2 id="photo-review-title">이 사진으로 제품을 찾을까요?</h2><button type="button" aria-label="사진 확인 닫기" onClick={cancel}>닫기</button></div>
    <div className="photo-review-body">
    <p>제품명과 용량이 보이는지 확인해 주세요.</p>
    <div className="photo-review-stage" ref={imageStage}>
      <img src={photo.previewUrl} draggable={false} alt="보낼 영역을 확인하는 제품 사진" />
      <div role="button" tabIndex={busy ? -1 : 0} aria-label="제품 영역 이동" aria-disabled={busy} className="photo-crop-frame"
        style={{left: `${crop.x}%`, top: `${crop.y}%`, width: `${crop.width}%`, height: `${crop.height}%`}}
        onPointerDown={event => startGesture(event, "move")} onPointerMove={moveGesture} onPointerUp={endGesture} onPointerCancel={endGesture} onLostPointerCapture={endGesture}
        onKeyDown={event => keyboardAdjust(event, "move")}>
        {([["nw", "왼쪽 위"], ["ne", "오른쪽 위"], ["sw", "왼쪽 아래"], ["se", "오른쪽 아래"]] as const).map(([mode, label]) =>
          <button key={mode} type="button" disabled={busy} className={`photo-crop-handle photo-crop-${mode}`} aria-label={`${label} 모서리 조정`}
            onPointerDown={event => startGesture(event, mode)} onPointerMove={moveGesture} onPointerUp={endGesture} onPointerCancel={endGesture} onLostPointerCapture={endGesture}
            onKeyDown={event => keyboardAdjust(event, mode)} />)}
      </div>
    </div>
    <p className="photo-crop-hint">영역 안을 끌어 이동하고, 모서리를 끌어 크기를 조정하세요.</p>
    <details className="photo-crop-controls"><summary>필요하면 영역 조정</summary><p>제품 글자를 남기고 얼굴·연락처는 제외해 주세요.</p>{controls.map(([key, label]) => <label key={key}>{label}<input aria-label={label} type="range" min={key === "width" || key === "height" ? 1 : 0} max={key === "x" ? 100 - crop.width : key === "y" ? 100 - crop.height : 100} value={crop[key]} disabled={busy} onChange={event => update(key, Number(event.target.value))} /></label>)}</details>
    <details className="photo-transfer-details"><summary>사진 처리 안내</summary><p>{rules.disclosure}</p></details>
    {message && <p role="status">{message}</p>}
    </div>
    <div className="photo-review-actions"><p className="photo-transfer-note">{rules.disclosure_summary}</p><button className="app-primary" type="button" disabled={busy} onClick={() => void send()}>{busy ? "제품 찾는 중" : rules.overseas_transfer_consent.affirmative_button_label}</button></div>

  </div></div>;
}
