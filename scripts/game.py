from round import Round
from agents import Player, Dealer
from deck import Deck



player = Player(name="Trevor")
deck = Deck()
dealer = Dealer()
r = Round([player], deck, dealer)

r.play()
r.check_wins()
r.pay_out()
