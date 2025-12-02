import { useState, useEffect, useRef } from 'react'
import { useQuery, useQueryClient } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import clsx from 'clsx'
import { UserPlus, ChevronDown, Search, RefreshCw } from 'lucide-react'
import { apiEndpoints } from '../services/api'

/**
 * TalentSelector - Composant de sélection de pilote avec autocomplétion
 *
 * Permet de:
 * - Sélectionner un talent existant via autocomplétion
 * - Créer un nouveau talent (lien vers création)
 * - Validation stricte des noms (seuls les talents existants sont valides)
 *
 * @param {string} value - Nom du talent sélectionné
 * @param {function} onChange - Callback appelé lors de la sélection (talent object)
 * @param {string} error - Message d'erreur à afficher
 * @param {string} label - Label du champ
 * @param {boolean} required - Si le champ est requis
 * @param {array} excludedTalents - Liste des noms de talents à exclure (déjà assignés)
 */
export default function TalentSelector({ value, onChange, error, label, required, excludedTalents = [] }) {
  const [isOpen, setIsOpen] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTalent, setSelectedTalent] = useState(null)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const containerRef = useRef(null)
  const queryClient = useQueryClient()

  // Charger tous les talents avec refetch périodique
  const { data: talents = [], isLoading, refetch } = useQuery({
    queryKey: ['talents'],
    queryFn: async () => {
      const response = await apiEndpoints.talents.list()
      return response.data
    },
    refetchInterval: 5000, // Rafraîchir toutes les 5 secondes si la fenêtre est active
    refetchIntervalInBackground: false, // Ne pas rafraîchir en arrière-plan
  })

  // Rafraîchir manuellement
  const handleRefresh = async () => {
    setIsRefreshing(true)
    await refetch()
    setIsRefreshing(false)
  }

  // Filtrer les talents selon la recherche et exclure ceux déjà assignés
  const filteredTalents = talents.filter(talent => {
    const matchesSearch = talent.name.toLowerCase().includes(searchTerm.toLowerCase())
    const isNotExcluded = !excludedTalents.includes(talent.name)
    return matchesSearch && isNotExcluded
  })

  // Initialiser le talent sélectionné si une valeur est fournie
  useEffect(() => {
    if (value && talents.length > 0) {
      const talent = talents.find(t => t.name === value)
      if (talent) {
        setSelectedTalent(talent)
        setSearchTerm(talent.name)
      }
    }
  }, [value, talents])

  // Fermer le dropdown au clic extérieur
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (talent) => {
    setSelectedTalent(talent)
    setSearchTerm(talent.name)
    setIsOpen(false)
    onChange(talent)
  }

  const handleInputChange = (e) => {
    const newValue = e.target.value
    setSearchTerm(newValue)
    setIsOpen(true)

    // Si l'input est vidé, réinitialiser la sélection
    if (newValue === '') {
      setSelectedTalent(null)
      onChange(null)
    }
  }

  const handleInputFocus = () => {
    setIsOpen(true)
  }

  return (
    <div className="mb-4" ref={containerRef}>
      {label && (
        <label className="block font-orbitron font-semibold text-xs uppercase tracking-wide text-chrome-silver mb-2">
          {label}
          {required && <span className="text-racing-red ml-1">*</span>}
        </label>
      )}

      <div className="relative">
        {/* Input de recherche */}
        <div className="relative">
          <input
            type="text"
            value={searchTerm}
            onChange={handleInputChange}
            onFocus={handleInputFocus}
            placeholder="Rechercher un pilote..."
            className={clsx(
              'racing-input w-full pr-20',
              error && 'border-status-danger border-l-status-danger'
            )}
          />
          <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-2">
            {isLoading || isRefreshing ? (
              <div className="w-4 h-4 border-2 border-racing-red border-t-transparent rounded-full animate-spin" />
            ) : (
              <>
                <button
                  type="button"
                  onClick={handleRefresh}
                  className="text-chrome-silver hover:text-racing-red transition-colors"
                  title="Rafraîchir la liste"
                >
                  <RefreshCw className="w-4 h-4" />
                </button>
                <Search className="w-4 h-4 text-chrome-silver" />
                <ChevronDown
                  className={clsx(
                    'w-4 h-4 text-chrome-silver transition-transform',
                    isOpen && 'rotate-180'
                  )}
                />
              </>
            )}
          </div>
        </div>

        {/* Dropdown avec liste des talents */}
        {isOpen && !isLoading && (
          <div className="absolute z-50 w-full mt-1 bg-[#1a1a1a] border-2 border-white/20 rounded shadow-xl max-h-64 overflow-y-auto">
            {filteredTalents.length > 0 ? (
              <ul>
                {filteredTalents.map((talent) => (
                  <li key={talent.name}>
                    <button
                      type="button"
                      onClick={() => handleSelect(talent)}
                      className={clsx(
                        'w-full text-left px-4 py-3 hover:bg-racing-red/10 transition-colors border-l-2 border-transparent hover:border-racing-red',
                        selectedTalent?.name === talent.name && 'bg-racing-red/20 border-racing-red'
                      )}
                    >
                      <div className="font-orbitron font-bold text-white">
                        {talent.name}
                      </div>
                      {talent.team && (
                        <div className="text-xs text-chrome-silver mt-1">
                          {talent.team}
                        </div>
                      )}
                    </button>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="px-4 py-6 text-center bg-[#1a1a1a]">
                <p className="text-chrome-silver mb-3">
                  Aucun pilote trouvé
                </p>
                <Link
                  to={`/talents/new?name=${encodeURIComponent(searchTerm)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-racing-red text-white font-orbitron font-bold text-sm hover:bg-racing-red/90 transition-colors"
                >
                  <UserPlus className="w-4 h-4" />
                  Créer un nouveau pilote
                </Link>
              </div>
            )}

            {filteredTalents.length > 0 && (
              <div className="border-t-2 border-white/10 p-2 bg-[#1a1a1a]">
                <Link
                  to={`/talents/new?name=${encodeURIComponent(searchTerm)}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-3 py-2 text-sm text-chrome-silver hover:text-racing-red transition-colors"
                >
                  <UserPlus className="w-4 h-4" />
                  Créer un nouveau pilote
                </Link>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Affichage des informations du talent sélectionné */}
      {selectedTalent && !isOpen && (
        <div className="mt-2 p-3 bg-status-info/10 border border-status-info rounded">
          <div className="flex items-start gap-3">
            <div className="flex-1">
              <div className="font-orbitron font-bold text-white">
                {selectedTalent.name}
              </div>
              {selectedTalent.team && (
                <div className="text-xs text-chrome-silver mt-1">
                  Équipe: {selectedTalent.team}
                </div>
              )}
              {selectedTalent.nationality && (
                <div className="text-xs text-chrome-silver">
                  Nationalité: {selectedTalent.nationality}
                </div>
              )}
            </div>
            <Link
              to={`/talents/${encodeURIComponent(selectedTalent.name)}`}
              className="text-xs text-status-info hover:text-status-info/80 underline"
            >
              Voir le profil
            </Link>
          </div>
        </div>
      )}

      {error && (
        <p className="mt-1 text-sm text-status-danger font-rajdhani">{error}</p>
      )}
    </div>
  )
}
