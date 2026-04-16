from pydantic import BaseModel
from src.entities import Metadata

class File(BaseModel): 
    id: str
    name: str
    meta: Metadata