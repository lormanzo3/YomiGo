/**
 * Vite configuration for YomiGo browser extension.
 *
 * This config handles building:
 * 1. popup.html - React app for the extension popup
 * 2. background.js - Service worker for message handling
 * 3. content.js - Content script injected into pages
 *
 * The build output goes to dist/ which can be loaded as an unpacked extension.
 */

import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],

  build: {
    outDir: "dist",
    emptyDirOnBuild: true,

    rollupOptions: {
      input: {
        // Main popup page (React app)
        popup: resolve(__dirname, "src/popup/index.html"),
        // Background service worker
        background: resolve(__dirname, "src/background.ts"),
        // Content script
        content: resolve(__dirname, "src/content.ts"),
      },

      output: {
        entryFileNames: "[name].js",
        chunkFileNames: "chunks/[name].[hash].js",
        assetFileNames: (assetInfo) => {
          // Keep CSS files at root level
          if (assetInfo.name?.endsWith(".css")) {
            return "[name][extname]";
          }
          return "assets/[name][extname]";
        },
      },
    },
  },

  // Resolve @ alias for cleaner imports
  resolve: {
    alias: {
      "@": resolve(__dirname, "src"),
    },
  },
});
