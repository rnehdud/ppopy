import { Component, type ReactNode } from "react";

type Props = { children: ReactNode; onRestart?: () => void };
type State = { failed: boolean };

export default class AppErrorBoundary extends Component<Props, State> {
  state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  componentDidCatch() {
    // 오류 원문과 component stack에는 사용자 입력이 섞일 수 있어 외부 전송·화면 표시를 하지 않는다.
  }

  render() {
    if (!this.state.failed) return this.props.children;
    return <main className="app-crash-screen">
      <section role="alert" aria-labelledby="app-crash-title">
        <p>잠시 문제가 생겼어요</p>
        <h1 id="app-crash-title">입력은 서버 초안에서 다시 불러올 수 있어요</h1>
        <p>앱을 다시 시작해 주세요. 오류 내용이나 입력값은 외부 서비스로 보내지 않습니다.</p>
        <button type="button" onClick={this.props.onRestart ?? (() => window.location.reload())}>앱 다시 시작</button>
      </section>
    </main>;
  }
}
