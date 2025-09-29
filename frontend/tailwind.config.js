/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "klein-blue": "#2563eb",
        "klein-green": "#059669",
        "ophir-amber": "#d97706",
        "ophir-red": "#dc2626",
        safe: "#10b981",
        flagged: "#f59e0b",
        denied: "#ef4444",
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Consolas", "Monaco", "monospace"],
      },
      animation: {
        "pulse-slow": "pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "bounce-slow": "bounce 2s infinite",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
