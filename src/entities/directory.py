from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class DirMetaData(BaseModel):
    created: datetime
    updated: Optional[datetime] = created
    size: Optional[int] = 0
 


class Dir(BaseModel): 
    id: str 
    name: str 
    meta: DirMetaData

