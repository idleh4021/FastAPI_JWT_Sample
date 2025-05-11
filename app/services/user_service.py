from crud import user as user_crud
from crud import auth as auth_crud
from schemas import user as user_schema
from schemas import auth as au
from fastapi import HTTPException
from sqlalchemy.orm import Session
from utils import bcrypt as bc
from utils import jwt_handler as jwt
from datetime import datetime

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
    if(account) is None:
        raise HTTPException(
            status_code=404,
            detail="Couldn't find your Account"
        )
    if(bc.verify_password(user.password,account.password)):
        access_token = jwt.create_access_token(data={"sub" : str(account.id)})
        refresh_token_dict = jwt.create_refresh_token(data={"sub" : str(account.id),"device_id":str(user.device_id)})
        refresh_token_info= au.refresh_token_info(**refresh_token_dict)                                            
        auth_crud.store_refresh_token(db,account.id,user.device_id,refresh_token_info)
        return {"access_token" : access_token , "refresh_token" : refresh_token_info.refresh_token , "token_type":"bearer"}
        #토큰 발행
    else:
        raise HTTPException(status_code=400,detail="Invalid credentials")
        #BadRequest
        
def delete_user(id:int,email:str,password:str,db:Session):
    user= user_crud.get_user(db,email)
    if bc.verify_password(password,user.password):
        cnt = user_crud.delete_user(id,db)
        if(cnt>0):
            return {"message":"User deleted","deleted":cnt}
        else :
            raise HTTPException(
            status_code=404,
            detail="Couldn't find your Account"
            )
            
    else :
        raise HTTPException(status_code=400,detail="Invalid credentials")
    
def refresh(refresh_token:str,db:Session):
    request_refresh_token = jwt.decode_token(refresh_token)
    id = request_refresh_token.get('sub')
    device_id = request_refresh_token.get('device_id')
    get_refresh_token = auth_crud.get_refresh_token(id,device_id,db)
    if get_refresh_token is None:
        raise HTTPException(status_code=404,detail="token not found")
    else :
        current_time = datetime.utcnow()
        if current_time>get_refresh_token.expired_at:
            raise HTTPException(status_code=401,detail="Token has expired.")
        elif refresh_token !=get_refresh_token.refresh_token:
            raise HTTPException(status_code=400,detail="invalid token")
        else :
            return {"access_token": jwt.create_access_token(data={"sub" : str(id)})}
            