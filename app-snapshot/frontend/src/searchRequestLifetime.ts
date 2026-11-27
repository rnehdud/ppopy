/** Abandon a late bridge result; cancellation is never a server settlement receipt. */
export function awaitSearchRequest<T>(
  dispatch: () => Promise<T>,
  cancel: () => Promise<unknown>,
  signal?: AbortSignal,
  timeout?: {milliseconds: number; error: unknown},
): Promise<T> {
  signal?.throwIfAborted();
  return new Promise<T>((resolve, reject) => {
    let settled = false;
    let timer: ReturnType<typeof setTimeout> | undefined;
    const finish = (done: () => void) => {
      if (settled) return;
      settled = true;
      if (timer !== undefined) clearTimeout(timer);
      signal?.removeEventListener("abort", aborted);
      done();
    };
    const stop = (error: unknown) => {
      if (settled) return;
      finish(() => reject(error));
      // A missing/failed native ACK cannot reopen the result or trigger a retry.
      try { void cancel().catch(() => undefined); } catch { /* best effort only */ }
    };
    const aborted = () => stop(signal?.reason ?? new DOMException("검색을 중단했어요.", "AbortError"));
    signal?.addEventListener("abort", aborted, {once:true});
    if (timeout) timer = setTimeout(() => stop(timeout.error), timeout.milliseconds);
    try {
      dispatch().then(value => finish(() => resolve(value)), error => finish(() => reject(error)));
    } catch (error) { finish(() => reject(error)); }
  });
}
