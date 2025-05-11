from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class refresh_token_info(BaseModel):
    #id:int
    refresh_token : str
    expired_at : datetime