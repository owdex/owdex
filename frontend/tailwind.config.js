/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
      "./owdex/templates/*.html"
    ]
  },
  theme: {
    extend: {},
  },
  plugins: [],
  variants: {
    extend: {
      visibility: ["group-hover"],
    },
   },
}
