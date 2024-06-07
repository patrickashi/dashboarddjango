/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './dashboard/templates/**/*.html',
    './dashboard/static_src/**/*.js',
    './dashboard/static/**/*.css', // If you have additional CSS files using Tailwind classes
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};

