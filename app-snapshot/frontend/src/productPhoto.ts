export const PRODUCT_PHOTO_POC_ENABLED = import.meta.env.VITE_PRODUCT_CAMERA_POC === "true";

const ACCEPTED_TYPES = new Set([
  "image/jpeg",
  "image/png",
  "image/webp",
  "image/heic",
  "image/heif",
  "image/heic-sequence",
  "image/heif-sequence",
]);
const ACCEPTED_EXTENSIONS = /\.(?:jpe?g|png|webp|heic|heif)$/i;
const WEB_PREVIEW_TYPES = new Set(["image/jpeg", "image/png", "image/webp"]);
const WEB_PREVIEW_EXTENSIONS = /\.(?:jpe?g|png|webp)$/i;
const MAX_INPUT_BYTES = 15 * 1024 * 1024;
const MAX_EDGE = 1600;
const JPEG_QUALITY = 0.82;

export type PreparedProductPhoto = {
  blob: Blob;
  previewUrl: string;
  width: number;
  height: number;
};

export function validateProductPhotoFile(file: File): string | null {
  if (!(ACCEPTED_TYPES.has(file.type.toLowerCase()) || (!file.type && ACCEPTED_EXTENSIONS.test(file.name)))) {
    return "JPG, PNG, WebP 또는 iPhone HEIC 이미지만 사용할 수 있어요.";
  }
  if (file.size > MAX_INPUT_BYTES) return "사진 용량은 15MB 이하여야 해요.";
  return null;
}

export function isProductPhotoWebPreviewable(file: File): boolean {
  return WEB_PREVIEW_TYPES.has(file.type.toLowerCase()) || (!file.type && WEB_PREVIEW_EXTENSIONS.test(file.name));
}

function loadImage(file: File): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const image = new Image();
    image.onload = () => {
      URL.revokeObjectURL(url);
      resolve(image);
    };
    image.onerror = () => {
      URL.revokeObjectURL(url);
      reject(new Error("사진을 읽지 못했습니다."));
    };
    image.src = url;
  });
}

export async function prepareProductPhoto(file: File, centerCrop = false): Promise<PreparedProductPhoto> {
  const validationError = validateProductPhotoFile(file);
  if (validationError) throw new Error(validationError);

  const image = await loadImage(file);
  const sourceWidth = centerCrop ? Math.min(image.naturalWidth, image.naturalHeight) * 0.8 : image.naturalWidth;
  const sourceHeight = centerCrop ? sourceWidth : image.naturalHeight;
  const scale = Math.min(1, MAX_EDGE / Math.max(sourceWidth, sourceHeight));
  const width = Math.max(1, Math.round(sourceWidth * scale));
  const height = Math.max(1, Math.round(sourceHeight * scale));
  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const context = canvas.getContext("2d");
  if (!context) throw new Error("사진 처리 기능을 사용할 수 없습니다.");
  context.drawImage(image, (image.naturalWidth-sourceWidth)/2, (image.naturalHeight-sourceHeight)/2, sourceWidth, sourceHeight, 0, 0, width, height);

  const blob = await new Promise<Blob>((resolve, reject) => {
    canvas.toBlob(
      (value) => (value ? resolve(value) : reject(new Error("사진을 변환하지 못했습니다."))),
      "image/jpeg",
      JPEG_QUALITY,
    );
  });

  // 캔버스 재인코딩으로 원본 EXIF·위치 메타데이터를 결과에 복사하지 않는다.
  return { blob, previewUrl: URL.createObjectURL(blob), width, height };
}
