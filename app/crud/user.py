from sqlalchemy.orm import Session
from app.db import models
from app.schemas import user as user_schema

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_user_by_id(db: Session, id: str):
    return db.query(models.User).filter(models.User.id == id).first()

def get_all_user(db:Session):
    return db.query(models.User).all()

def delete_user(id:int,db:Session):
    cnt = db.query(models.User).filter(models.User.id ==id).delete()
    db.commit()
    return cnt

def user_update(user_update:user_schema.UserUpdate,user:models.User,db:Session):
    print(user_update)
    user.name = user_update.name
    user.password = user_update.new_password
    db.commit()
#def email_exists(db:Session, email : str):
#    return db.query(models.User).filter(models.User.email == email).first() 