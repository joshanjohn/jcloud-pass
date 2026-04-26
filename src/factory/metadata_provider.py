"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.entities import File

class MetadataProvider(ABC):
    """
    Interface for File management metadata
    """

    @abstractmethod
    def get_user_record(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Method to return user record for a given: 
        - user id
        """
        pass
   
    @abstractmethod
    def get_all_directories(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Method to return all directories for given: 
        - user_id 
        """
        pass

    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> None:
        """
        Method to create new user record for given: 
        - user_data
        """
        pass

    @abstractmethod
    def create_file_record(self, user_id: str, file: File, path: str) -> None: 
        """
        Method to create file record of file with path for given: 
        - user_id
        - file
        - path
        """
        pass

    @abstractmethod
    def add_directory(self, user_id: str, dir_data: Dict[str, Any]) -> bool:
        """
        Method to create/add new directory record for given 
        - user_id 
        - dir_data  
        """
        pass

    @abstractmethod
    def remove_directory(self, user_id: str, dir_path: str) -> None:
        """
        Method to remove directory record for given: 
        - user_id 
        - dir_dir
        """
        pass

    @abstractmethod
    def remove_file_record(self, user_id: str, file_id: str, path: str) -> bool:
        """
        Method to remove file remove file record for given: 
        - user_id
        - file_id
        - path
        """
        pass

    @abstractmethod
    def update_size(self, user_id: str, dir_path: str, size_delta: float) -> None:
        """
        Method to update directory size for the given path and all parents.
        """
        pass
