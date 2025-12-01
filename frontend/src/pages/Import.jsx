import { Upload, Download, FileText } from 'lucide-react'
import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { apiEndpoints } from '../services/api'
import PageHeader from '../components/PageHeader'
import RacingCard from '../components/RacingCard'
import RacingButton from '../components/RacingButton'

export default function Import() {
  const queryClient = useQueryClient()
  const [selectedFile, setSelectedFile] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const mutation = useMutation({
    mutationFn: async (file) => {
      const response = await apiEndpoints.import.talents(file)
      return response.data
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries(['talents'])
      toast.success(`${data.success_count} talent(s) importé(s) avec succès !`)
      setSelectedFile(null)
    },
    onError: (error) => {
      toast.error(`Erreur lors de l'import : ${error.message}`)
    },
  })

  const handleFileSelect = (file) => {
    if (file && file.name.endsWith('.csv')) {
      setSelectedFile(file)
    } else {
      toast.error('Veuillez sélectionner un fichier CSV')
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0])
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (selectedFile) {
      mutation.mutate(selectedFile)
    }
  }

  const downloadTemplate = async () => {
    try {
      const response = await apiEndpoints.import.template()
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'talents_template.csv')
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('Template téléchargé !')
    } catch (error) {
      toast.error('Erreur lors du téléchargement')
    }
  }

  return (
    <div>
      <PageHeader
        icon={Upload}
        title="Import CSV"
        subtitle="Importez vos talents depuis un fichier CSV"
      />

      <div className="max-w-3xl">
        {/* Template Download */}
        <RacingCard className="p-6 mb-6 border-l-4 border-status-info">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-orbitron font-bold text-lg text-white mb-2">
                Template CSV
              </h3>
              <p className="text-chrome-silver text-sm">
                Téléchargez le template pour voir le format requis
              </p>
            </div>
            <RacingButton variant="secondary" onClick={downloadTemplate}>
              <Download className="inline-block w-5 h-5 mr-2" />
              Télécharger
            </RacingButton>
          </div>
        </RacingCard>

        {/* Upload Form */}
        <RacingCard className="p-6">
          <form onSubmit={handleSubmit}>
            <div
              className={`border-2 border-dashed rounded p-12 text-center transition-all ${
                dragActive
                  ? 'border-status-success bg-status-success/10'
                  : 'border-chrome-silver/30 hover:border-racing-red/50'
              }`}
              onDragEnter={handleDrag}
              onDragLeave={handleDrag}
              onDragOver={handleDrag}
              onDrop={handleDrop}
            >
              <input
                type="file"
                id="file-upload"
                accept=".csv"
                onChange={(e) => handleFileSelect(e.target.files[0])}
                className="hidden"
              />

              <label htmlFor="file-upload" className="cursor-pointer">
                <FileText className="w-16 h-16 mx-auto mb-4 text-chrome-silver" />

                {selectedFile ? (
                  <>
                    <p className="text-white font-bold mb-2">{selectedFile.name}</p>
                    <p className="text-sm text-chrome-silver">
                      Cliquez sur Importer pour continuer
                    </p>
                  </>
                ) : (
                  <>
                    <p className="text-white font-bold mb-2">
                      Glissez-déposez un fichier CSV ici
                    </p>
                    <p className="text-sm text-chrome-silver mb-4">ou cliquez pour sélectionner</p>
                    <span className="inline-block px-4 py-2 bg-carbon-metal text-chrome-silver font-bold uppercase tracking-wide">
                      Choisir un fichier
                    </span>
                  </>
                )}
              </label>
            </div>

            {selectedFile && (
              <div className="mt-6">
                <RacingButton
                  type="submit"
                  variant="primary"
                  loading={mutation.isPending}
                  className="w-full"
                >
                  <Upload className="inline-block w-5 h-5 mr-2" />
                  Importer les talents
                </RacingButton>
              </div>
            )}
          </form>
        </RacingCard>

        {/* Instructions */}
        <RacingCard className="p-6 mt-6 border-l-4 border-fluo-yellow">
          <h4 className="font-orbitron font-bold text-white mb-3">Instructions</h4>
          <ul className="space-y-2 text-sm text-chrome-silver">
            <li>• Le fichier CSV doit contenir les colonnes: name, nationality, speed, crash, aggression</li>
            <li>• Les valeurs doivent être comprises entre 0 et 100</li>
            <li>• Téléchargez le template pour un exemple complet</li>
            <li>• Les talents existants avec le même nom seront mis à jour</li>
          </ul>
        </RacingCard>
      </div>
    </div>
  )
}
