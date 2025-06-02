from .Database import Sqlite
from datetime import datetime
courseas =  {1:'Firstcourse', 
            2:'Secondcourse', 
            3:'Thirdcourse', 
            4:'Fourthcourse'}    



class Repo:
    '''
    Класс отвечающий за чтение/запись/изменение данных постов 
    '''
    # Singleton Init
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, "_initialized", False):
            return

        self.db_name = "Database"
        self.sq = Sqlite(db_name=self.db_name)
        self.connect = self.sq.GetConnent()
        self.cursor = self.sq.GetCursor()
        self._initialized = True

    ### GET
    def GetPostsByDiscipline(self, discipline_id:int) -> list:
        '''
        Возвращает все посты указанной дисциплины или указанного id дисциплины, и указанного курса
        Если курсов нет, вернет []
        :param discipline_id: ID дисциплины (вернет False, если такой дисциплины нет (в этом курсе))
        '''
        if not isinstance(discipline_id, int): return False 
        if discipline_id > self.GetDisciplineIDs(): return False
        course = self.GetСourseByDisciplineID(discipline_id)
        
        posts = self.sq.Get(table=courseas[course], conditions={'discipline_id':discipline_id}, fetch_all=True)
        posts_list=[]
        
        for i in posts:
            new_value = {
                'id':i[0],
                'title':i[2],
                'text':i[3],
                'file':i[4],
                'photo':i[5],
                'author':i[6],
                'date':i[7]
            }
            # print(new_value)
            posts_list.append(new_value)
        # print(posts_list)
        return posts_list

    def GetDisciplineIDs(self, course:int|None=None) -> list|int:
        '''
        Возврящает все дисциплины
        Если курс не укажан, вернет ID последнего курса 
        
        :param course: Номер курса (1-4)
        '''
        if course:
            disciplinesID = self.sq.Get(table="disciplines", conditions={"course":course}, fetch_all=True, return_column='id', element_only=True)
            if disciplinesID == None:
                return []
            return disciplinesID
        
        disciplinesID = self.sq.GetLastRow(table="disciplines", id_column='id')
        if disciplinesID == None:
            return []
        return disciplinesID[0]

    def GetСourseByDisciplineID(self, discipline_id:int) -> int|None:
        '''
        Возвращает курс в котором находится данная дисциплина
        
        :param discipline_id: ID дисциплины
        '''
        answer = self.sq.Get(table='disciplines', 
                             conditions={"id":discipline_id}, 
                             return_column='course', element_only=True)
        return answer

    def GetDisciplineName(self, discipline_id:int) -> str|None:
        '''
        Возвращает Имя дисциплины по ее ID
        
        :param discipline_id: ID дисциплины
        '''
        answer = self.sq.Get(table='disciplines', 
                             conditions={'id':discipline_id}, 
                             return_column='discipline_name', element_only=True)
        return answer
    
    def GetDisciplinesNamesBycourse(self, course) -> list|None:
        answer = self.sq.Get(table='disciplines', 
                             conditions={"course":course}, 
                             return_column='discipline_name', element_only=True)
        if answer == None: answer = []
        return answer
    
    ### ADD
    def AddDiscipline(self, course:int, discipline_name:str) -> bool:
        '''
        Добавляет новую дисциплину
        
        :param course: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такая дисциплины есть (в этом курсе))
        '''
        disciplines = self.GetDisciplinesNamesBycourse(course=course)
        if discipline_name in disciplines: return False
        
        answer = self.sq.AddRow(table_name='disciplines', course=course, discipline_name=discipline_name)
        return answer

    def AddPost(self, discipline_id:int, text:str, title=None, file=None, photo=None, author=None, date=datetime.now()) -> bool:
        '''
        Добавить новый пост

        :param course: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такой дисциплины нет)
        :param text: Текст поста
        :param title: Title поста
        :param file: файл прикрепленный к посту
        :param photo: фото прикрепленное к посту
        :param author: автор поста
        :param date: дата создания поста
        '''

        if not isinstance(discipline_id, int): 
            print('discipline_id не тот')
            return False

        # if not isinstance() title
        # if not isinstance() file
        # if not isinstance() photo
        # if not isinstance() author

        if discipline_id > self.GetDisciplineIDs(): return False

        course = self.GetСourseByDisciplineID(discipline_id)

        answer = self.sq.AddRow(
            table_name=courseas[course], 
            discipline_id=discipline_id,
            text=str(text),
            title=title, 
            file=file,
            photo=photo,
            author=author,
            date=date
            )

        return answer


    ### DELETE
    def DeletePost(self, post_id:int, discipline_id:int) -> bool:
        course = self.GetСourseByDisciplineID(discipline_id=discipline_id)
        
        answer = self.sq.Delete(
            table=courseas[course],
            conditions={'id':post_id}
            )
        return answer 
    
    def DeleteDiscipline(self, discipline_id:int) -> bool:
        course = self.GetСourseByDisciplineID(discipline_id=discipline_id)
        answer1 = self.sq.Delete(table='disciplines', conditions={'id':discipline_id})
        answer2 = self.sq.Delete(table=courseas[course], conditions={'discipline_id':discipline_id}, delete_all=True)
        return answer1 and answer2

    
    ### REDACT
### Разное 
    def GenerateDefaultTables(self) -> bool:
        '''
        Вернет `True` если бд создались/уже есть
        
        :returns: bool
        '''
        a=self.sq.GenerateTable(
            table_name="FirstСourse",
            discipline_id="INTEGER",
            title='TEXT',
            text='TEXT',
            file='TEXT',
            photo='TEXT',
            author='TEXT',
            date='TEXT'
            # FOREIGN_KEY="(course_id) REFERENCES courses(id)"
        )

        b=self.sq.GenerateTable(
            table_name="SecondСourse",
            discipline_id="INTEGER",
            title='TEXT',
            text='TEXT',
            file='TEXT',
            photo='TEXT',
            author='TEXT',
            date='TEXT'
            # FOREIGN_KEY="(course_id) REFERENCES courses(id)"
        )

        c=self.sq.GenerateTable(
            table_name="ThirdСourse",
            discipline_id="INTEGER",
            title='TEXT',
            text='TEXT',
            file='TEXT',
            photo='TEXT',
            author='TEXT',
            date='TEXT'
            # FOREIGN_KEY="(course_id) REFERENCES courses(id)"
        )

        d=self.sq.GenerateTable(
            table_name="FourthСourse",
            discipline_id="INTEGER",
            title='TEXT',
            text='TEXT',
            file='TEXT',
            photo='TEXT',
            author='TEXT',
            date='TEXT'
            # FOREIGN_KEY="(course_id) REFERENCES courses(id)"
        )

        e=self.sq.GenerateTable(
            table_name="disciplines",
            course="INTEGER",
            discipline_name="TEXT"
        )
        return a and b and c and d and e
        # return True
        #Если хоть одно будет False   return -> False
