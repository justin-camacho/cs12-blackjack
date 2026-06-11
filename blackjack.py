# pyright: strict

from __future__ import annotations
from collections.abc import MutableSequence, Sequence

from model.entity import Dealer, Player
from model.kit import Card
from model.model import BlackjackModel
from random import Random

import sys
import time

def wipe_last_line() -> None:
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")

class BlackjackView:
    def ask_for_decision(self, bet: int, chips: int, cards: MutableSequence[Card]) -> int:
        p: int = -1
        
        print("""CHOICES
              
[1] Hit
[2] Stand
[3] Double Down
[4] Exit
---------------""")
        while not 1 <= p <= 4:
            p = int(input('Decision: '))
            p = -1 if p == 3 and (bet * 2 > chips or len(cards) > 2) else p
            wipe_last_line()
            
        return p
    
    def ask_for_bet(self, chips: int, name: str) -> int:
        b: int = -1
        
        while not 0 < b <= chips:
            try:
                b = int(input(f"Place bet for {name} (0, {chips}]: "))
            except ValueError:
                wipe_last_line()
                b = -1
            wipe_last_line()
            
        return b
    
    def ask_for_insurance_bet(self, bet: int, name: str) -> int:
        b: int = -1
        
        while not 0 < b <= (bet // 2):
            try:
                b = int(input(f"Place insurance bet for {name} (0, {bet // 2}]: "))
            except ValueError:
                wipe_last_line()
                b = -1
            wipe_last_line()
            
        return b
    
    def display_double_down_reminder(self) -> None:
        print("""~> [ Double Down Requirements ]
1. You have not hit yet.
2. Your bet is at most half your chips.""")
        print()
    
    def display_stats(self, turn: int, chips: int) -> None:
        print(f'Turn {turn+1} <~> Chips: {chips}')
        print()
        
    def display_all_stats(self, players: MutableSequence[Player]) -> None:
        print("~> [ Chips ]")
        for player in players:
            print(f"{player.name} <~> {player.chips}")
        print()
        
        
    def display_cards(self, cards: MutableSequence[Card], name: str) -> None:
        lay: Sequence[Sequence[str]] = [str(card).splitlines() for card in cards]
        out: Sequence[str] = ['   '.join(row) for row in zip(*lay)]
        
        print(f'{name}\'s cards:')
        print(*out, sep='\n')
        
    def display_points(self, pttl: int, dttl: int) -> None:
        print(f'Player: {pttl} <~> Dealer: {dttl}')
        print()
        
    def display_all_points(self, players: MutableSequence[Player], dealer: Dealer) -> None:
        print("~> [ Point Totals ]")
        for player in players:
            print(f"{player.name} <~> {player.calculate()}")
        print(f"{dealer.name} <~> {dealer.calculate()}")
        print()
     
    def show_blackjack_message(self, bet: int) -> None:
        print(f"You got blackjack and won {int((bet * 1.5) // 1)} chips!")
        print()
        
    def show_blackjack_dealer_message(self, c1: str, c2: str) -> None:
        print(f"Dealer got a blackjack with { \
            'an' if any((
                c1.startswith('A'), 
                c1.startswith('E'), 
                c1.startswith('I'),
                c1.startswith('O'),
                c1.startswith('U')
            )) else 'a'} {c1.capitalize()} and {c2.capitalize()}!")
        print()
        
    def show_lose_message(self) -> None:
        print("All players went broke!")
           
    def show_win_message(self, turn: int, players: MutableSequence[Player]) -> None:
        print(f'You left the game after {turn} {"turn" if turn == 1 else "turns"}!')
        print()
        
        self.display_all_stats(players)
    
    def wipe_console(self) -> None:
        for _ in range(100):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
    
class BlackjackController:
    def __init__(self, model: BlackjackModel, view: BlackjackView):
        self._model: BlackjackModel = model
        self._view: BlackjackView = view
        
    def start(self) -> None:
        model: BlackjackModel = self._model
        view: BlackjackView = self._view
        
        view.wipe_console()
        while not model.is_game_over:
            for player in model.players:
                player.bet = view.ask_for_bet(player.chips, player.name)
                
            view.wipe_console()
            model.start_turn()
            
            for player in model.players:
                
                model.dealer.analyze_start()
                if model.dealer.ace:
                    view.display_all_stats(model.players)
                    
                    for player in model.players:
                        view.display_cards(player.cards, player.name)
                    
                    view.display_cards(model.dealer.cards, model.dealer.name)
                    view.display_all_points(model.players, model.dealer) 
                
                    for player in model.players:
                        player.insurance_bet = view.ask_for_insurance_bet(player.bet, player.name)
                        
                    if model.dealer.twenty_one:
                        view.wipe_console()
                        model.dealer.reveal_face_down()
                        
                        view.display_all_stats(model.players)
                    
                        for player in model.players:
                            view.display_cards(player.cards, player.name)
                        
                        view.display_cards(model.dealer.cards, model.dealer.name)
                        view.display_all_points(model.players, model.dealer) 
                        
                        view.show_blackjack_dealer_message(
                            str(model.dealer.cards[0].value.name), 
                            str(model.dealer.cards[1].value.name)
                        )
                        view.wipe_console()
                        
                        time.sleep(2)
                elif model.dealer.face:
                    if model.dealer.twenty_one:
                        view.wipe_console()
                        model.dealer.reveal_face_down()
                        
                        view.display_all_stats(model.players)
                    
                        for player in model.players:
                            view.display_cards(player.cards, player.name)
                        
                        view.display_cards(model.dealer.cards, model.dealer.name)
                        view.display_all_points(model.players, model.dealer) 
                        
                        view.show_blackjack_dealer_message(
                            str(model.dealer.cards[0].value.name), 
                            str(model.dealer.cards[1].value.name)
                        )
                        view.wipe_console()
                        
                        time.sleep(2)
                
                while not (player.stood or model.dealer.twenty_one):
                    
                    view.display_double_down_reminder()
                    view.display_stats(model.turn, player.chips)
                    view.display_cards(player.cards, player.name)
                    view.display_cards(model.dealer.cards, model.dealer.name)
                    view.display_points(player.calculate(), model.dealer.calculate())
                    
                    if player.calculate() == 21 and len(player.cards) == 2:
                        time.sleep(2)
                        view.wipe_console()
                        view.show_blackjack_message(player.bet)
                        player.blackjack()
                        break
                    
                    match view.ask_for_decision(
                        player.bet, 
                        player.chips, 
                        player.cards
                    ):
                        case 1:
                            player.hit(model.deck)
                        case 2:
                            player.stand()
                        case 3:
                            player.double(model.deck)
                        case 4:
                            view.wipe_console()
                            
                            view.show_win_message(model.turn, model.players)
                            
                            sys.exit()
                        case _:
                            raise ValueError
                    
                    view.wipe_console()
            
            model.dealer.reveal_face_down()
            while not model.dealer.stood:
                model.dealer.hit(model.deck)
                
                view.display_all_stats(model.players)
                
                for player in model.players:
                    view.display_cards(player.cards, player.name)
                
                view.display_cards(model.dealer.cards, model.dealer.name)
                view.display_all_points(model.players, model.dealer)
                
                view.wipe_console()
                
                time.sleep(1)
            time.sleep(5)
            
            model.finish_turn()
            
        view.show_lose_message()
        
if __name__ == '__main__':
    print('Welcome to Blackjack!')
    print('(Assumption: you know the rules of the game)')
    print('BLACKJACK PAYS 3:2')
    print()
    
    nums: int = -1
    seed: int = -1
    
    play: MutableSequence[Player] = []
    
    while True:
        try:
            seed = int(input("Enter seed: "))
        except ValueError:
            wipe_last_line()
            pass
        else:
            wipe_last_line()
            break
            
    while not (0 < nums <= 6):
        try:
            nums = int(input("Enter number of players (0, 6]: "))
        except ValueError:
            wipe_last_line()
            nums = -1
        wipe_last_line()
            
    for i in range(nums):
        while True:
            try:
                play.append(Player(
                    input(f"Enter Player {i+1}'s name: "), 
                    max(1, int(input(f"Enter Player {i+1}'s chips (>0): ")))
                ))
            except ValueError:
                wipe_last_line()
                wipe_last_line()
                pass
            else:
                wipe_last_line()
                wipe_last_line()
                break
        
    game: BlackjackController = BlackjackController(
        BlackjackModel(play, Dealer(), Random(seed)), 
        BlackjackView())
    game.start()