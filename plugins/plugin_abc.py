from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class Plugin(ABC):
    def __init__(self, keys):
        self.__keys = keys

    @property
    def keys(self):
        return self.__keys

    @abstractmethod
    def update(self, data_src: str, input_src: str, timestamp: datetime, data: dict[str, Any]):
        ...

    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def main_menu_bar(self):
        ...
