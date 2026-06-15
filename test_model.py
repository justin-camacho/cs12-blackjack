# pyright: strict

"""Test new features in the playground."""

from __future__ import annotations

from time import sleep

import pyxel # type: ignore

from view.component.button import Button
from view.component.image import Image
from view.component.text import Text

i: Image = Image("PAUSE")
t: Text = Text("COOL")
b: Button = Button(20, 20, lambda: print("work?"), i)

def update():
    b.update()

def draw():
    b.draw()
    
if __name__ == "__main__":
    pyxel.init(800, 400) # type: ignore
    pyxel.load("view/resources.pyxres") # type: ignore
    pyxel.run(update, draw) # type: ignore
    
    sleep(5)
    
    pyxel.quit() # type: ignore