# FastAPI_JWT_Sample/init_db.py

from app.db.database import engine, Base
from app.db import models

def init_db():
    print('Creating tables...')
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print('Done.')

if __name__ == '__main__':
    init_db()
