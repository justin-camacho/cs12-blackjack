# pyright: strict

from dataclasses import dataclass

import pyxel  # type: ignore

from view.kit import Color, Sprite

IMAGE_SPRITES: dict[str, Sprite] = \
    {
        "PAUSE": Sprite(0, 64, 176, 16, 16, Color.BLACK)
    }
 
@dataclass(frozen=True)    
class Image:
    content: str
    
    @property
    def sprite(self) -> Sprite:
        try:
            return IMAGE_SPRITES[self.content]
        except KeyError:
            raise ValueError(f'Image content {self.content} is invalid.')
    
    @property
    def width(self) -> int:
        return self.sprite.w
    
    @property
    def height(self) -> int:
        return self.sprite.h
    
    def draw(self, x: int, y: int) -> None:
        """ Write images using custom sprites. """
        sprite: Sprite = self.sprite
            
        pyxel.blt(x, y, sprite.bank, sprite.u, sprite.v, sprite.w, sprite.h, sprite.bgcolor)  # type: ignore