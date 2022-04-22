import random
import os

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
        self.cards = []
        for suit in self.SUITS:
            for rank in self.RANKS:
                self.cards.append(Card(rank, suit))

    def display(self):
        for card in self.cards:
            card.display()

    def shuffle(self):
        random.shuffle(self.cards)

    def take_card(self):
        return self.cards.pop()


class Player:
    # TODO split, double-down, betting
    
    def __init__(self):
        self.hand = []
        self.hard_total = 0
        self.soft_total = 0
        self.total = 0
        self.busted = False
        self.standing = False

    def choose_best_total(self):
        if self.hard_total >= self.soft_total:
            self.total = self.hard_total
        else:
            self.total = self.soft_total

    def show_hand(self):
        print('Player hand: ')
        for card in self.hand:
            card.display()
        if self.soft_total:
            print(f"Hand total: {self.hard_total} or {self.soft_total}")
        else:
            print(f"Hand total: {self.hard_total}")


class Dealer:
    # TODO payout
    def __init__(self):
        self.hand = []
        self.hard_total = 0
        self.soft_total = 0
        self.total = 0
        self.busted = False
        self.standing = False

    def choose_best_total(self):
        if self.hard_total >= self.soft_total:
            self.total = self.hard_total
        else:
            self.total = self.soft_total

    def deal(self, deck, face_down=False):
        card = deck.take_card()
        if face_down:
            card.face_down = True
        return card

    def show_hand(self):
        print('Dealer hand: ')
        for card in self.hand:
            card.display()
        if self.soft_total:
            print(f"Hand total: {self.hard_total} or {self.soft_total}")
        else:
            print(f"Hand total: {self.hard_total}")


class Game:
    # TODO implement betting
    def __init__(self):
        self.game_over = False
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.deck.shuffle()

    def play(self):
        self.reset_screen()
        self.initial_deal()
        self.update_totals(self.player)
        self.update_totals(self.dealer)
        self.display()
        print('')
        self.game_over = False
        while not self.game_over:
            self.player_events()
            self.dealer_events()
            self.check_win()

    def initial_deal(self):
        self.player.hand.append(self.dealer.deal(self.deck))
        self.dealer.hand.append(self.dealer.deal(self.deck))
        self.player.hand.append(self.dealer.deal(self.deck))
        self.dealer.hand.append(self.dealer.deal(self.deck, face_down=True))

    def check_win(self):
        # TODO redo the logic here
        if not self.player.busted and not self.dealer.busted:
            if self.player.total > self.dealer.total:
                print(f"You win! \nYour total: {self.player.total} \nDealer total {self.dealer.total}")
                self.game_over = True
            elif self.player.total < self.dealer.total:
                print(f"You lose! \nYour total: {self.player.total} \nDealer total {self.dealer.total}")
                self.game_over = True
            else:
                print(f"Push \nYour total: {self.player.total} \nDealer total {self.dealer.total}")
                self.game_over = True
        if self.player.busted:
            print("You bust!")
            self.game_over = True
        if self.dealer.busted:
            print("Dealer busts!")
            self.game_over = True

    def player_events(self):
        while not self.player.busted and not self.player.standing:
            self.player_input()
            self.reset_screen()
            self.display()
            print('')
            if self.player.total == 21:
                print('BLACKJACK!')
                self.game_over = True
                break
            elif self.player.total > 21:
                self.player.busted = True

    def player_input(self):
        player_choice = input("Please choose: \n1. Hit \n2. Stand \n")
        if player_choice == '1':
            self.player.hand.append(self.dealer.deal(self.deck))
            self.update_totals(self.player)
        elif player_choice == '2':
            self.player.standing = True
        self.player.choose_best_total()

    def dealer_events(self):
        self.dealer.choose_best_total()
        while not self.dealer.busted and (self.dealer.total < 17):
            self.dealer.hand.append(self.dealer.deal(self.deck))
            self.update_totals(self.dealer)
            self.dealer.choose_best_total()
            self.reset_screen()
            self.display()
            print('')
            if self.dealer.total > 21:
                self.dealer.busted = True
        
    def update_totals(self, actor):
        temp_total = 0
        aces = 0
        hard_total = 0
        soft_total = 0

        # Convert ranks to numbers
        for card in actor.hand:
            if card.rank in "2345678910":
                temp_total += int(card.rank)
            elif card.rank in "JQK":
                temp_total += int(10)
            elif card.rank == "A":
                temp_total += 11
                aces += 1

        # Check if total is 21 first
        if temp_total == 21:
            actor.hard_total = temp_total
            actor.soft_total = 0
        else:
            # Convert all aces to 1s and set the hard total
            hard_total = temp_total
            hard_aces = aces
            while hard_aces > 0:
                hard_total -= 10
                hard_aces -= 1
            actor.hard_total = hard_total

            # Convert only the necessary aces to 1s and set the soft total
            # if there are any aces left act as 11
            soft_total = temp_total
            while aces > 0 and soft_total > 21:
                soft_total -= 10
                aces -= 1
            if aces > 0 :
                actor.soft_total = soft_total

    def reset_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Black Jack!  v0.1  by Trevor')
        print ('-----------------------------')
        print('')
   
    def display(self):
        self.player.show_hand()
        print('')
        self.dealer.show_hand()

if __name__ == '__main__':
    game = Game()
    game.play()