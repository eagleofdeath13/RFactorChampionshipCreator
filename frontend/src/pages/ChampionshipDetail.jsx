import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Trophy, ArrowLeft, Users, Car, Flag, Settings, BarChart3, Medal, Target } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ChampionshipDetail() {
  const { name } = useParams()

  const { data: championship, isLoading, error } = useQuery({
    queryKey: ['championship', name],
    queryFn: async () => {
      const response = await apiEndpoints.championships.get(name)
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner message="Chargement du championnat..." />
  }

  if (error) {
    return (
      <div>
        <PageHeader
          icon={Trophy}
          title="Championnat non trouvé"
          subtitle="Le championnat demandé n'existe pas"
        />
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
          <Link to="/championships" className="mt-4 inline-block">
            <RacingButton variant="secondary">
              <ArrowLeft className="inline-block w-4 h-4 mr-2" />
              Retour à la liste
            </RacingButton>
          </Link>
        </RacingCard>
      </div>
    )
  }

  const statusLabels = ['Non démarré', 'Inconnu', 'En cours']
  const statusColors = ['bg-gray-500', 'bg-yellow-500', 'bg-racing-red']

  return (
    <div>
      <PageHeader
        icon={Trophy}
        title={championship.name}
        subtitle={`Statut: ${statusLabels[championship.status] || 'Inconnu'} • Course ${championship.current_race + 1}`}
        actions={
          <Link to="/championships">
            <RacingButton variant="secondary">
              <ArrowLeft className="inline-block w-4 h-4 mr-2" />
              Retour
            </RacingButton>
          </Link>
        }
      />

      {/* Basic Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <RacingCard className="p-6 mb-6">
          <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
            <Trophy className="w-6 h-6 text-fluo-yellow" />
            Informations générales
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-chrome-silver text-sm">Statut</p>
              <span className={`inline-block px-3 py-1 rounded-full text-white text-sm font-bold ${statusColors[championship.status]}`}>
                {statusLabels[championship.status]}
              </span>
            </div>
            <div>
              <p className="text-chrome-silver text-sm">Course actuelle</p>
              <p className="text-white font-bold">{championship.current_race + 1}</p>
            </div>
          </div>
        </RacingCard>
      </motion.div>

      {/* Player Info */}
      {championship.player && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
              <Target className="w-6 h-6 text-fluo-green" />
              Joueur
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <p className="text-chrome-silver text-sm">Nom</p>
                <p className="text-white font-bold">{championship.player.name}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Points</p>
                <p className="text-fluo-green font-bold text-2xl">{championship.player.season_points}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Position</p>
                <p className="text-white font-bold text-2xl">#{championship.player.points_position}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Poles</p>
                <p className="text-white font-bold">{championship.player.poles_taken}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Véhicule</p>
                <p className="text-chrome-silver font-mono text-xs">{championship.player.veh_file || 'N/A'}</p>
              </div>
            </div>
          </RacingCard>
        </motion.div>
      )}

      {/* Game Options */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
      >
        <RacingCard className="p-6 mb-6">
          <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
            <Settings className="w-6 h-6 text-racing-red" />
            Options de jeu
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <p className="text-chrome-silver text-sm">Tours par course</p>
              <p className="text-white font-bold">{championship.game_options.race_laps}</p>
            </div>
            <div>
              <p className="text-chrome-silver text-sm">Force IA</p>
              <p className="text-white font-bold">{championship.game_options.ai_strength}%</p>
            </div>
            <div>
              <p className="text-chrome-silver text-sm">Opposants</p>
              <p className="text-white font-bold">{championship.game_options.opponents}</p>
            </div>
            <div>
              <p className="text-chrome-silver text-sm">Dégâts</p>
              <p className="text-white font-bold">{championship.game_options.damage_multiplier}%</p>
            </div>
          </div>
        </RacingCard>
      </motion.div>

      {/* Opponents */}
      {championship.opponents && championship.opponents.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
              <Users className="w-6 h-6 text-fluo-blue" />
              Opposants ({championship.opponents.length})
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-carbon-gray">
                    <th className="text-left py-2 px-3 text-chrome-silver text-sm font-rajdhani">#</th>
                    <th className="text-left py-2 px-3 text-chrome-silver text-sm font-rajdhani">Nom</th>
                    <th className="text-left py-2 px-3 text-chrome-silver text-sm font-rajdhani">Points</th>
                    <th className="text-left py-2 px-3 text-chrome-silver text-sm font-rajdhani">Position</th>
                    <th className="text-left py-2 px-3 text-chrome-silver text-sm font-rajdhani">Poles</th>
                  </tr>
                </thead>
                <tbody>
                  {championship.opponents
                    .sort((a, b) => (a.points_position || 99) - (b.points_position || 99))
                    .map((opp) => (
                      <tr key={opp.opponent_id} className="border-b border-carbon-gray/30 hover:bg-carbon-gray/20">
                        <td className="py-2 px-3 text-chrome-silver">{opp.opponent_id}</td>
                        <td className="py-2 px-3">
                          <Link
                            to={`/talents/${encodeURIComponent(opp.name)}`}
                            className="text-white hover:text-racing-red font-bold"
                          >
                            {opp.name}
                          </Link>
                        </td>
                        <td className="py-2 px-3 text-fluo-green font-bold">{opp.season_points}</td>
                        <td className="py-2 px-3 text-white font-bold">
                          {opp.points_position ? `#${opp.points_position}` : 'N/A'}
                        </td>
                        <td className="py-2 px-3 text-white">{opp.poles_taken}</td>
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </RacingCard>
        </motion.div>
      )}

      {/* Track Stats */}
      {championship.track_stats && championship.track_stats.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.4 }}
        >
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
              <Flag className="w-6 h-6 text-fluo-yellow" />
              Circuits du championnat ({championship.track_stats.length})
            </h3>
            <div className="space-y-2">
              {championship.track_stats.map((track, index) => {
                const isCurrent = index === championship.current_race
                const isPast = index < championship.current_race
                let statusBadge = 'bg-gray-500 text-white'
                let statusText = 'À venir'

                if (isCurrent) {
                  statusBadge = 'bg-racing-red text-white'
                  statusText = 'En cours'
                } else if (isPast) {
                  statusBadge = 'bg-fluo-green text-dark-bg'
                  statusText = 'Terminée'
                }

                return (
                  <div
                    key={index}
                    className={`p-3 rounded-lg ${isCurrent ? 'bg-racing-red/10 border border-racing-red' : 'bg-carbon-gray/20'}`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-chrome-silver font-bold text-lg">#{index + 1}</span>
                        <div>
                          <p className="text-white font-bold">{track.track_name || 'N/A'}</p>
                          <p className="text-chrome-silver text-sm font-mono">{track.track_file}</p>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${statusBadge}`}>
                        {statusText}
                      </span>
                    </div>
                  </div>
                )
              })}
            </div>
          </RacingCard>
        </motion.div>
      )}

      {/* Career Stats */}
      {championship.career_stats && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.5 }}
        >
          <RacingCard className="p-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
              <BarChart3 className="w-6 h-6 text-fluo-blue" />
              Statistiques carrière
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              <div>
                <p className="text-chrome-silver text-sm">Expérience</p>
                <p className="text-white font-bold">{championship.career_stats.experience}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Total courses</p>
                <p className="text-white font-bold">{championship.career_stats.total_races}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Victoires</p>
                <p className="text-fluo-green font-bold">{championship.career_stats.total_wins}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Poles</p>
                <p className="text-fluo-yellow font-bold">{championship.career_stats.total_poles}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Total points</p>
                <p className="text-white font-bold">{championship.career_stats.total_points_scored}</p>
              </div>
              <div>
                <p className="text-chrome-silver text-sm">Championnats</p>
                <p className="text-racing-red font-bold">{championship.career_stats.total_championships}</p>
              </div>
            </div>
          </RacingCard>
        </motion.div>
      )}
    </div>
  )
}
