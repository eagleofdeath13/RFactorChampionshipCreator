import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Trophy, ArrowLeft, Flag, Info, Settings } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ChampionshipDetailRFM() {
  const { name } = useParams()

  const { data: championship, isLoading, error } = useQuery({
    queryKey: ['championship-rfm', name],
    queryFn: async () => {
      const response = await apiEndpoints.championships.getRfm(name)
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

  return (
    <div>
      <PageHeader
        icon={Trophy}
        title={championship.name}
        subtitle="Définition de championnat (RFM) • Prêt à lancer dans rFactor"
        actions={
          <div className="flex gap-3">
            {championship.is_custom && (
              <span className="inline-block px-3 py-1 text-xs font-bold bg-fluo-yellow/20 text-fluo-yellow border border-fluo-yellow uppercase tracking-wide">
                Custom
              </span>
            )}
            <Link to="/championships">
              <RacingButton variant="secondary">
                <ArrowLeft className="inline-block w-4 h-4 mr-2" />
                Retour
              </RacingButton>
            </Link>
          </div>
        }
      />

      {/* Basic Info */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <RacingCard className="p-6 mb-6 border-l-4 border-status-info">
          <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
            <Info className="w-6 h-6 text-status-info" />
            Informations
          </h3>
          <div className="space-y-3 text-chrome-silver">
            <p>
              Ce championnat est une <span className="text-white font-bold">définition RFM</span> prête à être lancée dans rFactor.
            </p>
            <p>
              Pour jouer ce championnat, lancez rFactor et sélectionnez "{championship.name}" dans le menu des championnats.
            </p>
            {championship.is_custom && (
              <div className="mt-4 p-3 bg-fluo-yellow/10 border border-fluo-yellow rounded">
                <p className="text-fluo-yellow text-sm">
                  <strong>Championnat personnalisé :</strong> Ce championnat a été créé via l'outil rFactor Championship Creator.
                </p>
              </div>
            )}
          </div>
        </RacingCard>
      </motion.div>

      {/* Seasons */}
      {championship.seasons && championship.seasons.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          {championship.seasons.map((season, seasonIndex) => (
            <div key={seasonIndex} className="mb-6">
              <RacingCard className="p-6">
                <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
                  <Trophy className="w-6 h-6 text-racing-red" />
                  {season.name || `Saison ${seasonIndex + 1}`}
                </h3>

                {/* Vehicle Filter */}
                {season.vehicle_filter && (
                  <div className="mb-6 p-4 bg-status-info/10 border border-status-info rounded">
                    <div className="flex items-center gap-2 mb-2">
                      <Settings className="w-5 h-5 text-status-info" />
                      <h4 className="font-orbitron font-bold text-white">Filtre de véhicules</h4>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {season.vehicle_filter.split(' ').map((filter, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-status-info/20 text-status-info border border-status-info text-xs font-bold uppercase tracking-wide"
                        >
                          {filter}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Tracks */}
                {season.tracks && season.tracks.length > 0 && (
                  <div>
                    <h4 className="font-orbitron font-bold text-white mb-3 flex items-center gap-2">
                      <Flag className="w-5 h-5 text-fluo-yellow" />
                      Circuits ({season.tracks.length})
                    </h4>
                    <div className="space-y-2">
                      {season.tracks.map((track, trackIndex) => (
                        <div
                          key={trackIndex}
                          className="p-3 rounded-lg bg-carbon-gray/20 hover:bg-carbon-gray/30 transition-colors"
                        >
                          <div className="flex items-center gap-3">
                            <span className="text-chrome-silver font-bold text-lg min-w-[40px]">
                              #{trackIndex + 1}
                            </span>
                            <div className="flex-1">
                              <p className="text-white font-bold font-rajdhani">{track}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </RacingCard>
            </div>
          ))}
        </motion.div>
      )}

      {/* Instructions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3, delay: 0.2 }}
      >
        <RacingCard className="p-6 bg-racing-red/10 border border-racing-red">
          <h3 className="text-xl font-orbitron font-bold text-white mb-4">
            Comment lancer ce championnat
          </h3>
          <ol className="space-y-2 text-chrome-silver list-decimal list-inside">
            <li>Lancez <span className="text-white font-bold">rFactor</span></li>
            <li>Sélectionnez <span className="text-white font-bold">Carrière / Championship</span></li>
            <li>Choisissez <span className="text-white font-bold">"{championship.name}"</span> dans la liste</li>
            <li>Configurez vos options et commencez à courir !</li>
          </ol>
          <p className="mt-4 text-sm text-chrome-silver/70">
            Une fois démarré, rFactor créera automatiquement un fichier .cch pour sauvegarder votre progression.
          </p>
        </RacingCard>
      </motion.div>
    </div>
  )
}
