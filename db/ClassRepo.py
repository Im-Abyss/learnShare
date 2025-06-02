from .Database import Sqlite
from datetime import datetime
curseas =  {1:'FirstCurse', 
            2:'SecondCurse', 
            3:'ThirdCurse', 
            4:'FourthCurse'}    

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
        if not hasattr(self, "_initialized"): 
            return

    def SetDb(self, db_name):
        '''
        :param db_name: имя базы данных
        '''
        self.db_name = db_name
        self.sq = sq = Sqlite(db_name=db_name)
        self.connect = sq.GetConnent()
        self.cursor = sq.GetCursor()

### GET
    def GetPostsByDiscipline(self, discipline_id:int) -> tuple:
        '''
        Возвращает все посты указанной дисциплины или указанного id дисциплины, и указанного курса
        Если курсов нет, вернет []
        :param discipline_id: ID дисциплины (вернет False, если такой дисциплины нет (в этом курсе))
        '''
        if isinstance(discipline_id, int): return False 
        if discipline_id > self.GetDisciplineIDs(): return False

        curse=self.GetCurseByDisciplineID(discipline_id)
        
        posts = self.sq.Get(table=curseas[curse], conditions={'discipline_id':discipline_id}, fetch_all=True)
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
            posts_list.append(new_value)
        
        return posts_list

    def GetDisciplineIDs(self, curse:int|None=None) -> list|int:
        '''
        Возврящает все дисциплины
        Если курс не укажан, вернет ID последнего курса 
        
        :param curse: Номер курса (1-4)
        '''
        
        if curse:
            disciplinesID = self.sq.Get(table="disciplines", conditions={"curse":curse}, fetch_all=True, return_column='id', element_only=True)
            if disciplinesID == None:
                return []
            return disciplinesID
        
        disciplinesID = self.sq.GetLastRow(table="disciplines", id_column='id')
        if disciplinesID == None:
            return []
        return disciplinesID[0]

    def GetCurseByDisciplineID(self, discipline_id:int) -> int|None:
        answer = self.sq.Get(table='disciplines', conditions={"id":discipline_id}, return_column='curse', element_only=True)
        return answer

    def GetDisciplineName(self, discipline_id:int) -> str|None:
        answer = self.sq.Get(table='disciplines', conditions={'discipline_id':discipline_id}, element_only=True)
        return answer

### ADD
    def AddDiscipline(self, curse:int, discipline_name:str) -> bool:
        '''
        Добавляет новую дисциплину
        
        :param curse: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такая дисциплины есть (в этом курсе))
        '''
        disciplines = self.GetDisciplinesNames(curse=curse)
        if discipline_name in disciplines: return False
        
        answer = self.sq.AddRow(table_name='disciplines', curse=curse, discipline_name=discipline_name)
        return answer

    def AddPost(self, discipline_id:int, text:str, title=None, file=None, photo=None, author=None, date=datetime.now()) -> bool:
        '''
        Добавить новый пост

        :param curse: Номер курса (1-4)
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

        # if isinstance() title
        # if isinstance() file
        # if isinstance() photo
        # if isinstance() author

        if discipline_id > self.GetDisciplineIDs(): return False

        curse = self.GetCurseByDisciplineID(discipline_id)

        answer = self.sq.AddRow(
            table_name=curseas[curse], 
            discipline_id=discipline_id,
            text=str(text),
            title=title, 
            file=file,
            photo=photo,
            author=author,
            date=date
            )

        return answer

    def AddDiscipline(self, curse:int, discipline_name:str):
        answer = self.sq.AddRow(table_name='disciplines', curse=curse, discipline_name=discipline_name)
        return answer


### Разное 
    def GenerateDefaultTables(self) -> bool:
        '''
        Вернет `True` если бд создались/уже есть
        
        :returns: bool
        '''
        a=self.sq.GenerateTable(
            table_name="FirstCurse",
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
            table_name="SecondCurse",
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
            table_name="ThirdCurse",
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
            table_name="FourthCurse",
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
            curse="INTEGER",
            discipline_name="TEXT"
        )
        return a and b and c and d and e
        #Если хоть одно будет False   return -> False
    