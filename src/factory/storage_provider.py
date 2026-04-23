"""
Author : Joshan John
Student Number : 3092883
Email: joshanjohn2003@mail.com
Project : https://github.com/joshanjohn/jcloud-pass.git
"""

from abc import ABC, abstractmethod
from typing import Iterator, List, Dict, Any


class StorageProvider(ABC):
    """
    Interface for Blob Data Storage management 
    """

    @abstractmethod
    def upload_blob(self, blob_name: str, file_data: bytes) -> bool:
        """
        Method to upload blob for given 
        - blob name
        - file data 
        """
        pass


    @abstractmethod
    def delete_blob(self, blob_name: str) -> bool:
        """
        Method to delete blob for a given: 
        - blob name 
        """
        pass

    @abstractmethod
    def get_blobs_in_dir(self, dir_path: str) -> list:
        """
        Method to return all the blobs for given: 
        - dir_path
        """
        pass


    @abstractmethod
    def download_blob(self, blob_name: str) -> Iterator[bytes]: 
        """
        Method to return bytes of blob for given: 
        - blob_name
        """
        pass
    
    @abstractmethod
    def duplicated_blob(self) ->  List[Dict[str, Any]]: 
        """
        Method to return the duplicated blobs
        """
        pass
    