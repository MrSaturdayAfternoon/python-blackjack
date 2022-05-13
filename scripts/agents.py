import random

class Entity:
    def __init__(self):
        self.hand = []
        self.hard_total = 0
        self.soft_total = 0
        self.total = 0
        self.busted = False
        self.standing = False
        self.blackjack = False

    def choose_best_total(self):
        if self.hard_total >= self.soft_total:
            self.total = self.hard_total
        else:
            self.total = self.soft_total

    def display_hand(self):
        for card in self.hand:
            card.display()
        if self.soft_total:
            print(f"Hand total: {self.hard_total} or {self.soft_total}")
        else:
            print(f"Hand total: {self.hard_total}")

    def update_totals(self):
        temp_total = 0
        aces = 0
        hard_total = 0
        soft_total = 0

        # Convert ranks to numbers
        for card in self.hand:
            if card.rank in "2345678910":
                temp_total += int(card.rank)
            elif card.rank in "JQK":
                temp_total += int(10)
            elif card.rank == "A":
                temp_total += 11
                aces += 1

        # Check if total is 21 first
        if temp_total == 21:
         self.hard_total = temp_total
         self.soft_total = 0
        else:
            # Convert all aces to 1s and set the hard total
            hard_total = temp_total
            hard_aces = aces
            while hard_aces > 0:
                hard_total -= 10
                hard_aces -= 1
            self.hard_total = hard_total

            # Convert only the necessary aces to 1s and set the soft total
            # if there are any aces left act as 11
            soft_total = temp_total
            while aces > 0 and soft_total > 21:
                soft_total -= 10
                aces -= 1
            if aces > 0 :
             self.soft_total = soft_total


class Player(Entity):
    # TODO split, double-down, betting
    DEFAULT_BANK = 100
    def __init__(self, bank=DEFAULT_BANK, name=f"player {random.randint(1,1000)}", owner=None):
        super().__init__()
        self.bank = bank
        self.bet = 5
        self.name = name
        self.owner = owner


    def play(self):
        self.player_input()


    def get_choice(self, dealer, deck):
        player_choice = input("Please choose: \n1. Hit \n2. Stand \n>>")
        if player_choice == '1':
            self.hand.append(dealer.deal(deck))
            self.update_totals()
        elif player_choice == '2':
            self.standing = True
        self.choose_best_total()
    

class Dealer(Entity):
    # TODO payout

    def __init__(self):
        super().__init__()


    def deal(self, deck, face_down=False):
        card = deck.take_card()
        if face_down:
            card.face_down = True
        return card


    def play(self):
        print("Dealer's Turn")


    def peek(self):
        pass