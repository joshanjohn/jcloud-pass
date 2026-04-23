"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from pydantic import BaseModel
from typing import Optional
from src.entities import Metadata, File

class Dir(BaseModel): 
    """
    Model for Directory entity 
    """
    id: str  # directory id  
    name: str # name of directory  
    meta: Metadata # meta data of directory  
    data: Optional[list[File | None]] = None # list of file data 



    
