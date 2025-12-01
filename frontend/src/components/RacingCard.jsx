import { motion } from 'framer-motion'
import clsx from 'clsx'

export default function RacingCard({
  children,
  className,
  hover = true,
  borderColor = 'border-white/10',
  cornerAccent = false,
  ...props
}) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={hover ? { y: -8, scale: 1.02 } : {}}
      className={clsx(
        'racing-card',
        borderColor,
        className
      )}
      {...props}
    >
      {children}

      {cornerAccent && (
        <motion.div
          initial={{ opacity: 0 }}
          whileHover={{ opacity: 1 }}
          className="absolute top-0 right-0 w-0 h-0 border-t-[25px] border-r-[25px] border-t-racing-red border-r-transparent"
        />
      )}
    </motion.div>
  )
}
