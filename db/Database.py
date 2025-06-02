import sqlite3

class Sqlite:
    
    # Singleton Init
    ##### СИГНЛТОН ОЗНАЧАЕТ ЧТО ПАРАМЕТР db_name НАДО ПЕРЕДАТЬ ТОЛЬКО 1 РАЗ В ФАЙЛЕ MAIN.PY
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, db_name:str=None):
        '''
        `isNotBotDatabase = True`, если вы подключаетесь к основной таблице, связывающей все таблицы\n
        `isNotBotDatabase изнач. = False`
        '''
        if not hasattr(self, "_initialized"):   
            self.db_name = db_name.replace('.db', '')
            self.conn = sqlite3.connect(f'{self.db_name}.db')
            self.cursor = self.conn.cursor()


    def GenerateTable(self, table_name:str, **kwargs) -> bool:
        '''
        
        '''
        try:
            values = ''
            rows = list(kwargs.keys())
            params = list(kwargs.values())

            for i in range(len(list(rows))):
                values += f"{rows[i]} {params[i]},"
            else:
                values = values[:-1]

            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS "{table_name}" (
                id INTEGER PRIMARY KEY,
                {values}
            );
            ''')

            self.conn.commit()
            return True

        except Exception as e:
            print('[sql GenerateTable]',e)
            return False

    def GetTables(self, is_company:bool=False) -> list|bool:
        '''
        is_company 
        True - вернуть только компании
        False - вернуть все
        '''
        try:
            command = "SELECT name FROM sqlite_master WHERE type='table'"
            self.cursor.execute(command)
            tables = self.cursor.fetchall()

            if is_company:
                retlist = [i[0] for i in tables if not('Auto' in i[0] or i[0] == 'Users' or i[0] == 'Main')]
            else:
                retlist = [i[0] for i in tables]

            self.conn.commit()
            return retlist

        except Exception as e:
            print('[sql GetTables]', e)
            return False
    
    def UpdateTableName(self, old_table_name, new_table_name):
        try:
            command = f''' 
            ALTER TABLE "{old_table_name}" RENAME TO "{new_table_name}";
            '''
            self.cursor.execute(command)
            self.conn.commit()

        except Exception as e:
            print('[sql AddRow]', e)
            return False

    def AddField(self, table_name, field_name, field_type):
        command = f'ALTER TABLE "{table_name}" ADD COLUMN "{field_name}" {field_type};'
        self.cursor.execute(command)
        self.conn.commit()
        
        return True
            
    def AddRow(self, table_name, **kwargs) -> bool:
        
        try:
            values = '?,'*(len(kwargs)-1) + '?'

            command = f''' 
            INSERT INTO "{table_name}" ({", ".join(list(kwargs.keys()))})
            VALUES ({values})
            '''

            self.cursor.execute(command, tuple(kwargs.values()))
            self.conn.commit()
            return True

        except Exception as e:
            print('[sql AddRow]', e)
            return False

    def CopyTable(self, old_table_name, new_table_name) -> bool:
        try:
            # 1. Проверка: существует ли старая таблица
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (old_table_name,))
            if not self.cursor.fetchone():
                raise ValueError(f"Таблица '{old_table_name}' не существует.")

            # 2. Проверка: не существует ли уже новая таблица
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (new_table_name,))
            if self.cursor.fetchone():
                raise ValueError(f"Таблица '{new_table_name}' уже существует.")

            # 3. Копирование структуры (без данных)
            self.cursor.execute(f'CREATE TABLE "{new_table_name}" AS SELECT * FROM "{old_table_name}" WHERE 0')

            # 4. Копирование данных
            self.cursor.execute(f'INSERT INTO "{new_table_name}" SELECT * FROM "{old_table_name}"')

            self.conn.commit()
            print(f"Таблица '{old_table_name}' успешно скопирована в '{new_table_name}'.")

            return True

        except sqlite3.Error as e:
            print(f"[ОШИБКА] {e}")
            return False

#Get
    def Get(self, table:str, conditions:dict|None = None, 
        return_column=None, fetch_all=False, element_only=False, 
        logic="AND", method="="):
        """
        :param table: имя таблицы
        :param conditions: словарь {column: value}, для поиска
        :param return_column: колонка, которую нужно вернуть (если element_only)
        :param fetch_all: вернуть все строки или только одну
        :param element_only: вернуть одно поле или всю строку
        :param logic: 'AND' или 'OR' между условиями
        :param method: '=', 'LIKE' или 'REGEXP'
        """
        try:
            if element_only and return_column is None:
                raise ValueError("При element_only=True нужно указать return_column")

            if method not in ["=", "LIKE", "REGEXP"]:
                raise ValueError("method должен быть '=', 'LIKE' или 'REGEXP'")

            # SELECT часть
            select_part = return_column if element_only else "*"

            # WHERE часть
            where_str = ""
            values = []
            if conditions:
                where_clauses = [f'"{col}" {method} ?' for col in conditions]
                where_str = " WHERE " + f" {logic} ".join(where_clauses)
                values = list(conditions.values())
            else:
                where_str = ""
                values = []

            # Финальный запрос
            query = f'SELECT {select_part} FROM "{table}"{where_str}'
            self.cursor.execute(query, values)

            result = self.cursor.fetchall() if fetch_all else self.cursor.fetchone()

            # Обработка результата
            if element_only:
                if fetch_all:
                    return [row[0] for row in result]
                else:
                    return result[0] if result else None
            else:
                return result

        except sqlite3.OperationalError as e:
            print(f"[ОШИБКА БД] {e}")
            return None

#замена данных
    def Replace(self, table_name: str, updates: dict, conditions: dict = None,
            logic: str = "AND", method: str = "=") -> bool:
        """
        Обновляет значения в таблице по условиям.

        :param table_name: имя таблицы
        :param updates: словарь {column: new_value}, что обновить
        :param conditions: словарь {column: value}, по каким условиям искать
        :param logic: логика между условиями (AND / OR)
        :param method: тип сравнения (=, LIKE, REGEXP)
        :return: True при успехе, False при ошибке
        """
        try:
            if method not in ["=", "LIKE", "REGEXP"]:
                raise ValueError("method должен быть '=', 'LIKE' или 'REGEXP'")

            if not updates:
                raise ValueError("updates не должен быть пустым")

            # SET часть
            set_clause = ", ".join([f'"{col}" = ?' for col in updates])
            set_values = list(updates.values())

            # WHERE часть
            where_clause = ""
            where_values = []
            if conditions:
                condition_parts = [f'"{col}" {method} ?' for col in conditions]
                where_clause = f' WHERE {" " + logic + " ".join(condition_parts)}'
                where_values = list(conditions.values())

            query = f'UPDATE "{table_name}" SET {set_clause}{where_clause}'

            self.cursor.execute(query, set_values + where_values)
            self.conn.commit()

            return True

        except Exception as e:
            print("[sql Replace]", e)
            return False


    def Count(self, table_name)-> int: 
        '''
        кол-во строк в таблице
        '''
        try:
            command = f'SELECT COUNT(*) FROM "{table_name}"'
            self.cursor.execute(command)

            self.conn.commit()
            return int(self.cursor.fetchone()[0])
        
        except Exception as e:
            print('[sql Count]', e)
            return False

    def LikeAll(self, param, value, table_name) -> int|bool:
        """
        получить кол-во совпадений строк формата {---}%

        SELECT COUNT(*) FROM {table_name} WHERE {param} LIKE '{value}'
        """
        try:
            command  =  f"""SELECT COUNT(*) FROM "{table_name}" WHERE {param} LIKE '{value}'"""

            self.cursor.execute(command)
            LikeAll = self.cursor.fetchone()[0]

            self.conn.commit()
            return int(LikeAll)

        except Exception as e:
            print('[sql LikeAll]', e)
            return False

#удаление данных
    def Delete(
        self,
        table,
        conditions:dict,
        like=False,
        delete_all=False,
        clear_column=None,
        clear_column_all_rows=False
    ) -> bool:
        """
        Удаляет строки или очищает значения в колонке по условиям.

        :param table: Имя таблицы.
        :param conditions: Словарь условий {column: value}.
        :param like: Использовать LIKE вместо точного сравнения.
        :param delete_all: Удалить все строки (True) или только одну (False).
        :param clear_column: Название колонки, в которой нужно удалить (очистить) значение.
        :param clear_column_all_rows: True — очистить во всех строках, False — только в одной.
        """
        try:

            if not conditions:
                raise ValueError("Условия должны быть заданы.")

            # Построение WHERE и значений
            if like:
                where_clause = " AND ".join([f"{col} LIKE ?" for col in conditions])
            else:
                where_clause = " AND ".join([f"{col} = ?" for col in conditions])
            values = list(conditions.values())

            if clear_column:
                # Очистка значения в колонке (обновление на NULL)
                if clear_column_all_rows:
                    query = f'UPDATE "{table}" SET {clear_column} = NULL WHERE {where_clause}'
                else:
                    query = f"""
                        UPDATE "{table}"
                        SET {clear_column} = NULL
                        WHERE rowid IN (
                            SELECT rowid FROM "{table}" WHERE {where_clause} LIMIT 1
                        )
                    """
            else:
                # Удаление строк
                if delete_all:
                    query = f'DELETE FROM "{table}" WHERE {where_clause}'
                else:
                    query = f"""
                        DELETE FROM "{table}"
                        WHERE rowid IN (
                            SELECT rowid FROM "{table}" WHERE {where_clause} LIMIT 1
                        )
                    """

            self.cursor.execute(query, values)
            self.conn.commit()
            print(f"Изменено строк: {self.cursor.rowcount}")
            return True

        except sqlite3.Error as e:
            print(f"[ОШИБКА БД Delete] {e}")
            return False

    def DeleteTable(self, table_name) -> bool:
        '''
        DROP TABLE IF EXISTS "{table_name}";
        '''

        try:
            command = f'DROP TABLE IF EXISTS "{table_name}";'
            self.cursor.execute(command)
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print('[sql DeleteTable]', e)
            return False

    def DeleteDuplicates(self, table_name, is_users):
        command = f'''
            DELETE FROM "{table_name}"
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM "{table_name}"
                GROUP BY flag
            );
            '''

        if is_users:
            command = f'''
            DELETE FROM "{table_name}"
            WHERE rowid NOT IN (
                SELECT MIN(rowid)
                FROM "{table_name}"
                GROUP BY tg_id
            );
            '''

        self.cursor.execute(command)
        self.conn.commit() 

        return True

#системные функции
    def GetConnent(self):
        return self.conn

    def GetCursor(self):
        return self.cursor
