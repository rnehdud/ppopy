// Fresh canvas/UIImage encoders can add EXIF of their own (observed on WebKit).
// Remove application metadata/comments after orientation + pixel re-encoding.
export function removeJpegMetadata(bytes: Uint8Array): Uint8Array {
  if (bytes.length < 4 || bytes[0] !== 0xff || bytes[1] !== 0xd8 || bytes[bytes.length-2] !== 0xff || bytes[bytes.length-1] !== 0xd9) throw new Error("사진을 변환하지 못했습니다.");
  const parts: Uint8Array[] = [bytes.slice(0,2)]; let offset=2;
  while (offset < bytes.length) {
    const start=offset;
    if (bytes[offset++] !== 0xff) throw new Error("사진을 변환하지 못했습니다.");
    while (bytes[offset] === 0xff) offset++;
    const marker=bytes[offset++];
    if (marker === undefined || offset + 2 > bytes.length) throw new Error("사진을 변환하지 못했습니다.");
    const length=bytes[offset]*256 + bytes[offset+1];
    if (length < 2 || offset + length > bytes.length) throw new Error("사진을 변환하지 못했습니다.");
    if (marker === 0xda) {parts.push(bytes.slice(start));const size=parts.reduce((sum,value)=>sum+value.length,0);const clean=new Uint8Array(size);let position=0;for(const part of parts){clean.set(part,position);position+=part.length;}return clean;}
    const metadata=(marker >= 0xe1 && marker <= 0xef) || marker === 0xfe;
    if (!metadata) parts.push(bytes.slice(start,offset+length));
    offset+=length;
  }
  throw new Error("사진을 변환하지 못했습니다.");
}
export async function metadataFreeJpeg(blob: Blob): Promise<Blob> {
  const buffer=await new Promise<ArrayBuffer>((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>reader.result instanceof ArrayBuffer?resolve(reader.result):reject(new Error("사진을 변환하지 못했습니다."));reader.onerror=()=>reject(new Error("사진을 변환하지 못했습니다."));reader.readAsArrayBuffer(blob);});
  const bytes=removeJpegMetadata(new Uint8Array(buffer));
  return new Blob([bytes as Uint8Array<ArrayBuffer>],{type:"image/jpeg"});
}
