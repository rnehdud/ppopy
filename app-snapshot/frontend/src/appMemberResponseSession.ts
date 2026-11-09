/** A late response belongs to its requesting bearer, never a replacement login. */
export class AppMemberResponseSessionChanged extends Error {
  constructor() {
    super("로그인 상태가 변경됐습니다. 다시 로그인 상태를 확인해 주세요.");
    this.name = "AppMemberResponseSessionChanged";
  }
}

/** One connection lifetime stays on its first usable bearer, including later writes. */
type BoundMemberResponseSessionLoader = (() => Promise<string | null>) & {
  /** Consumer retirement withholds its await without retiring live siblings. */
  within: (isConsumerCurrent: () => boolean) => () => Promise<string | null>;
};
type MemberResponseSessionLoader = (() => Promise<string | null>) & {
  within?: BoundMemberResponseSessionLoader["within"];
};
export function createBoundMemberResponseSessionLoader(
  loadSessionToken: MemberResponseSessionLoader, onSessionChanged?: () => void,
  isCurrent: () => boolean = () => true,
): BoundMemberResponseSessionLoader {
  let bound: string | undefined;
  let retired = false;
  const retire = (): never => {
    if (!retired) {
      retired = true;
      try { onSessionChanged?.(); } catch { /* notification cannot reopen the connection */ }
    }
    throw new AppMemberResponseSessionChanged();
  };
  const assertLive = () => {
    if (retired) throw new AppMemberResponseSessionChanged();
    let active = false;
    try { active = isCurrent(); } catch { /* uncertain lifetime stays closed */ }
    if (!active) retire();
  };
  const load = async (isConsumerCurrent: () => boolean): Promise<string | null> => {
    const assertConsumerLive=()=>{
      let active=false;
      try {active=isConsumerCurrent();} catch { /* uncertain consumer stays closed */ }
      if(!active)throw new AppMemberResponseSessionChanged();
    };
    // Server closure can be confirmed even when the device cannot clear its token.
    assertConsumerLive();
    assertLive();
    let current: string | null;
    // Preserve a consumer fence through nested compositions down to the vault.
    // An inner loader must not retire the account before the outer await can
    // discard an obsolete result. Plain injected loaders keep their old call.
    try { current = await (loadSessionToken.within?.(isConsumerCurrent) ?? loadSessionToken)(); }
    catch (error) {
      assertConsumerLive();
      if (error instanceof AppMemberResponseSessionChanged) { retired = true; throw error; }
      return retire();
    }
    // A vault read may have started before logout, withdrawal or unmount.
    assertConsumerLive();
    assertLive();
    if (bound !== undefined && current !== bound) retire();
    if (bound === undefined && current && /^[A-Za-z0-9_-]{32,200}$/.test(current)) bound = current;
    return current;
  };
  const within=(isConsumerCurrent:()=>boolean):BoundMemberResponseSessionLoader=>
    Object.assign(()=>load(isConsumerCurrent),{within:(nested:()=>boolean)=>within(()=>isConsumerCurrent() && nested())});
  return within(()=>true);
}

/** No credential mutation or automatic retry; storage failures also withhold the response. */
export async function assertCurrentMemberResponseSession(
  loadSessionToken: () => Promise<string | null>, expectedToken: string,
  onSessionChanged?: () => void,
): Promise<void> {
  const changed = (): never => {
    try { onSessionChanged?.(); } catch { /* notification cannot release an old response */ }
    throw new AppMemberResponseSessionChanged();
  };
  let current: string | null;
  try { current = await loadSessionToken(); }
  catch (error) {
    if (error instanceof AppMemberResponseSessionChanged) throw error;
    return changed();
  }
  if (current !== expectedToken) changed();
}

/** Apply the same boundary to explicitly injected asynchronous member services. */
export async function runWithMemberResponseSession<T>(
  loadSessionToken: () => Promise<string | null>, onSessionChanged: () => void,
  operation: () => Promise<T>,
): Promise<T> {
  const token = await loadSessionToken();
  if (!token || !/^[A-Za-z0-9_-]{32,200}$/.test(token)) {
    try { onSessionChanged(); } catch { /* do not call the service */ }
    throw new AppMemberResponseSessionChanged();
  }
  await assertCurrentMemberResponseSession(loadSessionToken,token,onSessionChanged);
  let result:T;
  try { result=await operation(); }
  catch (error) {
    await assertCurrentMemberResponseSession(loadSessionToken,token,onSessionChanged);
    throw error;
  }
  await assertCurrentMemberResponseSession(loadSessionToken,token,onSessionChanged);
  return result;
}
