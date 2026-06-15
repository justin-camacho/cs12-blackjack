# pyright: strict

from view.screen import Screen

class MainMenuScreen(Screen):
    def __init__(self):
        super().__init__()
    
    def update(self):
        pass
    
    def draw(self):
        self.draw_screen()
        pass