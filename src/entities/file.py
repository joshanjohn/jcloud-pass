"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from pydantic import BaseModel
from src.entities import Metadata

class File(BaseModel): 
    """
    Mode for File entity 
    """
    id: str # file id 
    name: str # file name
    meta: Metadata # file metadata 