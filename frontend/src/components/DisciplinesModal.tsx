import { Discipline } from "@/pages/CoursesPage";
import './Modal.css';

interface DisciplinesModalProps {
    isOpen: boolean;
    onClose: () => void;
    courseId: number | null;
    disciplines: Discipline[];
}

export default function DisciplinesModal({
    isOpen,
    onClose,
    courseId,
    disciplines
}: DisciplinesModalProps) {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <button className="close-button" onClick={onClose}>×</button>
                <h2>Предметы {courseId} курса</h2>
                <ul className="disciplines-list">
                    {disciplines.map(discipline => (
                        <li key={discipline.id} className="discipline-item">
                            {discipline.name}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}