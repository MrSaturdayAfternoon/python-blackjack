from round import Round
from agents import Player, Dealer
from deck import Deck


class BlackJackTable:

    # STATES = ['INITIALIZE', 'OFFER INSURANCE', 'PLAYER ACTIONS', 'DEALER ACTIONS', 'DISPLAY', 'CHECK FOR WINS', 'PAYOUT', 'RESET', 'QUIT']

    def __init__(self, min_bet=1):
        self.game_over = False
        self.min_bet = min_bet
        self.players = []


    def setup(self, player_list):
        for player in player_list:
            self.players.append(player)
        self.round = Round(self.players, self.min_bet)


    def play(self):
        while not self.game_over:
            self.game_manager()
        

    def game_manager(self):
        if self.round.state == "INITIALIZE":
            self.round.initialize()
        elif self.round.state == "PLAYER ACTIONS":
            self.round.player_actions()
        elif self.round.state == "DEALER ACTIONS":
            self.round.dealer_actions()
        elif self.round.state == "CHECK FOR WINS":
            self.round.check_wins()
        elif self.round.state == "PAYOUT":
            self.round.payout()
        elif self.round.state == "RESET":
            self.round.reset()
        elif self.round.state == "QUIT":
            self.game_over = True




if __name__ == "__main__":
    table = BlackJackTable(min_bet=5)
    table.setup([Player(name="Trevor")])
    table.play()


