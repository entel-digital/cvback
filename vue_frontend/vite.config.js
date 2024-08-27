import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'
import {resolve} from 'path'
import cssInjectedByJsPlugin from "vite-plugin-css-injected-by-js";
import {splitVendorChunkPlugin} from 'vite'
import { quasar, transformAssetUrls } from '@quasar/vite-plugin'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    port: 5173,
    host: true,
    strictPort: true,
  },
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "@/assets/styles/main.css";`,
      },
    },
  },
  build: {
    rollupOptions: {
      input: {
        main: resolve('./src/main.js'),
        reward: resolve('./src/reward.js'),
      },
      output: {
        dir: '../cvback/static/vue/',
        entryFileNames: '[name].js',
      },
    },
  },
  plugins: [
    vue({
      template: { transformAssetUrls }
    }),
    cssInjectedByJsPlugin({jsAssetsFilterFunction: () => true}),
    splitVendorChunkPlugin(),
    quasar({
      sassVariables: 'src/css/quasar-variables.sass'
    })
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
