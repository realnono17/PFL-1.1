import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  server: {
    allowedHosts: ['1860-51-37-207-22.ngrok-free.app'],
    historyApiFallback: true, // Prevents Vue Router 404s on refresh ✅
  },
});
