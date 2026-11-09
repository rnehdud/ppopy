import {useEffect, useRef, useState} from "react";
import ProductPhotoInput from "./ProductPhotoInput";
import ProductPhotoReview from "./ProductPhotoReview";
import ProductPhotoTestSettings from "./ProductPhotoTestSettings";
import type {PreparedProductPhoto} from "./productPhoto";
import {preparePhotoForReview} from "./productPhotoPreparation";
import {productPhotoClientEnabled} from "./testProductPhotoTransport";
import {prepareNativeOwnerProductSearch, searchNativeIOSProductPhoto} from "./iosProductPhotoSearch";

const search = searchNativeIOSProductPhoto;
export default function TestProductPhotoInput(props: React.ComponentProps<typeof ProductPhotoInput>) {
  const [photo, setPhoto] = useState<PreparedProductPhoto | null>(null);
  const currentCapture = useRef<() => boolean>(() => true);
  const active = useRef(true);
  useEffect(() => {
    active.current = true;
    return () => { active.current = false; };
  }, []);
  useEffect(() => () => { if (photo) URL.revokeObjectURL(photo.previewUrl); }, [photo]);
  // A repo config flag alone is insufficient to make a live endpoint or pair a credential.
  if (!productPhotoClientEnabled()) return <ProductPhotoInput {...props} />;
  return <><ProductPhotoTestSettings /><ProductPhotoInput {...props} onPhotoSelected={async file => {
    const capture = props.onCaptureStart?.() ?? (() => true);
    currentCapture.current = capture;
    const isCurrent = () => active.current && currentCapture.current === capture && capture();
    let prepared: PreparedProductPhoto;
    try { prepared = await preparePhotoForReview(file); }
    catch (error) {
      if (!isCurrent()) throw new DOMException("Capture superseded", "AbortError");
      throw error;
    }
    if (!isCurrent()) {
      URL.revokeObjectURL(prepared.previewUrl);
      throw new DOMException("Capture superseded", "AbortError");
    }
    setPhoto(prepared);
    // Wake the DB with no photo/query/provider call while the owner reviews it.
    void prepareNativeOwnerProductSearch();
  }} />{photo && <ProductPhotoReview photo={photo} search={search} isCurrent={() => currentCapture.current()} onCancel={() => setPhoto(null)} onIdentity={async identity => {
    if (!identity.brand || !identity.product_name) throw new Error("제품명을 읽지 못했습니다.");
    if (props.onProductIdentity) { await props.onProductIdentity(identity); return; }
    const count = await props.onRecognizedLines?.([identity.brand, identity.product_name, identity.variant ?? "", identity.volume ?? ""]) ?? 0;
    props.onAnnouncement(count ? `사진에서 카탈로그 후보 ${count}개를 찾았습니다. 제품명과 용량을 직접 확인해 주세요.` : "사진에서 확인된 카탈로그 후보가 없습니다. 제품명을 직접 검색해 주세요.");
  }} />}</>;
}
