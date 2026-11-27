import type {ReactNode} from "react";
import "./poppyVisualTheme.css";

/** Presentation only. Child authentication and data lifetimes stay intact. */
export default function AppVisualFrame({children}:{children:ReactNode}) {
  return <div className="poppy-visual-theme">{children}</div>;
}
