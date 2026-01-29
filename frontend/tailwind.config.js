/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        board: {
          bg: '#EBC88C',
          line: '#654321',
          river: '#B0C4DE',
        },
        piece: {
          red: '#C0392B',
          black: '#2C3E50',
          redBg: '#FFFAF0',
          blackBg: '#F5F5DC',
        },
        ui: {
          primary: '#3498DB',
          success: '#2ECC71',
          warning: '#F39C12',
          danger: '#E74C3C',
        }
      }
    },
  },
  plugins: [],
}
