from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .schemas import PostCreate, PostResponse
from .create_db import db
from utils.Database.Database import Sqlite


app = FastAPI(title='LearnShare')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Курсы. Тестовые данные, которые будут потом в БД
test_courses = [
    {'id': 1, 'name': '1 курс'},
    {'id': 2, 'name': '2 курс'},
    {'id': 3, 'name': '3 курс'},
    {'id': 4, 'name': '4 курс'}
]


# Предметы. Тестовые данные, которые будут потом в БД
test_disciplines = {
    1: [{'id': 1, 'name': 'Электроника'}, {'id': 2, 'name': 'Математика'}],
    2: [{'id': 3, 'name': 'БЖД'}]
}


# Посты. Тестовые данные, которые будут потом в БД
test_posts = {
    # ключ - id дисциплины
    1: [
        {
            'id': 1,
            'title': 'Это пост',
            'content': 'Тексты, файлы, фото и т. д.',
            'author': 'Слон',
            'date': 'Дата поста'
        },
    ],
    2: [
        {
            'id': 2,
            'title': 'Это тоже какой-то пост',
            'content': 'Тексты, файлы, фото и т. д.',
            'author': 'Автор поста',
            'date': 'Дата поста'
        }
    ],
    3: [
        {
            'id': 3,
            'title': 'Ещё какой-то пост',
            'content': 'Тексты, файлы, фото и т. д.',
            'author': 'Автор поста',
            'date': 'Дата поста'
        }
    ]
}


@app.get('/courses', 
         tags=['Пользовательская панель'], 
         description='Возвращает все курсы')
async def get_courses():
    return test_courses


@app.get('/courses/{course_id}/disciplines', 
         tags=['Пользовательская панель'], 
         description='Возвращает предметы по выбранному курсу')
async def get_disciplines(course_id: int):
    if course_id not in test_disciplines:
        raise HTTPException(status_code=404, detail="Course not found")
    return test_disciplines.get(course_id, '')


@app.get('/disciplines/{disciplines_id}/posts', 
         tags=['Пользовательская панель'], 
         description='Возвращает посты по выбранному премету')
async def get_posts(discipline_id: int):
    if discipline_id not in test_posts:
        raise HTTPException(
            status_code=404,
            detail="No posts found for this discipline"
        )
    return test_posts.get(discipline_id, '')


@app.post('/disciplines/{disciplines_id}/posts/add',
          tags=['Пользовательская панель'], 
          description='Добавление поста')
async def add_posts(discipline_id: int, post: PostCreate):
    pass