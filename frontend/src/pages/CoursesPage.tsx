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

  useEffect(() => {
    fetch('http://localhost:8000/courses')
      .then(response => response.json())
      .then(data => setCourses(data));
  }, []);

  const toggleCourse = (courseId: number) => {
    const newSet = new Set(expandedCourses);
    
    if (newSet.has(courseId)) {
      newSet.delete(courseId);
    } else {
      newSet.add(courseId);

      if (!disciplines[courseId]) {
        fetch(`http://localhost:8000/courses/${courseId}/disciplines`)
          .then(response => response.json())
          .then(data => {
            setDisciplines(prev => ({ ...prev, [courseId]: data }));
          });
      }
    }
    
    setExpandedCourses(newSet);
  };

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
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}