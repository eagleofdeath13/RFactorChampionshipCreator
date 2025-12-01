import { motion } from 'framer-motion'
import { Loader2 } from 'lucide-react'

export default function LoadingSpinner({ message = 'Chargement...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <motion.div
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
      >
        <Loader2 className="w-12 h-12 text-racing-red" />
      </motion.div>
      <p className="mt-4 font-orbitron font-bold text-lg uppercase tracking-wider text-chrome-silver">
        {message}
      </p>
    </div>
  )
}
