import {StrictMode} from "react";
import {createRoot} from "react-dom/client";
import {Capacitor} from "@capacitor/core";
import "./nativeShell.css";
import AppPublicCandidate from "./AppPublicCandidate";
import AppErrorBoundary from "./AppErrorBoundary";
import AppVisualFrame from "./AppVisualFrame";

// Separate build entry: no AppAuthTest or native TEST candidate import.
if(Capacitor.isNativePlatform()){
  document.documentElement.classList.add("poppy-native");document.body.classList.add("poppy-native");
}
createRoot(document.getElementById("root")!).render(<StrictMode><AppErrorBoundary><AppVisualFrame><AppPublicCandidate/></AppVisualFrame></AppErrorBoundary></StrictMode>);
// Native public shell does not install a service worker over member state.
