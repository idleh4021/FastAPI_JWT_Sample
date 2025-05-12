from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class refresh_token_info(BaseModel):
    #id:int
    refresh_token : str= Field(...,description="refresh token")
    expired_at : datetime= Field(...,description="만료일")
    
class Access_token_Model (BaseModel):
    id:str
    email:str
    device_id:str
    
class response_refresh(BaseModel):
    access_token : str
    
class response_login(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str