from fastapi import APIRouter, Depends,Form
from sqlalchemy.orm import Session
from schemas import user as user_schema
from crud import user as user_crud
from typing import List
from services import user_service
from fastapi.security import OAuth2PasswordBearer
from api import deps


router = APIRouter()

@router.post('/signup', response_model=user_schema.UserRead)
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    return user_service.create_user(db, user)

#@router.get('/{user_id}', response_model=user_schema.UserRead)
@router.get('/me', response_model=user_schema.UserRead)
def read_user(current_user = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    return user_crud.get_user(db, current_user.email)

@router.post('/login')
#def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
def login(email:str = Form(...),
          password:str = Form(...),
          device_id:str = Form(...),
          db:Session = Depends(deps.get_db)):
    loginModel = user_schema.Login(email=email,password=password,device_id = device_id)
    return user_service.login(db,loginModel)
#@router.get('/', response_model=List[user_schema.UserRead])
#def get_all_user(db: Session = Depends(get_db)):
#    return user_crud.get_all_user(db)

