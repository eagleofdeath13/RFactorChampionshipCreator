import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Car, Search } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Vehicles() {
  const [searchTerm, setSearchTerm] = useState('')

  const { data: vehicles, isLoading, error } = useQuery({
    queryKey: ['vehicles'],
    queryFn: async () => {
      const response = await apiEndpoints.vehicles.list()
      return response.data
    },
  })

  const filteredVehicles = vehicles?.filter((vehicle) =>
    vehicle.team_info?.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.file_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.team_info?.classes?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div>
      <PageHeader
        icon={Car}
        title="Véhicules"
        subtitle="Parcourez tous les véhicules disponibles"
      />

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
            placeholder="Rechercher un véhicule..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12"
          />
        </div>
      </motion.div>

      {isLoading ? (
        <LoadingSpinner message="Chargement des véhicules..." />
      ) : error ? (
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
        </RacingCard>
      ) : (
        <>
          <div className="mb-4 text-chrome-silver font-rajdhani">
            {filteredVehicles?.length || 0} véhicule(s) trouvé(s)
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredVehicles?.map((vehicle, index) => (
              <VehicleCard key={vehicle.relative_path} vehicle={vehicle} delay={index * 0.03} />
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function VehicleCard({ vehicle, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
    >
      <Link to={`/vehicles/${encodeURIComponent(vehicle.relative_path)}`}>
        <RacingCard className="p-4 border-l-4 border-fluo-yellow hover:border-racing-red transition-colors cursor-pointer">
          <div className="flex items-start gap-3">
            <Car className="w-8 h-8 text-fluo-yellow flex-shrink-0" />

            <div className="flex-1 min-w-0">
              <h4 className="font-rajdhani font-bold text-white truncate">
                {vehicle.team_info?.description || vehicle.file_name}
              </h4>

              {vehicle.team_info?.classes && (
                <span className="inline-block px-2 py-0.5 text-xs bg-chrome-silver/20 text-chrome-silver mt-1">
                  {vehicle.team_info.classes}
                </span>
              )}

              <p className="text-xs text-chrome-silver/60 mt-2 truncate">
                {vehicle.relative_path}
              </p>
            </div>
          </div>

          <div className="mt-3 pt-3 border-t border-white/10">
            <span className="text-xs text-chrome-silver">
              Cliquez pour plus de détails →
            </span>
          </div>
        </RacingCard>
      </Link>
    </motion.div>
  )
}
