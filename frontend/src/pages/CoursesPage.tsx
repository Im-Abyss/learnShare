import { useEffect, useState } from "react";
import CourseCard from "@/components/CourseCard";
import DisciplinesModal from "@/components/DisciplinesModal";
import '../App.css';

interface Course {
    id: number;
    name: string;
}

export interface Discipline {  // Добавьте ключевое слово export
    id: number;
    name: string;
}

export default function CoursesPage() {
    const [courses, setCourses] = useState<Course[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [selectedCourse, setSelectedCourse] = useState<number | null>(null);
    const [disciplines, setDisciplines] = useState<Discipline[]>([]);
    const [isModalOpen, setIsModalOpen] = useState(false);

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await fetch('http://localhost:8000/courses');
                if (!response.ok) throw new Error('Ошибка загрузки курсов');
                setCourses(await response.json());
            } catch(err) {
                setError(err instanceof Error ? err.message : 'Неизвестная ошибка');
            } finally {
                setLoading(false);
            }
        };
        fetchCourses();
    }, []);

    const handleCourseClick = async (courseId: number) => {
        try {
            const response = await fetch(`http://localhost:8000/courses/${courseId}/disciplines`);
            if (!response.ok) throw new Error('Ошибка загрузки предметов');
            setDisciplines(await response.json());
            setSelectedCourse(courseId);
            setIsModalOpen(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Ошибка загрузки');
        }
    };

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <div className="courses-container">
            <h1>Выберите курс</h1>
            <div className="courses-grid">
                {courses.map((course) => (
                    <CourseCard 
                        key={course.id} 
                        id={course.id} 
                        name={course.name}
                        onClick={() => handleCourseClick(course.id)} 
                    />
                ))}
            </div>
            
            <DisciplinesModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                courseId={selectedCourse}
                disciplines={disciplines}
            />
        </div>
    );
}