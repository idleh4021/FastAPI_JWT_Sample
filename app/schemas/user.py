from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    #id: str
    email: str= Field(...,description="이메일 계정")
    name: str= Field(...,description="사용자 이름")
    password: str= Field(...,description="암호")
    

class UserUpdate(BaseModel):
    name:str = Field(...,description="사용자 이름")
    old_password:str = Field(...,description="기존 암호")
    new_password:str = Field(...,description="신규 암호")

class UserRead(BaseModel):
    id: int = Field(...,description="내부 고유아이디(자동생성)")
    email: str= Field(...,description="이메일 계정")
    name: str= Field(...,description="사용자 이름")
    #password: str
    created_at: Optional[datetime]= Field(...,description="생성날짜")
    updated_at: Optional[datetime]= Field(...,description="수정날짜")
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    email:str= Field(...,description="이메일 계정")
    password:str= Field(...,description="암호")
    device_id:str= Field(...,description="디바이스정보")
    
class UserDelete(BaseModel):
    password:str