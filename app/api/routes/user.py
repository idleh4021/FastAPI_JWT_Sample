from fastapi import APIRouter, Depends,Form
from sqlalchemy.orm import Session
from schemas import user as user_schema
from crud import user as user_crud
from typing import List
from services import user_service
from fastapi.security import OAuth2PasswordBearer
from api import deps


router = APIRouter()

@router.post('/signup', response_model=user_schema.UserRead,summary='회원가입')
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    return user_service.create_user(db, user)

#@router.get('/{user_id}', response_model=user_schema.UserRead)
@router.get('/me', response_model=user_schema.UserRead,summary='사용자 정보 조회')
def read_user(current_user = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    return user_crud.get_user(db, current_user.email)

@router.post('/login',summary='로그인',description='Access Token과 refresh Token이 발급됩니다.')
#def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
def login(email:str = Form(...),
          password:str = Form(...),
          device_id:str = Form(...),
          db:Session = Depends(deps.get_db)):
    loginModel = user_schema.Login(email=email,password=password,device_id = device_id)
    return user_service.login(db,loginModel)

@router.post('/refresh',summary='Access Token 재발급',description='refresh Token을 이용해서 Access Token을 재발급 합니다.')
def refresh(refresh_token:str,db:Session=Depends(deps.get_db)):
    return user_service.refresh(refresh_token,db)

@router.delete('/me',summary="사용자정보 삭제")
def delete_user(password:str=Form(...), current_user = Depends(deps.get_current_user),db:Session=Depends(deps.get_db)):
    return user_service.delete_user(current_user.id,current_user.email,password,db)
#@router.get('/', response_model=List[user_schema.UserRead])
#def get_all_user(db: Session = Depends(get_db)):
#    return user_crud.get_all_user(db)

@router.put('/me',summary='사용자정보 수정')
def user_update(user:user_schema.UserUpdate,current_user=Depends(deps.get_current_user),db:Session=Depends(deps.get_db)):
    return user_service.user_update(user,current_user.id,db)
    
