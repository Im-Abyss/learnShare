import { Routes, Route } from 'react-router-dom'
import CoursesPage from './pages/CoursesPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<CoursesPage />} />
    </Routes>
  )
}

export default App