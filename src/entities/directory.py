from pydantic import BaseModel
from datetime import datetime
from typing import Optional



class DirMetadata(BaseModel):
    created: datetime
    updated: Optional[datetime]
    size: Optional[float] = 0
 


class Dir(BaseModel): 
    id: str 
    name: str 
    meta: DirMetadata

