export type ProductIngredientDraft = {
  product_name: string; option: string; source_url: string; raw_ingredients: string;
  version_note: string; verification_status: "review_required"; provenance_hash: string;
};
export function checkedIngredientDrafts(value: unknown): ProductIngredientDraft[] {
  const invalid = () => new Error("전성분 검색 결과와 출처를 확인하지 못했어요.");
  if (!value || typeof value !== "object" || Array.isArray(value)) throw invalid();
  const envelope = value as Record<string, unknown>;
  if (Object.keys(envelope).sort().join("|") !== "auto_confirmed|drafts|provider" || envelope.provider !== "openai_responses"
    || envelope.auto_confirmed !== false || !Array.isArray(envelope.drafts) || envelope.drafts.length > 2) throw invalid();
  return envelope.drafts.map(value => {
    if (!value || typeof value !== "object" || Array.isArray(value)) throw invalid();
    const item = value as Record<string, unknown>;
    const fields = ["option", "product_name", "provenance_hash", "raw_ingredients", "source_url", "verification_status", "version_note"];
    if (Object.keys(item).sort().join("|") !== fields.join("|") || fields.some(key => typeof item[key] !== "string")) throw invalid();
    const draft = item as ProductIngredientDraft;
    let url: URL; try {url = new URL(draft.source_url);} catch {throw invalid();}
    if (draft.verification_status !== "review_required" || url.protocol !== "https:" || url.username || url.password || !url.hostname
      || draft.source_url.length > 4096 || !draft.product_name.trim() || draft.product_name.length > 400
      || !draft.raw_ingredients.trim() || draft.raw_ingredients.length > 24000 || draft.option.length > 400 || draft.version_note.length > 400
      || !/^[a-f0-9]{64}$/.test(draft.provenance_hash)) throw invalid();
    return {...draft};
  });
}
