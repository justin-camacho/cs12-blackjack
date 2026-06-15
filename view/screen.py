# pyright: strict

from abc import ABC, abstractmethod
from dataclasses import dataclass

from view.kit import Color

import pyxel  # type: ignore

@dataclass(frozen=True)
class Screen(ABC):
    x: int = 0
    y: int = 0
    w: int = 800
    h: int = 400
    
    def draw_screen(self) -> None:
        pyxel.rectb(self.x, self.y, self.w, self.h, Color.WHITE)  # type: ignore
    
    @abstractmethod
    def update(self) -> None:
        pass
    
    @abstractmethod
    def draw(self) -> None:
        pass