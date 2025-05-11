from sqlalchemy.orm import Session
from db import models
from schemas import user as user_schema

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()

def get_all_user(db:Session):
    return db.query(models.User).all()

#def email_exists(db:Session, email : str):
#    return db.query(models.User).filter(models.User.email == email).first() 