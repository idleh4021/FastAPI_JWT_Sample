from fastapi import APIRouter, Depends,Form
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.schemas import auth as auth_schema
from app.schemas import response
from app.crud import user as user_crud
from typing import List
from app.services import user_service
#from fastapi.security import OAuth2PasswordBearer
from app.api import deps
from fastapi import HTTPException
from app.schemas import enum as valid

router = APIRouter()
@router.post('/signup', response_model=user_schema.UserRead, summary='회원가입')
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    if user_service.get_user(db, user.email):
        raise HTTPException(
            status_code=400,
            detail=f"A user with the email '{user.email}' already exists."
        )
    else:
        result = user_service.create_user(db, user)
    return result


@router.get('/me', response_model=user_schema.UserRead, summary='사용자정보 조회')
def read_user(current_user=Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    return user_service.get_user(db, current_user.email)


@router.post('/login', response_model=auth_schema.response_login, summary='로그인', description='로그인에 성공하면 refresh_token과 access_token을 발급합니다.')
def login(
    email: str = Form(..., description="Email address"),
    password: str = Form(..., description="Password"),
    device_id: str = Form(..., description="Device ID"),
    db: Session = Depends(deps.get_db)
):
    login_model = user_schema.Login(email=email, password=password, device_id=device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Account not found.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    return user_service.login(db, login_model, account)


@router.post('/refresh', response_model=auth_schema.response_refresh, summary='access_token 갱신', description='refresh_token으로 access_token을 갱신 발급합니다.')
def refresh(refresh_token: str, db: Session = Depends(deps.get_db)):
    result, user_id, device_id = user_service.validate_refresh_token(refresh_token, db)

    if result == valid.RefreshValidationResult.NOT_FOUND:
        raise HTTPException(status_code=404, detail="Refresh token not found.")
    elif result == valid.RefreshValidationResult.EXPIRED:
        raise HTTPException(status_code=401, detail="Refresh token has expired.")
    elif result == valid.RefreshValidationResult.INVALID:
        raise HTTPException(status_code=400, detail="Invalid refresh token.")

    return user_service.refresh(user_id, device_id)


@router.delete('/me', response_model=response.CudResponseModel, summary="사용자정보 삭제")
def delete_user(password: str = Form(...), current_user=Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    login_model = user_schema.Login(email=current_user.email, password=password, device_id=current_user.device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Account not found.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    result = user_service.delete_user(current_user.id, current_user.email, password, db)
    return result


@router.put('/me', response_model=response.CudResponseModel, summary='사용자정보 수정')
def user_update(user: user_schema.UserUpdate, current_user=Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    login_model = user_schema.Login(email=current_user.email, password=user.old_password, device_id=current_user.device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="Account not found.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="Incorrect password.")

    return user_service.user_update(user, account, db)
