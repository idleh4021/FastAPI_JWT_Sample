from fastapi import APIRouter, Depends,Form
from sqlalchemy.orm import Session
from schemas import todo as td_scheme
from crud import user as user_crud
from typing import List
from services import user_service
from fastapi.security import OAuth2PasswordBearer
from api import deps

router = APIRouter()

@router.post('/',summary='일정 생성')
def create_todo(create_todo:td_scheme.create_todo, current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'

@router.get('/',summary='일정 조회')
def get_todos_all(current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'

@router.get('/{id}',summary='일정 상세조회')
def get_todo(current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'

@router.put('/{id}',summary='일정 수정')
def todo_update(current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'

@router.delete('/{id}',summary='일정 삭제')
def todo_delete(current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'

@router.get('/search',summary='일정 정보 검색')
def get_todo_filter(current_user = Depends(deps.get_current_user),db: Session = Depends(deps.get_db)):
    return 'haha'
