/** Fixed local stages only: never expose SDK text, tokens or response bodies. */
export type LoginStartStage = "L01" | "A01" | "A02" | "A03" | "A04";
class LoginStartFailure extends Error {
  constructor(readonly stage: LoginStartStage) { super("Login start failed"); }
}
export async function atLoginStartStage<T>(stage: LoginStartStage, action: () => Promise<T>): Promise<T> {
  try { return await action(); } catch { throw new LoginStartFailure(stage); }
}
export function loginStartFailureNotice(error: unknown): string {
  const message = "로그인을 시작하지 못했어요. 잠시 뒤 다시 시도해 주세요.";
  return error instanceof LoginStartFailure ? `${message} 확인 코드: ${error.stage}` : message;
}
