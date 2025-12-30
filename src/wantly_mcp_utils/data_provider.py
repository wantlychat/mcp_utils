from abc import abstractmethod
from typing import Protocol


class DataProvider(Protocol):
    @abstractmethod
    def get_file_data(self, file_name: str) -> bytes | None:
        pass
