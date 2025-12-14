import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Settings, Save, CheckCircle2, AlertCircle, Dices, RotateCcw } from 'lucide-react'
import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'
import RacingInput from '../components/RacingInput'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Config() {
  const queryClient = useQueryClient()
  const [rfactorPath, setRfactorPath] = useState('')
  const [currentPlayer, setCurrentPlayer] = useState('')
  const [randomizerBounds, setRandomizerBounds] = useState(null)

  const { data: config, isLoading } = useQuery({
    queryKey: ['config'],
    queryFn: async () => {
      const response = await apiEndpoints.config.get()
      return response.data
    },
    onSuccess: (data) => {
      setRfactorPath(data.rfactor_path || '')
      setCurrentPlayer(data.current_player || '')
    },
  })

  // Load randomizer bounds
  const { data: bounds, isLoading: isLoadingBounds } = useQuery({
    queryKey: ['randomizer-bounds'],
    queryFn: async () => {
      const response = await fetch('/api/config/randomizer-bounds')
      if (!response.ok) throw new Error('Failed to load randomizer bounds')
      return response.json()
    },
  })

  useEffect(() => {
    if (bounds) {
      setRandomizerBounds(bounds)
    }
  }, [bounds])

  const mutation = useMutation({
    mutationFn: async (data) => {
      await apiEndpoints.config.update(data)
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['config'])
      toast.success('Configuration enregistrée avec succès !')
    },
    onError: (error) => {
      toast.error(`Erreur: ${error.message}`)
    },
  })

  const randomizerMutation = useMutation({
    mutationFn: async (data) => {
      const response = await fetch('/api/config/randomizer-bounds', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      if (!response.ok) throw new Error('Failed to update randomizer bounds')
      return response.json()
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['randomizer-bounds'])
      toast.success('Bornes du randomizer mises à jour !')
    },
    onError: (error) => {
      toast.error(`Erreur: ${error.message}`)
    },
  })

  const resetBoundsMutation = useMutation({
    mutationFn: async () => {
      const response = await fetch('/api/config/randomizer-bounds/reset', {
        method: 'POST',
      })
      if (!response.ok) throw new Error('Failed to reset randomizer bounds')
      return response.json()
    },
    onSuccess: (data) => {
      setRandomizerBounds(data)
      queryClient.invalidateQueries(['randomizer-bounds'])
      toast.success('Bornes réinitialisées aux valeurs par défaut !')
    },
    onError: (error) => {
      toast.error(`Erreur: ${error.message}`)
    },
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    mutation.mutate({
      rfactor_path: rfactorPath,
      current_player: currentPlayer,
    })
  }

  const handleBoundsChange = (key, subkey, value) => {
    setRandomizerBounds((prev) => {
      const newBounds = { ...prev }
      if (subkey) {
        newBounds[key] = { ...newBounds[key], [subkey]: parseFloat(value) }
      } else {
        newBounds[key] = parseFloat(value)
      }
      return newBounds
    })
  }

  const handleSaveBounds = () => {
    randomizerMutation.mutate(randomizerBounds)
  }

  const handleResetBounds = () => {
    if (confirm('Réinitialiser toutes les bornes aux valeurs par défaut ?')) {
      resetBoundsMutation.mutate()
    }
  }

  if (isLoading) {
    return <LoadingSpinner message="Chargement de la configuration..." />
  }

  return (
    <div>
      <PageHeader
        icon={Settings}
        title="Configuration"
        subtitle="Configurez les chemins d'accès à rFactor"
      />

      <div className="max-w-3xl">
        {/* Status Card */}
        <RacingCard className={`p-6 mb-6 border-t-4 ${config?.is_configured ? 'border-status-success' : 'border-status-warning'}`}>
          <div className="flex items-center gap-3">
            {config?.is_configured ? (
              <>
                <CheckCircle2 className="w-8 h-8 text-status-success" />
                <div>
                  <h3 className="font-orbitron font-bold text-lg text-white">
                    Configuration valide
                  </h3>
                  <p className="text-chrome-silver text-sm">
                    L'application est correctement configurée
                  </p>
                </div>
              </>
            ) : (
              <>
                <AlertCircle className="w-8 h-8 text-status-warning" />
                <div>
                  <h3 className="font-orbitron font-bold text-lg text-white">
                    Configuration requise
                  </h3>
                  <p className="text-chrome-silver text-sm">
                    Veuillez configurer le chemin vers rFactor
                  </p>
                </div>
              </>
            )}
          </div>
        </RacingCard>

        {/* Config Form */}
        <RacingCard className="p-6">
          <form onSubmit={handleSubmit} className="space-y-6">
            <RacingInput
              label="Chemin rFactor"
              placeholder="C:/Program Files/rFactor"
              value={rfactorPath}
              onChange={(e) => setRfactorPath(e.target.value)}
              required
            />

            <RacingInput
              label="Nom du joueur"
              placeholder="NomDuJoueur"
              value={currentPlayer}
              onChange={(e) => setCurrentPlayer(e.target.value)}
              required
            />

            <div className="pt-4 border-t border-white/10">
              <RacingButton
                type="submit"
                variant="primary"
                loading={mutation.isPending}
                className="w-full"
              >
                <Save className="inline-block w-5 h-5 mr-2" />
                Enregistrer la configuration
              </RacingButton>
            </div>
          </form>
        </RacingCard>

        {/* Info Card */}
        <RacingCard className="p-6 mt-6 border-l-4 border-status-info">
          <h4 className="font-orbitron font-bold text-white mb-3">
            Informations
          </h4>
          <ul className="space-y-2 text-sm text-chrome-silver">
            <li>• Le chemin rFactor doit pointer vers le dossier d'installation principal</li>
            <li>• Le nom du joueur correspond au nom du dossier dans UserData/</li>
            <li>• Exemple: C:/Program Files/rFactor</li>
          </ul>
        </RacingCard>

        {/* Randomizer Bounds Configuration */}
        {randomizerBounds && (
          <RacingCard className="p-6 mt-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="font-orbitron font-bold text-lg text-white flex items-center gap-2">
                  <Dices className="w-6 h-6" />
                  Configuration du Générateur Aléatoire
                </h3>
                <p className="text-chrome-silver text-sm mt-1">
                  Définissez les bornes pour la génération aléatoire des statistiques des talents
                </p>
              </div>
              <RacingButton
                variant="secondary"
                onClick={handleResetBounds}
                loading={resetBoundsMutation.isPending}
                className="text-sm"
              >
                <RotateCcw className="inline-block w-4 h-4 mr-2" />
                Réinitialiser
              </RacingButton>
            </div>

            <div className="space-y-6">
              {/* Niveau général (Overall Skill) */}
              <div>
                <h4 className="font-bold text-racing-cyan mb-3">Niveau Général (Overall Skill)</h4>
                <div className="grid grid-cols-2 gap-4">
                  <RacingInput
                    label="Minimum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.overall_skill?.min || 0}
                    onChange={(e) => handleBoundsChange('overall_skill', 'min', e.target.value)}
                  />
                  <RacingInput
                    label="Maximum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.overall_skill?.max || 100}
                    onChange={(e) => handleBoundsChange('overall_skill', 'max', e.target.value)}
                  />
                </div>
              </div>

              {/* Agressivité */}
              <div>
                <h4 className="font-bold text-racing-cyan mb-3">Agressivité</h4>
                <div className="grid grid-cols-2 gap-4">
                  <RacingInput
                    label="Minimum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.aggression?.min || 0}
                    onChange={(e) => handleBoundsChange('aggression', 'min', e.target.value)}
                  />
                  <RacingInput
                    label="Maximum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.aggression?.max || 100}
                    onChange={(e) => handleBoundsChange('aggression', 'max', e.target.value)}
                  />
                </div>
              </div>

              {/* Courtoisie */}
              <div>
                <h4 className="font-bold text-racing-cyan mb-3">Courtoisie</h4>
                <div className="grid grid-cols-2 gap-4">
                  <RacingInput
                    label="Minimum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.courtesy?.min || 0}
                    onChange={(e) => handleBoundsChange('courtesy', 'min', e.target.value)}
                  />
                  <RacingInput
                    label="Maximum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.courtesy?.max || 100}
                    onChange={(e) => handleBoundsChange('courtesy', 'max', e.target.value)}
                  />
                </div>
              </div>

              {/* Tours complétés */}
              <div>
                <h4 className="font-bold text-racing-cyan mb-3">Tours Complétés (%)</h4>
                <div className="grid grid-cols-2 gap-4">
                  <RacingInput
                    label="Minimum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.completed_laps_min || 0}
                    onChange={(e) => handleBoundsChange('completed_laps_min', null, e.target.value)}
                  />
                  <RacingInput
                    label="Maximum"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.completed_laps_max || 100}
                    onChange={(e) => handleBoundsChange('completed_laps_max', null, e.target.value)}
                  />
                </div>
              </div>

              {/* Variances (Advanced) */}
              <details className="border border-white/10 rounded-lg p-4">
                <summary className="cursor-pointer font-bold text-racing-cyan mb-3">
                  Paramètres Avancés (Variances)
                </summary>
                <div className="space-y-4 mt-4">
                  <RacingInput
                    label="Variance Vitesse"
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.speed_variance || 0}
                    onChange={(e) => handleBoundsChange('speed_variance', null, e.target.value)}
                  />
                  <RacingInput
                    label="Variance Sang-froid"
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.composure_variance || 0}
                    onChange={(e) => handleBoundsChange('composure_variance', null, e.target.value)}
                  />
                  <RacingInput
                    label="Base Crash"
                    type="number"
                    min="0"
                    max="100"
                    step="1"
                    value={randomizerBounds.crash_base || 50}
                    onChange={(e) => handleBoundsChange('crash_base', null, e.target.value)}
                  />
                  <RacingInput
                    label="Variance Crash"
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.crash_variance || 0}
                    onChange={(e) => handleBoundsChange('crash_variance', null, e.target.value)}
                  />
                  <RacingInput
                    label="Variance Récupération"
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.recovery_variance || 0}
                    onChange={(e) => handleBoundsChange('recovery_variance', null, e.target.value)}
                  />
                  <RacingInput
                    label="Variance Réputation"
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.reputation_variance || 0}
                    onChange={(e) => handleBoundsChange('reputation_variance', null, e.target.value)}
                  />
                  <RacingInput
                    label="Variance Compétence Min."
                    type="number"
                    min="0"
                    max="50"
                    step="1"
                    value={randomizerBounds.min_racing_skill_variance || 0}
                    onChange={(e) => handleBoundsChange('min_racing_skill_variance', null, e.target.value)}
                  />
                </div>
              </details>

              <div className="pt-4 border-t border-white/10">
                <RacingButton
                  variant="primary"
                  onClick={handleSaveBounds}
                  loading={randomizerMutation.isPending}
                  className="w-full"
                >
                  <Save className="inline-block w-5 h-5 mr-2" />
                  Enregistrer les Bornes
                </RacingButton>
              </div>
            </div>
          </RacingCard>
        )}
      </div>
    </div>
  )
}
