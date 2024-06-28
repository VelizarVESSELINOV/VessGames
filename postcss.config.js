/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{html,js}',
    './templates/*.{html,js}',
    './components/**/*.{html,js}'
  ],
  theme: {
    extend: {
      'animation': {
            'text':'text 5s ease infinite',
        },
        'keyframes': {
            'text': {
                '0%, 100%': {
                   'background-size':'200% 200%',
                    'background-position': 'left center'
                },
                '50%': {
                   'background-size':'200% 200%',
                    'background-position': 'right center'
                }
            },
        }
    },
  },
  content: ["./src/**/*.{html,js}"],
  darkMode: "selector",
  plugins: [
    require("@tailwindcss/forms"),
    tailwindcss: {},
    autoprefixer: {},
  ],
};
