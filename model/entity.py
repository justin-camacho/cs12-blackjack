# pyright: strict

from abc import ABC, abstractmethod
from collections.abc import MutableSequence

from model.kit import Card, Value

class Entity(ABC):
    """Abstact Base Class for game actors.
    
    Args:
        _name (_str_): _Name of the Entity._
        _cards (_MutableSequence[_Card_]_): _Current cards the Entity has. May be empty._
        _stood (_bool_): _Standing status of the Entity._ 
    """
    def __init__(self, n: str = ""):
        self._name: str = n
        self._cards: MutableSequence[Card] = []
        self._stood: bool = False
    
    def calculate(self) -> int:
        running: int = 0
        
        for card in self._cards:
            running += card.intValue if not card.flipped else 0
        
        if running > 21:
            for card in self._cards:
                running -= 10 if card.value is Value.ACE and running > 21 else 0
        
        return running
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def cards(self) -> MutableSequence[Card]:
        return self._cards
    
    @property
    def stood(self) -> bool:
        return self._stood
    
    def stand(self) -> None:
        self._stood = True
    
    @abstractmethod
    def stand_condition(self) -> bool:
        pass
        
    @abstractmethod
    def hit(self, deck: MutableSequence[Card]) -> None:
        pass
        
    @abstractmethod
    def reset(self) -> None:
        pass
            
class Player(Entity):
    """Regular game actor.
    
    Args:
        _name (_str_): _Name of the Player._
        _cards (_MutableSequence[_Card_]_): _Current cards the Player has. May be empty._
        _stood (_bool_): _Standing status of the Player._ 
        
        _chips (_int_): _Name of the Player._
        _bet (_int_): _Bet amount of the Player. Must be a positive integer._
        _insurance_bet (_int_): _Insurance bet amount of the Player. Must be a positive integer._
        _elim (_bool_): _Elimination status of the Player. When True, Player is out of the game._
    """
    
    def __init__(self, n: str, c: int):
        super().__init__(n.capitalize())
        
        self._chips: int = c
        self._bet: int = 0
        self._insurance_bet: int = 0
        self._elim: bool = False
        
    @property
    def chips(self) -> int:
        return self._chips
    
    @chips.setter
    def chips(self, c: int) -> None:
        self._chips = c
        
        if self._chips <= 0:
            self._elim = True
            
    @property
    def bet(self) -> int:
        return self._bet
    
    @bet.setter
    def bet(self, b : int) -> None:
        if b < 0:
            raise ValueError(f'The bet amount ({b}) must be a positive integer.')
        else:
            self._bet = b
            
    @property
    def insurance_bet(self) -> int:
        return self._insurance_bet
    
    @insurance_bet.setter
    def insurance_bet(self, i : int) -> None:
        if i < 0:
            raise ValueError(f'The bet amount ({i}) must be a positive integer.')
        else:
            self._insurance_bet = i
            
    @property
    def elim(self) -> bool:
        return self._elim
            
    def stand_condition(self) -> bool:
        return self.calculate() >= 21
        
    def hit(self, deck: MutableSequence[Card]) -> None:
        self._cards.append(deck.pop())
        if self.stand_condition():
            self.stand()
    
    def double(self, deck: MutableSequence[Card]) -> None:
        if self._bet * 2 <= self._chips:
            self._bet *= 2
            self._cards.append(deck.pop())
            self.stand()            
        else:
            pass
        
    def blackjack(self) -> None:
        self._chips += int((self._bet * 1.5) // 1)
    
    def reset(self) -> None:
        self._cards = []
        self._stood = False
        self._bet = 0
        self._insurance_bet = 0

class Dealer(Entity):
    """Special game actor. Can never be eliminated.
    
    Args:
        _name (_str_): _Name of the Dealer._
        _cards (_MutableSequence[_Card_]_): _Current cards the Dealer has. May be empty._
        _stood (_bool_): _Standing status of the Dealer._ 
        
        _ace (_bool_): _True if the Dealer's first card is an Ace._
        _face (_bool_): _True if the Dealer's first card is a Face or Ten._
    """
    
    def __init__(self):
        super().__init__("Dealer")
        
        self._ace: bool = False
        self._face: bool = False
    
    @property
    def ace(self) -> bool:
        return self._ace
    
    @property
    def face(self) -> bool:
        return self._face
    
    @property
    def twenty_one(self) -> bool:
        """Return True if the Dealer's first two cards add to exactly 21."""
        return self._cards[0].intValue \
             + self._cards[1].intValue == 21
    
    def analyze_start(self) -> None:
        card: Card = self._cards[0]
        
        if card.value in (Value.TEN, Value.JACK, Value.QUEEN, Value.KING):
            self._face = True
        elif card.value is Value.ACE:
            self._ace = True
        
    def stand_condition(self) -> bool:
        return self.calculate() > 17
        
    def hit(self, deck: MutableSequence[Card]) -> None:
        self._cards.append(deck.pop())
        if self.stand_condition():
            self.stand()
            
    def hit_face_down(self, deck: MutableSequence[Card]) -> None:
        card: Card = deck.pop()
        card.flip()
        self._cards.append(card)
        
    def reveal_face_down(self) -> None:
        for card in self._cards:
            if card.flipped:
                card.unflip()
        if self.stand_condition():
            self.stand()
            
    def reset(self) -> None:
        self._cards = []
        self._stood = False
        self._ace = False
        self._face = False
            
    
            
    
        
        
    
        
    
    