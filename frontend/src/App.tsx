import { Routes, Route } from 'react-router-dom'
import ThemeToggle from './components/ThemeToggle';
import CoursesPage from './pages/CoursesPage'

function App() {
  return (
    <>
      <ThemeToggle />
      <Routes>
        <Route path="/" element={<CoursesPage />} />
      </Routes>
    </>
  )
}

export default App