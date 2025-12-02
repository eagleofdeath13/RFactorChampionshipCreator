import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Talents from './pages/Talents'
import TalentDetail from './pages/TalentDetail'
import TalentCreate from './pages/TalentCreate'
import TalentEdit from './pages/TalentEdit'
import Championships from './pages/Championships'
import ChampionshipDetail from './pages/ChampionshipDetail'
import ChampionshipDetailRFM from './pages/ChampionshipDetailRFM'
import ChampionshipCreate from './pages/ChampionshipCreate'
import Vehicles from './pages/Vehicles'
import VehicleDetail from './pages/VehicleDetail'
import VehicleEdit from './pages/VehicleEdit'
import Tracks from './pages/Tracks'
import TrackDetail from './pages/TrackDetail'
import Import from './pages/Import'
import Config from './pages/Config'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Dashboard />} />
        <Route path="talents">
          <Route index element={<Talents />} />
          <Route path="new" element={<TalentCreate />} />
          <Route path=":name/edit" element={<TalentEdit />} />
          <Route path=":name" element={<TalentDetail />} />
        </Route>
        <Route path="championships">
          <Route index element={<Championships />} />
          <Route path="create" element={<ChampionshipCreate />} />
          <Route path="rfm/:name" element={<ChampionshipDetailRFM />} />
          <Route path="cch/:name" element={<ChampionshipDetail />} />
          <Route path=":name" element={<ChampionshipDetail />} />
        </Route>
        <Route path="vehicles">
          <Route index element={<Vehicles />} />
          <Route path=":path/edit" element={<VehicleEdit />} />
          <Route path=":path" element={<VehicleDetail />} />
        </Route>
        <Route path="tracks">
          <Route index element={<Tracks />} />
          <Route path=":path" element={<TrackDetail />} />
        </Route>
        <Route path="import" element={<Import />} />
        <Route path="config" element={<Config />} />
      </Route>
    </Routes>
  )
}

export default App
