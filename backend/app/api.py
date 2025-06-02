from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PostCreate, DisciplineCreate
from db import Repo


app = FastAPI(title='LearnShare')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


#Оставляем так 
# Курсы. Тестовые данные, которые будут потом в БД
courses = [
    {'id': 1, 'name': '1 курс'},
    {'id': 2, 'name': '2 курс'},
    {'id': 3, 'name': '3 курс'},
    {'id': 4, 'name': '4 курс'}
]


@app.get('/courses', 
         tags=['Пользовательская панель'], 
         description='Возвращает все курсы')
async def get_courses():
    return courses


@app.get('/courses/{course_id}/disciplines', 
         tags=['Пользовательская панель'], 
         description='Возвращает предметы по выбранному курсу')
async def get_disciplines(course_id: int):

    disciplines_ids = Repo().GetDisciplineIDs(course=course_id)
    if course_id not in disciplines_ids:
        raise HTTPException(status_code=404, detail="Course not found")
    
    disciplines = []
    for discipline_id in disciplines_ids:
        name = Repo().GetDisciplineName(discipline_id=discipline_id)
        data = {'id':discipline_id, 'name': name}
        disciplines.append(data)
        
    return disciplines


@app.get('/courses/{course_id}/disciplines/add', 
         tags=['Пользовательская панель'], 
         description='Добавляет дисциплину к выбранному курсу')
async def add_disciplines(course_id: int, discipline: DisciplineCreate):
    answer = Repo().AddDiscipline(course=course_id, discipline_name=discipline.title)
    if answer: return 200
    return 404


@app.get('/courses/{course_id}/disciplines/{discipline_id}/delete', 
         tags=['Пользовательская панель'], 
         description='Удаляет выбранную дисциплину')
async def delete_disciplines(discipline_id: int):
    answer = Repo().DeleteDiscipline(discipline_id=discipline_id)
    if answer: return 200
    return 404


@app.get('/disciplines/{discipline_id}/posts', 
         tags=['Пользовательская панель'], 
         description='Возвращает посты по выбранному премету')
async def get_posts(discipline_id: int):
        
    posts = Repo().GetPostsByDiscipline(discipline_id=discipline_id)
    return sorted(posts, key=lambda x: x["id"], reverse=True)


@app.post('/disciplines/{disciplines_id}/posts/add',
          tags=['Пользовательская панель'], 
          description='Добавление поста')
async def add_posts(disciplines_id: int, post: PostCreate):

    new_post = {
        'title': post.title,
        'text': post.text,
        'file': post.file,
        'photo': post.photo,
        'author': post.author,
        'date': post.date or datetime.now().strftime("%d.%m.%Y")
    }

    answer = Repo().AddPost(
        discipline_id = disciplines_id,
        title = post.title,
        text = post.text,
        file = post.file,
        photo = post.photo,
        author = post.author,
        date = post.date or datetime.now().strftime("%d.%m.%Y")
    )
    
    if answer: return new_post


@app.post('/disciplines/{disciplines_id}/posts/{posts_id}/delete',
          tags=['Пользовательская панель'], 
          description='Удаление поста')
async def delete_posts(disciplines_id: int, posts_id: int):
    answer = Repo().DeletePost(post_id=posts_id, discipline_id=disciplines_id)
    if answer: return 200
    return 404
