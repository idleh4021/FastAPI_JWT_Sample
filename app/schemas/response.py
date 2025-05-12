from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

class CudResponseModel(BaseModel):
    #id:int
    message:str
    
