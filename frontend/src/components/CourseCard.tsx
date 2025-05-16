interface CourseCardProps {
    id: number;
    name: string;
}

export default function CourseCard({ id, name }: CourseCardProps) {
    return (
        <div className="course-card">
            <h3>{name}</h3>
            <button onClick={() => console.log(`Selected course ${id}`)}>
                Выбрать
            </button>
        </div>
    );
}