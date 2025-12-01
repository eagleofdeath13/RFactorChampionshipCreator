import { useQuery } from '@tanstack/react-query'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, ArrowLeft, Edit, Trash2, Flag, Zap, Target, TrendingUp } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function TalentDetail() {
  const { name } = useParams()
  const navigate = useNavigate()

  const { data: talent, isLoading, error } = useQuery({
    queryKey: ['talent', name],
    queryFn: async () => {
      const response = await apiEndpoints.talents.get(name)
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner message="Chargement du talent..." />
  }

  if (error) {
    return (
      <div>
        <PageHeader
          icon={User}
          title="Talent non trouvé"
          subtitle="Le talent demandé n'existe pas"
        />
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
          <Link to="/talents" className="mt-4 inline-block">
            <RacingButton variant="secondary">
              <ArrowLeft className="inline-block w-4 h-4 mr-2" />
              Retour à la liste
            </RacingButton>
          </Link>
        </RacingCard>
      </div>
    )
  }

  return (
    <div>
      <PageHeader
        icon={User}
        title={talent.name}
        subtitle={`${talent.nationality} • ${talent.team || 'Sans équipe'}`}
        actions={
          <div className="flex gap-3">
            <Link to="/talents">
              <RacingButton variant="secondary">
                <ArrowLeft className="inline-block w-4 h-4 mr-2" />
                Retour
              </RacingButton>
            </Link>
          </div>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Stats */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="lg:col-span-2"
        >
          <RacingCard className="p-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-6 flex items-center gap-2">
              <Zap className="w-6 h-6 text-fluo-yellow" />
              Compétences
            </h3>

            <div className="space-y-4">
              {/* Speed */}
              <StatBar
                label="Vitesse"
                value={talent.speed || 0}
                icon={Zap}
                color="racing-red"
              />

              {/* Crash */}
              <StatBar
                label="Résistance aux crashes"
                value={talent.crash || 0}
                icon={Target}
                color="status-success"
              />

              {/* Aggression */}
              <StatBar
                label="Agressivité"
                value={talent.aggression || 0}
                icon={TrendingUp}
                color="fluo-yellow"
              />
            </div>
          </RacingCard>

          {/* Additional Stats */}
          <RacingCard className="p-6 mt-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-6">
              Informations détaillées
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem label="Nom complet" value={talent.name} />
              <InfoItem label="Nationalité" value={talent.nationality} />
              <InfoItem label="Équipe" value={talent.team || 'N/A'} />
              <InfoItem label="Région" value={talent.region || 'N/A'} />
              <InfoItem label="Voiture" value={talent.car || 'N/A'} />
              <InfoItem label="Numéro" value={talent.number || 'N/A'} />

              {/* Reputation */}
              {talent.reputation != null && (
                <InfoItem label="Réputation" value={`${talent.reputation}/100`} />
              )}

              {/* Championships */}
              {talent.championships != null && (
                <InfoItem label="Championnats gagnés" value={talent.championships} />
              )}

              {/* Wins */}
              {talent.wins != null && (
                <InfoItem label="Victoires" value={talent.wins} />
              )}

              {/* Podiums */}
              {talent.podiums != null && (
                <InfoItem label="Podiums" value={talent.podiums} />
              )}

              {/* Poles */}
              {talent.poles != null && (
                <InfoItem label="Pole positions" value={talent.poles} />
              )}

              {/* Fastest laps */}
              {talent.fastest_laps != null && (
                <InfoItem label="Tours les plus rapides" value={talent.fastest_laps} />
              )}
            </div>
          </RacingCard>
        </motion.div>

        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="space-y-6"
        >
          {/* Quick Stats */}
          <RacingCard className="p-6 border-l-4 border-racing-red">
            <h4 className="font-orbitron font-bold text-white mb-4">
              Moyenne générale
            </h4>
            <div className="text-center">
              <div className="text-5xl font-orbitron font-black text-racing-red mb-2">
                {(((talent.speed || 0) + (talent.crash || 0) + (talent.aggression || 0)) / 3).toFixed(1)}
              </div>
              <div className="text-sm text-chrome-silver">/ 100</div>
            </div>
          </RacingCard>

          {/* Nationality Card */}
          <RacingCard className="p-6 border-l-4 border-status-info">
            <div className="flex items-center gap-3">
              <Flag className="w-8 h-8 text-status-info" />
              <div>
                <div className="text-sm text-chrome-silver">Nationalité</div>
                <div className="font-orbitron font-bold text-white text-lg">
                  {talent.nationality}
                </div>
              </div>
            </div>
          </RacingCard>

          {/* Team Card */}
          {talent.team && (
            <RacingCard className="p-6 border-l-4 border-fluo-yellow">
              <div className="flex items-center gap-3">
                <User className="w-8 h-8 text-fluo-yellow" />
                <div>
                  <div className="text-sm text-chrome-silver">Équipe</div>
                  <div className="font-orbitron font-bold text-white text-lg">
                    {talent.team}
                  </div>
                </div>
              </div>
            </RacingCard>
          )}
        </motion.div>
      </div>
    </div>
  )
}

function StatBar({ label, value, icon: Icon, color }) {
  const numValue = value || 0

  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2 text-chrome-silver">
          <Icon className="w-4 h-4" />
          <span className="font-rajdhani font-semibold">{label}</span>
        </div>
        <span className={`font-orbitron font-bold text-${color}`}>
          {numValue.toFixed(1)}
        </span>
      </div>
      <div className="relative h-3 bg-carbon-black rounded-full overflow-hidden border border-white/10">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${numValue}%` }}
          transition={{ duration: 1, delay: 0.3, ease: 'easeOut' }}
          className={`absolute top-0 left-0 h-full bg-gradient-to-r from-${color} to-${color}/70 rounded-full`}
          style={{
            boxShadow: `0 0 10px rgba(227, 30, 36, 0.5)`,
          }}
        />
      </div>
    </div>
  )
}

function InfoItem({ label, value }) {
  return (
    <div className="border-l-2 border-white/10 pl-3">
      <div className="text-xs text-chrome-silver uppercase tracking-wide mb-1">
        {label}
      </div>
      <div className="font-rajdhani font-semibold text-white">
        {value}
      </div>
    </div>
  )
}
