# pyright: strict

"""Test new features in the playground."""

from __future__ import annotations

from time import sleep

import pyxel # type: ignore

from model.kit import ButtonType

from view.component.button import Button
from view.component.image import Image
from view.component.text import Text

def func() -> None:
    print("work?")

i: Image = Image(ButtonType.PAUSE)
t: Text = Text("COOL")
b: Button = Button(20, 20, func, i)

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