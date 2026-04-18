from abc import ABC, abstractmethod


class StorageProvider(ABC):
    @abstractmethod
    def upload_file(self, blob_name: str, file_data: bytes) -> bool:
        pass

    @abstractmethod
    def download_file(self, blob_name: str) -> bytes:
        pass

    @abstractmethod
    def delete_file(self, blob_name: str) -> bool:
        pass

    @abstractmethod
    def list_dirs(self, dir_path: str) -> list:
        pass


    @abstractmethod
    def delete_file(self, blob_name: str) -> bool:
        pass

    # @abstractmethod
    # def delete_dir(self, blob_name: str) -> None: 
    #     pass
