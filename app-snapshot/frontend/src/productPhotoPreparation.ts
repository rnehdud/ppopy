import {metadataFreeJpeg} from "./productPhotoJpeg";
import {Capacitor, registerPlugin} from "@capacitor/core";
import rules from "../../skin_engine/config/product_photo_client.json";
import {isProductPhotoWebPreviewable, prepareProductPhoto, validateProductPhotoFile, type PreparedProductPhoto} from "./productPhoto";

export type PhotoCrop = {x: number; y: number; width: number; height: number};
export const defaultPhotoCrop: PhotoCrop = {x: 10, y: 5, width: 80, height: 90};
type NativePreparation = {imageBase64: string; width: number; height: number};
const bridge = registerPlugin<{prepare(options: {imageBase64: string}): Promise<NativePreparation>}>("IOSProductTextRecognizer");

export async function photoBase64(blob: Blob): Promise<string> {
  if (typeof blob.arrayBuffer === "function") {
    const bytes = new Uint8Array(await blob.arrayBuffer());
    let binary = "";
    for (let index = 0; index < bytes.length; index += 0x8000) binary += String.fromCharCode(...bytes.subarray(index, index + 0x8000));
    return btoa(binary);
  }
  // FileReader works with iOS photo-provider Files as well as ordinary Blobs.
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      if (typeof reader.result !== "string" || !reader.result.includes(",")) { reject(new Error("사진 파일을 읽지 못했습니다. 사진을 다시 선택해 주세요.")); return; }
      resolve(reader.result.slice(reader.result.indexOf(",") + 1));
    };
    reader.onerror = reader.onabort = () => reject(new Error("사진 파일을 읽지 못했습니다. 사진을 다시 선택해 주세요."));
    reader.readAsDataURL(blob);
  });
}

export function checkedCrop(crop: PhotoCrop): PhotoCrop {
  if (Object.values(crop).some(value => !Number.isFinite(value)) || crop.x < 0 || crop.y < 0
    || crop.width < 1 || crop.height < 1 || crop.x + crop.width > 100 || crop.y + crop.height > 100) {
    throw new Error("제품 영역을 사진 안에서 선택해 주세요.");
  }
  return crop;
}

export async function preparePhotoForReview(file: File): Promise<PreparedProductPhoto> {
  const problem = validateProductPhotoFile(file);
  if (problem) throw new Error(problem);
  const nativeIOS = Capacitor.isNativePlatform() && Capacitor.getPlatform() === "ios";
  if (!nativeIOS) {
    if (isProductPhotoWebPreviewable(file)) return prepareProductPhoto(file);
    throw new Error("HEIC 사진은 iPhone 앱에서 선택하거나 JPG로 다시 선택해 주세요.");
  }
  // Do not trust the picker MIME/extension to choose a WebView decoder. ImageIO
  // detects the actual container, downsamples before decoding and applies orientation.
  let result: NativePreparation;
  try { result = await bridge.prepare({imageBase64: await photoBase64(file)}); }
  catch { throw new Error("사진 파일을 열지 못했습니다. 사진을 다시 선택하거나 제품을 다시 촬영해 주세요."); }
  if (!result || typeof result.imageBase64 !== "string" || result.imageBase64.length > 4 * Math.ceil(rules.maximum_image_bytes / 3)
    || !Number.isInteger(result.width) || !Number.isInteger(result.height) || result.width < 1 || result.height < 1
    || Math.max(result.width, result.height) > rules.maximum_image_edge) throw new Error("사진을 변환하지 못했습니다. JPG로 다시 선택해 주세요.");
  const binary = atob(result.imageBase64);
  const blob = new Blob([Uint8Array.from(binary, character => character.charCodeAt(0))], {type: "image/jpeg"});
  if (blob.size > rules.maximum_image_bytes) throw new Error("사진이 너무 큽니다. 제품 부분만 다시 선택해 주세요.");
  return {blob, width: result.width, height: result.height, previewUrl: URL.createObjectURL(blob)};
}

export async function cropPhotoForTransmission(photo: PreparedProductPhoto, rawCrop: PhotoCrop): Promise<PreparedProductPhoto> {
  const crop = checkedCrop(rawCrop);
  const image = await new Promise<HTMLImageElement>((resolve, reject) => {
    const value = new Image(); value.onload = () => resolve(value); value.onerror = () => reject(new Error("사진을 읽지 못했습니다.")); value.src = photo.previewUrl;
  });
  const sw = image.naturalWidth * crop.width / 100, sh = image.naturalHeight * crop.height / 100;
  const scale = Math.min(1, rules.maximum_image_edge / Math.max(sw, sh));
  const canvas = document.createElement("canvas");
  canvas.width = Math.max(1, Math.round(sw * scale)); canvas.height = Math.max(1, Math.round(sh * scale));
  const context = canvas.getContext("2d");
  if (!context) throw new Error("사진 영역을 처리하지 못했습니다.");
  context.fillStyle = "#fff"; context.fillRect(0, 0, canvas.width, canvas.height);
  context.drawImage(image, image.naturalWidth * crop.x / 100, image.naturalHeight * crop.y / 100, sw, sh, 0, 0, canvas.width, canvas.height);
  const encoded = await new Promise<Blob>((resolve, reject) => canvas.toBlob(value => value ? resolve(value) : reject(new Error("사진을 변환하지 못했습니다.")), "image/jpeg", 0.82));
  const blob = await metadataFreeJpeg(encoded);
  if (blob.size > rules.maximum_image_bytes) throw new Error("사진이 너무 큽니다. 제품 부분만 다시 선택해 주세요.");
  // Only a newly encoded crop can enter the external request. No original File/EXIF is forwarded.
  return {blob, width: canvas.width, height: canvas.height, previewUrl: URL.createObjectURL(blob)};
}
