# pyright: strict

from dataclasses import dataclass
from enum import auto, Flag, IntEnum

class Interface(Flag):
    CONFS = auto()
    CREDS = auto()
    GAMES = auto()
    MENUS = auto()
    START = auto()

class Color(IntEnum):
    BLACK = 0
    NAVY = 1
    PURPLE = 2
    TURQUOISE = 3
    BROWN = 4
    DARK_BLUE = 5
    LIGHT_BLUE = 6
    WHITE = 7
    PINK = 8
    ORANGE = 9
    YELLOW = 10
    MINT = 11
    BABY_BLUE = 12
    GRAY = 13
    PEACH = 14
    BEIGE = 15
    
@dataclass(frozen=True)
class Sprite:
    bank: int
    u: int
    v: int
    w: int
    h: int
    bgcolor: Color