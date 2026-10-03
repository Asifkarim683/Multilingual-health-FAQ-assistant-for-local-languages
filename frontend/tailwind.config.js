/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        devanagari: ['"Noto Sans Devanagari"', 'sans-serif'],
        odia: ['"Noto Sans Oriya"', 'sans-serif'],
        bengali: ['"Noto Sans Bengali"', 'sans-serif'],
        telugu: ['"Noto Sans Telugu"', 'sans-serif'],
        tamil: ['"Noto Sans Tamil"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
