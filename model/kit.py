# pyright: strict

from __future__ import annotations

from dataclasses import dataclass
from enum import auto, Flag, IntEnum, StrEnum

class Value(StrEnum):
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    
class IntValue(IntEnum):
    ACE = 11
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10


class Suit(StrEnum):
    CLUB = "♧"
    DIAMOND = "♢"
    HEART = "♡"
    SPADE = "♤"
    
    
class Card:
    
    def __init__(self, intValue: IntValue, value: Value, suit: Suit):
        self._intValue : IntValue = intValue
        self._value : Value = value
        self._suit : Suit = suit
        self._flipped : bool = False
        
    def __str__(self):
        return f"""
┍━━━━━┑
│    {self._value}│
│     │
│  {self._suit}  │
│     │
│{self._value}    │
┕━━━━━┙

""" if not self._flipped else """
┍━━━━━┑
│    ?│
│     │
│  ?  │
│     │
│?    │
┕━━━━━┙

"""

    @property
    def intValue(self) -> IntValue:
        return self._intValue
    
    @property
    def value(self) -> Value:
        return self._value
    
    @property
    def suit(self) -> Suit:
        return self._suit
    
    @property
    def flipped(self) -> bool:
        return self._flipped
    
    def flip(self) -> None:
        self._flipped = True
        
    def unflip(self) -> None:
        self._flipped = False

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
    
class ButtonType(StrEnum):
    PAUSE = "PAUSE"
    
@dataclass(frozen=True)
class Sprite:
    bank: int
    u: int
    v: int
    w: int
    h: int
    bgcolor: Color
    
    def __len__(self) -> int:
        return self.w