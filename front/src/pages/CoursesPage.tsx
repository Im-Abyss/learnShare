import { useEffect, useState } from "react";
import CourseCard from "@/components/CourseCard";
import '../App.css';

interface Course {
    id: number;
    name: string;
}

export default function CoursesPage() {
    const [courses, setCourses] = useState<Course[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response  = await fetch('http://localhost:8000/courses');
                if (!response.ok) {
                    throw new Error('Ошибка загрузки курсов');
                }
                const data = await response.json();
                setCourses(data);
            }   catch(err) {
                setError(err instanceof Error ? err.message : 'Неизвестная ошибка');
            } finally {
                setLoading(false);
            }
        };

        fetchCourses();
    }, []);

    if (loading) return <div>Загрузка...</div>;
    if (error) return <div>Ошибка: {error}</div>;

    return (
        <div className="courses-container">
            <h1>Выберите курс</h1>
            <div className="courses-grid">
            {courses.map((course) => (
                <CourseCard key={course.id} id={course.id} name={course.name} />
            ))}
            </div>
        </div>
    );
}