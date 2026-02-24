# pyright: strict

from enum import StrEnum

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


class Suit(StrEnum):
    CLUB = "♧"
    DIAMOND = "♢"
    HEART = "♡"
    SPADE = "♤"
    
    
class Card:
    
    def __init__(self, value: Value, suit: Suit):
        self._value = value
        self._suit = suit
        
    def __str__(self):
        return f"""
┍━━━━━┑
│    {self._value}│
│     │
│  {self._suit}  │
│     │
│{self._value}    │
┕━━━━━┙

"""
        
    @property
    def value(self) -> Value:
        return self._value
    
    @property
    def suit(self) -> Suit:
        return self._suit
