import random

class Card:
    
    def __init__(self, rank, suit, face_down = False):
        self.rank = rank
        self.suit = suit
        self.face_down = face_down

    def display(self):
        print(f'*{self.rank} {self.suit}*' if self.face_down else f'{self.rank} {self.suit}')


class Deck:
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['Spades', 'Hearts', 'Clubs', "Diamonds"]

    def __init__(self):
        self.reset()

    def display(self):
        for card in self.cards:
            card.display()

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self):
        return self.cards.pop()

    def reset(self):
        self.cards = []
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.cards.append(Card(rank, suit))
