import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Settings, Save, CheckCircle2, AlertCircle } from 'lucide-react'
import { useState } from 'react'
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

  const handleSubmit = (e) => {
    e.preventDefault()
    mutation.mutate({
      rfactor_path: rfactorPath,
      current_player: currentPlayer,
    })
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
      </div>
    </div>
  )
}
