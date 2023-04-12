/** @type {import('tailwindcss').Config} */

const colors = require('tailwindcss/colors')

module.exports = {
  content: {
    relative: true,
    files: [
      "./**/*.html"
      // this looks in the source directory, because it is run in a Docker env where ./owdex/templates/* is copied next to it
    ]
  },
  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',
      gray: colors.gray,
      blue: colors.blue,
      green: colors.green,
      orange: colors.orange,
    }
  },
  plugins: [],
  variants: {
    extend: {
      visibility: ["group-hover"],
    },
   },
}
