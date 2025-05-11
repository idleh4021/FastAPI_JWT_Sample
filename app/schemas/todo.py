from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class create_todo(BaseModel):
    user_id :str
    title  :str
    description:str
    todo_date : datetime
    complete :bool
    
    class Config:
        orm_mode = True