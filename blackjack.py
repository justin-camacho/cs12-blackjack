# pyright: strict

from __future__ import annotations
from collections.abc import MutableSequence, Sequence

from kit import Card
from model import BlackjackModel
from random import Random

import sys
import time

class BlackjackView:
    def ask_for_decision(self, bet: int, chips: int, cards: MutableSequence[Card]) -> int:
        p: int = -1
        
        print('''CHOICES
              
[1] Hit
[2] Stand
[3] Double Down
[4] Exit
---------------''')
        while not 1 <= p <= 4:
            p = int(input('Decision: '))
            p = -1 if p == 3 and (bet * 2 > chips or len(cards) > 2) else p
            
        return p
    
    def ask_for_bet(self, chips: int) -> int:
        b: int = -1
        
        while not 0 < b <= chips:
            b = int(input(f"Place bet (0, {chips}]: "))
            
        return b
    
    def display_double_down_reminder(self) -> None:
        print("""~> [ Double Down Requirements ]
1. You have not hit yet.
2. Your bet is at most half your chips.""")
        print()
    
    def display_stats(self, turn: int, chips: int) -> None:
        print(f'Turn {turn+1} <~> Chips: {chips}')
        print()
        
    def display_cards(self, cards: MutableSequence[Card], name: str) -> None:
        lay: Sequence[Sequence[str]] = [str(card).splitlines() for card in cards]
        out: Sequence[str] = ['   '.join(row) for row in zip(*lay)]
        
        print(f'{name}\'s cards:')
        print(*out, sep='\n')
        
    def display_points(self, pttl: int, dttl: int) -> None:
        print(f'Player: {pttl} <~> Dealer: {dttl}')
        print()
        
    def show_win_message(self, turn: int, chips: int) -> None:
        print(f'You left the game after {turn} {"turn" if turn == 1 else "turns"} with {chips} {"chip" if chips == 1 else "chips"}!')
        
    def show_lose_message(self) -> None:
        print("You went broke.")
    
    def wipe_console(self) -> None:
        for _ in range(50):
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
        while model.chips > 0:
            model.set_bet(view.ask_for_bet(model.chips))
            view.wipe_console()
            model.start_turn()
            
            if model.player_total == 11 and model.player[-1].value in ('T', 'Q', 'J', 'K') \
            or model.player_total == 10 and model.player[-1].value == 'A':
                model.update_points()
                
                view.display_double_down_reminder()
                view.display_stats(model.turn, model.chips)
                view.display_cards(model.player, "Player")
                view.display_cards(model.dealer, "Dealer")
                view.display_points(model.player_total, model.dealer_total)
                
                time.sleep(4)
                model.blackjack()
                view.wipe_console()
                continue
            
            while not model.is_player_round_over:
                model.update_points()
                
                view.display_double_down_reminder()
                view.display_stats(model.turn, model.chips)
                view.display_cards(model.player, "Player")
                view.display_cards(model.dealer, "Dealer")
                view.display_points(model.player_total, model.dealer_total)
                
                match view.ask_for_decision(model.bet, model.chips, model.player):
                    case 1:
                        model.hit()
                    case 2:
                        model.stand()
                    case 3:
                        model.double()
                    case 4:
                        view.wipe_console()
                        view.wipe_console()
                        
                        view.show_win_message(model.turn, model.chips)
                        
                        sys.exit()
                    case _:
                        raise ValueError
                    
                view.wipe_console()
                    
            while not model.is_dealer_round_over:
                
                model.dealer_hit()
                model.update_dealer_points()
                
                view.display_stats(model.turn, model.chips)
                view.display_cards(model.player, "Player")
                view.display_cards(model.dealer, "Dealer")
                view.display_points(model.player_total, model.dealer_total)
                
                view.wipe_console()
                
                time.sleep(1)
            time.sleep(1)
                
            model.finish_turn()
            
        view.show_lose_message()
        
if __name__ == '__main__':
    print('Welcome to Blackjack!')
    print('(Assumption: you know the rules of the game)')
    print('BLACKJACK PAYS 3:2')
    print()
    
    chip: int = -1
    seed: int = -1
    
    while True:
        try:
            seed = int(input("Enter seed: "))
        except ValueError:
            pass
        else:
            break
            
    while chip <= 0:
        try:
            chip = int(input("Enter chips (>0): "))
        except ValueError:
            chip = -1
    
    game: BlackjackController = BlackjackController(BlackjackModel(chip, Random(seed)), BlackjackView())
    game.start()