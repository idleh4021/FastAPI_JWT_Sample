from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    #id: str
    email: str
    name: str
    password: str
    
    

class UserRead(BaseModel):
    id: int
    email: str
    name: str
    #password: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True

class Login(BaseModel):
    email:str
    password:str