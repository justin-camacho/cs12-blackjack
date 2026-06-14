# pyright: strict

"""Create a Button with a text or image that executes a function when pressed."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pyxel # type: ignore

from model.kit import Color
from view.component.image import Image
from view.component.text import Text

@dataclass(frozen=True)
class Button:
    x: int
    y: int
    func: Callable[[], None]
    content: Text | Image
    border: Color | None = None
    
    def update(self) -> None:
        x, y = self.x, self.y
        w, h = len(self.content), self.content.height
        
        pressed: bool = pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) # type: ignore
        within_x: bool = x <= pyxel.mouse_x <= x + w # type: ignore
        within_y: bool = y <= pyxel.mouse_y <= y + h # type: ignore
        
        if pressed and within_x and within_y:
            self.func()
        
    def draw(self) -> None:
        x, y = self.x, self.y
        w, h = len(self.content), self.content.height
        
        self.content.draw(x, y)
        
        if self.border is not None:
            pyxel.rectb(x, y, w, h, self.border) # type: ignore