import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Car, Search, SlidersHorizontal, X } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Vehicles() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [filters, setFilters] = useState({
    searchDriver: true,
    searchTeam: true,
    searchDescription: true,
  })

  const { data: vehicles, isLoading, error } = useQuery({
    queryKey: ['vehicles', searchTerm, filters],
    queryFn: async () => {
      if (searchTerm) {
        // Use advanced search API
        const params = new URLSearchParams()
        params.append('search', searchTerm)
        params.append('search_driver', filters.searchDriver)
        params.append('search_team', filters.searchTeam)
        params.append('search_description', filters.searchDescription)

        const response = await fetch(`/api/vehicles/?${params.toString()}`)
        if (!response.ok) throw new Error('Search failed')
        return response.json()
      } else {
        // Regular list
        const response = await apiEndpoints.vehicles.list()
        return response.data
      }
    },
  })

  const handleFilterChange = (name, value) => {
    setFilters((prev) => ({ ...prev, [name]: value }))
  }

  const clearFilters = () => {
    setSearchTerm('')
    setFilters({
      searchDriver: true,
      searchTeam: true,
      searchDescription: true,
    })
  }

  // Group vehicles by category
  const groupedVehicles = {}
  vehicles?.forEach((vehicle) => {
    const pathParts = vehicle.relative_path.split(/[/\\]/)
    let category = 'Unknown'
    if (pathParts.length > 0) {
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

  customCategories.sort()
  regularCategories.sort()
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
        <div className="relative mb-4">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-chrome-silver" />
          <input
            type="text"
            placeholder="Rechercher un véhicule..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12 pr-12"
          />
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className={`absolute right-4 top-1/2 -translate-y-1/2 p-2 rounded transition-colors ${
              showAdvanced
                ? 'text-racing-cyan bg-racing-cyan/10'
                : 'text-chrome-silver hover:text-racing-cyan'
            }`}
            title="Filtres avancés"
          >
            <SlidersHorizontal className="w-5 h-5" />
          </button>
        </div>

        {/* Advanced Filters */}
        <AnimatePresence>
          {showAdvanced && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3 }}
            >
              <RacingCard className="p-6 mb-4">
                <div className="flex items-center justify-between mb-4">
                  <h4 className="font-orbitron font-bold text-racing-cyan">Filtres de recherche</h4>
                  <button
                    onClick={clearFilters}
                    className="text-sm text-chrome-silver hover:text-status-danger transition-colors flex items-center gap-2"
                  >
                    <X className="w-4 h-4" />
                    Réinitialiser
                  </button>
                </div>

                <div>
                  <label className="block text-sm font-bold text-chrome-silver mb-2">
                    Rechercher dans :
                  </label>
                  <div className="flex flex-wrap gap-4">
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchDriver}
                        onChange={(e) => handleFilterChange('searchDriver', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Pilote
                    </label>
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchTeam}
                        onChange={(e) => handleFilterChange('searchTeam', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Équipe
                    </label>
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchDescription}
                        onChange={(e) => handleFilterChange('searchDescription', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Description
                    </label>
                  </div>
                </div>
              </RacingCard>
            </motion.div>
          )}
        </AnimatePresence>
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
            {vehicles?.length || 0} véhicule(s) trouvé(s) dans {sortedCategories.length} catégorie(s)
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
                  <h3 className={`font-orbitron font-bold text-xl ${isCustom ? 'text-fluo-yellow' : 'text-racing-cyan'}`}>
                    {isCustom && <span className="text-sm mr-2">🏆</span>}
                    {category}
                    <span className="ml-2 text-sm text-chrome-silver font-rajdhani">
                      ({categoryVehicles.length})
                    </span>
                  </h3>
                  {isCustom && (
                    <span className="text-xs px-2 py-1 bg-fluo-yellow/10 border border-fluo-yellow/30 rounded text-fluo-yellow">
                      Championnat Custom
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {categoryVehicles.map((vehicle, index) => (
                    <VehicleCard
                      key={`${vehicle.file_path}-${index}`}
                      vehicle={vehicle}
                      delay={index * 0.02}
                      isCustom={isCustom}
                    />
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

function VehicleCard({ vehicle, delay, isCustom }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, duration: 0.3 }}
    >
      <Link to={`/vehicles/${encodeURIComponent(vehicle.file_path)}`}>
        <RacingCard
          className={`p-4 border-l-4 hover:border-l-8 transition-all ${
            isCustom ? 'border-fluo-yellow' : 'border-status-info'
          }`}
        >
          <div className="mb-2">
            <h4 className="font-orbitron font-bold text-white truncate">
              {vehicle.display_name || vehicle.file_name}
            </h4>
            {vehicle.driver && (
              <p className="text-sm text-chrome-silver">
                <span className="text-racing-cyan">Pilote:</span> {vehicle.driver}
              </p>
            )}
            {vehicle.team && (
              <p className="text-sm text-chrome-silver truncate">
                <span className="text-racing-cyan">Équipe:</span> {vehicle.team}
              </p>
            )}
          </div>

          {vehicle.classes && (
            <div className="mt-2 pt-2 border-t border-white/10">
              <span className="text-xs text-chrome-silver/70">Classes: </span>
              <span className="text-xs text-status-info">{vehicle.classes}</span>
            </div>
          )}

          <div className="mt-2 text-xs text-chrome-silver/50 truncate">
            {vehicle.file_name}
          </div>
        </RacingCard>
      </Link>
    </motion.div>
  )
}
