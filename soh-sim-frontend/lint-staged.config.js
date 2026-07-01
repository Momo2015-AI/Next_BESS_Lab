{
  "name": "soh-sim-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src/ --fix",
    "format": "prettier --write src/",
    "lint-staged": "lint-staged"
  },
  "lint-staged": {
    "src/**/*.{vue,js,ts}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
