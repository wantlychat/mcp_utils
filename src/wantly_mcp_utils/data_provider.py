from abc import abstractmethod
from typing import Protocol


class DataProvider(Protocol):
    @abstractmethod
    def get_file_data(self, file_name: str) -> bytes | None:
        pass
    
    def get_file_data_from_branch(self, file_name: str, branch: str) -> bytes | None:
        """Get file data from a specific branch, defaults to main"""
        return self.get_file_data(file_name)