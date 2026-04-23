"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Metadata(BaseModel):
    """
    Model for Metadata entity 
    """

    created: datetime # date time of created 
    updated: Optional[datetime] # date time of updated 
    size: Optional[float] = 0 # storage size 
    path: str # file location path  