/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
      "./**/*.html"
      // this looks in the source directory, because it is run in a Docker env where ./owdex/templates/* is copied next to it
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
