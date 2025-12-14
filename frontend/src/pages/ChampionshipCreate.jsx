import { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  Trophy,
  Car,
  MapPin,
  Settings,
  ChevronRight,
  ChevronLeft,
  Check,
  Plus,
  Trash2,
  Search,
  ArrowUpDown,
  X,
  AlertCircle
} from 'lucide-react'
import clsx from 'clsx'
import TalentSelector from '../components/TalentSelector'
import { apiEndpoints } from '../services/api'

// Session storage key
const SESSION_KEY = 'championship_create_session'

const STEPS = [
  { id: 'info', label: 'Informations', icon: Trophy },
  { id: 'vehicles', label: 'Véhicules', icon: Car },
  { id: 'drivers', label: 'Pilotes', icon: Trophy },
  { id: 'tracks', label: 'Circuits', icon: MapPin },
  { id: 'options', label: 'Options', icon: Settings },
]

export default function ChampionshipCreate() {
  const navigate = useNavigate()
  const [currentStep, setCurrentStep] = useState(0)
  const [errors, setErrors] = useState({})
  const [sessionRestored, setSessionRestored] = useState(false)

  // État du formulaire
  const [formData, setFormData] = useState({
    name: '',
    full_name: '',
    vehicle_assignments: [],
    tracks: [],
  })

  // État pour la sélection de véhicules
  const [vehicleSearch, setVehicleSearch] = useState('')
  const [selectedVehicles, setSelectedVehicles] = useState([])

  // État pour la sélection de circuits
  const [trackSearch, setTrackSearch] = useState('')
  const [selectedTracks, setSelectedTracks] = useState([])

  // Load session on mount
  useEffect(() => {
    const savedSession = localStorage.getItem(SESSION_KEY)
    if (savedSession) {
      try {
        const session = JSON.parse(savedSession)
        setCurrentStep(session.currentStep || 0)
        setFormData(session.formData || {
          name: '',
          full_name: '',
          vehicle_assignments: [],
          tracks: [],
        })
        setSelectedVehicles(session.selectedVehicles || [])
        setSelectedTracks(session.selectedTracks || [])
        setSessionRestored(true)
        // Auto-hide notification after 5 seconds
        setTimeout(() => setSessionRestored(false), 5000)
      } catch (error) {
        console.error('Error loading session:', error)
        localStorage.removeItem(SESSION_KEY)
      }
    }
  }, [])

  // Save session on state changes
  useEffect(() => {
    const session = {
      currentStep,
      formData,
      selectedVehicles,
      selectedTracks,
      timestamp: new Date().toISOString(),
    }
    localStorage.setItem(SESSION_KEY, JSON.stringify(session))
  }, [currentStep, formData, selectedVehicles, selectedTracks])

  // Clear session handler
  const clearSession = () => {
    const confirmed = window.confirm(
      '⚠️ Êtes-vous sûr de vouloir abandonner la création du championnat ?\n\nToutes les données seront perdues.'
    )
    if (confirmed) {
      localStorage.removeItem(SESSION_KEY)
      navigate('/championships')
    }
  }

  // Charger les véhicules originaux (sans préfixe M_)
  const { data: vehicles = [], isLoading: loadingVehicles } = useQuery({
    queryKey: ['vehicles', 'original'],
    queryFn: async () => {
      const response = await apiEndpoints.vehicles.list()
      // Filtrer les véhicules originaux uniquement
      return response.data.filter(v => !v.relative_path.startsWith('M_'))
    },
  })

  // Charger les circuits
  const { data: tracks = [], isLoading: loadingTracks } = useQuery({
    queryKey: ['tracks'],
    queryFn: async () => {
      const response = await apiEndpoints.tracks.list()
      return response.data
    },
  })

  // Mutation de création
  const createMutation = useMutation({
    mutationFn: async (data) => {
      const response = await apiEndpoints.championships.createCustom(data)
      return response.data
    },
    onSuccess: (data) => {
      // Clear session on success
      localStorage.removeItem(SESSION_KEY)
      navigate('/championships')
    },
    onError: (error) => {
      const detail = error.response?.data?.detail || 'Erreur lors de la création'
      setErrors({ submit: detail })
    },
  })

  // Validation par étape
  const validateStep = (step) => {
    const newErrors = {}

    if (step === 0) {
      if (!formData.name.trim()) {
        newErrors.name = 'Le nom est requis'
      } else if (formData.name.length > 17) {
        newErrors.name = 'Le nom ne doit pas dépasser 17 caractères'
      } else if (!/^[a-zA-Z0-9_]+$/.test(formData.name)) {
        newErrors.name = 'Seuls les caractères alphanumériques et underscore sont autorisés'
      }
    }

    if (step === 1) {
      if (selectedVehicles.length === 0) {
        newErrors.vehicles = 'Au moins un véhicule doit être sélectionné'
      }
    }

    if (step === 2) {
      const missingDrivers = selectedVehicles.filter(v => !v.driver)
      if (missingDrivers.length > 0) {
        newErrors.drivers = `${missingDrivers.length} véhicule(s) sans pilote assigné`
      }
    }

    if (step === 3) {
      if (selectedTracks.length === 0) {
        newErrors.tracks = 'Au moins un circuit doit être sélectionné'
      }
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Navigation entre étapes
  const goToStep = (step) => {
    if (validateStep(currentStep)) {
      setCurrentStep(step)
    }
  }

  const nextStep = () => {
    if (validateStep(currentStep) && currentStep < STEPS.length - 1) {
      setCurrentStep(currentStep + 1)
    }
  }

  const prevStep = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1)
    }
  }

  // Handlers véhicules
  const toggleVehicle = (vehicle) => {
    setSelectedVehicles(prev => {
      const exists = prev.find(v => v.relative_path === vehicle.relative_path)
      if (exists) {
        return prev.filter(v => v.relative_path !== vehicle.relative_path)
      }
      return [...prev, { ...vehicle, driver: '' }]
    })
  }

  const updateVehicleDriver = (vehiclePath, talent) => {
    setSelectedVehicles(prev =>
      prev.map(v =>
        v.relative_path === vehiclePath
          ? { ...v, driver: talent?.name || '' }
          : v
      )
    )
  }

  const removeVehicle = (vehiclePath) => {
    setSelectedVehicles(prev => prev.filter(v => v.relative_path !== vehiclePath))
  }

  // Handlers circuits
  const toggleTrack = (track) => {
    setSelectedTracks(prev => {
      const exists = prev.find(t => t.file_name === track.file_name)
      if (exists) {
        return prev.filter(t => t.file_name !== track.file_name)
      }
      return [...prev, track]
    })
  }

  const moveTrack = (index, direction) => {
    setSelectedTracks(prev => {
      const newTracks = [...prev]
      const newIndex = index + direction
      if (newIndex >= 0 && newIndex < newTracks.length) {
        [newTracks[index], newTracks[newIndex]] = [newTracks[newIndex], newTracks[index]]
      }
      return newTracks
    })
  }

  const removeTrack = (trackFileName) => {
    setSelectedTracks(prev => prev.filter(t => t.file_name !== trackFileName))
  }

  // Soumission finale
  const handleSubmit = () => {
    if (!validateStep(currentStep)) return

    const payload = {
      name: formData.name.trim(),
      full_name: formData.full_name.trim() || formData.name.trim(),
      vehicle_assignments: selectedVehicles.map(v => ({
        vehicle_path: v.relative_path,
        driver_name: v.driver,
      })),
      tracks: selectedTracks.map(t => t.file_name.replace('.gdb', '')),
    }

    createMutation.mutate(payload)
  }

  // Filtrage véhicules
  const filteredVehicles = vehicles.filter(v => {
    const search = vehicleSearch.toLowerCase()
    return (
      v.description?.toLowerCase().includes(search) ||
      v.team?.toLowerCase().includes(search) ||
      v.classes?.toLowerCase().includes(search)
    )
  })

  // Filtrage circuits
  const filteredTracks = tracks.filter(t => {
    const search = trackSearch.toLowerCase()
    return (
      t.file_name?.toLowerCase().includes(search) ||
      t.display_name?.toLowerCase().includes(search) ||
      t.venue_name?.toLowerCase().includes(search) ||
      t.relative_path?.toLowerCase().includes(search)
    )
  })

  // Rendu des étapes
  const renderStepContent = () => {
    switch (currentStep) {
      case 0:
        return <StepInfo formData={formData} setFormData={setFormData} errors={errors} />
      case 1:
        return (
          <StepVehicles
            vehicles={filteredVehicles}
            selectedVehicles={selectedVehicles}
            toggleVehicle={toggleVehicle}
            removeVehicle={removeVehicle}
            search={vehicleSearch}
            setSearch={setVehicleSearch}
            loading={loadingVehicles}
            errors={errors}
          />
        )
      case 2:
        return (
          <StepDrivers
            selectedVehicles={selectedVehicles}
            updateVehicleDriver={updateVehicleDriver}
            errors={errors}
          />
        )
      case 3:
        return (
          <StepTracks
            tracks={filteredTracks}
            selectedTracks={selectedTracks}
            toggleTrack={toggleTrack}
            removeTrack={removeTrack}
            moveTrack={moveTrack}
            search={trackSearch}
            setSearch={setTrackSearch}
            loading={loadingTracks}
            errors={errors}
          />
        )
      case 4:
        return (
          <StepOptions
            formData={formData}
            selectedVehicles={selectedVehicles}
            selectedTracks={selectedTracks}
          />
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-dark-charcoal">
      {/* Header */}
      <div className="bg-gradient-to-r from-racing-red to-racing-red/80 text-white py-8">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="font-orbitron font-black text-4xl mb-2">
                Créer un Championnat
              </h1>
              <p className="text-chrome-silver">
                Configuration d'un nouveau championnat personnalisé
              </p>
            </div>
            <button
              onClick={clearSession}
              className="flex items-center gap-2 px-4 py-2 bg-white/10 hover:bg-white/20 border border-white/30 rounded transition-colors"
            >
              <X className="w-5 h-5" />
              <span className="font-orbitron font-bold text-sm">Abandonner</span>
            </button>
          </div>
        </div>
      </div>

      {/* Session restored notification */}
      {sessionRestored && (
        <div className="bg-status-success/10 border-b-2 border-status-success">
          <div className="max-w-7xl mx-auto px-6 py-3">
            <div className="flex items-center gap-3 text-status-success">
              <AlertCircle className="w-5 h-5 flex-shrink-0" />
              <p className="font-rajdhani text-sm">
                Session restaurée. Vous pouvez continuer là où vous vous êtes arrêté.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stepper */}
      <div className="bg-dark-charcoal/50 border-b-2 border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {STEPS.map((step, index) => {
              const Icon = step.icon
              const isActive = index === currentStep
              const isCompleted = index < currentStep

              return (
                <div key={step.id} className="flex items-center flex-1">
                  <button
                    onClick={() => index <= currentStep && goToStep(index)}
                    disabled={index > currentStep}
                    className={clsx(
                      'flex items-center gap-3 px-4 py-2 rounded transition-all',
                      isActive && 'bg-racing-red text-white',
                      isCompleted && 'text-status-success hover:bg-white/5',
                      !isActive && !isCompleted && 'text-chrome-silver',
                      index > currentStep && 'opacity-50 cursor-not-allowed'
                    )}
                  >
                    <div
                      className={clsx(
                        'w-8 h-8 rounded-full flex items-center justify-center border-2',
                        isActive && 'border-white bg-white/10',
                        isCompleted && 'border-status-success bg-status-success',
                        !isActive && !isCompleted && 'border-chrome-silver'
                      )}
                    >
                      {isCompleted ? (
                        <Check className="w-5 h-5" />
                      ) : (
                        <Icon className="w-5 h-5" />
                      )}
                    </div>
                    <span className="font-orbitron font-bold text-sm hidden md:inline">
                      {step.label}
                    </span>
                  </button>
                  {index < STEPS.length - 1 && (
                    <div
                      className={clsx(
                        'flex-1 h-0.5 mx-2',
                        isCompleted ? 'bg-status-success' : 'bg-white/20'
                      )}
                    />
                  )}
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* Contenu de l'étape */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {renderStepContent()}

        {/* Erreur de soumission */}
        {errors.submit && (
          <div className="mt-4 p-4 bg-status-danger/10 border border-status-danger rounded">
            <p className="text-status-danger font-rajdhani">{errors.submit}</p>
          </div>
        )}

        {/* Boutons de navigation */}
        <div className="flex justify-between mt-8">
          <button
            onClick={prevStep}
            disabled={currentStep === 0}
            className={clsx(
              'flex items-center gap-2 px-6 py-3 font-orbitron font-bold text-sm transition-colors',
              currentStep === 0
                ? 'opacity-50 cursor-not-allowed text-chrome-silver'
                : 'text-white hover:text-racing-red'
            )}
          >
            <ChevronLeft className="w-5 h-5" />
            Précédent
          </button>

          {currentStep < STEPS.length - 1 ? (
            <button
              onClick={nextStep}
              className="flex items-center gap-2 px-6 py-3 bg-racing-red text-white font-orbitron font-bold text-sm hover:bg-racing-red/90 transition-colors"
            >
              Suivant
              <ChevronRight className="w-5 h-5" />
            </button>
          ) : (
            <button
              onClick={handleSubmit}
              disabled={createMutation.isPending}
              className="flex items-center gap-2 px-8 py-3 bg-status-success text-white font-orbitron font-bold text-sm hover:bg-status-success/90 transition-colors disabled:opacity-50"
            >
              {createMutation.isPending ? 'Création...' : 'Créer le championnat'}
              <Check className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>
    </div>
  )
}

// Étape 1: Informations de base
function StepInfo({ formData, setFormData, errors }) {
  return (
    <div className="max-w-2xl">
      <h2 className="font-orbitron font-bold text-2xl text-white mb-6">
        Informations de base
      </h2>

      <div className="space-y-6">
        <div>
          <label className="block font-orbitron font-semibold text-xs uppercase tracking-wide text-chrome-silver mb-2">
            Nom du championnat <span className="text-racing-red">*</span>
          </label>
          <input
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="ex: TC2025"
            maxLength={17}
            className={clsx(
              'racing-input w-full',
              errors.name && 'border-status-danger border-l-status-danger'
            )}
          />
          <p className="mt-1 text-xs text-chrome-silver">
            Maximum 17 caractères (alphanumérique + underscore uniquement)
          </p>
          {errors.name && (
            <p className="mt-1 text-sm text-status-danger font-rajdhani">{errors.name}</p>
          )}
        </div>

        <div>
          <label className="block font-orbitron font-semibold text-xs uppercase tracking-wide text-chrome-silver mb-2">
            Nom complet (optionnel)
          </label>
          <input
            type="text"
            value={formData.full_name}
            onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
            placeholder="ex: Test Championship 2025"
            maxLength={50}
            className="racing-input w-full"
          />
          <p className="mt-1 text-xs text-chrome-silver">
            Si vide, le nom court sera utilisé
          </p>
        </div>

        <div className="p-4 bg-status-info/10 border border-status-info rounded">
          <p className="text-sm text-chrome-silver">
            Le championnat sera créé avec le préfixe <span className="font-mono text-white">M_</span>
            {formData.name && (
              <>
                {' '}→ <span className="font-mono text-racing-red">M_{formData.name}</span>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  )
}

// Étape 2: Sélection des véhicules
function StepVehicles({ vehicles, selectedVehicles, toggleVehicle, removeVehicle, search, setSearch, loading, errors }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-orbitron font-bold text-2xl text-white">
            Sélection des véhicules
          </h2>
          <p className="text-chrome-silver text-sm mt-1">
            {selectedVehicles.length} véhicule(s) sélectionné(s)
          </p>
        </div>
      </div>

      {errors.vehicles && (
        <div className="mb-4 p-3 bg-status-danger/10 border border-status-danger rounded">
          <p className="text-status-danger font-rajdhani">{errors.vehicles}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Liste des véhicules disponibles */}
        <div>
          <div className="mb-4">
            <div className="relative">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un véhicule..."
                className="racing-input w-full pl-10"
              />
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-chrome-silver" />
            </div>
          </div>

          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading ? (
              <div className="text-center py-8">
                <div className="inline-block w-8 h-8 border-4 border-racing-red border-t-transparent rounded-full animate-spin" />
              </div>
            ) : vehicles.length === 0 ? (
              <div className="text-center py-8 text-chrome-silver">
                Aucun véhicule trouvé
              </div>
            ) : (
              vehicles.map((vehicle) => {
                const isSelected = selectedVehicles.some(v => v.relative_path === vehicle.relative_path)
                return (
                  <button
                    key={vehicle.relative_path}
                    onClick={() => toggleVehicle(vehicle)}
                    className={clsx(
                      'w-full text-left p-4 border-2 rounded transition-all',
                      isSelected
                        ? 'border-racing-red bg-racing-red/10'
                        : 'border-white/20 hover:border-white/40 bg-dark-charcoal/50'
                    )}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-orbitron font-bold text-white">
                          {vehicle.description || vehicle.file_name}
                        </div>
                        {vehicle.team && (
                          <div className="text-xs text-chrome-silver mt-1">
                            {vehicle.team}
                          </div>
                        )}
                        {vehicle.classes && (
                          <div className="text-xs text-chrome-silver">
                            Classe: {vehicle.classes}
                          </div>
                        )}
                      </div>
                      {isSelected && (
                        <Check className="w-5 h-5 text-racing-red flex-shrink-0" />
                      )}
                    </div>
                  </button>
                )
              })
            )}
          </div>
        </div>

        {/* Véhicules sélectionnés */}
        <div>
          <h3 className="font-orbitron font-bold text-white mb-4">
            Véhicules sélectionnés ({selectedVehicles.length})
          </h3>
          <div className="space-y-2">
            {selectedVehicles.length === 0 ? (
              <div className="p-8 text-center text-chrome-silver border-2 border-dashed border-white/20 rounded">
                Aucun véhicule sélectionné
              </div>
            ) : (
              selectedVehicles.map((vehicle) => (
                <div
                  key={vehicle.relative_path}
                  className="p-4 bg-dark-charcoal/50 border-2 border-racing-red/50 rounded flex items-start justify-between"
                >
                  <div className="flex-1">
                    <div className="font-orbitron font-bold text-white">
                      {vehicle.description || vehicle.file_name}
                    </div>
                    {vehicle.team && (
                      <div className="text-xs text-chrome-silver mt-1">
                        {vehicle.team}
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => removeVehicle(vehicle.relative_path)}
                    className="text-status-danger hover:text-status-danger/80 transition-colors ml-2"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Étape 3: Association pilotes
function StepDrivers({ selectedVehicles, updateVehicleDriver, errors }) {
  return (
    <div>
      <h2 className="font-orbitron font-bold text-2xl text-white mb-6">
        Association des pilotes
      </h2>

      {errors.drivers && (
        <div className="mb-4 p-3 bg-status-danger/10 border border-status-danger rounded">
          <p className="text-status-danger font-rajdhani">{errors.drivers}</p>
        </div>
      )}

      <div className="space-y-4">
        {selectedVehicles.map((vehicle) => {
          // Exclure les pilotes déjà assignés à d'autres véhicules
          const excludedTalents = selectedVehicles
            .filter(v => v.relative_path !== vehicle.relative_path && v.driver)
            .map(v => v.driver)

          return (
            <div
              key={vehicle.relative_path}
              className="p-6 bg-dark-charcoal/50 border-2 border-white/20 rounded"
            >
              <div className="mb-4">
                <h3 className="font-orbitron font-bold text-white">
                  {vehicle.description || vehicle.file_name}
                </h3>
                {vehicle.team && (
                  <p className="text-xs text-chrome-silver mt-1">{vehicle.team}</p>
                )}
              </div>

              <TalentSelector
                value={vehicle.driver}
                onChange={(talent) => updateVehicleDriver(vehicle.relative_path, talent)}
                label="Pilote assigné"
                required={true}
                error={!vehicle.driver ? 'Un pilote doit être assigné' : ''}
                excludedTalents={excludedTalents}
              />
            </div>
          )
        })}
      </div>
    </div>
  )
}

// Étape 4: Sélection des circuits
function StepTracks({ tracks, selectedTracks, toggleTrack, removeTrack, moveTrack, search, setSearch, loading, errors }) {
  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="font-orbitron font-bold text-2xl text-white">
            Sélection des circuits
          </h2>
          <p className="text-chrome-silver text-sm mt-1">
            {selectedTracks.length} circuit(s) sélectionné(s)
          </p>
        </div>
      </div>

      {errors.tracks && (
        <div className="mb-4 p-3 bg-status-danger/10 border border-status-danger rounded">
          <p className="text-status-danger font-rajdhani">{errors.tracks}</p>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Liste des circuits disponibles */}
        <div>
          <div className="mb-4">
            <div className="relative">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Rechercher un circuit..."
                className="racing-input w-full pl-10"
              />
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-chrome-silver" />
            </div>
          </div>

          <div className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading ? (
              <div className="text-center py-8">
                <div className="inline-block w-8 h-8 border-4 border-racing-red border-t-transparent rounded-full animate-spin" />
              </div>
            ) : tracks.length === 0 ? (
              <div className="text-center py-8 text-chrome-silver">
                Aucun circuit trouvé
              </div>
            ) : (
              tracks.map((track) => {
                const isSelected = selectedTracks.some(t => t.file_name === track.file_name)
                return (
                  <button
                    key={track.file_name}
                    onClick={() => toggleTrack(track)}
                    className={clsx(
                      'w-full text-left p-4 border-2 rounded transition-all',
                      isSelected
                        ? 'border-racing-red bg-racing-red/10'
                        : 'border-white/20 hover:border-white/40 bg-dark-charcoal/50'
                    )}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="font-orbitron font-bold text-white">
                          {track.display_name}
                        </div>
                        {track.venue_name && (
                          <div className="text-xs text-chrome-silver mt-1">
                            {track.venue_name}
                          </div>
                        )}
                      </div>
                      {isSelected && (
                        <Check className="w-5 h-5 text-racing-red flex-shrink-0" />
                      )}
                    </div>
                  </button>
                )
              })
            )}
          </div>
        </div>

        {/* Circuits sélectionnés avec ordre */}
        <div>
          <h3 className="font-orbitron font-bold text-white mb-4">
            Ordre des courses ({selectedTracks.length})
          </h3>
          <div className="space-y-2">
            {selectedTracks.length === 0 ? (
              <div className="p-8 text-center text-chrome-silver border-2 border-dashed border-white/20 rounded">
                Aucun circuit sélectionné
              </div>
            ) : (
              selectedTracks.map((track, index) => (
                <div
                  key={track.file_name}
                  className="p-4 bg-dark-charcoal/50 border-2 border-racing-red/50 rounded flex items-center gap-3"
                >
                  <div className="flex flex-col gap-1">
                    <button
                      onClick={() => moveTrack(index, -1)}
                      disabled={index === 0}
                      className="text-chrome-silver hover:text-white disabled:opacity-30 disabled:cursor-not-allowed"
                    >
                      <ChevronLeft className="w-4 h-4 rotate-90" />
                    </button>
                    <button
                      onClick={() => moveTrack(index, 1)}
                      disabled={index === selectedTracks.length - 1}
                      className="text-chrome-silver hover:text-white disabled:opacity-30 disabled:cursor-not-allowed"
                    >
                      <ChevronLeft className="w-4 h-4 -rotate-90" />
                    </button>
                  </div>

                  <div className="w-8 h-8 bg-racing-red rounded-full flex items-center justify-center font-orbitron font-bold text-white">
                    {index + 1}
                  </div>

                  <div className="flex-1">
                    <div className="font-orbitron font-bold text-white">
                      {track.display_name}
                    </div>
                    {track.venue_name && (
                      <div className="text-xs text-chrome-silver mt-1">
                        {track.venue_name}
                      </div>
                    )}
                  </div>

                  <button
                    onClick={() => removeTrack(track.file_name)}
                    className="text-status-danger hover:text-status-danger/80 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Étape 5: Récapitulatif et options
function StepOptions({ formData, selectedVehicles, selectedTracks }) {
  return (
    <div className="max-w-3xl">
      <h2 className="font-orbitron font-bold text-2xl text-white mb-6">
        Récapitulatif
      </h2>

      <div className="space-y-6">
        {/* Informations générales */}
        <div className="p-6 bg-dark-charcoal/50 border-2 border-white/20 rounded">
          <h3 className="font-orbitron font-bold text-racing-red mb-4">
            Informations générales
          </h3>
          <dl className="grid grid-cols-2 gap-4">
            <div>
              <dt className="text-xs text-chrome-silver uppercase">Nom</dt>
              <dd className="font-orbitron font-bold text-white mt-1">
                M_{formData.name}
              </dd>
            </div>
            <div>
              <dt className="text-xs text-chrome-silver uppercase">Nom complet</dt>
              <dd className="font-orbitron font-bold text-white mt-1">
                {formData.full_name || formData.name}
              </dd>
            </div>
          </dl>
        </div>

        {/* Véhicules */}
        <div className="p-6 bg-dark-charcoal/50 border-2 border-white/20 rounded">
          <h3 className="font-orbitron font-bold text-racing-red mb-4">
            Véhicules et pilotes ({selectedVehicles.length})
          </h3>
          <div className="space-y-2">
            {selectedVehicles.map((vehicle) => (
              <div key={vehicle.relative_path} className="flex items-center justify-between p-3 bg-dark-charcoal/30 rounded">
                <div>
                  <div className="font-orbitron text-white text-sm">
                    {vehicle.description || vehicle.file_name}
                  </div>
                  {vehicle.team && (
                    <div className="text-xs text-chrome-silver">{vehicle.team}</div>
                  )}
                </div>
                <div className="text-sm text-racing-red font-rajdhani">
                  {vehicle.driver || 'Non assigné'}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Circuits */}
        <div className="p-6 bg-dark-charcoal/50 border-2 border-white/20 rounded">
          <h3 className="font-orbitron font-bold text-racing-red mb-4">
            Calendrier des courses ({selectedTracks.length})
          </h3>
          <div className="space-y-2">
            {selectedTracks.map((track, index) => (
              <div key={track.file_name} className="flex items-center gap-3 p-3 bg-dark-charcoal/30 rounded">
                <div className="w-8 h-8 bg-racing-red rounded-full flex items-center justify-center font-orbitron font-bold text-white text-sm">
                  {index + 1}
                </div>
                <div>
                  <div className="font-orbitron text-white text-sm">
                    {track.display_name}
                  </div>
                  {track.venue_name && (
                    <div className="text-xs text-chrome-silver">{track.venue_name}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Configuration automatique */}
        <div className="p-6 bg-status-info/10 border-2 border-status-info rounded">
          <h3 className="font-orbitron font-bold text-status-info mb-4">
            Configuration automatique
          </h3>
          <ul className="space-y-2 text-sm text-chrome-silver">
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-status-success" />
              Argent de départ: 500,000,000
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-status-success" />
              Classe unique: {formData.name}
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-status-success" />
              Véhicules isolés dans M_{formData.name}/
            </li>
            <li className="flex items-center gap-2">
              <Check className="w-4 h-4 text-status-success" />
              Fichier RFM créé automatiquement
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
