"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from typing import Optional
from pydantic import BaseModel


class User(BaseModel): 
    """
    Model for User entity 
    """

    id: str  # user id 
    name: Optional[str] = None # user name 
    email: Optional[str] = None # user email 
    