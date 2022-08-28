/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        'discord-bg': '#2F3136',
        'discord-text-light': '#B9BBBE',
        'discord-blue': '#5865F2',
        'discord-grey': '#5D5F62',
        'discord-dark': '#202225',
        'discord-glow-blue': '#2091F9',
      },
    },
  },
  plugins: [],
}
