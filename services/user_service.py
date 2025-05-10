from crud import user as user_crud
from schemas import user as user_schema
from fastapi import HTTPException
from sqlalchemy.orm import Session

def create_user(db:Session,user:user_schema.UserCreate ):
    user_exists = user_crud.get_user(db,user.id)
    if(user_exists):
        raise HTTPException(
            status_code=400,
            detail=f"User with ID '{user.id}' already exists."
        )
    email_exists = user_crud.email_exists(db,user.email)
    if(email_exists):
        raise HTTPException(
            status_code=400,
            detail=f"email '{user.email}' already exists."
        )
    
    return user_crud.create_user(db,user)