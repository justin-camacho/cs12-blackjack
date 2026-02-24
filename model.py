# pyright: strict

from __future__ import annotations
from collections.abc import MutableSequence

from kit import Card, Suit, Value
from random import Random
from typing import ClassVar

class BlackjackModel:
    DECK: ClassVar[MutableSequence[Card]] = [Card(value, suit) for value in Value for suit in Suit]
    VALS: ClassVar[dict[str, int]] = {
        'A': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, \
        'J': 10, 'Q': 10, 'K': 10
    }
    
    def __init__(self, chips: int, rng: Random):
        self._chips: int = chips
        self._rng: Random = rng
        self._bet: int = 0
        self._turn: int = 0
        self._deck_idx: int = -1
        self._player_total: int = 0
        self._dealer_total: int = 0
        self._raw_p_total: int = 0
        self._raw_d_total: int = 0
        self._player_card: MutableSequence[Card] = []
        self._dealer_card: MutableSequence[Card] = []
        self._is_player_round_over: bool = False
        self._is_dealer_round_over: bool = False
    
    @property
    def chips(self) -> int:
        return self._chips
    
    @property
    def rng(self) -> Random:
        return self._rng
    
    @property
    def bet(self) -> int:
        return self._bet
    
    @property
    def turn(self) -> int:
        return self._turn
            
    @property
    def player(self) -> MutableSequence[Card]:
        return self._player_card
    
    @property
    def dealer(self) -> MutableSequence[Card]:
        return self._dealer_card
    
    @property
    def player_total(self) -> int:
        return self._player_total
    
    @property
    def dealer_total(self) -> int:
        return self._dealer_total
    
    @property
    def is_player_round_over(self) -> bool:
        return self._is_player_round_over
    
    @property
    def is_dealer_round_over(self) -> bool:
        return self._is_dealer_round_over
        
    def set_bet(self, value: int) -> None:
        if value <= 0:
            raise ValueError(f'The bet amount ({value}) is a nonpositive integer.')
        else:
            self._bet = value
    
    def win(self) -> None:
        self._chips += self._bet

    def lose(self) -> None:
        self._chips -= self._bet

    def blackjack(self) -> None:
        self._chips += int((self._bet * 1.5) // 1)

    def draw(self) -> Card:
        self._deck_idx += 1
        return self.DECK[self._deck_idx]
          
    def hit(self) -> None:
        self._player_card.append(self.draw())
    
    def stand(self) -> None:
        self._is_player_round_over = True
        
    def dealer_hit(self) -> None:
        self._dealer_card.append(self.draw())
    
    def dealer_stand(self) -> None:
        self._is_dealer_round_over = True
        
    def double(self) -> None:
        self._bet *= 2
        self._player_card.append(self.draw())
        self._is_player_round_over = True
    
    def update_points(self) -> None:
        temp: int = -1
        
        self._raw_p_total += self.VALS[self._player_card[-1].value]
            
        if self._raw_p_total > 21:
            temp = self._raw_p_total
            for card in self._player_card:
                temp -= 10 if card.value == 'A' else 0  
            else:
                self._player_total = temp
        else:
            self._player_total = self._raw_p_total
                
        if self._player_total > 21:
           self.stand()
                
    def update_dealer_points(self) -> None:
        temp: int = -1
        
        self._raw_d_total += self.VALS[self._dealer_card[-1].value]
            
        if self._raw_d_total > 21:
            temp = self._raw_d_total
            for card in self._dealer_card:
                temp -= 10 if card.value == 'A' else 0  
            else:
                self._dealer_total = temp
        else:
            self._dealer_total = self._raw_d_total
                
        if self._dealer_total > 16:
           self.dealer_stand()
        
    def start_turn(self) -> None:
        self._rng.shuffle(self.DECK)
        
        self.hit()
        self.update_points()
        self.dealer_hit()
        self.update_dealer_points()
        self.hit()
        
    def finish_turn(self) -> None:
        
        if (self._dealer_total <= 21 and self._player_total < self._dealer_total) or self._player_total > 21:
            self.lose()
        elif (self._player_total <= 21 and self._dealer_total < self._player_total) or self._dealer_total > 21:
            self.win()
        else:
            pass
        
        self._raw_p_total = 0
        self._raw_d_total = 0
        self._player_total = 0
        self._dealer_total = 0
        self._player_card = []
        self._dealer_card = []
        self._is_player_round_over = False
        self._is_dealer_round_over = False
        self._deck_idx = -1
        self._turn += 1