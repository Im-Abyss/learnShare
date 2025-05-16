class Repo:

    # Singleton Init
    ##### СИГНЛТОН ОЗНАЧАЕТ ЧТО ПАРАМЕТР db_name НАДО ПЕРЕДАТЬ ТОЛЬКО 1 РАЗ В ФАЙЛЕ MAIN.PY
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    class Get:
        ...
    
    class Add:
        ...
        
    class Replace: