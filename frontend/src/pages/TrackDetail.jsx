import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Flag, ArrowLeft, MapPin, Info, Gauge } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function TrackDetail() {
  const { path } = useParams()

  const { data: track, isLoading, error } = useQuery({
    queryKey: ['track', path],
    queryFn: async () => {
      const response = await apiEndpoints.tracks.get(path)
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner message="Chargement du circuit..." />
  }

  if (error) {
    return (
      <div>
        <PageHeader
          icon={Flag}
          title="Circuit non trouvé"
          subtitle="Le circuit demandé n'existe pas"
        />
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
          <Link to="/tracks" className="mt-4 inline-block">
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
        icon={Flag}
        title={track.display_name}
        subtitle={track.venue_name || 'Circuit'}
        actions={
          <Link to="/tracks">
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
            <Info className="w-6 h-6 text-fluo-yellow" />
            Informations du circuit
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <p className="text-chrome-silver text-sm mb-1">Nom complet</p>
              <p className="text-white font-bold text-lg">{track.display_name}</p>
            </div>

            {track.venue_name && (
              <div>
                <p className="text-chrome-silver text-sm mb-1">Localisation</p>
                <div className="flex items-center gap-2">
                  <MapPin className="w-5 h-5 text-fluo-green" />
                  <p className="text-white font-bold text-lg">{track.venue_name}</p>
                </div>
              </div>
            )}

            {track.layout && (
              <div>
                <p className="text-chrome-silver text-sm mb-1">Configuration</p>
                <p className="text-fluo-yellow font-bold">{track.layout}</p>
              </div>
            )}

            {track.file_name && (
              <div>
                <p className="text-chrome-silver text-sm mb-1">Fichier</p>
                <p className="text-chrome-silver font-mono text-sm">{track.file_name}</p>
              </div>
            )}
          </div>
        </RacingCard>
      </motion.div>

      {/* Track Details */}
      {track.length && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.1 }}
        >
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-2">
              <Gauge className="w-6 h-6 text-racing-red" />
              Caractéristiques
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {track.length && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Longueur</p>
                  <p className="text-white font-bold text-2xl">{track.length} m</p>
                </div>
              )}

              {track.pit_spots && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Emplacements stand</p>
                  <p className="text-white font-bold text-2xl">{track.pit_spots}</p>
                </div>
              )}

              {track.racing_condition && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Condition de course</p>
                  <p className="text-white font-bold">{track.racing_condition}</p>
                </div>
              )}
            </div>
          </RacingCard>
        </motion.div>
      )}

      {/* Sky Configuration */}
      {(track.sky_boxa || track.sky_boxb || track.sky_boxc) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
        >
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4">
              Configuration météo
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {track.sky_boxa && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Sky Box A</p>
                  <p className="text-white">{track.sky_boxa}</p>
                </div>
              )}
              {track.sky_boxb && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Sky Box B</p>
                  <p className="text-white">{track.sky_boxb}</p>
                </div>
              )}
              {track.sky_boxc && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Sky Box C</p>
                  <p className="text-white">{track.sky_boxc}</p>
                </div>
              )}
            </div>
          </RacingCard>
        </motion.div>
      )}

      {/* AI Configuration */}
      {(track.ai_dry_grip || track.ai_wet_grip || track.ai_min_corridor_width || track.ai_max_corridor_width) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.3 }}
        >
          <RacingCard className="p-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-4">
              Configuration IA
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {track.ai_dry_grip && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Adhérence piste sèche</p>
                  <p className="text-white font-bold">{track.ai_dry_grip}</p>
                </div>
              )}
              {track.ai_wet_grip && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Adhérence piste mouillée</p>
                  <p className="text-white font-bold">{track.ai_wet_grip}</p>
                </div>
              )}
              {track.ai_min_corridor_width && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Largeur couloir min</p>
                  <p className="text-white font-bold">{track.ai_min_corridor_width} m</p>
                </div>
              )}
              {track.ai_max_corridor_width && (
                <div>
                  <p className="text-chrome-silver text-sm mb-1">Largeur couloir max</p>
                  <p className="text-white font-bold">{track.ai_max_corridor_width} m</p>
                </div>
              )}
            </div>
          </RacingCard>
        </motion.div>
      )}
    </div>
  )
}
