import uvicorn

import sys
from pathlib import Path

# Добавляем корень проекта (LEARN_SHARE) в пути Python
sys.path.append(str(Path(__file__).parent.parent))

from db import Repo

if __name__ == '__main__':
    Repo().SetDb("Database.db")

    if Repo().GenerateDefaultTables():
        uvicorn.run(app='app:app',
                    reload=True)
