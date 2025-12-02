import { useState, useEffect } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import { useNavigate, useParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Edit, Save, X } from 'lucide-react'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingInput from '../components/RacingInput'
import RacingButton from '../components/RacingButton'
import LoadingSpinner from '../components/LoadingSpinner'
import TalentSelector from '../components/TalentSelector'

export default function VehicleEdit() {
  const { path } = useParams()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [formData, setFormData] = useState({
    driver: '',
  })

  const [errors, setErrors] = useState({})

  const { data: vehicle, isLoading } = useQuery({
    queryKey: ['vehicle', path],
    queryFn: async () => {
      const response = await apiEndpoints.vehicles.get(path)
      return response.data
    },
  })

  useEffect(() => {
    if (vehicle) {
      setFormData({
        driver: vehicle.team_info?.driver || '',
      })
    }
  }, [vehicle])

  const updateMutation = useMutation({
    mutationFn: async (data) => {
      const response = await apiEndpoints.vehicles.update(path, {
        driver: data.driver,
      })
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries(['vehicles'])
      queryClient.invalidateQueries(['vehicle', path])
      navigate(`/vehicles/${encodeURIComponent(path)}`)
    },
    onError: (error) => {
      setErrors({ submit: error.message || 'Erreur lors de la modification du véhicule' })
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

  const handleTalentChange = (talent) => {
    if (talent) {
      setFormData((prev) => ({ ...prev, driver: talent.name }))
      // Clear error for driver field
      if (errors.driver) {
        setErrors((prev) => ({ ...prev, driver: undefined }))
      }
    } else {
      setFormData((prev) => ({ ...prev, driver: '' }))
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setErrors({})

    // Basic validation
    const newErrors = {}
    if (!formData.driver.trim()) {
      newErrors.driver = 'Le nom du pilote est requis'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    updateMutation.mutate(formData)
  }

  if (isLoading) {
    return <LoadingSpinner message="Chargement du véhicule..." />
  }

  if (!vehicle) {
    return (
      <div>
        <PageHeader
          icon={Edit}
          title="Véhicule non trouvé"
          subtitle="Le véhicule demandé n'existe pas"
        />
        <RacingCard className="p-6 border-status-danger">
          <p className="text-status-danger font-bold">Véhicule introuvable</p>
        </RacingCard>
      </div>
    )
  }

  return (
    <div>
      <PageHeader
        icon={Edit}
        title={`Modifier ${vehicle.description || 'Véhicule'}`}
        subtitle="Modifier les informations du véhicule"
      />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <form onSubmit={handleSubmit}>
          <RacingCard className="p-6 mb-6">
            <h3 className="text-xl font-orbitron font-bold text-white mb-6">
              Informations du pilote
            </h3>

            <div className="grid grid-cols-1 gap-4">
              <TalentSelector
                label="Pilote"
                value={formData.driver}
                onChange={handleTalentChange}
                error={errors.driver}
                required
              />
            </div>

            <div className="mt-6 p-4 bg-status-info/10 border border-status-info rounded">
              <p className="text-status-info text-sm">
                <strong>Note :</strong> La modification du pilote mettra à jour le fichier .veh du véhicule.
              </p>
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
              disabled={updateMutation.isPending}
            >
              <Save className="inline-block w-5 h-5 mr-2" />
              {updateMutation.isPending ? 'Enregistrement...' : 'Enregistrer les modifications'}
            </RacingButton>

            <RacingButton
              type="button"
              variant="secondary"
              onClick={() => navigate(`/vehicles/${encodeURIComponent(path)}`)}
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
