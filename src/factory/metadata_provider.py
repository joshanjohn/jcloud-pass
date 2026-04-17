from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from src.entities import File

class MetadataProvider(ABC):
    @abstractmethod
    def get_user_record(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_user(self, user_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def add_directory(self, user_id: str, dir_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def get_all_directories(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def create_file_record(self, user_id: str, file: File) -> None: 
        pass


