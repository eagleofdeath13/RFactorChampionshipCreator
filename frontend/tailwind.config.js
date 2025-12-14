/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Racing theme colors
        racing: {
          red: '#E31E24',
          'red-dark': '#B01419',
          'red-glow': 'rgba(227, 30, 36, 0.4)',
          cyan: '#00D9FF',
        },
        carbon: {
          black: '#0A0A0A',
          dark: '#151515',
          light: '#1F1F1F',
          metal: '#2A2A2A',
        },
        dark: {
          primary: '#0A0A0A',
          secondary: '#1A1A1A',
        },
        chrome: {
          silver: '#C0C0C0',
        },
        fluo: {
          yellow: '#FFE700',
          'yellow-glow': 'rgba(255, 231, 0, 0.3)',
        },
        status: {
          success: '#00FF41',
          warning: '#FFB800',
          danger: '#FF0040',
          info: '#00D9FF',
        },
      },
      fontFamily: {
        orbitron: ['Orbitron', 'monospace'],
        rajdhani: ['Rajdhani', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-racing': 'linear-gradient(135deg, #E31E24 0%, #B01419 100%)',
        'gradient-carbon': 'linear-gradient(180deg, #1F1F1F 0%, #0A0A0A 100%)',
        'carbon-fiber': `
          repeating-linear-gradient(45deg, transparent, transparent 2px, rgba(255,255,255,0.01) 2px, rgba(255,255,255,0.01) 4px),
          repeating-linear-gradient(-45deg, transparent, transparent 2px, rgba(255,255,255,0.01) 2px, rgba(255,255,255,0.01) 4px)
        `,
      },
      boxShadow: {
        'racing-glow': '0 0 20px rgba(227, 30, 36, 0.4), 0 0 40px rgba(227, 30, 36, 0.4)',
        'yellow-glow': '0 0 15px rgba(255, 231, 0, 0.3)',
        'deep': '0 8px 32px rgba(0, 0, 0, 0.8)',
        'card': '0 4px 16px rgba(0, 0, 0, 0.6)',
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'pulse-racing': 'pulse-racing 2s ease-in-out infinite',
        'slide-in': 'slide-in 0.5s ease-out',
        'fade-in-up': 'fade-in-up 0.6s ease-out',
        'rev-counter': 'rev-counter 0.3s ease-out',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
          '50%': { transform: 'translateY(-5px) rotate(-5deg)' },
        },
        'pulse-racing': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.05)' },
        },
        'slide-in': {
          '0%': { opacity: '0', transform: 'translateX(50px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'rev-counter': {
          '0%': { transform: 'scale(1)', filter: 'brightness(1)' },
          '50%': { transform: 'scale(1.1)', filter: 'brightness(1.3)' },
          '100%': { transform: 'scale(1)', filter: 'brightness(1)' },
        },
      },
    },
  },
  plugins: [],
}
