import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import '../App.css'

export interface Discipline {
  id: number;
  name: string;
}

interface Course {
  id: number;
  name: string;
}

export default function CoursesPage() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [disciplines, setDisciplines] = useState<Record<number, Discipline[]>>({});
  const [expandedCourses, setExpandedCourses] = useState<Set<number>>(new Set());
  const [newDisciplineName, setNewDisciplineName] = useState('');
  const [isAdding, setIsAdding] = useState(false);
  const [addingCourse, setAddingCourse] = useState<number | null>(null);
  
  useEffect(() => {
    fetch('http://localhost:8000/courses')
      .then(response => response.json())
      .then(data => setCourses(data));
  }, []);

  // Новая функция для загрузки дисциплин
  const fetchDisciplines = async (courseId: number) => {
    try {
      const response = await fetch(`http://localhost:8000/courses/${courseId}/disciplines`);
      if (!response.ok) {
        throw new Error('Ошибка загрузки дисциплин');
      }
      const data = await response.json();
      setDisciplines(prev => ({ ...prev, [courseId]: data }));
    } catch (error) {
      console.error('Ошибка:', error);
    }
  };

  const toggleCourse = (courseId: number) => {
    const newSet = new Set(expandedCourses);
    
    if (newSet.has(courseId)) {
      newSet.delete(courseId);
    } else {
      newSet.add(courseId);
      if (!disciplines[courseId]) {
        fetchDisciplines(courseId); // Используем новую функцию
      }
    }
    
    setExpandedCourses(newSet);
  };

  const handleAddDiscipline = async (courseId: number) => {
    if (!newDisciplineName.trim()) {
      alert('Название дисциплины не может быть пустым');
      return;
    }

    setIsAdding(true);
    try {
      const response = await fetch(
        `http://localhost:8000/courses/${courseId}/disciplines/add`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ title: newDisciplineName }),
        }
      );

      if (!response.ok) {
        throw new Error('Ошибка при добавлении дисциплины');
      }

      // Вместо получения новой дисциплины просто обновляем список
      await fetchDisciplines(courseId);
      
      // Сбрасываем состояние
      setNewDisciplineName('');
      setAddingCourse(null);
    } catch (error) {
      console.error('Ошибка:', error);
      alert('Не удалось добавить дисциплину');
    } finally {
      setIsAdding(false);
    }
  };

  // Остальной код компонента остается без изменений
  return (
    <div className="courses-page">
      <h1>Выберите курс</h1>
      <div className="courses-container">
        {courses.map(course => (
          <div key={course.id} className="course-wrapper">
            <CourseCard 
              id={course.id}
              name={course.name}
              isExpanded={expandedCourses.has(course.id)}
              onClick={() => toggleCourse(course.id)}
            />
            
            {expandedCourses.has(course.id) && (
              <div className="disciplines-dropdown">
                <ul className="disciplines-list">
                  {disciplines[course.id]?.length > 0 ? (
                    disciplines[course.id].map(discipline => (
                      <li key={discipline.id} className="discipline-item">
                        <Link 
                          to={`/disciplines/${discipline.id}/posts`}
                          state={{ disciplineName: discipline.name }}
                          className="discipline-link"
                        >
                          {discipline.name}
                        </Link>
                      </li>
                    ))
                  ) : (
                    <li className="discipline-item empty">
                      <span>Предметы не найдены</span>
                    </li>
                  )}

                  <li className="discipline-item">
                    {addingCourse === course.id ? (
                      <div className="add-discipline-form">
                        <input
                          type="text"
                          value={newDisciplineName}
                          onChange={(e) => setNewDisciplineName(e.target.value)}
                          placeholder="Название новой дисциплины"
                          className="discipline-input"
                        />
                        <div className="form-buttons">
                          <button 
                            onClick={() => handleAddDiscipline(course.id)}
                            disabled={isAdding || !newDisciplineName.trim()}
                            className="add-button"
                          >
                            {isAdding ? 'Добавление...' : 'Добавить'}
                          </button>
                          <button 
                            onClick={() => setAddingCourse(null)}
                            className="cancel-button"
                          >
                            Отмена
                          </button>
                        </div>
                      </div>
                    ) : (
                      <button 
                        onClick={() => setAddingCourse(course.id)}
                        className="add-discipline-button"
                      >
                        + Добавить дисциплину
                      </button>
                    )}
                  </li>
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}