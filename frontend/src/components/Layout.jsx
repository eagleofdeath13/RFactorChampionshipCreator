import { Outlet } from 'react-router-dom'
import Navigation from './Navigation'
import { motion } from 'framer-motion'

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navigation />

      <motion.main
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="flex-1 container mx-auto px-4 py-8 relative z-10"
      >
        <Outlet />
      </motion.main>

      {/* Footer */}
      <footer className="bg-gradient-carbon border-t-4 border-racing-red py-6 mt-auto text-center text-chrome-silver text-sm tracking-wide">
        <span className="text-racing-red font-bold">rFactor Championship Creator</span> v1.4.0 |{' '}
        <span className="text-chrome-silver">68 tests passants</span> |
        Powered by <span className="text-fluo-yellow font-bold">React</span> &{' '}
        <span className="text-racing-red font-bold">FastAPI</span>
      </footer>
    </div>
  )
}
