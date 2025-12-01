import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Trophy, PlusCircle, Search, Calendar, Flag } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Championships() {
  const [searchTerm, setSearchTerm] = useState('')

  const { data: championships, isLoading, error } = useQuery({
    queryKey: ['championships'],
    queryFn: async () => {
      const response = await apiEndpoints.championships.list()
      return response.data
    },
  })

  const filteredChampionships = championships?.filter((champ) =>
    champ.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div>
      <PageHeader
        icon={Trophy}
        title="Championnats"
        subtitle="Gérez et créez vos championnats personnalisés"
        actions={
          <Link to="/championships/create">
            <RacingButton variant="success">
              <PlusCircle className="inline-block w-5 h-5 mr-2" />
              Nouveau Championnat
            </RacingButton>
          </Link>
        }
      />

      {/* Search */}
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
            placeholder="Rechercher un championnat..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12"
          />
        </div>
      </motion.div>

      {/* Championships Grid */}
      {isLoading ? (
        <LoadingSpinner message="Chargement des championnats..." />
      ) : error ? (
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">
            Erreur : {error.message}
          </p>
        </RacingCard>
      ) : filteredChampionships?.length === 0 ? (
        <RacingCard className="p-12 text-center">
          <Trophy className="w-16 h-16 mx-auto mb-4 text-chrome-silver opacity-50" />
          <h3 className="text-xl font-orbitron font-bold text-chrome-silver mb-2">
            Aucun championnat trouvé
          </h3>
          <p className="text-chrome-silver/70 mb-4">
            {searchTerm ? 'Essayez une autre recherche' : 'Créez votre premier championnat'}
          </p>
          {!searchTerm && (
            <Link to="/championships/create">
              <RacingButton variant="success">
                <PlusCircle className="inline-block w-5 h-5 mr-2" />
                Créer un Championnat
              </RacingButton>
            </Link>
          )}
        </RacingCard>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredChampionships.map((champ, index) => (
            <ChampionshipCard key={champ.name} championship={champ} delay={index * 0.05} />
          ))}
        </div>
      )}
    </div>
  )
}

function ChampionshipCard({ championship, delay }) {
  const isRFM = championship.is_rfm || championship.type === 'RFM'
  const isCustom = championship.is_custom

  // Status mapping
  const statusMap = {
    '-1': { text: 'Non démarré', color: 'text-chrome-silver' },
    '0': { text: 'En attente', color: 'text-fluo-yellow' },
    '1': { text: 'En cours', color: 'text-status-info' },
    '2': { text: 'Terminé', color: 'text-status-success' },
  }
  const status = statusMap[championship.status] || statusMap['-1']

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.5 }}
    >
      <RacingCard
        cornerAccent
        className={`p-6 border-t-4 ${isRFM ? 'border-status-info' : 'border-status-success'}`}
      >
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1">
            <h3 className="font-orbitron font-bold text-xl text-white mb-2">
              {championship.name}
            </h3>

            <div className="flex gap-2 flex-wrap">
              {/* RFM/CCH Badge */}
              <span className={`inline-block px-2 py-1 text-xs font-bold ${
                isRFM
                  ? 'bg-status-info/20 text-status-info border border-status-info'
                  : 'bg-status-success/20 text-status-success border border-status-success'
              } uppercase tracking-wide`}>
                {isRFM ? 'Définition (RFM)' : 'Progression (CCH)'}
              </span>

              {/* Custom Badge */}
              {isCustom && (
                <span className="inline-block px-2 py-1 text-xs font-bold bg-fluo-yellow/20 text-fluo-yellow border border-fluo-yellow uppercase tracking-wide">
                  Custom
                </span>
              )}
            </div>
          </div>

          <Trophy className={`w-8 h-8 ${isRFM ? 'text-status-info' : 'text-status-success'}`} />
        </div>

        <div className="space-y-2 text-sm">
          {/* Status */}
          <div className={`flex items-center gap-2 font-bold ${status.color}`}>
            <span>● {status.text}</span>
          </div>

          {/* Player (only for CCH) */}
          {!isRFM && championship.player && championship.player !== 'N/A' && (
            <div className="flex items-center gap-2 text-chrome-silver">
              <span>Joueur : <span className="text-white font-bold">{championship.player}</span></span>
            </div>
          )}

          {/* Tracks count */}
          {championship.num_tracks != null && championship.num_tracks > 0 && (
            <div className="flex items-center gap-2 text-chrome-silver">
              <Flag className="w-4 h-4" />
              <span>{championship.num_tracks} circuit(s)</span>
            </div>
          )}

          {/* Current race and points (for CCH in progress) */}
          {!isRFM && championship.current_race > 0 && (
            <div className="flex items-center gap-2 text-chrome-silver">
              <Calendar className="w-4 h-4" />
              <span>Course {championship.current_race} - {championship.player_points} pts</span>
            </div>
          )}

          {/* Opponents (for CCH) */}
          {!isRFM && championship.opponents > 0 && (
            <div className="flex items-center gap-2 text-chrome-silver">
              <span>{championship.opponents} adversaire(s)</span>
            </div>
          )}
        </div>

        <div className="mt-4 pt-4 border-t border-white/10">
          <Link to={`/championships/${encodeURIComponent(championship.filename)}`}>
            <span className="text-sm text-racing-red hover:text-racing-red-dark font-bold">
              Voir les détails →
            </span>
          </Link>
        </div>
      </RacingCard>
    </motion.div>
  )
}
