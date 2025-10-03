import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/app/**/*.{js,ts,jsx,tsx}",
    "./src/components/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        "nexus-navy": "#1F3C88",
        "nexus-mint": "#3BC9A7",
        "nexus-cream": "#F5F7FB"
      }
    }
  },
  plugins: []
};

export default config;
