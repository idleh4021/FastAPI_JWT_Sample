from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    title: str = Field(..., description="할 일 제목")
    description: Optional[str] = Field(None, description="할 일 설명")
    todo_date: Optional[datetime] = Field(None, description="할 일 날짜")

class TodoUpdate(BaseModel):
    title: Optional[str]  = Field(..., description="할 일 제목")
    description: Optional[str]   = Field(..., description="할 일 설명")
    todo_date: Optional[datetime] = Field(..., description="할 일 날짜")
    complete: Optional[int]   = Field(..., description="완료여부")

class TodoResponse(BaseModel):
    id: int = Field(..., description="ID")
    user_id: int=Field(..., description="사용자ID")
    title: Optional[str]  = Field(..., description="할 일 제목")          
    description: Optional[str] = Field(..., description="할 일 설명")
    todo_date: Optional[datetime]  = Field(..., description="할 일 날짜")
    complete: int  = Field(..., description="완료여부")
    created_at: datetime  = Field(..., description="생성일")
    updated_at: Optional[datetime]  = Field(..., description="수정일")

    class Config:
        orm_mode = True
