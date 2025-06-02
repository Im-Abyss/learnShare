from .Database import Sqlite
from datetime import datetime
curseas = {1:'FirstCurse', 
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
    def GetPostByDiscipline(self, curse, discipline_name:str|None=None, discipline_id:int|None=None):
        '''
        Возвращает все посты указанной дисциплины или указанного id дисциплины, и указанного курса
        
        :param curse: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такой дисциплины нет (в этом курсе))
        '''
        if discipline_name == discipline_id == None: return (False, 'укажи хоть что-то')
        
        disciplines = self.GetDisciplinesNames(curse=curse)
        if discipline_name not in disciplines: return (False, 'Такой дисциплины нет')
        
        posts = self.sq.Get(table=curseas[curse], conditions={'discipline_name':discipline_name}, fetch_all=True)
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
        
        return (True, posts_list)

    def GetDisciplinesNames(self, curse:int) -> list:
        '''
        Возврящает все дисциплины
        
        :param curse: Номер курса (1-4)
        '''
        disciplines = self.sq.Get(table="disciplines", conditions={"curse":curse}, fetch_all=True, return_column='discipline_name', element_only=True)
        if disciplines == None:
            return []
        return disciplines
    
    def GetDisciplineID(self, curse:int, discipline_name:str):
        '''
        Возвращает ID дисциплины
        
        :param curse: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такой дисциплины нет (в этом курсе))
        '''
        disciplines = self.GetDisciplinesNames(curse=curse)
        if discipline_name not in disciplines: return (False, 'Такой дисциплины нет')
        
        disciplineID = self.sq.Get(table='discilines', conditions={'curse':curse, 'discipline_name':discipline_name}, return_column='id', element_only=True)
        return disciplineID

    # def GetCurseByDisciplineID(self, dis)

    
### ADD
    def AddDiscipline(self, curse:int, discipline_name:str) -> tuple[bool, str]:
        '''
        Добавляет новую дисциплину
        
        :param curse: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такая дисциплины есть (в этом курсе))
        '''
        disciplines = self.GetDisciplinesNames(curse=curse)
        if discipline_name in disciplines: return (False, 'Такая дисциплина уже есть')
        
        answer = self.sq.AddRow(table_name='disciplines', curse=curse, discipline_name=discipline_name)
        return (answer, 'Успешно')


    def AddPost(self, curse:int, discipline_name:str, text:str, title=None, file=None, photo=None, author=None, date=datetime.now()) -> tuple[bool, str]:
        '''
        Добавить новый пост
        
        :param curse: Номер курса (1-4)
        :param discipline_name: Название дисциплины (вернет False, если такой дисциплины нет)
        :param text: имя базы данных
        :param title: имя базы данных
        :param file: имя базы данных
        :param photo: имя базы данных
        :param author: имя базы данных
        :param date: имя базы данных
        '''

        disciplines = self.GetDisciplinesNames(curse=curse)
    
        if discipline_name not in disciplines: return (False, 'Такой дисциплины нет')
        answer = self.sq.AddRow(table_name=curseas[curse], 
                                discipline_name=discipline_name,
                                text=text,
                                title=title, 
                                file=file,
                                photo=photo,
                                author=author,
                                date=date
                                )
        return (answer, 'Успешно')


    def GenerateDefaultTables(self) -> bool:
        '''
        Вернет `True` если бд создались/уже есть
        
        :returns: bool
        '''
        a=self.sq.GenerateTable(
            table_name="FirstCurse",
            discipline_name="TEXT",
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
            discipline_name="TEXT",
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
            discipline_name="TEXT",
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
            discipline_name="TEXT",
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
    