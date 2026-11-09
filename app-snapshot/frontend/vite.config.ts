import react from "@vitejs/plugin-react";
import {defineConfig} from "vite";
// Course preview has no API proxy or production entry point.
export default defineConfig({plugins: [react()], server: {host: "127.0.0.1"}, preview: {host: "127.0.0.1"}});
