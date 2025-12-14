import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Flag, Search, MapPin, SlidersHorizontal, X } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Tracks() {
  const [searchTerm, setSearchTerm] = useState('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [filters, setFilters] = useState({
    searchTrackName: true,
    searchVenueName: true,
    searchLayout: true,
    searchFileName: true,
  })

  const { data: tracks, isLoading, error } = useQuery({
    queryKey: ['tracks', searchTerm, filters],
    queryFn: async () => {
      if (searchTerm) {
        // Use advanced search API
        const params = new URLSearchParams()
        params.append('search', searchTerm)
        params.append('search_track_name', filters.searchTrackName)
        params.append('search_venue_name', filters.searchVenueName)
        params.append('search_layout', filters.searchLayout)
        params.append('search_file_name', filters.searchFileName)

        const response = await fetch(`/api/tracks/?${params.toString()}`)
        if (!response.ok) throw new Error('Search failed')
        return response.json()
      } else {
        // Regular list
        const response = await apiEndpoints.tracks.list()
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
      searchTrackName: true,
      searchVenueName: true,
      searchLayout: true,
      searchFileName: true,
    })
  }

  // Group tracks by venue
  const groupedTracks = {}
  tracks?.forEach((track) => {
    const venue = track.venue_name || 'Autres circuits'
    if (!groupedTracks[venue]) {
      groupedTracks[venue] = []
    }
    groupedTracks[venue].push(track)
  })

  const sortedVenues = Object.keys(groupedTracks).sort()

  return (
    <div>
      <PageHeader
        icon={Flag}
        title="Circuits"
        subtitle="Découvrez tous les circuits disponibles"
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
            placeholder="Rechercher un circuit..."
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
                        checked={filters.searchTrackName}
                        onChange={(e) => handleFilterChange('searchTrackName', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Nom du circuit
                    </label>
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchVenueName}
                        onChange={(e) => handleFilterChange('searchVenueName', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Localisation
                    </label>
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchLayout}
                        onChange={(e) => handleFilterChange('searchLayout', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Configuration
                    </label>
                    <label className="flex items-center gap-2 text-sm text-chrome-silver cursor-pointer">
                      <input
                        type="checkbox"
                        checked={filters.searchFileName}
                        onChange={(e) => handleFilterChange('searchFileName', e.target.checked)}
                        className="rounded border-racing-cyan/30 bg-dark-secondary text-racing-cyan focus:ring-racing-cyan"
                      />
                      Nom de fichier
                    </label>
                  </div>
                </div>
              </RacingCard>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {isLoading ? (
        <LoadingSpinner message="Chargement des circuits..." />
      ) : error ? (
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Erreur : {error.message}</p>
        </RacingCard>
      ) : (
        <>
          <div className="mb-6 text-chrome-silver font-rajdhani">
            {tracks?.length || 0} circuit(s) trouvé(s) • {sortedVenues.length} localisation(s)
          </div>

          {/* Grouped by venue */}
          {sortedVenues.map((venue, venueIndex) => (
            <div key={venue} className="mb-8">
              <motion.h2
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: venueIndex * 0.05 }}
                className="text-xl font-orbitron font-bold text-white mb-4 flex items-center gap-3"
              >
                <MapPin className="w-5 h-5 text-fluo-green" />
                {venue}
                <span className="text-sm font-rajdhani text-chrome-silver">
                  • {groupedTracks[venue].length} tracé(s)
                </span>
              </motion.h2>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {groupedTracks[venue].map((track, index) => (
                  <TrackCard key={track.file_name} track={track} delay={(venueIndex * 0.1) + (index * 0.03)} />
                ))}
              </div>
            </div>
          ))}
        </>
      )}
    </div>
  )
}

function TrackCard({ track, delay }) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay, duration: 0.3 }}
    >
      <Link to={`/tracks/${encodeURIComponent(track.file_path)}`}>
        <RacingCard className="p-4 border-l-4 border-fluo-green hover:border-l-8 transition-all">
          <div className="mb-2">
            <h4 className="font-orbitron font-bold text-white truncate">
              {track.display_name || track.file_name}
            </h4>
            {track.layout && track.layout !== track.display_name && (
              <p className="text-sm text-chrome-silver">
                <span className="text-fluo-green">Configuration:</span> {track.layout}
              </p>
            )}
          </div>

          {track.length && (
            <div className="mt-2 pt-2 border-t border-white/10">
              <div className="flex items-center justify-between text-xs">
                <span className="text-chrome-silver/70">Longueur</span>
                <span className="text-fluo-green font-bold">{track.length} km</span>
              </div>
            </div>
          )}

          <div className="mt-2 text-xs text-chrome-silver/50 truncate">
            {track.file_name}
          </div>
        </RacingCard>
      </Link>
    </motion.div>
  )
}
