import type { CapacitorConfig } from "@capacitor/cli";

const config: CapacitorConfig = {
  appId: "example.ppopy.preview",
  appName: "Poppy",
  webDir: "dist",
  server: {
    cleartext: false,
  },
  ios: {
    preferredContentMode: "mobile",
    backgroundColor: "#f7f8fa",
    allowsLinkPreview: false,
  },
};

export default config;
