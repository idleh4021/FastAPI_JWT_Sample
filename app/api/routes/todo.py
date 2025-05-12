from fastapi import APIRouter, Depends,Form,Query
from sqlalchemy.orm import Session
from app.schemas import todo as td_scheme
from app.crud import user as user_crud
from typing import List
from app.services import todo_service
from fastapi.security import OAuth2PasswordBearer
from app.api import deps
from fastapi import HTTPException
from typing import Optional
from datetime import datetime
from app.schemas import response

router = APIRouter()

@router.post("/", response_model=td_scheme.TodoResponse,summary='일정 생성')
def create_todo(todo: td_scheme.TodoCreate, db: Session = Depends(deps.get_db), current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    return todo_service.create_todo(db, user_id, todo)

@router.get("/", response_model=List[td_scheme.TodoResponse],summary='일정 조회')
def read_todos(db: Session = Depends(deps.get_db),  current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    return todo_service.get_todos(db, user_id)

@router.get("/{id}", response_model=td_scheme.TodoResponse,summary='특정 일정 조회')
def read_todo(id: int, db: Session = Depends(deps.get_db),  current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    todo = todo_service.get_todo_by_id(db, id, user_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.put("/{id}", response_model=td_scheme.TodoResponse,summary='일정 수정')
def update_todo(id: int, update_data: td_scheme.TodoUpdate, db: Session = Depends(deps.get_db),  current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    todo = todo_service.update_todo(db, id, user_id, update_data)
    return todo

@router.delete("/{id}",response_model =response.CudResponseModel ,summary='일정 삭제')
def delete_todo(id: int, db: Session = Depends(deps.get_db),  current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    deleted = todo_service.delete_todo(db, id, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found or unauthorized")
    result = response.CudResponseModel(message="Todo deleted")
    return result

@router.get("/search/", response_model=List[td_scheme.TodoResponse],summary='일정 정보 검색')
def search_todos(title: Optional[str]=Query(None,description='타이틀'),date: Optional[datetime]=Query(None,description='날짜'), db: Session = Depends(deps.get_db),  current_user = Depends(deps.get_current_user)):
    user_id = current_user.id
    return todo_service.search_todos(db, user_id, title,date)