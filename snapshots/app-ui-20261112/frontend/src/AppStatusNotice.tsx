import { appStatusContent, type AppStatusKind } from "./appStatusContent";

export default function AppStatusNotice({ kind, detail }: { kind: AppStatusKind; detail?: string }) {
  const value = appStatusContent(kind);
  return <section className={`app-status-notice app-status-${value.technical ? "technical" : "decision"}`} role={value.technical ? "alert" : "status"}>
    <strong>{value.title}</strong>
    <p>{detail || value.defaultDetail}</p>
  </section>;
}
