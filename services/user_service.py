from crud import user as user_crud
from schemas import user as user_schema
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils.bcrypt import hash_password

def create_user(db:Session,user:user_schema.UserCreate ):
    user_exists = user_crud.get_user(db,user.email)
    if(user_exists):
        raise HTTPException(
            status_code=400,
            detail=f"User with email '{user.email}' already exists."
        )
    user.password = hash_password(user.password)
    
    return user_crud.create_user(db,user)