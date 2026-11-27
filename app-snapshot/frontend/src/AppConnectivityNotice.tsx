import { useEffect, useState } from "react";
import { Network } from "@capacitor/network";

function useConnectivityStatus(): "online" | "offline" {
  const [status, setStatus] = useState<"online" | "offline">(() => navigator.onLine ? "online" : "offline");
  useEffect(() => {
    let active = true;
    let removeListener: (() => Promise<void>) | undefined;

    void Network.getStatus().then(({ connected }) => {
      if (active) setStatus(connected ? "online" : "offline");
    });
    void Network.addListener("networkStatusChange", ({ connected }) => {
      if (active) setStatus(connected ? "online" : "offline");
    }).then((handle) => {
      if (!active) void handle.remove();
      else removeListener = handle.remove;
    });

    return () => {
      active = false;
      if (removeListener) void removeListener();
    };
  }, []);
  return status;
}

export default function AppConnectivityNotice() {
  if (useConnectivityStatus() === "online") return null;
  return <section className="app-connectivity-notice" role="status">
    <strong>인터넷 연결을 확인해 주세요</strong>
    <p>작성 중인 입력은 그대로 둡니다. 연결된 뒤 현재 화면에서 다시 시도해 주세요.</p>
  </section>;
}
