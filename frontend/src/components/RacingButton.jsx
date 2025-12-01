import { motion } from 'framer-motion'
import clsx from 'clsx'
import { Loader2 } from 'lucide-react'

export default function RacingButton({
  children,
  variant = 'primary',
  loading = false,
  disabled = false,
  className,
  ...props
}) {
  const variants = {
    primary: 'racing-btn-primary',
    success: 'racing-btn-success',
    secondary: 'racing-btn-secondary',
    danger: 'racing-btn bg-gradient-to-r from-status-danger to-red-600 text-white',
  }

  return (
    <motion.button
      whileHover={{ scale: disabled || loading ? 1 : 1.05 }}
      whileTap={{ scale: disabled || loading ? 1 : 0.95 }}
      disabled={disabled || loading}
      className={clsx(
        variants[variant],
        disabled && 'opacity-50 cursor-not-allowed',
        className
      )}
      {...props}
    >
      {loading && <Loader2 className="inline-block w-4 h-4 mr-2 animate-spin" />}
      {children}
    </motion.button>
  )
}
