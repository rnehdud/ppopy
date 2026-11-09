import type {PhotoCrop} from "./productPhotoPreparation";
export type CropGesture = "move" | "nw" | "ne" | "sw" | "se";
const clamp = (value: number, min: number, max: number) => Math.max(min, Math.min(max, value));
// Coordinates are percentages of the displayed image, also used by the JPEG encoder.
export function adjustPhotoCrop(start: PhotoCrop, mode: CropGesture, dx: number, dy: number): PhotoCrop {
  if (![dx, dy].every(Number.isFinite)) return start;
  if (mode === "move") return {...start, x: clamp(start.x + dx, 0, 100 - start.width), y: clamp(start.y + dy, 0, 100 - start.height)};
  let left = start.x, top = start.y, right = left + start.width, bottom = top + start.height;
  if (mode.includes("w")) left = clamp(left + dx, 0, right - 1);
  else right = clamp(right + dx, left + 1, 100);
  if (mode.includes("n")) top = clamp(top + dy, 0, bottom - 1);
  else bottom = clamp(bottom + dy, top + 1, 100);
  return {x: left, y: top, width: right - left, height: bottom - top};
}
