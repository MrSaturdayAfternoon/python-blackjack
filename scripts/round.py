from deck import Deck, Card
from agents import Player, Dealer
import os


class Betting:
    pass


class PayOut:
    pass


class Round:
    
    # STATES = ['INITIALIZE', 'SHUFFLE', 'INITIAL DEAL', 'CHECK FOR BLACKJACK', 'OFFER INSURANCE', 'PLAYER ACTIONS', 'DEALER ACTIONS', 'DISPLAY', 'CHECK FOR WINS', 'PAYOUT', 'RESET', 'QUIT']

    def __init__(self, player_list, min_bet, deck=Deck(), dealer=Dealer(), ):
        self.player_list = player_list
        self.deck = deck
        self.dealer = dealer
        self.min_bet = min_bet
        self.state = "INITIALIZE"
        self.display_table()


    def initialize(self):
        self.betting()
        self.shuffle()
        self.initial_deal()
        self.display_table()
        self.post_deal_checks()
        self.display_table()
        self.state = 'PLAYER ACTIONS'

    def betting(self):
        for player in self.player_list:
            self.clear_screen()
            self.display_betting(player)

    def shuffle(self):
        self.deck.shuffle()


    def initial_deal(self):
        deal_order = [*self.player_list, self.dealer]

        for entity in deal_order:
            if type(entity) is Player:
                entity.hand.append(self.dealer.deal(self.deck))
                entity.hand.append(self.dealer.deal(self.deck))
            elif type(entity) is Dealer:
                entity.hand.append(Card("A", "Clubs"))
                entity.hand.append(Card("10", "Clubs"))
                #entity.hand.append(Card("5", "Clubs"))

        # for entity in deal_order:
        #     entity.hand.append(self.dealer.deal(self.deck))
        # for entity in deal_order:
        #     if type(entity) is Player:
        #         entity.hand.append(self.dealer.deal(self.deck))
        #     elif type(entity) is Dealer:
        #         entity.hand.append(self.dealer.deal(self.deck, face_down=True))
        for entity in deal_order:
            entity.update_totals()
            entity.choose_best_total()


    def post_deal_checks(self):
        for player in self.player_list:
            player.check_for_blackjack()
        self.dealer_checks()
                

    def dealer_checks(self):
        if self.dealer.hand[0].rank == "A":
            self.offer_insurance()
            if self.dealer.total == 21:
                self.state = 'CHECK WINS'
            else:
                self.take_insurance_bets()
        if self.dealer.soft_total == 21:
            self.dealer.blackjack = True
            self.state = 'CHECK WINS'


    def take_insurance_bets(self):
        for player in self.player_list:
            if player.insurance_bet:
                player.insurance_bet = 0


    def offer_insurance(self):
        ## Insurance pays 2:1
        ## So an insurance bet of $100 pays $200 is dealer has blackjack
        for player in self.player_list:
            entered = False
            print(f"{player.name}, would you like to take insurance? \n1. Yes \n2. No")
            while not entered:
                player_input = input(">>")
                if player_input in "yY1":
                    player.make_bet(0.5*player.current_bet, 'insurance')
                    entered = True
                elif player_input in "nN2":
                    entered = True
                else:
                    print("That's not an option! Please choose again!")
                    print('')


    def player_actions(self):
        for player in self.player_list:
            player.choose_best_total()
            while not player.busted and not player.standing and not player.blackjack:
                player.get_choice(player.name, self.dealer, self.deck)
                self.display_table()
                if player.total == 21:
                    print('21!')
                    print("")
                    player.blackjack = True
                elif player.total > 21:
                    print("BUSTED!")
                    print("")
                    player.busted = True
        self.state = 'DEALER ACTIONS'


    def dealer_actions(self):
        self.dealer.choose_best_total()
        while not self.dealer.busted and (self.dealer.total < 17):
                self.dealer.hand.append(self.dealer.deal(self.deck))
                self.dealer.update_totals()
                self.dealer.choose_best_total()
                self.display_table()
                if self.dealer.total > 21:
                    print("Dealer Busts!")
                    print('')
                    self.dealer.busted = True
                elif self.dealer.total == 21:
                    print("Dealer Wins!")
                    print('')
                elif self.dealer.total > 17 and self.dealer.total <=21:
                    print("Dealer Stands")
                    print('')
        self.state = 'CHECK FOR WINS'


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
        self.state = 'PAYOUT'


    def display_table(self):
        self.clear_screen()

        print("Dealer's Hand:")
        self.dealer.display_hand()
        print('\n')

        for player in self.player_list:
            print(f"{player.name}'s Hand:")
            player.display_hand()
            print(f"{player.name}'s Bet: {player.current_bet}")
            print(f"{player.name}'s Insurance Bet: {player.insurance_bet}")
            print(f"{player.name}'s Bank: {player.bank}")
            print('')
        
    
    def display_game_over(self):
        self.display_table

        print("Winners:")
        for winner in self.winner_list:
            print(f"{winner.name}", end=" ")
        print('\n')

        print('Losers:')
        for loser in self.loser_list:
            print(f"{loser.name}", end=" ")
        print('\n')
        
        print('Pushes:')
        for push in self.push_list:
            print(f"{push.name}", end=" ")
        print('\n')
        
        for player in self.player_list:
            print(f"{player.name} Bank: {player.bank}")


    def display_betting(self, player):
        entered = False
        while not entered:
            user_in = input(f"{player.name}, please enter your bet. (Min {self.min_bet}): ")
            user_input_bet = float(user_in)
            if (user_input_bet >= self.min_bet):
                player.make_bet(user_input_bet)
                entered = True
            else:
                print(f"Please enter a bet that is at least {self.min_bet}")


    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Black Jack!  v0.1  by Trevor')
        print ('-----------------------------')
        print('')


    def payout(self):
        for player in self.player_list:
            if player.insurance_bet:
                player.winnings += player.insurance_bet
                if player in self.winner_list:
                    if player.blackjack:
                        player.winnings += 1.5 * player.current_bet
                    else:
                        player.winnings += player.current_bet
                    player.bank += player.winnings + player.current_bet + player.insurance_bet
                elif player in self.push_list:
                    player.bank += player.winnings + player.current_bet + player.insurance_bet
                elif player in self.loser_list:
                    player.bank += player.winnings + player.insurance_bet
            else:
                if player in self.winner_list:
                    if player.blackjack:
                        player.winnings += 1.5 * player.current_bet
                    else:
                        player.winnings += player.current_bet
                    player.bank += player.winnings + player.current_bet
                elif player in self.push_list:
                    player.bank += player.winnings + player.current_bet
                elif player in self.loser_list:
                    player.bank += player.winnings


            player.current_bet = 0
            player.winnings = 0
            player.insurance_bet = 0 


        
        
        self.display_game_over()
        input('Press enter to play again. >>')
        self.state = 'RESET'


    def reset(self):
        for player in self.player_list:
            player.reset()
            player.bet = self.min_bet
        self.dealer.reset()
        self.deck.reset()
        self.clear_screen()
        self.state = 'INITIALIZE'


    def quit(self):
        pass









    


    

                


            