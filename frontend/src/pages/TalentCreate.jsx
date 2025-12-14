import { useState, useEffect } from 'react'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UserPlus, Save, X, Dices } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingInput from '../components/RacingInput'
import RacingButton from '../components/RacingButton'

// Helper functions for date conversion
const rfactorDateToISO = (rfDate) => {
  // Convert DD-MM-YYYY to YYYY-MM-DD
  if (!rfDate || !rfDate.includes('-')) return ''
  const [day, month, year] = rfDate.split('-')
  return `${year}-${month}-${day}`
}

const isoDateToRFactor = (isoDate) => {
  // Convert YYYY-MM-DD to DD-MM-YYYY
  if (!isoDate || !isoDate.includes('-')) return ''
  const [year, month, day] = isoDate.split('-')
  return `${day}-${month}-${year}`
}

export default function TalentCreate() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [searchParams] = useSearchParams()

  const [formData, setFormData] = useState({
    name: searchParams.get('name') || '',
    nationality: '',
    date_of_birth: '',
    starts: 0,
    poles: 0,
    wins: 0,
    drivers_championships: 0,
    aggression: 50.0,
    reputation: 50.0,
    courtesy: 50.0,
    composure: 50.0,
    speed: 50.0,
    crash: 50.0,
    recovery: 50.0,
    completed_laps: 90.0,
    min_racing_skill: 50.0,
  })

  const [errors, setErrors] = useState({})

  // Load nationalities list
  const { data: nationalities = [] } = useQuery({
    queryKey: ['nationalities'],
    queryFn: async () => {
      const response = await fetch('/api/talents/nationalities/?from_existing=true')
      if (!response.ok) throw new Error('Failed to load nationalities')
      return response.json()
    },
  })

  const createMutation = useMutation({
    mutationFn: async (data) => {
      const response = await apiEndpoints.talents.create({
        name: data.name,
        personal_info: {
          nationality: data.nationality,
          date_of_birth: data.date_of_birth,
          starts: parseInt(data.starts),
          poles: parseInt(data.poles),
          wins: parseInt(data.wins),
          drivers_championships: parseInt(data.drivers_championships),
        },
        stats: {
          aggression: parseFloat(data.aggression),
          reputation: parseFloat(data.reputation),
          courtesy: parseFloat(data.courtesy),
          composure: parseFloat(data.composure),
          speed: parseFloat(data.speed),
          crash: parseFloat(data.crash),
          recovery: parseFloat(data.recovery),
          completed_laps: parseFloat(data.completed_laps),
          min_racing_skill: parseFloat(data.min_racing_skill),
        },
      })
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries(['talents'])
      navigate(`/talents/${encodeURIComponent(data.name)}`)
    },
    onError: (error) => {
      if (error.response?.data?.detail) {
        setErrors({ submit: error.response.data.detail })
      } else {
        setErrors({ submit: 'Erreur lors de la création du talent' })
      }
    },
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({ ...prev, [name]: value }))
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: undefined }))
    }
  }

  // Load random stats on mount
  useEffect(() => {
    loadRandomStats()
  }, [])

  const loadRandomStats = async () => {
    try {
      const response = await fetch('/api/talents/random-stats/')
      if (!response.ok) throw new Error('Failed to load random stats')
      const data = await response.json()

      // Ne mettre à jour QUE les stats de course, préserver tout le reste
      setFormData((prev) => ({
        ...prev,
        // Statistiques de course uniquement
        aggression: data.stats.aggression,
        reputation: data.stats.reputation,
        courtesy: data.stats.courtesy,
        composure: data.stats.composure,
        speed: data.stats.speed,
        crash: data.stats.crash,
        recovery: data.stats.recovery,
        completed_laps: data.stats.completed_laps,
        min_racing_skill: data.stats.min_racing_skill,
      }))
    } catch (error) {
      console.error('Error loading random stats:', error)
    }
  }

  const generateRandomStats = () => {
    loadRandomStats()
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setErrors({})

    // Basic validation
    const newErrors = {}
    if (!formData.name.trim()) {
      newErrors.name = 'Le nom est requis'
    }
    if (!formData.nationality.trim()) {
      newErrors.nationality = 'La nationalité est requise'
    }
    if (!formData.date_of_birth.trim()) {
      newErrors.date_of_birth = 'La date de naissance est requise'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    createMutation.mutate(formData)
  }

  return (
    <div>
      <PageHeader
        icon={UserPlus}
        title="Nouveau Talent"
        subtitle="Créer un nouveau pilote"
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <form onSubmit={handleSubmit}>
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-6">
              Informations Personnelles
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <RacingInput
                label="Nom complet"
                name="name"
                value={formData.name}
                onChange={handleChange}
                error={errors.name}
                required
                placeholder="Jean Dupont"
              />

              <div>
                <label className="block text-sm font-bold text-racing-cyan mb-2">
                  Nationalité <span className="text-status-danger">*</span>
                </label>
                <input
                  type="text"
                  name="nationality"
                  value={formData.nationality}
                  onChange={handleChange}
                  list="nationalities-list"
                  required
                  placeholder="Ex: American, French, British..."
                  className={`w-full px-4 py-3 bg-dark-secondary border ${
                    errors.nationality ? 'border-status-danger' : 'border-racing-cyan/30'
                  } rounded-lg focus:outline-none focus:border-racing-cyan text-white transition-colors`}
                />
                <datalist id="nationalities-list">
                  {nationalities.map((nat) => (
                    <option key={nat} value={nat} />
                  ))}
                </datalist>
                {errors.nationality && (
                  <p className="text-status-danger text-sm mt-1">{errors.nationality}</p>
                )}
              </div>

              <RacingInput
                label="Date de naissance"
                name="date_of_birth"
                type="date"
                value={rfactorDateToISO(formData.date_of_birth)}
                onChange={(e) => {
                  const isoDate = e.target.value
                  const rfDate = isoDateToRFactor(isoDate)
                  setFormData((prev) => ({ ...prev, date_of_birth: rfDate }))
                  if (errors.date_of_birth) {
                    setErrors((prev) => ({ ...prev, date_of_birth: undefined }))
                  }
                }}
                error={errors.date_of_birth}
                required
              />

              <RacingInput
                label="Départs"
                name="starts"
                type="number"
                min="0"
                value={formData.starts}
                onChange={handleChange}
              />

              <RacingInput
                label="Pole positions"
                name="poles"
                type="number"
                min="0"
                value={formData.poles}
                onChange={handleChange}
              />

              <RacingInput
                label="Victoires"
                name="wins"
                type="number"
                min="0"
                value={formData.wins}
                onChange={handleChange}
              />

              <RacingInput
                label="Championnats"
                name="drivers_championships"
                type="number"
                min="0"
                value={formData.drivers_championships}
                onChange={handleChange}
              />
            </div>
          </RacingCard>

          <RacingCard className="p-6 mb-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-xl font-orbitron font-bold text-white">
                Statistiques de Course
              </h3>
              <RacingButton
                type="button"
                variant="secondary"
                onClick={generateRandomStats}
                className="text-sm"
              >
                <Dices className="inline-block w-4 h-4 mr-2" />
                Régénérer
              </RacingButton>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <RacingInput
                label="Vitesse"
                name="speed"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.speed}
                onChange={handleChange}
              />

              <RacingInput
                label="Résistance aux crashes"
                name="crash"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.crash}
                onChange={handleChange}
              />

              <RacingInput
                label="Agressivité"
                name="aggression"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.aggression}
                onChange={handleChange}
              />

              <RacingInput
                label="Réputation"
                name="reputation"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.reputation}
                onChange={handleChange}
              />

              <RacingInput
                label="Courtoisie"
                name="courtesy"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.courtesy}
                onChange={handleChange}
              />

              <RacingInput
                label="Sang-froid"
                name="composure"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.composure}
                onChange={handleChange}
              />

              <RacingInput
                label="Récupération"
                name="recovery"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.recovery}
                onChange={handleChange}
              />

              <RacingInput
                label="Tours complétés"
                name="completed_laps"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.completed_laps}
                onChange={handleChange}
              />

              <RacingInput
                label="Compétence min."
                name="min_racing_skill"
                type="number"
                min="0"
                max="100"
                step="0.01"
                value={formData.min_racing_skill}
                onChange={handleChange}
              />
            </div>
          </RacingCard>

          {errors.submit && (
            <RacingCard className="p-4 mb-6 border-status-danger">
              <p className="text-status-danger font-bold">{errors.submit}</p>
            </RacingCard>
          )}

          <div className="flex gap-4">
            <RacingButton
              type="submit"
              variant="primary"
              disabled={createMutation.isPending}
            >
              <Save className="inline-block w-5 h-5 mr-2" />
              {createMutation.isPending ? 'Création...' : 'Créer le Talent'}
            </RacingButton>

            <RacingButton
              type="button"
              variant="secondary"
              onClick={() => navigate('/talents')}
            >
              <X className="inline-block w-5 h-5 mr-2" />
              Annuler
            </RacingButton>
          </div>
        </form>
      </motion.div>
    </div>
  )
}
