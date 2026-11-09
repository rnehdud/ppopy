import {useLayoutEffect, useMemo, useRef, useState} from "react";
import type {ProductCandidate} from "./productCatalog";
import type {ProductIngredientDraft} from "./productIngredientDraft";

type Lookup = ((query: string) => Promise<ProductIngredientDraft[]>) | undefined;
export type IngredientLookupState = {status: "queued" | "searching" | "found" | "empty" | "failed"; drafts: ProductIngredientDraft[]};
type Binding = {lookup: Lookup; live: boolean};
type Task = {product: ProductCandidate; token: number; epoch: number; binding: Binding; lookup: Exclude<Lookup, undefined>};

// One paid request at a time; deletion/unmount invalidates queued and late work.
export function useIngredientLookup(lookup: Lookup) {
  const binding = useMemo<Binding>(() => ({lookup, live: false}), [lookup]);
  const owner = useRef<Binding | null>(null);
  const [resolved, setResolved] = useState<{binding: Binding; entries: Record<string, IngredientLookupState>}>({binding, entries: {}});
  const queue = useRef<Task[]>([]);
  const pending = useRef(new Map<string, number>());
  const current = useRef(new Map<string, number>());
  const sequence = useRef(0);
  const epoch = useRef(0);
  const running = useRef(false);
  useLayoutEffect(() => {
    binding.live = true; owner.current = binding;
    const pendingProducts = pending.current, currentProducts = current.current;
    return () => {
      binding.live = false; epoch.current += 1;
      queue.current = queue.current.filter(task => task.binding !== binding);
      if (owner.current === binding) {owner.current = null; pendingProducts.clear(); currentProducts.clear();}
    };
  }, [binding]);
  const isCurrent = () => binding.live && owner.current === binding;
  const update = (target: Binding, change: (values: Record<string, IngredientLookupState>) => Record<string, IngredientLookupState>) => {
    if (!target.live || owner.current !== target) return;
    setResolved(previous => ({binding: target, entries: change(previous.binding === target ? previous.entries : {})}));
  };

  const pump = async () => {
    if (running.current) return;
    running.current = true;
    try {
      while (queue.current.length) {
        const task = queue.current.shift()!;
        const id = task.product.id;
        const valid = () => task.binding.live && owner.current === task.binding && task.epoch === epoch.current && current.current.get(id) === task.token;
        if (!valid()) continue;
        update(task.binding, values => ({...values, [id]: {status: "searching", drafts: []}}));
        try {
          const product = task.product;
          const option = ["용량·옵션 미확인", "용량·옵션 확인 필요"].includes(product.option) ? "" : product.option;
          const query = (product.matchSource === "public_web" ? product.name : `${product.brand} ${product.name} ${option}`).trim().slice(0, 200);
          const drafts = await task.lookup(query);
          if (valid()) update(task.binding, values => ({...values, [id]: {status: drafts.length ? "found" : "empty", drafts}}));
        } catch {
          if (valid()) update(task.binding, values => ({...values, [id]: {status: "failed", drafts: []}}));
        } finally {
          if (pending.current.get(id) === task.token) pending.current.delete(id);
        }
      }
    } finally {running.current = false;}
  };

  const enqueue = (product: ProductCandidate) => {
    if (!isCurrent() || !lookup || pending.current.has(product.id)) return;
    const token = ++sequence.current;
    current.current.set(product.id, token); pending.current.set(product.id, token);
    queue.current.push({product, token, epoch: epoch.current, binding, lookup});
    update(binding, values => ({...values, [product.id]: {status: "queued", drafts: []}}));
    void pump();
  };
  const remove = (id: string) => {
    if (!isCurrent()) return;
    current.current.delete(id); pending.current.delete(id);
    queue.current = queue.current.filter(task => task.product.id !== id);
    update(binding, values => {const next = {...values}; delete next[id]; return next;});
  };
  // Mask old provider drafts during render, before the layout cleanup runs.
  // The single in-flight request is not presumed cancelled or refunded; a new
  // provider's explicit queue waits for settlement and never replays old work.
  const entries: Record<string, IngredientLookupState> = resolved.binding === binding ? resolved.entries : {};
  return {entries, enqueue, remove};
}

export function ingredientLookupMessage(status: IngredientLookupState["status"]) {
  return {
    queued: "추가한 제품의 전성분을 순서대로 확인할게요.",
    searching: "전성분을 찾고 있어요. 다른 제품을 추가하거나 다음으로 진행해도 괜찮아요.",
    found: "전성분 목록을 찾았어요. 원문과 제품 버전 검증이 필요해요.",
    empty: "전성분 목록을 찾지 못했어요. 제품 정보는 유지되며 포장이나 출처에서 확인할 수 있어요.",
    failed: "전성분을 가져오지 못했어요. 제품 정보는 유지돼요. 필요하면 다시 시도해 주세요.",
  }[status];
}
