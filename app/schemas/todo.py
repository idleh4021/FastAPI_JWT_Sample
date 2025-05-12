from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(..., description="할 일 제목")
    description: Optional[str] = Field(None, description="할 일 설명")
    todo_date: Optional[datetime] = Field(None, description="실행 예정일")

class TodoUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    todo_date: Optional[datetime]
    complete: Optional[int]

class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    todo_date: Optional[datetime]
    complete: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
