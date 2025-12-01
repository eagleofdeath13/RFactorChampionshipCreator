import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Car, ArrowLeft, Wrench, Users, Palette, Info } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'

export default function VehicleDetail() {
  const { path } = useParams()

  const { data: vehicle, isLoading, error } = useQuery({
    queryKey: ['vehicle', path],
    queryFn: async () => {
      const response = await apiEndpoints.vehicles.get(path)
      return response.data
    },
  })

  if (isLoading) {
    return <LoadingSpinner message="Chargement du véhicule..." />
  }

  if (error) {
    return (
      <div>
        <PageHeader
          icon={Car}
          title="Véhicule non trouvé"
          subtitle="Le véhicule demandé n'existe pas"
        />
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
          <Link to="/vehicles" className="mt-4 inline-block">
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
        icon={Car}
        title={vehicle.description || 'Véhicule'}
        subtitle={vehicle.classes || 'Sans catégorie'}
        actions={
          <Link to="/vehicles">
            <RacingButton variant="secondary">
              <ArrowLeft className="inline-block w-4 h-4 mr-2" />
              Retour
            </RacingButton>
          </Link>
        }
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Info */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="lg:col-span-2 space-y-6"
        >
          {/* General Info */}
          <RacingCard className="p-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-6 flex items-center gap-2">
              <Info className="w-6 h-6 text-racing-red" />
              Informations générales
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <InfoItem label="Description" value={vehicle.description || 'N/A'} />
              <InfoItem label="Catégorie" value={vehicle.category || 'N/A'} />
              <InfoItem label="Classes" value={vehicle.classes || 'N/A'} />
              <InfoItem label="Numéro" value={vehicle.number || 'N/A'} />
              <InfoItem label="Fichier" value={vehicle.file_name || 'N/A'} />
            </div>
          </RacingCard>

          {/* Team Info */}
          {vehicle.team && (
            <RacingCard className="p-6">
              <h3 className="text-xl font-orbitron font-bold text-white mb-6 flex items-center gap-2">
                <Users className="w-6 h-6 text-status-info" />
                Informations équipe
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <InfoItem label="Équipe" value={vehicle.team} />
                {vehicle.manufacturer && (
                  <InfoItem label="Constructeur" value={vehicle.manufacturer} />
                )}
                {vehicle.full_team_name && (
                  <InfoItem label="Nom complet" value={vehicle.full_team_name} span2 />
                )}
              </div>
            </RacingCard>
          )}

          {/* Paint/Livery */}
          {(vehicle.default_livery || vehicle.alternate_livery) && (
            <RacingCard className="p-6">
              <h3 className="text-xl font-orbitron font-bold text-white mb-6 flex items-center gap-2">
                <Palette className="w-6 h-6 text-fluo-yellow" />
                Livrées
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {vehicle.default_livery && (
                  <InfoItem label="Livrée par défaut" value={vehicle.default_livery} />
                )}
                {vehicle.alternate_livery && (
                  <InfoItem label="Livrée alternative" value={vehicle.alternate_livery} />
                )}
                {vehicle.pit_crew_livery && (
                  <InfoItem label="Livrée équipe stand" value={vehicle.pit_crew_livery} />
                )}
                {vehicle.track_livery && (
                  <InfoItem label="Livrée circuit" value={vehicle.track_livery} />
                )}
              </div>
            </RacingCard>
          )}

          {/* Technical Specs */}
          {(vehicle.engine || vehicle.hdv_file || vehicle.tbc_file) && (
            <RacingCard className="p-6">
              <h3 className="text-xl font-orbitron font-bold text-white mb-6 flex items-center gap-2">
                <Wrench className="w-6 h-6 text-status-success" />
                Spécifications techniques
              </h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {vehicle.engine && (
                  <InfoItem label="Moteur" value={vehicle.engine} />
                )}
                {vehicle.hdv_file && (
                  <InfoItem label="Fichier HDV" value={vehicle.hdv_file} />
                )}
                {vehicle.tbc_file && (
                  <InfoItem label="Fichier TBC" value={vehicle.tbc_file} />
                )}
                {vehicle.sounds_file && (
                  <InfoItem label="Fichier sons" value={vehicle.sounds_file} />
                )}
                {vehicle.spinner_file && (
                  <InfoItem label="Fichier spinner" value={vehicle.spinner_file} />
                )}
                {vehicle.gen_string && (
                  <InfoItem label="Gen string" value={vehicle.gen_string} />
                )}
              </div>
            </RacingCard>
          )}
        </motion.div>

        {/* Sidebar */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="space-y-6"
        >
          {/* Category Card */}
          {vehicle.category && (
            <RacingCard className="p-6 border-l-4 border-racing-red">
              <div className="flex items-center gap-3">
                <Car className="w-8 h-8 text-racing-red" />
                <div>
                  <div className="text-sm text-chrome-silver">Catégorie</div>
                  <div className="font-orbitron font-bold text-white text-lg">
                    {vehicle.category}
                  </div>
                </div>
              </div>
            </RacingCard>
          )}

          {/* Classes Card */}
          {vehicle.classes && (
            <RacingCard className="p-6 border-l-4 border-status-info">
              <div>
                <div className="text-sm text-chrome-silver mb-2">Classes</div>
                <div className="flex flex-wrap gap-2">
                  {vehicle.classes.split(' ').map((cls, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-status-info/20 text-status-info border border-status-info text-xs font-bold uppercase tracking-wide"
                    >
                      {cls}
                    </span>
                  ))}
                </div>
              </div>
            </RacingCard>
          )}

          {/* Number Card */}
          {vehicle.number && (
            <RacingCard className="p-6 border-l-4 border-fluo-yellow text-center">
              <div className="text-sm text-chrome-silver mb-2">Numéro de course</div>
              <div className="text-6xl font-orbitron font-black text-fluo-yellow">
                {vehicle.number}
              </div>
            </RacingCard>
          )}

          {/* Team Card */}
          {vehicle.team && (
            <RacingCard className="p-6 border-l-4 border-status-success">
              <div className="flex items-center gap-3">
                <Users className="w-8 h-8 text-status-success" />
                <div>
                  <div className="text-sm text-chrome-silver">Équipe</div>
                  <div className="font-orbitron font-bold text-white text-lg">
                    {vehicle.team}
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

function InfoItem({ label, value, span2 = false }) {
  return (
    <div className={`border-l-2 border-white/10 pl-3 ${span2 ? 'md:col-span-2' : ''}`}>
      <div className="text-xs text-chrome-silver uppercase tracking-wide mb-1">
        {label}
      </div>
      <div className="font-rajdhani font-semibold text-white break-words">
        {value}
      </div>
    </div>
  )
}
