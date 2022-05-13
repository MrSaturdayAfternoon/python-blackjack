from deck import Deck
from agents import Player, Dealer
import os


class Round:
    
    def __init__(self, player_list, deck=Deck(), dealer=Dealer()):
        self.player_list = player_list
        self.deck = deck
        self.dealer = dealer


    def play(self):
        self.deck.shuffle()
        self.initial_deal()
        self.dealer_peek()
        self.check_player_blackjack()
        self.display()
        self.player_actions()
        self.dealer_actions()


    def initial_deal(self):
        deal_order = [*self.player_list, self.dealer]
        for entity in deal_order:
            entity.hand.append(self.dealer.deal(self.deck))
        for entity in deal_order:
            if type(entity) is Player:
                entity.hand.append(self.dealer.deal(self.deck))
            elif type(entity) is Dealer:
                entity.hand.append(self.dealer.deal(self.deck, face_down=True))
        for entity in deal_order:
            entity.update_totals()


    def dealer_peek(self):
        # If dealer up card is A or 10 checks to see if they have a natural blackjack
        # If they have natural blackjack then the game immediately switches to payout
        # If they have an ace then the dealer offers insurance
        pass


    def check_player_blackjack(self):
        pass


    def display(self):
        self.reset_screen()
        for player in self.player_list:
            print(f"{player.name} Hand:")
            player.display_hand()
            print('')
        print("Dealer Hand:")
        self.dealer.display_hand()
        print('')


    def reset_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Black Jack!  v0.1  by Trevor')
        print ('-----------------------------')
        print('')


    def player_actions(self):
        for player in self.player_list:
            player.choose_best_totals()
            while not player.busted and not player.standing and not player.blackjack:
                player.get_choice(self.dealer, self.deck)
                self.display()
                if player.total == 21:
                    print('BLACKJACK!')
                    print("")
                    player.blackjack = True
                elif player.total > 21:
                    print("BUSTED!")
                    print("")
                    player.busted = True

    
    def dealer_actions(self):
        self.dealer.choose_best_total()
        while not self.dealer.busted and (self.dealer.total < 17):
                self.dealer.hand.append(self.dealer.deal(self.deck))
                self.dealer.update_totals()
                self.dealer.choose_best_total()
                self.display()
                if self.dealer.total > 21:
                    print("Dealer Busts!")
                    print('')
                    self.dealer.busted = True
                elif self.dealer.total == 21:
                    print("Dealer Wins!")
                    print('')
                elif self.dealer.total > 17 and self.dealer <=21:
                    print("Dealer Stands")
                    print('')

    
    def check_wins(self):
        self.winner_list = []
        self.push_list = []
        self.loser_list = []
        for player in self.player_list:
            if player.busted:
                self.loser_list.append(player)
            elif not player.busted:
                if self.dealer.busted:
                    self.winner_list.append(player)
                elif not self.dealer.busted:
                    if player.total > self.dealer.total:
                        self.winner_list.append(player)
                    elif player.total < self.dealer.total:
                        self.loser_list.append(player)
                    elif player.total == self.dealer.total:
                        self.push_list.append(player)
                

    def pay_out(self):
        ## Black jack pays 3:2
        ## So a $100 bet would win $150
        if self.loser_list:
            for player in self.loser_list:
                player.bank -= player.bet
        if self.winner_list:
            for player in self.winner_list:
                if player.blackjack:
                    player.bank += player.bet * 1.5
                else:
                    player.bank += player.bet
        if self.push_list:
            pass
        for player in self.player_list:
            print(f"{player.name} Bank: {player.bank}")
            