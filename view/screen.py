# pyright: strict

from abc import ABC, abstractmethod
from typing import Any

class Screen(ABC):
    @abstractmethod
    def __init__(self):
        pass
    
    @abstractmethod
    def draw(self, **kwargs: dict[str, Any]):
        pass
    
    @abstractmethod
    def update(self, **kwargs: dict[str, Any]):
        pass