# pyright: strict

from dataclasses import dataclass
from string import ascii_uppercase

import pyxel  # type: ignore

from model.kit import Color, Sprite

ASCII_NUMBER_SPRITES: dict[str, Sprite] = \
    {value: Sprite(0, 64 + 16 * (idx % 4), 128 + 16 * (idx // 4), 16, 16, Color.BEIGE) for idx, value in enumerate("1234567890 ")}
ASCII_UPPERCASE_SPRITES: dict[str, Sprite] = \
    {value: Sprite(0, 16 * (idx % 4), 128 + 16 * (idx // 4), 16, 16, Color.BEIGE) for idx, value in enumerate(ascii_uppercase)}
 
@dataclass(frozen=True)    
class Text:
    content: str
    
    def __len__(self) -> int:
        return len(self.content) * 16
    
    @property
    def height(self) -> int:
        return 16
    
    def draw(self, x: int, y: int) -> None:
        """ Write text using custom font sprites. """
        for idx, char in enumerate(self.content):
            try:
                sprite: Sprite = \
                    ASCII_NUMBER_SPRITES[char] if char not in ascii_uppercase else \
                    ASCII_UPPERCASE_SPRITES[char]
            except KeyError:
                raise ValueError(f'Text content {self.content} is invalid.')
            
            pyxel.blt(x + 16 * idx, y, sprite.bank, sprite.u, sprite.v, sprite.w, sprite.h, sprite.bgcolor)  # type: ignore