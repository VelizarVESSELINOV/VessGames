/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  darkMode: "selector",
  plugins: [
    require("@tailwindcss/forms"),
    // ...
  ],
};
