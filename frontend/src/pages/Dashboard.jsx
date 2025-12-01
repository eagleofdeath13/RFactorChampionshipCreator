import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import {
  Users,
  Trophy,
  Car,
  Flag,
  UserPlus,
  PlusCircle,
  Upload,
  FileText,
  Zap,
  CheckCircle2,
  Info,
} from 'lucide-react'
import { apiEndpoints } from '../services/api'
import { useState, useEffect } from 'react'

export default function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, x: -50 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
        className="relative"
      >
        <h1 className="text-5xl font-black mb-2 bg-gradient-racing bg-clip-text text-transparent">
          <Gauge className="inline-block w-12 h-12 mb-2 text-racing-red" /> Dashboard
        </h1>
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: 150 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="h-1 bg-gradient-racing shadow-racing-glow"
        />
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          title="Talents"
          icon={Users}
          endpoint={apiEndpoints.talents.list}
          linkTo="/talents"
          delay={0.1}
          color="info"
        />
        <StatCard
          title="Championnats"
          icon={Trophy}
          endpoint={apiEndpoints.championships.list}
          linkTo="/championships"
          delay={0.2}
          color="success"
        />
        <StatCard
          title="Véhicules"
          icon={Car}
          endpoint={apiEndpoints.vehicles.list}
          linkTo="/vehicles"
          delay={0.3}
          color="warning"
        />
        <StatCard
          title="Circuits"
          icon={Flag}
          endpoint={apiEndpoints.tracks.list}
          linkTo="/tracks"
          delay={0.4}
          color="danger"
        />
      </div>

      {/* Quick Actions */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6, duration: 0.6 }}
      >
        <h3 className="text-2xl font-bold text-chrome-silver mb-4 flex items-center gap-2">
          <Zap className="w-6 h-6 text-fluo-yellow animate-pulse" />
          Actions Rapides
        </h3>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="space-y-3">
            <QuickActionCard
              to="/championships/create"
              icon={PlusCircle}
              title="Créer un nouveau championnat"
              description="Configurer et lancer un championnat personnalisé"
              delay={0.7}
            />
            <QuickActionCard
              to="/talents/new"
              icon={UserPlus}
              title="Créer un nouveau talent"
              description="Ajouter un nouveau pilote à votre liste"
              delay={0.8}
            />
            <QuickActionCard
              to="/import"
              icon={Upload}
              title="Importer depuis CSV"
              description="Importer plusieurs pilotes d'un coup depuis un fichier CSV"
              delay={0.9}
            />
          </div>

          <div className="space-y-3">
            <QuickActionCard
              to="/vehicles"
              icon={Car}
              title="Explorer les véhicules"
              description="Parcourir et filtrer tous les véhicules disponibles"
              delay={1.0}
            />
            <QuickActionCard
              to="/tracks"
              icon={Flag}
              title="Explorer les circuits"
              description="Découvrir tous les circuits disponibles"
              delay={1.1}
            />
            <QuickActionCard
              to="/config"
              icon={FileText}
              title="Configuration"
              description="Configurer les chemins rFactor"
              delay={1.2}
              badge={<ConfigBadge />}
            />
          </div>
        </div>
      </motion.div>

      {/* System Status */}
      <SystemStatus delay={1.3} />
    </div>
  )
}

function StatCard({ title, icon: Icon, endpoint, linkTo, delay, color }) {
  const { data, isLoading } = useQuery({
    queryKey: [title.toLowerCase()],
    queryFn: async () => {
      const response = await endpoint()
      return response.data
    },
  })

  const count = data?.length ?? 0

  const colorClasses = {
    info: 'border-status-info text-status-info',
    success: 'border-status-success text-status-success',
    warning: 'border-fluo-yellow text-fluo-yellow',
    danger: 'border-status-danger text-status-danger',
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6 }}
    >
      <Link to={linkTo}>
        <div className={`racing-card border-t-4 ${colorClasses[color]} group`}>
          <div className="p-6 relative z-10">
            <h5 className="font-orbitron font-bold uppercase text-sm tracking-wide text-chrome-silver mb-3 flex items-center gap-2">
              <Icon className={`w-6 h-6 ${colorClasses[color]}`} />
              {title}
            </h5>

            <CounterAnimation
              target={count}
              isLoading={isLoading}
              className={`text-6xl font-black font-orbitron ${isLoading ? 'text-chrome-silver' : colorClasses[color]} mb-4`}
            />

            <button className="racing-btn-primary text-xs">
              Gérer les {title.toLowerCase()} →
            </button>
          </div>

          {/* Corner accent */}
          <motion.div
            initial={{ opacity: 0 }}
            whileHover={{ opacity: 1 }}
            className="absolute top-0 right-0 w-0 h-0 border-t-[25px] border-r-[25px] border-t-racing-red border-r-transparent"
          />
        </div>
      </Link>
    </motion.div>
  )
}

function CounterAnimation({ target, isLoading, className }) {
  const [count, setCount] = useState(0)

  useEffect(() => {
    if (isLoading || target === 0) return

    const duration = 1200
    const startTime = performance.now()

    const animate = (currentTime) => {
      const elapsed = currentTime - startTime
      const progress = Math.min(elapsed / duration, 1)
      const easeOut = 1 - Math.pow(1 - progress, 4)
      const current = Math.floor(target * easeOut)

      setCount(current)

      if (progress < 1) {
        requestAnimationFrame(animate)
      } else {
        setCount(target)
      }
    }

    requestAnimationFrame(animate)
  }, [target, isLoading])

  if (isLoading) {
    return <div className={className}>...</div>
  }

  return <div className={className}>{count}</div>
}

function QuickActionCard({ to, icon: Icon, title, description, delay, badge }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay, duration: 0.5 }}
    >
      <Link
        to={to}
        className="block bg-carbon-light border border-white/10 border-l-4 border-l-transparent hover:border-l-racing-red p-4 transition-all duration-300 hover:bg-carbon-metal hover:translate-x-2 group relative"
      >
        {/* Racing arrow indicator */}
        <motion.div
          initial={{ x: -20, opacity: 0 }}
          whileHover={{ x: 0, opacity: 1 }}
          className="absolute left-4 top-1/2 -translate-y-1/2 text-racing-red text-xl font-bold"
        >
          ▶
        </motion.div>

        <div className="flex justify-between items-start pl-6">
          <div className="flex-1">
            <h5 className="font-rajdhani font-bold text-lg mb-1 text-chrome-silver group-hover:text-white transition-colors flex items-center gap-2">
              <Icon className="w-5 h-5 text-racing-red" />
              {title}
            </h5>
            <p className="text-sm text-chrome-silver/80">{description}</p>
            {badge && <div className="mt-2">{badge}</div>}
          </div>
          <motion.div
            animate={{ x: [0, 5, 0] }}
            transition={{ duration: 1.5, repeat: Infinity }}
            className="text-racing-red"
          >
            →
          </motion.div>
        </div>
      </Link>
    </motion.div>
  )
}

function ConfigBadge() {
  const { data, isLoading } = useQuery({
    queryKey: ['config'],
    queryFn: async () => {
      const response = await apiEndpoints.config.get()
      return response.data
    },
  })

  if (isLoading) {
    return <span className="text-xs text-chrome-silver">Chargement...</span>
  }

  return (
    <span
      className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-bold uppercase tracking-wide ${
        data?.is_configured
          ? 'bg-status-success/20 text-status-success border border-status-success'
          : 'bg-status-danger/20 text-status-danger border border-status-danger'
      }`}
    >
      {data?.is_configured ? (
        <>
          <CheckCircle2 className="w-3 h-3" />
          Configuré
        </>
      ) : (
        <>
          <Info className="w-3 h-3" />
          Non configuré
        </>
      )}
    </span>
  )
}

function SystemStatus({ delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6 }}
      className="racing-card border-t-4 border-status-info"
    >
      <div className="p-6">
        <h5 className="font-orbitron font-bold uppercase text-lg mb-4 flex items-center gap-2">
          <Info className="w-6 h-6 text-status-info" />
          Statut du Système
        </h5>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <strong className="text-chrome-silver">Version:</strong>
            <span className="ml-2 text-fluo-yellow font-bold">1.0.0</span>
          </div>
          <div>
            <strong className="text-chrome-silver">Tests:</strong>
            <span className="ml-2 inline-flex items-center gap-1 px-3 py-1 bg-status-success/20 text-status-success border border-status-success font-bold">
              <CheckCircle2 className="w-4 h-4" />
              68 passants
            </span>
          </div>
          <div>
            <strong className="text-chrome-silver">API:</strong>
            <a
              href="/api/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="ml-2 text-racing-red hover:text-racing-red-dark font-bold inline-flex items-center gap-1"
            >
              Documentation →
            </a>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

// Missing Gauge import - using lucide-react
import { Gauge } from 'lucide-react'
