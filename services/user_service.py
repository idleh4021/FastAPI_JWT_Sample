from crud import user as user_crud
from schemas import user as user_schema
from fastapi import HTTPException
from sqlalchemy.orm import Session
import utils.bcrypt as bc

def create_user(db:Session,user:user_schema.UserCreate ):
    user_exists = user_crud.get_user(db,user.email)
    if(user_exists):
        raise HTTPException(
            status_code=400,
            detail=f"User with email '{user.email}' already exists."
        )
    print(f'create: {user.password}')
    user.password = bc.hash_password(user.password)
    print(user.password)
    return user_crud.create_user(db,user)

def login(db:Session,user:user_schema.Login):
    
    account = user_crud.get_user(db,user.email)
    if(user) is None:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find your Account"
        )
    if(bc.verify_password(user.password,account.password)):
        print('success') 
        #토큰 발행
    else:
        print('fail')
        #BadRequest