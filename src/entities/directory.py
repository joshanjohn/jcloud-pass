from pydantic import BaseModel
from typing import Optional
from src.entities import Metadata, File

class Dir(BaseModel): 
    id: str 
    name: str 
    meta: Metadata
    data: Optional[list[File | None]] = None



    
