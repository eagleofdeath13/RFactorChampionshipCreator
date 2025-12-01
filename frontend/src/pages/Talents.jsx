import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Users, UserPlus, Search, Zap } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Talents() {
  const [searchTerm, setSearchTerm] = useState('')

  const { data: talents, isLoading, error } = useQuery({
    queryKey: ['talents'],
    queryFn: async () => {
      const response = await apiEndpoints.talents.list()
      return response.data
    },
  })

  const filteredTalents = talents?.filter((talent) =>
    talent.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    talent.nationality?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div>
      <PageHeader
        icon={Users}
        title="Talents"
        subtitle="Gérez vos pilotes et leurs caractéristiques"
        actions={
          <Link to="/talents/new">
            <RacingButton variant="primary">
              <UserPlus className="inline-block w-5 h-5 mr-2" />
              Nouveau Talent
            </RacingButton>
          </Link>
        }
      />

      {/* Search Bar */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mb-6"
      >
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-chrome-silver" />
          <input
            type="text"
            placeholder="Rechercher un talent..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12"
          />
        </div>
      </motion.div>

      {/* Talents Grid */}
      {isLoading ? (
        <LoadingSpinner message="Chargement des talents..." />
      ) : error ? (
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">
            Erreur lors du chargement : {error.message}
          </p>
        </RacingCard>
      ) : filteredTalents?.length === 0 ? (
        <RacingCard className="p-12 text-center">
          <Users className="w-16 h-16 mx-auto mb-4 text-chrome-silver opacity-50" />
          <h3 className="text-xl font-orbitron font-bold text-chrome-silver mb-2">
            Aucun talent trouvé
          </h3>
          <p className="text-chrome-silver/70 mb-4">
            {searchTerm ? 'Essayez une autre recherche' : 'Commencez par créer votre premier talent'}
          </p>
          {!searchTerm && (
            <Link to="/talents/new">
              <RacingButton variant="primary">
                <UserPlus className="inline-block w-5 h-5 mr-2" />
                Créer un Talent
              </RacingButton>
            </Link>
          )}
        </RacingCard>
      ) : (
        <>
          <div className="mb-4 text-chrome-silver font-rajdhani">
            <Zap className="inline-block w-4 h-4 mr-1 text-fluo-yellow" />
            {filteredTalents.length} talent{filteredTalents.length > 1 ? 's' : ''} trouvé{filteredTalents.length > 1 ? 's' : ''}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTalents.map((talent, index) => (
              <TalentCard key={`${talent.name}-${index}`} talent={talent} delay={index * 0.05} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function TalentCard({ talent, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
    >
      <Link to={`/talents/${encodeURIComponent(talent.name)}`}>
        <RacingCard cornerAccent className="p-6 border-t-4 border-status-info">
          <div className="flex items-start justify-between mb-4">
            <div>
              <h3 className="font-orbitron font-bold text-xl text-white mb-1">
                {talent.name}
              </h3>
              <p className="text-chrome-silver text-sm">
                {talent.nationality || 'Nationalité inconnue'}
              </p>
            </div>

            <div className="text-right">
              <div className="text-3xl font-black font-orbitron text-status-info">
                {talent.speed || 0}
              </div>
              <div className="text-xs text-chrome-silver uppercase tracking-wide">
                Speed
              </div>
            </div>
          </div>

          {/* Stats Bar */}
          <div className="grid grid-cols-3 gap-2 mt-4">
            <StatBar label="Speed" value={talent.speed || 0} color="text-status-info" />
            <StatBar label="Crash" value={talent.crash || 0} color="text-status-warning" />
            <StatBar label="Aggro" value={talent.aggression || 0} color="text-status-danger" />
          </div>

          <div className="mt-4 pt-4 border-t border-white/10">
            <span className="text-xs text-chrome-silver">
              Cliquez pour plus de détails →
            </span>
          </div>
        </RacingCard>
      </Link>
    </motion.div>
  )
}

function StatBar({ label, value, color }) {
  return (
    <div>
      <div className="text-xs text-chrome-silver uppercase mb-1">{label}</div>
      <div className="h-2 bg-carbon-metal rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${value}%` }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className={`h-full ${color} bg-current`}
        />
      </div>
      <div className={`text-xs font-bold mt-1 ${color}`}>{value}</div>
    </div>
  )
}
