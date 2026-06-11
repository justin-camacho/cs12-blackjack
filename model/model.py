# pyright: strict

from __future__ import annotations
from collections.abc import MutableSequence, Set

from model.entity import Dealer, Player
from model.kit import Card, IntValue, Suit, Value
from random import Random

class BlackjackModel:
    def __init__(self, players: MutableSequence[Player], dealer: Dealer, rng: Random):
        
        self._shoe: Set[Card] = {Card(iv, v, suit) for (iv, v) in zip(IntValue, Value) for suit in Suit}
        self._deck: MutableSequence[Card] = self.shuffle()
    
        if players:
            self._players: MutableSequence[Player] = players
        else:
            raise ValueError(f"Player configuration ({repr(players)}) is invalid.")
        self._dealer: Dealer = dealer
        
        self._rng: Random = rng
        self._turn: int = 0
    
    @property
    def deck(self) -> MutableSequence[Card]:
        return self._deck
    
    @property
    def players(self) -> MutableSequence[Player]:
        return self._players
    
    @property
    def dealer(self) -> Dealer:
        return self._dealer
    
    @property
    def rng(self) -> Random:
        return self._rng
    
    @property
    def turn(self) -> int:
        return self._turn
    
    @property
    def is_game_over(self) -> bool:
        return not bool(self._players)
    
    def compare(self, player: Player) -> None:
        if self._dealer.twenty_one:
            player.chips += (2 * player.insurance_bet - player.bet)
        elif (self._dealer.calculate() <= 21 and player.calculate() < self._dealer.calculate()) or player.calculate() > 21:
            player.chips -= player.bet
        elif (player.calculate() <= 21 and self._dealer.calculate() < player.calculate()) or self._dealer.calculate() > 21:
            player.chips += player.bet
    
    def distribute(self) -> None:
        for player in self._players:
            player.hit(self.deck)
    
    def shuffle(self) -> MutableSequence[Card]:
        return sorted([*self._shoe], key=lambda i: (i.suit.__class__.__name__, i.intValue))
    
    def start_turn(self) -> None:
        self._rng.shuffle(self.deck)
        self.distribute()
        self._dealer.hit(self.deck)
        self.distribute()
        self._dealer.hit_face_down(self.deck)
    
    def finish_turn(self) -> None:
        for player in self._players[:]:
            self.compare(player)
            
            if player.chips <= 0:
                self._players.remove(player)
            else:
                player.reset()
            
        self._dealer.reset()
        self._deck = self.shuffle()
        self._turn += 1