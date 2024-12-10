import { defineConfig } from 'vite'
import { svelte } from '@sveltejs/vite-plugin-svelte'
import preprocess from 'svelte-preprocess'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [svelte({
    preprocess: preprocess({
      postcss: true,
    })
  })],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api'),
      },
    },
  },
  resolve: {
    conditions: mode === 'test' ? ['browser'] : ['browser', 'module'],
  },
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./setupTests.ts'],
    deps: {
      interopDefault: false
    }
  }
}))
