import random

SUITS = ['Clubs','Diamonds','Hearts','Spadas']
RANKS = ['2','3','4','5','6','7','8','9','Jack','Queen','King','Ace']

rank = random.randrange(0,len(RANKS))
suit = random.randrange(0,len(SUITS))


deck = []

for rank in RANKS:
    for suit in SUITS:
        card = rank + ' of ' + suit
        deck += [card]
print(deck)