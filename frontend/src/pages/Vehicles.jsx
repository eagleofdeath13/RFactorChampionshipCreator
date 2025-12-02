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
    vehicle.display_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.file_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.driver?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.team?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    vehicle.classes?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Group vehicles by category
  const groupedVehicles = {}
  filteredVehicles?.forEach((vehicle) => {
    // Extract category from path (e.g., GAMEDATA\VEHICLES\M_TestChampionship2025 -> M_TestChampionship2025)
    // Use both \ and / as separators (backend uses Windows paths)
    const pathParts = vehicle.relative_path.split(/[/\\]/)

    // Find the first non-empty segment (category/brand folder)
    let category = 'Unknown'
    if (pathParts.length > 0) {
      // Get first segment that's not empty
      category = pathParts.find(part => part && part.trim() !== '') || 'Unknown'
    }

    if (!groupedVehicles[category]) {
      groupedVehicles[category] = []
    }
    groupedVehicles[category].push(vehicle)
  })

  // Separate custom (M_) categories from others
  const customCategories = []
  const regularCategories = []

  Object.keys(groupedVehicles).forEach((category) => {
    if (category.startsWith('M_')) {
      customCategories.push(category)
    } else {
      regularCategories.push(category)
    }
  })

  // Sort categories alphabetically within each group
  customCategories.sort()
  regularCategories.sort()

  // Combine: custom categories first, then regular ones
  const sortedCategories = [...customCategories, ...regularCategories]

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
            {filteredVehicles?.length || 0} véhicule(s) trouvé(s) dans {sortedCategories.length} catégorie(s)
          </div>

          {/* Display categories */}
          {sortedCategories.map((category, categoryIndex) => {
            const isCustom = category.startsWith('M_')
            const categoryVehicles = groupedVehicles[category]

            return (
              <motion.div
                key={category}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: categoryIndex * 0.05 }}
                className="mb-8"
              >
                <div className="flex items-center gap-3 mb-4">
                  <h2 className={`text-2xl font-orbitron font-bold ${
                    isCustom ? 'text-fluo-yellow' : 'text-white'
                  }`}>
                    {category}
                  </h2>
                  {isCustom && (
                    <span className="inline-block px-2 py-1 text-xs font-bold bg-fluo-yellow/20 text-fluo-yellow border border-fluo-yellow uppercase tracking-wide">
                      Custom
                    </span>
                  )}
                  <span className="text-sm font-rajdhani text-chrome-silver">
                    • {categoryVehicles.length} véhicule(s)
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {categoryVehicles.map((vehicle, index) => (
                    <VehicleCard key={vehicle.relative_path} vehicle={vehicle} delay={0} />
                  ))}
                </div>
              </motion.div>
            )
          })}
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
                {vehicle.display_name}
              </h4>

              {vehicle.classes && (
                <span className="inline-block px-2 py-0.5 text-xs bg-chrome-silver/20 text-chrome-silver mt-1">
                  {vehicle.classes}
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
