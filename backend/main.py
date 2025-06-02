import uvicorn
from app import app
from db import Repo


if __name__ == '__main__':
    Repo().SetDb("Database.db")

    if Repo().GenerateDefaultTables():
        uvicorn.run(app='app:app',
                    reload=True)
