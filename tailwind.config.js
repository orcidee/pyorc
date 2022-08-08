const colors = require('tailwindcss/colors')

module.exports = {
  purge: {
    content: ['./pyorc/**/*.html'],
    options: {},
  },
  theme: {
    // FIXME: Define here the branding colors
    colors: {
      'gray': colors.warmGray,
      // 'purple': '#7e5bef',
      // 'pink': '#ff49db',
      // 'orange': '#ff7849',
      // 'green': '#13ce66',
      // 'yellow': '#ffc82c',
      // 'gray-dark': '#273444',
      // 'gray': '#8492a6',
      // 'gray-light': '#d3dce6',
    },
  },
  variants: {},
  plugins: [],
};
