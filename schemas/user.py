from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    id: str
    name: str
    password: str
    email: str
    

class UserRead(BaseModel):
    id: str
    name: str
    #password: str
    email: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True
