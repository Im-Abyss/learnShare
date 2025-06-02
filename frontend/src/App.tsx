import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ThemeToggle from './components/ThemeToggle';
import CoursesPage from './pages/CoursesPage'
import PostsPage from './pages/PostsPage';

function App() {
  return (
    <>
      <ThemeToggle />
      <Routes>
        <Route path="/" element={<CoursesPage />} />
        <Route path='/disciplines/:disciplineId/posts' element={<PostsPage />}></Route>
      </Routes>
    </>
  )
}

export default App