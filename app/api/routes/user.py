from fastapi import APIRouter, Depends,Form
from sqlalchemy.orm import Session
from app.schemas import user as user_schema
from app.crud import user as user_crud
from typing import List
from app.services import user_service
#from fastapi.security import OAuth2PasswordBearer
from app.api import deps
from fastapi import HTTPException
from app.schemas import enum as valid

router = APIRouter()

@router.post('/signup', response_model=user_schema.UserRead,summary='회원가입')
def create_user(user: user_schema.UserCreate, db: Session = Depends(deps.get_db)):
    if user_service.get_user(db,user.email) :
        raise HTTPException(
            status_code=400,
            detail=f"User with email '{user.email}' already exists."
        )
        
    else :
        result = user_service.create_user(db,user)
    return result

#@router.get('/{user_id}', response_model=user_schema.UserRead)
@router.get('/me', response_model=user_schema.UserRead,summary='사용자 정보 조회')
def read_user(current_user = Depends(deps.get_current_user), db: Session = Depends(deps.get_db)):
    return user_service.get_user(db, current_user.email)

@router.post('/login', summary='로그인', description='Access Token과 Refresh Token이 발급됩니다.')
def login(
    email: str = Form(..., description="이메일 주소"),
    password: str = Form(..., description="비밀번호"),
    device_id: str = Form(..., description="디바이스 ID"),
    db: Session = Depends(deps.get_db)
):
    login_model = user_schema.Login(email=email, password=password, device_id=device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")

    return user_service.login(db, login_model, account)

@router.post('/refresh', summary='Access Token 재발급', description='Refresh Token을 이용해 Access Token을 재발급합니다.')
def refresh(refresh_token: str, db: Session = Depends(deps.get_db)):
    print('refrsh')
    result, user_id, device_id = user_service.validate_refresh_token(refresh_token, db)

    if result == valid.RefreshValidationResult.NOT_FOUND:
        raise HTTPException(status_code=404, detail="토큰이 존재하지 않습니다.")
    elif result == valid.RefreshValidationResult.EXPIRED:
        raise HTTPException(status_code=401, detail="Refresh Token이 만료되었습니다.")
    elif result == valid.RefreshValidationResult.INVALID:
        raise HTTPException(status_code=400, detail="유효하지 않은 Refresh Token입니다.")

    return user_service.refresh(user_id,device_id)

@router.delete('/me',summary="사용자정보 삭제")
def delete_user(password:str=Form(...), current_user = Depends(deps.get_current_user),db:Session=Depends(deps.get_db)):
    login_model = user_schema.Login(email=current_user.email, password=password, device_id=current_user.device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")
    
    result = user_service.delete_user(current_user.id,current_user.email,password,db)

    return result
#@router.get('/', response_model=List[user_schema.UserRead])
#def get_all_user(db: Session = Depends(get_db)):
#    return user_crud.get_all_user(db)

@router.put('/me',summary='사용자정보 수정')
def user_update(user:user_schema.UserUpdate,current_user=Depends(deps.get_current_user),db:Session=Depends(deps.get_db)):
    print(f'ddededededed{current_user.device_id}')
    login_model = user_schema.Login(email=current_user.email, password=user.old_password, device_id=current_user.device_id)
    validation_result, account = user_service.validate_login_and_get_user(db, login_model)

    if validation_result == valid.LoginValidationResult.USER_NOT_FOUND:
        raise HTTPException(status_code=404, detail="계정을 찾을 수 없습니다.")
    elif validation_result == valid.LoginValidationResult.INVALID_PASSWORD:
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")
    
    return user_service.user_update(user,account,db)
    
