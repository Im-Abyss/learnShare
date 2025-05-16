import uvicorn
from app import app
from db import Sqlite


if __name__ == '__main__':
    
    uvicorn.run(app='app:app',
                reload=True)