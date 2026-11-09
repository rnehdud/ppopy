import React from "react";
import {createRoot} from "react-dom/client";
import AppLaunchShell from "./AppLaunchShell";
import AppVisualFrame from "./AppVisualFrame";
import "./nativeShell.css";

// Shared synthetic preview only; no auth, service transport, or persistence is injected.
createRoot(document.getElementById("root")!).render(<React.StrictMode><AppVisualFrame><AppLaunchShell allowOwnerTestSession newNavigationEnabled /></AppVisualFrame></React.StrictMode>);
