# pyright: strict

from enum import IntEnum, StrEnum

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
