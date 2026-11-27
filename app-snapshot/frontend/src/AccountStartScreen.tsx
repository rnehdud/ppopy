import {loginStartFailureNotice} from "./loginStartStage";
import { FormEvent, useEffect, useRef, useState } from "react";

import policy from "../../skin_engine/config/app_login_plan.json";
import type {AppLoginNotices} from "./appLoginNotices";
import type {AppProtectionAcceptance} from "./appProtectionSession";
import "./appPrototype.css";
import "./accountStart.css";

export type AccountProvider = "apple" | "google" | "naver" | "kakao";

const providerLabels: Record<AccountProvider, string> = {
  apple: "Apple로 계속하기",
  google: "Google로 계속하기",
  naver: "네이버로 계속하기",
  kakao: "카카오로 계속하기",
};

export default function AccountStartScreen({
  connectionsEnabled = policy.provider_connections_enabled,
  availableProviders = policy.primary_providers as AccountProvider[],
  emailEnabled = true,
  availabilityNotice,
  accountNotice,
  onProviderStart,
  onEmailOtpStart,
  onEmailOtpVerify,
  loginNotices = null,
  onProtectionStart,
  onTestSessionStart,
  previewMode = false,
}: {
  connectionsEnabled?: boolean;
  availableProviders?: readonly AccountProvider[];
  emailEnabled?: boolean;
  availabilityNotice?: string;
  accountNotice?: string;
  onProviderStart: (provider: AccountProvider) => Promise<void>;
  onEmailOtpStart: (email: string) => Promise<void>;
  onEmailOtpVerify?: (email: string, code: string) => Promise<void>;
  loginNotices?: AppLoginNotices | null;
  onProtectionStart?: (acceptance: AppProtectionAcceptance) => Promise<void>;
  onTestSessionStart?: () => void;
  previewMode?: boolean;
}) {
  const [pending, setPending] = useState<AccountProvider | "email" | "verify" | null>(null);
  const [sentEmail, setSentEmail] = useState<string | null>(null);
  const [verified, setVerified] = useState(false);
  const [ageConfirmed, setAgeConfirmed] = useState(false);
  const [termsAcceptedVersion, setTermsAcceptedVersion] = useState<string | null>(null);
  const [privacyAcceptedVersion, setPrivacyAcceptedVersion] = useState<string | null>(null);
  const [sensitiveAcceptedVersion, setSensitiveAcceptedVersion] = useState<string | null>(null);
  const [historyAcceptedVersion, setHistoryAcceptedVersion] = useState<string | null>(null);
  const [selectedMethod, setSelectedMethod] = useState<AccountProvider | "email" | null>(null);
  const [emailToStart, setEmailToStart] = useState("");
  const requestPending = useRef(false);
  const entryDialog = useRef<HTMLElement>(null);
  const entryHeading = useRef<HTMLHeadingElement>(null);
  const entryTrigger = useRef<HTMLElement | null>(null);
  const [notice, setNotice] = useState("");
  const availableProviderSet = new Set(availableProviders);
  const canChooseMethod = connectionsEnabled && loginNotices !== null && !!onProtectionStart;
  const entryEnabled = connectionsEnabled && ageConfirmed
    && termsAcceptedVersion === loginNotices?.service_terms.version
    && privacyAcceptedVersion === loginNotices?.general_personal_information.version
    && sensitiveAcceptedVersion === loginNotices?.sensitive_information.version
    && (!loginNotices?.history_storage || historyAcceptedVersion === loginNotices.history_storage.version)
    && loginNotices !== null && !!onProtectionStart;
  useEffect(() => {
    if (!selectedMethod) return;
    const trigger = entryTrigger.current;
    const root = document.getElementById("root");
    const bodyOverflow = document.body.style.overflow;
    const rootOverflow = root?.style.overflow ?? "";
    document.body.style.overflow = "hidden";
    if (root) root.style.overflow = "hidden";
    entryHeading.current?.focus();
    return () => {
      document.body.style.overflow = bodyOverflow;
      if (root) root.style.overflow = rootOverflow;
      if (trigger?.isConnected) trigger.focus();
    };
  }, [selectedMethod]);
  const startProtection = async () => {
    if (!entryEnabled || !loginNotices || !onProtectionStart) throw new Error("Login notices unavailable");
    await onProtectionStart({
      age_gate:"over_or_equal_14",
      accepted_notices:{
        service_terms:loginNotices.service_terms.version,
        general_personal_information:loginNotices.general_personal_information.version,
        sensitive_information:loginNotices.sensitive_information.version,
        ...(loginNotices.history_storage ? {history_storage:loginNotices.history_storage.version} : {}),
      },
    });
  };

  const startProvider = async (provider: AccountProvider) => {
    if (!entryEnabled || !availableProviderSet.has(provider) || requestPending.current || verified) return;
    requestPending.current = true;
    setPending(provider);
    setNotice("");
    try {
      await startProtection();
      await onProviderStart(provider);
      setSelectedMethod(null);
    } catch (error) {
      setNotice(loginStartFailureNotice(error));
    } finally {
      requestPending.current = false;
      setPending(null);
    }
  };

  const requestEmail = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!canChooseMethod || requestPending.current || verified) return;
    const email = String(new FormData(event.currentTarget).get("email") ?? "").trim();
    if (!/^\S+@\S+\.\S+$/.test(email)) {
      setNotice("이메일 주소를 확인해 주세요.");
      return;
    }
    setEmailToStart(email);
    entryTrigger.current = event.currentTarget.querySelector<HTMLButtonElement>("button[type=submit]");
    setSelectedMethod("email");
    setNotice("");
  };

  const startEmail = async (email: string) => {
    if (!entryEnabled || requestPending.current || verified) return;
    requestPending.current = true;
    setPending("email");
    setNotice("");
    try {
      await startProtection();
      await onEmailOtpStart(email);
      setSentEmail(email);
      setSelectedMethod(null);
      setNotice("인증 코드를 보냈어요. 받은 편지함을 확인해 주세요.");
    } catch {
      setNotice("인증 코드를 보내지 못했어요. 잠시 뒤 다시 시도해 주세요.");
    } finally {
      requestPending.current = false;
      setPending(null);
    }
  };

  const verifyEmail = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!entryEnabled || !onEmailOtpVerify || !sentEmail || requestPending.current || verified) return;
    const form = event.currentTarget;
    const code = String(new FormData(form).get("code") ?? "").trim();
    if (!code) { setNotice("이메일로 받은 인증 코드를 입력해 주세요."); return; }
    requestPending.current = true;
    setPending("verify");
    setNotice("");
    try {
      await onEmailOtpVerify(sentEmail, code);
      setVerified(true);
      setNotice("이메일 인증을 완료했어요.");
    } catch {
      setNotice("인증하지 못했어요. 코드를 확인하거나 새 코드를 받아 주세요.");
    } finally {
      form.reset();
      requestPending.current = false;
      setPending(null);
    }
  };

  return <main className="account-start-screen">
    <div className="account-start-content" inert={selectedMethod !== null} aria-hidden={selectedMethod ? true : undefined}>
    <header>
      {previewMode && <small className="account-preview-label">화면 미리보기 · 로그인 연결 전</small>}
      <p>ppopy</p>
      <h1>내 루틴을 이어서 관리해요</h1>
      <span>제품 찾기, 맞춤 점검과 기록 관리는 회원가입 또는 로그인 후 이용할 수 있어요.</span>
    </header>

    {accountNotice && <section className="account-status-notice" role="status" aria-label="탈퇴 접수 상태">
      <strong>탈퇴 요청을 접수했어요</strong>
      <p>{accountNotice}</p>
    </section>}

    <section className="account-provider-list" aria-label="로그인 방법">
      {(policy.primary_providers as AccountProvider[]).filter(provider => availableProviderSet.has(provider)).map((provider) =>
        <button
          className={`account-provider account-provider-${provider}`}
          type="button"
          key={provider}
          aria-label={provider === "kakao" ? providerLabels[provider] : undefined}
          disabled={!canChooseMethod || !availableProviderSet.has(provider) || pending !== null || verified}
          onClick={event => { if (availableProviderSet.has(provider)) { entryTrigger.current = event.currentTarget; setSelectedMethod(provider); setNotice(""); } }}
        >
          {provider === "kakao"
            ? <img className="account-provider-kakao-art" src="/auth/kakao-login-wide.png" alt="" />
            : <><img aria-hidden="true" className="account-provider-mark" src={`/auth/${provider}-login-${provider === "apple" ? "logo" : "icon"}.png`} alt="" /><span>{providerLabels[provider]}</span></>}
        </button>)}
    </section>

    {availabilityNotice && <p className="account-availability-note" role="status">{availabilityNotice}</p>}

    {emailEnabled && <details className="account-other-method">
      <summary>{policy.overflow_label}</summary>
      {!sentEmail && <form onSubmit={requestEmail} noValidate>
        <label htmlFor="account-email">이메일로 인증 코드 받기</label>
        <div>
          <input id="account-email" name="email" type="email" inputMode="email" autoComplete="email" placeholder="name@example.com" disabled={!canChooseMethod || pending !== null} />
          <button type="submit" disabled={!canChooseMethod || pending !== null}>계속하기</button>
        </div>
      </form>}
      {sentEmail && !verified && <section className="account-otp" aria-label="이메일 인증">
        <p>{sentEmail}로 보낸 코드를 입력해 주세요.</p>
        <form onSubmit={(event) => void verifyEmail(event)} noValidate>
          <label htmlFor="account-code">인증 코드</label>
          <div>
            <input id="account-code" name="code" autoComplete="one-time-code" autoCapitalize="none" spellCheck={false} autoFocus disabled={!entryEnabled || pending !== null || !onEmailOtpVerify} />
            <button type="submit" disabled={!entryEnabled || pending !== null || !onEmailOtpVerify}>{pending === "verify" ? "확인 중…" : "인증하고 계속하기"}</button>
          </div>
        </form>
        {!onEmailOtpVerify && <p role="status">인증 연결을 준비 중이에요.</p>}
        <button type="button" disabled={pending !== null} onClick={() => { setSentEmail(null); setNotice(""); }}>이메일 변경·코드 다시 받기</button>
      </section>}
      <p className="account-identity-note">이미 가입했다면 같은 로그인 방법을 사용해 주세요. 이메일이 같아도 계정을 자동으로 합치지 않아요.</p>
    </details>}

    {!canChooseMethod && <p className="account-connection-note" role="status">{!loginNotices ? "약관과 개인정보 처리 안내 전문을 준비 중이에요." : "로그인 연결을 준비 중이에요."}</p>}
    {notice && !selectedMethod && <p className="account-login-notice" role="status">{notice}</p>}

    {onTestSessionStart && <button className="account-test-session" type="button" onClick={onTestSessionStart}>테스트 화면 보기</button>}
    </div>

    {selectedMethod && <div className="account-entry-backdrop">
      <section ref={entryDialog} className="account-entry-dialog" role="dialog" aria-modal="true" aria-labelledby="account-entry-title" aria-describedby="account-entry-intro" onKeyDown={event => {
        if (event.key === "Escape") {
          event.preventDefault();
          event.stopPropagation();
          if (pending === null) setSelectedMethod(null);
          return;
        }
        if (event.key !== "Tab") return;
        const controls = Array.from(entryDialog.current?.querySelectorAll<HTMLElement>("button:not(:disabled), input:not(:disabled), a[href]") ?? []);
        const first = controls[0];
        const last = controls.at(-1);
        const active = document.activeElement;
        if (!first || !last) {
          event.preventDefault();
          entryHeading.current?.focus();
        } else if (!controls.includes(active as HTMLElement) || (event.shiftKey ? active === first : active === last)) {
          event.preventDefault();
          (event.shiftKey ? last : first).focus();
        }
      }}>
        <button className="account-entry-close" type="button" disabled={pending !== null} onClick={() => setSelectedMethod(null)} aria-label="닫기"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5 5l14 14M19 5L5 19" /></svg></button>
        <h2 ref={entryHeading} id="account-entry-title" aria-describedby="account-entry-intro" tabIndex={-1}>시작하기 전에 확인해 주세요</h2>
        <p id="account-entry-intro" aria-hidden="true">{selectedMethod === "email" ? `${emailToStart}로 인증 코드를 보내기 전 이용 연령과 필수 안내를 확인해요.` : `${providerLabels[selectedMethod]} 전 이용 연령과 필수 안내를 확인해요.`}</p>
        <section className="account-entry-checks" aria-label="이용 연령과 필수 동의">
          <label><input type="checkbox" checked={ageConfirmed} disabled={pending !== null} onChange={event => setAgeConfirmed(event.target.checked)} /><span>만 14세 이상입니다</span></label>
          {loginNotices && <>
            <div><label><input type="checkbox" checked={termsAcceptedVersion === loginNotices.service_terms.version} disabled={pending !== null} onChange={event => setTermsAcceptedVersion(event.target.checked ? loginNotices.service_terms.version : null)} /><span>서비스 이용약관 동의 (필수)</span></label><a href={loginNotices.service_terms.url} target="_blank" rel="noopener noreferrer" aria-label="서비스 이용약관 전문 보기"><span aria-hidden="true">전문 보기</span></a></div>
            <div><label><input type="checkbox" checked={privacyAcceptedVersion === loginNotices.general_personal_information.version} disabled={pending !== null} onChange={event => setPrivacyAcceptedVersion(event.target.checked ? loginNotices.general_personal_information.version : null)} /><span>일반 개인정보 수집·이용 동의 (필수)</span></label><a href={loginNotices.general_personal_information.url} target="_blank" rel="noopener noreferrer" aria-label="일반 개인정보 수집·이용 안내 전문 보기"><span aria-hidden="true">전문 보기</span></a></div>
            <div><label><input type="checkbox" checked={sensitiveAcceptedVersion === loginNotices.sensitive_information.version} disabled={pending !== null} onChange={event => setSensitiveAcceptedVersion(event.target.checked ? loginNotices.sensitive_information.version : null)} aria-describedby="account-sensitive-summary" /><span>민감정보 수집·이용 동의 (필수)</span></label><a href={loginNotices.sensitive_information.url} target="_blank" rel="noopener noreferrer" aria-label="민감정보 수집·이용 안내 전문 보기"><span aria-hidden="true">전문 보기</span></a></div>
            <p id="account-sensitive-summary" className="account-sensitive-summary">{loginNotices.sensitive_information.summary}</p>
            {loginNotices.history_storage && <><div><label><input type="checkbox" checked={historyAcceptedVersion === loginNotices.history_storage.version} disabled={pending !== null} onChange={event => setHistoryAcceptedVersion(event.target.checked ? loginNotices.history_storage!.version : null)} aria-describedby="account-history-summary"/><span>상태·루틴 이력 저장 동의 (필수)</span></label><a href={loginNotices.history_storage.url} target="_blank" rel="noopener noreferrer" aria-label="상태·루틴 이력 저장 안내 전문 보기"><span aria-hidden="true">전문 보기</span></a></div><p id="account-history-summary" className="account-sensitive-summary">{loginNotices.history_storage.summary}</p></>}
          </>}
        </section>
        {notice && <p className="account-login-notice" role="status">{notice}</p>}
        <button className="account-entry-continue" type="button" disabled={!entryEnabled || pending !== null} onClick={() => void (selectedMethod === "email" ? startEmail(emailToStart) : startProvider(selectedMethod))}>{pending ? "연결 중…" : selectedMethod === "email" ? "인증 코드 받기" : `${providerLabels[selectedMethod]}`}</button>
      </section>
    </div>}
  </main>;
}
