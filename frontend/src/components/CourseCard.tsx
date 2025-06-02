import { MouseEvent } from 'react';

interface CourseCardProps {
    id: number;
    name: string;
    isExpanded: boolean;
    onClick: () => void;
}

export default function CourseCard({ id, name, isExpanded, onClick }: CourseCardProps) {
    return (
        <div className={`course-card ${isExpanded ? 'expanded' : ''}`} onClick={onClick}>
            <div className="course-header">
                <h3>{name}</h3>
                <span className="arrow-icon">{isExpanded ? '▼' : '▶'}</span>
            </div>
        </div>
    );
}