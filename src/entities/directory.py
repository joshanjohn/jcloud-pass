from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class MetaData(BaseModel):
    path: str 
    created: datetime
    size: Optional[int] = 0
 


class Dir(BaseModel): 
    id: int 
    name: str 
    meta: MetaData

