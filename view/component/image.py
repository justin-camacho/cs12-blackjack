# pyright: strict

from dataclasses import dataclass

import pyxel  # type: ignore

from model.kit import ButtonType, Color, Sprite

IMAGE_SPRITES: dict[str, Sprite] = \
    {
        "PAUSE": Sprite(0, 64, 176, 16, 16, Color.BLACK)
    }
 
@dataclass(frozen=True)    
class Image:
    content: ButtonType
    
    @property
    def sprite(self) -> Sprite:
        try:
            return IMAGE_SPRITES[self.content]
        except KeyError:
            raise ValueError(f'Image content {self.content} is invalid.')
    
    def __len__(self) -> int:
        return self.sprite.w
    
    @property
    def height(self) -> int:
        return self.sprite.h
    
    def draw(self, x: int, y: int) -> None:
        """ Write text using custom font sprites. """
        sprite: Sprite = self.sprite
            
        pyxel.blt(x, y, sprite.bank, sprite.u, sprite.v, sprite.w, sprite.h, sprite.bgcolor)  # type: ignore