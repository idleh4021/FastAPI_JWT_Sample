from app.crud import user as user_crud
from app.crud import auth as auth_crud
from app.schemas import user as user_schema
from app.schemas import auth as au
from app.schemas import response
#from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.utils import bcrypt as bc
from app.utils import jwt_handler as jwt
from datetime import datetime
from app.schemas import  enum as valid

def get_user(db,email:str):
    return user_crud.get_user(db,email)

def create_user(db:Session,user:user_schema.UserCreate ):
    #print(f'create: {user.password}')
    user.password = bc.hash_password(user.password)
    #print(user.password)
    return user_crud.create_user(db,user)

def validate_login_and_get_user(db: Session, user: user_schema.Login) -> tuple[valid.LoginValidationResult, any]:
    account = get_user(db, user.email)
    if account is None:
        return valid.LoginValidationResult.USER_NOT_FOUND, None
    if not bc.verify_password(user.password, account.password):
        return valid.LoginValidationResult.INVALID_PASSWORD, None
    return valid.LoginValidationResult.OK, account

def login(db: Session, user: user_schema.Login, account):
    access_token = jwt.create_access_token(data={"sub": str(account.id), "device_id": str(user.device_id)})
    refresh_token_dict = jwt.create_refresh_token(data={"sub": str(account.id), "device_id": str(user.device_id)})
    refresh_token_info = au.refresh_token_info(**refresh_token_dict)

    auth_crud.store_refresh_token(db, account.id, user.device_id, refresh_token_info)
    result = au.response_login(access_token = access_token,refresh_token =refresh_token_info.refresh_token,token_type ='bearer')
    return result
    '''
    return {
        "access_token": access_token,
        "refresh_token": refresh_token_info.refresh_token,
        "token_type": "bearer"
    }
    '''
        #BadRequest
        
def delete_user(id:int,email:str,password:str,db:Session):
        cnt = user_crud.delete_user(id,db)
        result = response.CudResponseModel(message="User deleted")
        return result 



def validate_refresh_token(refresh_token: str, db: Session):
    try:
        request_refresh_token = jwt.decode_token(refresh_token)
    except Exception:
        return valid.RefreshValidationResult.INVALID, None, None

    user_id = request_refresh_token.get("sub")
    device_id = request_refresh_token.get("device_id")
    
    if not user_id or not device_id:
        return valid.RefreshValidationResult.INVALID, None, None

    stored_token = auth_crud.get_refresh_token(user_id, device_id, db)
    if stored_token is None:
        return valid.RefreshValidationResult.NOT_FOUND, None, None

    if stored_token.refresh_token != refresh_token:
        return valid.RefreshValidationResult.INVALID, None, None

    if datetime.utcnow() > stored_token.expired_at:
        return valid.RefreshValidationResult.EXPIRED, None, None

    return valid.RefreshValidationResult.VALID, user_id, device_id


def refresh(user_id:int,device_id:str):
    result = au.response_refresh(access_token=jwt.create_access_token(data={"sub" : str(user_id),"device_id" : str(device_id)}) )
    return result
    #return {"access_token": jwt.create_access_token(data={"sub" : str(user_id),"device_id" : device_id})}

def user_update(user:user_schema.UserUpdate,account,db:Session):
            user.new_password = bc.hash_password(user.new_password)
            user_crud.user_update(user,account,db)
            result = response.CudResponseModel(message="User information has been successfully updated")
            return result       