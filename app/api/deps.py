from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from utils import jwt_handler as jwt
from db.models import User
from db.database import SessionLocal
from jose import ExpiredSignatureError

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
api_key_scheme = APIKeyHeader(name="Authorization", auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

def get_current_user(token: str = Depends(api_key_scheme), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    #print(f'token is str : {type(token)}')
    try:
        payload = jwt.decode_token(str(token))
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    id = payload.get("sub")

    if id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user


