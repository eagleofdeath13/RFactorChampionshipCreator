import { NavLink } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Trophy,
  Users,
  Car,
  Flag,
  Upload,
  Settings,
  Gauge,
  Book,
} from 'lucide-react'

const navItems = [
  { to: '/', label: 'Dashboard', icon: Gauge },
  { to: '/talents', label: 'Talents', icon: Users },
  { to: '/championships', label: 'Championnats', icon: Trophy },
  { to: '/vehicles', label: 'Véhicules', icon: Car },
  { to: '/tracks', label: 'Circuits', icon: Flag },
  { to: '/import', label: 'Import CSV', icon: Upload },
]

const secondaryNavItems = [
  { to: '/config', label: 'Configuration', icon: Settings },
  { to: '/api/docs', label: 'API Docs', icon: Book, external: true },
]

export default function Navigation() {
  return (
    <nav className="sticky top-0 z-50 bg-gradient-carbon border-b-4 border-racing-red shadow-deep backdrop-blur-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between py-4">
          {/* Brand */}
          <NavLink to="/" className="flex items-center gap-3 group">
            <motion.div
              animate={{
                rotate: [0, -5, 0],
                y: [0, -5, 0],
              }}
              transition={{
                duration: 3,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            >
              <Trophy className="w-8 h-8 text-racing-red" />
            </motion.div>
            <span className="font-orbitron font-black text-xl uppercase tracking-wide text-white group-hover:text-racing-red transition-colors">
              rFactor Championship Creator
            </span>
          </NavLink>

          {/* Main Navigation */}
          <div className="flex items-center gap-2">
            {navItems.map((item) => (
              <NavItem key={item.to} {...item} />
            ))}

            {/* Separator */}
            <div className="w-px h-8 bg-white/20 mx-2" />

            {/* Secondary Navigation */}
            {secondaryNavItems.map((item) => (
              <NavItem key={item.to} {...item} />
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

function NavItem({ to, label, icon: Icon, external = false }) {
  const baseClassName =
    'group relative flex items-center gap-2 px-4 py-2 font-rajdhani font-semibold text-sm uppercase tracking-wide transition-all duration-300'
  const inactiveClassName = 'text-chrome-silver hover:text-white'
  const activeClassName = 'text-white'

  if (external) {
    return (
      <a
        href={to}
        target="_blank"
        rel="noopener noreferrer"
        className={`${baseClassName} ${inactiveClassName}`}
      >
        <Icon className="w-5 h-5 group-hover:animate-pulse" />
        <span>{label}</span>
      </a>
    )
  }

  return (
    <NavLink
      to={to}
      className={({ isActive }) =>
        `${baseClassName} ${isActive ? activeClassName : inactiveClassName}`
      }
    >
      {({ isActive }) => (
        <>
          <Icon className={`w-5 h-5 ${isActive ? 'text-racing-red' : 'group-hover:text-racing-red'} transition-colors`} />
          <span>{label}</span>

          {/* Active indicator */}
          <motion.div
            initial={false}
            animate={{
              scaleX: isActive ? 1 : 0,
            }}
            transition={{ duration: 0.3 }}
            className="absolute bottom-0 left-0 w-full h-1 bg-racing-red origin-left"
          />

          {/* Hover glow effect */}
          {isActive && (
            <motion.div
              animate={{
                opacity: [0.5, 0.8, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
              className="absolute inset-0 bg-racing-red/10 -z-10 blur-xl"
            />
          )}
        </>
      )}
    </NavLink>
  )
}
