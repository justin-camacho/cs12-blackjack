# cs12-blackjack
Sample Blackjack game program, with unit tests, made as practice for CS12. Made by Justin Camacho.


### Object of the Game 🏆
[(source)](https://www.compliance.lottery.nh.gov/sites/g/files/ehbemt686/files/inline-documents/agp-blackjack-v-9.pdf)

The object of the game is for a player to have a hand closer to **21** than that of the dealer without going
**over**. If players are dealt an **ace** and at the same time a **10**, **jack**, **queen** or **king**, on 
the first two cards, the player has blackjack and will win **3:2**.

### Rules of the Game 📜
[(source)](https://www.compliance.lottery.nh.gov/sites/g/files/ehbemt686/files/inline-documents/agp-blackjack-v-9.pdf)

The values of the cards are as follows, an **ace** may count as either **1** or **11**. A hand that contains an ace is
called a **soft** total if the ace can be counted as either 1 or 11 without the total going over 21. If the ace
must be counted as 1 to prevent the hand from going over 21, the hand is then called a **hard** total.
The cards from 2 to 9 are valued at their face value. The **10**, **jack**, **queen** and **king** are all valued at **10**.

The dealer must stand on all **hard 17’s**. A tie with the dealer results in a **push**. 

All players with blackjack are **guaranteed winners**.

### Program Mechanics 🛠️

The player will be prompted to enter some number of **chips** (`>0`) and a **seed**.
Play will begin from there and continue until either:

1. The player has **no chips**
2. The player **exits** the game

### Running the Game 🎮
```bash
python3 whacamole.py
```

### Running Pytest 🎬
```bash
coverage run --branch -m pytest && coverage html
```

Alternative Command:

```bash
python3 -m coverage run --branch -m pytest && python3 -m coverage html
```

### Farthest Phase 🥉
> **Phase 3**.

(There are no phases)