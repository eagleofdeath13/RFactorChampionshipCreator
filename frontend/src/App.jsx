import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Talents from './pages/Talents'
import TalentDetail from './pages/TalentDetail'
import Championships from './pages/Championships'
import Vehicles from './pages/Vehicles'
import VehicleDetail from './pages/VehicleDetail'
import Tracks from './pages/Tracks'
import Import from './pages/Import'
import Config from './pages/Config'

// Placeholder for Championship Creator (à créer)
function ChampionshipCreator() {
  return (
    <div className="text-center py-12">
      <h2 className="text-3xl font-orbitron font-bold text-white mb-4">
        Championship Creator
      </h2>
      <p className="text-chrome-silver">
        Formulaire multi-étapes en cours de développement...
      </p>
    </div>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="talents">
          <Route index element={<Talents />} />
          <Route path=":name" element={<TalentDetail />} />
        </Route>
        <Route path="championships">
          <Route index element={<Championships />} />
          <Route path="create" element={<ChampionshipCreator />} />
        </Route>
        <Route path="vehicles">
          <Route index element={<Vehicles />} />
          <Route path=":path" element={<VehicleDetail />} />
        </Route>
        <Route path="tracks" element={<Tracks />} />
        <Route path="import" element={<Import />} />
        <Route path="config" element={<Config />} />
      </Route>
    </Routes>
  )
}

export default App
