import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Flag, Search, MapPin } from 'lucide-react'
import { useState } from 'react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Tracks() {
  const [searchTerm, setSearchTerm] = useState('')

  const { data: tracks, isLoading, error } = useQuery({
    queryKey: ['tracks'],
    queryFn: async () => {
      const response = await apiEndpoints.tracks.list()
      return response.data
    },
  })

  const filteredTracks = tracks?.filter((track) =>
    track.display_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    track.venue_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    track.file_name?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  // Group tracks by venue
  const groupedTracks = {}
  filteredTracks?.forEach((track) => {
    const venue = track.venue_name || 'Autres circuits'
    if (!groupedTracks[venue]) {
      groupedTracks[venue] = []
    }
    groupedTracks[venue].push(track)
  })

  // Sort venues alphabetically
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
        <div className="relative">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-chrome-silver" />
          <input
            type="text"
            placeholder="Rechercher un circuit..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="racing-input w-full pl-12"
          />
        </div>
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
            {filteredTracks?.length || 0} circuit(s) trouvé(s) • {sortedVenues.length} localisation(s)
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
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
    >
      <Link to={`/tracks/${encodeURIComponent(track.relative_path)}`}>
        <RacingCard className="p-4 border-l-4 border-status-danger hover:border-racing-red hover:bg-carbon-gray/30 transition-all cursor-pointer">
          <div className="flex items-start gap-3">
            <Flag className="w-8 h-8 text-status-danger flex-shrink-0" />

            <div className="flex-1">
              <h4 className="font-orbitron font-bold text-white group-hover:text-racing-red">
                {track.display_name}
              </h4>

              {track.venue_name && (
                <div className="flex items-center gap-1 mt-1 text-sm text-chrome-silver">
                  <MapPin className="w-3 h-3" />
                  {track.venue_name}
                </div>
              )}

              {track.layout && (
                <div className="text-xs text-fluo-yellow mt-1">
                  {track.layout}
                </div>
              )}

              <div className="text-xs text-racing-red mt-2 font-bold">
                Voir les détails →
              </div>
            </div>
          </div>
        </RacingCard>
      </Link>
    </motion.div>
  )
}
