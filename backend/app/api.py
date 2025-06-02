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
test_courses = [
    {'id': 1, 'name': '1 курс'},
    {'id': 2, 'name': '2 курс'},
    {'id': 3, 'name': '3 курс'},
    {'id': 4, 'name': '4 курс'}
]
# Предметы. Тестовые данные, которые будут потом в БД
test_disciplines = {
    1: [{'id': 1, 'name': 'Физика'}, 
        {'id': 2, 'name': 'Высшая математика'}],
    2: [{'id': 3, 'name': 'Введение в инженерную деятельность'},
        {'id': 4, 'name': 'Материалловедение'},
        {'id': 5, 'name': 'Компьютерные технологии'},
        {'id': 6, 'name': 'Инженерная и компьютерная графика'}]
}


# Посты. Тестовые данные, которые будут потом в БД
test_posts = {
    # ключ - Название дисциплины
    "1": [
        {
            'id': 1,
            'text': 'Пост по физике без фото и файлов',
            'file': '',
            'photo': '',
            'author': 'Анонимный пост',
            'date': 'Дата поста'
        }
    ],
    "2": [
        {
            'id': 1,
            'text': 'Пересдать высшую математику можно будет до конца мая',
            'file': '',
            'photo': '',
            'author': 'Анонимный пост',
            'date': 'Дата поста'
        }
    ],
    "3": [
        {
            'id': 1,
            'text': 'Формулы для задания по линейной регрессии',
            'file': '',
            'photo': 'https://sun9-15.userapi.com/impg/l8UyBbmZrS59mWMISH6WvtXcJrvTD8CAOGzLbA/8i7OZU_JdSs.jpg?size=810x1080&quality=95&sign=516c77f5facddc344aa619fe0df22097&type=album',
            'author': 'Анонимный пост',
            'date': 'Дата поста'
        },
        {
            'id': 2,
            'text': 'Второй пост для этого же предмета',
            'file': '',
            'photo': 'https://sun9-15.userapi.com/impg/l8UyBbmZrS59mWMISH6WvtXcJrvTD8CAOGzLbA/8i7OZU_JdSs.jpg?size=810x1080&quality=95&sign=516c77f5facddc344aa619fe0df22097&type=album',
            'author': 'Анонимный пост',
            'date': 'Дата поста'
        }
    ],
    4: [
        {
            'id': 1,
            'text': 'Третья лаба',
            'file': '',
            'photo': 'https://sun9-19.userapi.com/impg/wpMQICaB6vXm0IDCYAII5IV00c8yzpSIq8YLLg/AVu1m8tsncg.jpg?size=810x1080&quality=95&sign=c73a23707a9a3c95269f241c6099c32b&type=album',
            'author': 'Анонимный пост',
            'date': 'Дата поста'
        }
    ],
    6: [
        {
            'id': 1,
            'text': 'Задание по инженерной графике',
            'file': '',
            'photo': 'https://sun9-3.userapi.com/impg/5gTuuxUaNXPD9s1DmHkuH98fOwE3g0VNJz131A/nqwkCYHjJIo.jpg?size=810x1080&quality=95&sign=29bff1d480b08cc46579ef2b0331ab39&type=album',
            'author': 'Анонимный пост',
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

    disciplines_ids = Repo().GetDisciplineIDs(curse=course_id)
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
         description='Возвращает предметы по выбранному курсу')
async def add_disciplines(course_id: int, discipline: DisciplineCreate):
    pass


@app.get('/courses/{course_id}/disciplines/{discipline_id}/delete', 
         tags=['Пользовательская панель'], 
         description='Возвращает предметы по выбранному курсу')
async def delete_disciplines(course_id: int):
    pass


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
    disciplines = Repo().GetDisciplineIDs()

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


@app.post('/disciplines/{disciplines_id}/posts/{posts_id}/delete')
async def delete_posts(disciplines_id: int, posts_id: int):
    pass
