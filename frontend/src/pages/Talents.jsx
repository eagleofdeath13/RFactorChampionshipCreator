import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Users, UserPlus, Search, Zap, SlidersHorizontal, X } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import RacingInput from '../components/RacingInput'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Talents() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [filters, setFilters] = useState({
    searchName: true,
    searchNationality: true,
    minSpeed: '',
    maxSpeed: '',
    minAggression: '',
    maxAggression: '',
  })

  const { data: talents, isLoading, error } = useQuery({
    queryKey: ['talents', searchTerm, filters],
    queryFn: async () => {
      if (searchTerm || filters.minSpeed || filters.maxSpeed || filters.minAggression || filters.maxAggression) {
        // Use advanced search API
        const params = new URLSearchParams()
        if (searchTerm) {
          params.append('q', searchTerm)
          params.append('search_name', filters.searchName)
          params.append('search_nationality', filters.searchNationality)
        }
        if (filters.minSpeed) params.append('min_speed', filters.minSpeed)
        if (filters.maxSpeed) params.append('max_speed', filters.maxSpeed)
        if (filters.minAggression) params.append('min_aggression', filters.minAggression)
        if (filters.maxAggression) params.append('max_aggression', filters.maxAggression)

        const response = await fetch(`/api/talents/search/?${params.toString()}`)
        if (!response.ok) throw new Error('Search failed')
        return response.json()
      } else {
        // Regular list
        const response = await apiEndpoints.talents.list()
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
      searchName: true,
      searchNationality: true,
      minSpeed: '',
      maxSpeed: '',
      minAggression: '',
      maxAggression: '',
    })
  }

  const hasActiveFilters = filters.minSpeed || filters.maxSpeed || filters.minAggression || filters.maxAggression

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
        <div className="relative mb-4">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-chrome-silver" />
          <input
            type="text"
            placeholder="Rechercher un talent..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12 pr-12"
          />
          <button
            onClick={() => setShowAdvanced(!showAdvanced)}
            className={`absolute right-4 top-1/2 -translate-y-1/2 p-2 rounded transition-colors ${
              showAdvanced || hasActiveFilters
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
                  <h4 className="font-orbitron font-bold text-racing-cyan">Filtres avancés</h4>
                  {hasActiveFilters && (
                    <button
                      onClick={clearFilters}
                      className="text-sm text-chrome-silver hover:text-status-danger transition-colors flex items-center gap-2"
                    >
                      <X className="w-4 h-4" />
                      Réinitialiser
                    </button>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-bold text-chrome-silver mb-2">
                      Rechercher dans :
                    </label>
                    <div className="flex gap-4">
                      <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.searchName}
                          onChange={(e) => handleFilterChange('searchName', e.target.checked)}
                          className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                        />
                        Nom
                      </label>
                      <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                        <input
                          type="checkbox"
                          checked={filters.searchNationality}
                          onChange={(e) => handleFilterChange('searchNationality', e.target.checked)}
                          className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                        />
                        Nationalité
                      </label>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-bold text-chrome-silver mb-2">Vitesse</label>
                    <div className="flex gap-2">
                      <RacingInput
                        type="number"
                        placeholder="Min"
                        value={filters.minSpeed}
                        onChange={(e) => handleFilterChange('minSpeed', e.target.value)}
                        min="0"
                        max="100"
                      />
                      <RacingInput
                        type="number"
                        placeholder="Max"
                        value={filters.maxSpeed}
                        onChange={(e) => handleFilterChange('maxSpeed', e.target.value)}
                        min="0"
                        max="100"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-bold text-chrome-silver mb-2">Agressivité</label>
                    <div className="flex gap-2">
                      <RacingInput
                        type="number"
                        placeholder="Min"
                        value={filters.minAggression}
                        onChange={(e) => handleFilterChange('minAggression', e.target.value)}
                        min="0"
                        max="100"
                      />
                      <RacingInput
                        type="number"
                        placeholder="Max"
                        value={filters.maxAggression}
                        onChange={(e) => handleFilterChange('maxAggression', e.target.value)}
                        min="0"
                        max="100"
                      />
                    </div>
                  </div>
                </div>
              </RacingCard>
            </motion.div>
          )}
        </AnimatePresence>
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
      ) : talents?.length === 0 ? (
        <RacingCard className="p-12 text-center">
          <Users className="w-16 h-16 mx-auto mb-4 text-chrome-silver opacity-50" />
          <h3 className="text-xl font-orbitron font-bold text-chrome-silver mb-2">
            Aucun talent trouvé
          </h3>
          <p className="text-chrome-silver/70 mb-4">
            {searchTerm || hasActiveFilters ? 'Essayez une autre recherche' : 'Commencez par créer votre premier talent'}
          </p>
          {!searchTerm && !hasActiveFilters && (
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
            {talents.length} talent{talents.length > 1 ? 's' : ''} trouvé{talents.length > 1 ? 's' : ''}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {talents.map((talent, index) => (
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
      <div className="text-xs text-chrome-silver mb-1">{label}</div>
      <div className="bg-dark-secondary rounded-full h-2 overflow-hidden">
        <div
          className={`h-full ${color} bg-current transition-all duration-500`}
          style={{ width: `${Math.min(value, 100)}%` }}
        />
      </div>
      <div className={`text-xs ${color} font-bold mt-1`}>{value.toFixed(0)}</div>
    </div>
  )
}
