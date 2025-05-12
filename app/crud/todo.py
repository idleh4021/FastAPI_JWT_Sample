from sqlalchemy.orm import Session
from app.db.models import Todo
from app.schemas import todo as td_scheme
from datetime import datetime



def create_todo(db: Session, user_id: int, todo_data: td_scheme.TodoCreate):
    todo = Todo(
        user_id=user_id,
        title=todo_data.title,
        description=todo_data.description,
        todo_date=todo_data.todo_date,
        complete=0
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def get_todos(db: Session, user_id: int):
    return db.query(Todo).filter(Todo.user_id == user_id).all()

def get_todo_by_id(db: Session, todo_id: int, user_id: int):
    return db.query(Todo).filter(Todo.id == todo_id, Todo.user_id == user_id).first()

def update_todo(db: Session, todo_id: int, user_id: int, update_data: td_scheme.TodoUpdate):
    todo = get_todo_by_id(db, todo_id, user_id)
    if not todo:
        return None
    for key, value in update_data.dict(exclude_unset=True).items():
        setattr(todo, key, value)
    todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    todo = get_todo_by_id(db, todo_id, user_id)
    if not todo:
        return None
    db.delete(todo)
    db.commit()
    return True

def search_todos(db: Session, user_id: int, keyword: str):
    return db.query(Todo).filter(
        Todo.user_id == user_id,
        Todo.title.ilike(f'%{keyword}%')
    ).all()