import { Capacitor, registerPlugin } from "@capacitor/core";

type IOSProductTextRecognizerPlugin = {
  recognize(options: { imageBase64: string }): Promise<{ lines: string[] }>;
};

const nativeRecognizer = registerPlugin<IOSProductTextRecognizerPlugin>("IOSProductTextRecognizer");

async function blobAsBase64(blob: Blob): Promise<string> {
  if (blob.size > 15 * 1024 * 1024) throw new Error("사진이 너무 큽니다. 다시 촬영해 주세요.");
  const bytes = new Uint8Array(await blob.arrayBuffer());
  let binary = "";
  const chunk = 0x8000;
  for (let index = 0; index < bytes.length; index += chunk) {
    binary += String.fromCharCode(...bytes.subarray(index, index + chunk));
  }
  return btoa(binary);
}

export async function recognizeProductText(photo: Blob): Promise<string[]> {
  if (!Capacitor.isNativePlatform()) throw new Error("제품 사진 글자 읽기는 iPhone TEST 앱에서 사용할 수 있습니다.");
  const result = await nativeRecognizer.recognize({ imageBase64: await blobAsBase64(photo) });
  if (!Array.isArray(result.lines) || result.lines.some(line => typeof line !== "string")) {
    throw new Error("사진 글자 읽기 결과를 확인하지 못했습니다.");
  }
  return result.lines
    .map(line => line.normalize("NFKC").trim().replace(/\s+/g, " "))
    .filter(Boolean)
    .slice(0, 100)
    .map(line => line.slice(0, 120));
}
