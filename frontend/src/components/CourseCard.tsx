interface CourseCardProps {
    id: number;
    name: string;
    onClick: (courseId: number) => void; // Добавьте этот пропс
}

export default function CourseCard({ id, name, onClick }: CourseCardProps) {
    return (
        <div className="course-card">
            <h3>{name}</h3>
            <button onClick={() => onClick(id)}> {/* Передаем id курса */}
                Выбрать
            </button>
        </div>
    );
}