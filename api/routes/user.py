from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas import user as user_schema
from crud import user as user_crud
from typing import List
from services import user_service
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=user_schema.UserRead)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user)

@router.get("/{user_id}", response_model=user_schema.UserRead)
def read_user(user_id: str, db: Session = Depends(get_db)):
    return user_crud.get_user(db, user_id)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    loginModel = user_schema.Login(email=form_data.username,password=form_data.password)
    return user_service.login(db,loginModel)
#@router.get("/", response_model=List[user_schema.UserRead])
#def get_all_user(db: Session = Depends(get_db)):
#    return user_crud.get_all_user(db)