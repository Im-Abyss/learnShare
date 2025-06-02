import { useParams, useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './PostsPage.css';

interface Post {
  id: number;
  text: string;
  file: string;
  photo: string;
  author: string;
  date: string;
  discipline_name?: string;
}

interface NewPost {
  text: string;
  file: string;
  photo: string;
  author: string;
}

export default function PostsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { disciplineId } = useParams<{ disciplineId: string }>();
  
  // Состояние для названия дисциплины
  const [disciplineName, setDisciplineName] = useState<string>(
    location.state?.disciplineName || 'Загрузка...'
  );
  
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newPost, setNewPost] = useState<NewPost>({
    text: '',
    file: '',
    photo: '',
    author: 'Анонимный пост',
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Устанавливаем название дисциплины из location.state
        if (location.state?.disciplineName) {
          setDisciplineName(location.state.disciplineName);
        }

        // Загружаем посты для дисциплины
        const postsResponse = await fetch(`http://localhost:8000/disciplines/${disciplineId}/posts`);
        
        if (!postsResponse.ok) {
          if (postsResponse.status === 404) {
            setPosts([]);
            return;
          }
          throw new Error('Ошибка загрузки постов');
        }
        
        const postsData = await postsResponse.json();
        setPosts(postsData || []);
        
        // Если в данных есть название дисциплины, используем его
        if (postsData.length > 0 && postsData[0].discipline_name) {
          setDisciplineName(postsData[0].discipline_name);
        }

      } catch (err) {
        console.error('Ошибка:', err);
        setPosts([]);
        setError(err instanceof Error ? err.message : 'Произошла ошибка');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [disciplineId, location.state]);

  const handleAddPost = async () => {
    if (!newPost.text.trim()) {
      alert('Текст поста не может быть пустым');
      return;
    }

    setIsSubmitting(true);

    try {
      const response = await fetch(`http://localhost:8000/disciplines/${disciplineId}/posts/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: newPost.text.trim(),
          file: newPost.file.trim() || '',
          photo: newPost.photo.trim() || '',
          author: newPost.author.trim() || 'Анонимный пост',
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(
          errorData?.detail || 
          errorData?.message || 
          `Ошибка сервера: ${response.status}`
        );
      }

      const addedPost = await response.json();
      setPosts([addedPost, ...posts]);
      setNewPost({
        text: '',
        file: '',
        photo: '',
        author: 'Анонимный пост',
      });
      setShowAddForm(false);

    } catch (err) {
      console.error('Ошибка при добавлении поста:', err);
      alert(`Ошибка: ${err instanceof Error ? err.message : 'Неизвестная ошибка'}`);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) return <div className="loading-message">Загрузка...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="posts-container">
      <h1>{disciplineName}</h1> {}
      <div className="posts-header">
        <button onClick={() => navigate('/')} className="home-button">
          На главную
        </button>
        <button 
          onClick={() => setShowAddForm(!showAddForm)} 
          className="add-post-button"
        >
          {showAddForm ? 'Отмена' : 'Добавить пост'}
        </button>
      </div>

      {showAddForm && (
        <div className="add-post-form">
          <h2>Добавить новый пост</h2>
          
          <textarea
            placeholder="Текст поста"
            value={newPost.text}
            onChange={(e) => setNewPost({...newPost, text: e.target.value})}
          />
          
          <input
            type="text"
            placeholder="Файл (ссылка на диск)"
            value={newPost.file}
            onChange={(e) => setNewPost({...newPost, file: e.target.value})}
          />
          
          <input
            type="text"
            placeholder="Фото (URL адрес)"
            value={newPost.photo}
            onChange={(e) => setNewPost({...newPost, photo: e.target.value})}
          />

          {/* Исправлено поле для автора: */}
          <input
            type="text"
            placeholder="Имя автора"
            value={newPost.author}
            onChange={(e) => setNewPost({...newPost, author: e.target.value})}
          />
          
          <button 
            onClick={handleAddPost}
            disabled={isSubmitting || !newPost.text.trim()}
          >
            {isSubmitting ? 'Отправка...' : 'Опубликовать'}
          </button>
        </div>
      )}
      
      <div className="posts-list">
        {posts.length > 0 ? (
          posts.map(post => (
            <div key={post.id} className="post-card">
              <p className="post-text">{post.text}</p>
              
              {/* Файл отображается только если есть значение */}
              {post.file && post.file.trim() !== "" && (
                <div className="post-file">
                  <span>Файл:</span> 
                  <a href={post.file} target="_blank" rel="noopener noreferrer">
                    {post.file.split('/').pop() || 'Скачать файл'}
                  </a>
                </div>
              )}
              
              {/* Фото отображается только если есть значение */}
              {post.photo && post.photo.trim() !== "" && (
                <div className="post-photo">
                  <img src={post.photo} alt="Прикрепленное фото" />
                </div>
              )}
              
              <div className="post-meta">
                <span>Автор: {post.author}</span>
                <span>Дата: {post.date}</span>
              </div>
            </div>
          ))
        ) : (
          <p className="no-posts-message">Пока нет постов для этого предмета</p>
        )}
      </div>
    </div>
  );
}