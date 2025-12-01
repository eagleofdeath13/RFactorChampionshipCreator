import { motion } from 'framer-motion'

export default function PageHeader({ icon: Icon, title, subtitle, actions }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6 }}
      className="mb-8"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h1 className="text-5xl font-black mb-2 bg-gradient-racing bg-clip-text text-transparent flex items-center gap-4">
            {Icon && <Icon className="text-racing-red" size={48} />}
            {title}
          </h1>

          {subtitle && (
            <p className="text-chrome-silver font-rajdhani text-lg mt-2">
              {subtitle}
            </p>
          )}

          <motion.div
            initial={{ width: 0 }}
            animate={{ width: 150 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="h-1 bg-gradient-racing shadow-racing-glow mt-3"
          />
        </div>

        {actions && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.4 }}
            className="ml-4"
          >
            {actions}
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}
