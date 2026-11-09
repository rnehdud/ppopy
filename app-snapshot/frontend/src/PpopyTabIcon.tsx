import type {MirayTab} from "./mirayNavigation";

/** Decorative icons; the accompanying tab text provides the accessible name. */
export default function PpopyTabIcon({tab}: {tab: MirayTab}) {
  return <svg className="ppopy-tab-icon" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
    {tab === "cosmetics" && <><path d="M9 4h6M10 2.5h4M7.5 7.5h9A1.5 1.5 0 0 1 18 9v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2V9a1.5 1.5 0 0 1 1.5-1.5ZM9 4v3.5m6-3.5v3.5"/></>}
    {tab === "routine" && <><circle cx="12" cy="12" r="8"/><path d="M12 7v5l3 2M4.5 3.5 3 5M19.5 3.5 21 5"/></>}
    {tab === "home" && <><path d="M3 10.5 12 3l9 7.5"/><path d="M5.5 9.5V20h13V9.5M10 20v-6h4v6"/></>}
    {tab === "explore" && <><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 4.5 4.5"/></>}
    {tab === "my" && <><circle cx="12" cy="8" r="3.5"/><path d="M5 20a7 7 0 0 1 14 0"/></>}
  </svg>;
}
