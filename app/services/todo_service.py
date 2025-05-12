from sqlalchemy.orm import Session
from app.db.models import Todo
from app.schemas import todo as td_scheme
from typing import List, Optional
from datetime import datetime
from app.crud import todo as td_crud
from sqlalchemy import func

def create_todo(db: Session, user_id: int, todo_data: td_scheme.TodoCreate):
    return td_crud.create_todo(db,user_id,todo_data)

def get_todos(db: Session, user_id: int):
    return td_crud.get_todos(db,user_id)

def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def update_todo(db: Session, todo_id: int, user_id: int, update_data: td_scheme.TodoUpdate):
    todo = td_crud.update_todo(db,todo_id,user_id,update_data)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = get_todo_by_id(db, todo_id, user_id)
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return True

def search_todos(db: Session, user_id: int, title: Optional[str],date:Optional[datetime]):
    query =db.query(Todo).filter(Todo.user_id == user_id)
    if title and title.strip() != '':
        query = query.filter(Todo.title.ilike(f'%{title}%'))
    if date :
        query = query.filter( func.Date(Todo.todo_date)==date.date())
    return query.all()
        
