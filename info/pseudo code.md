# Game
Manage the game state
- Create a list/dict of players []
- Create a dealer []
- Create a deck []
- Intialize a round []
    * Pass a list of layers to the Round object
- Tell the round to play
    * Round.play()
- Check to see when the round is over []
- If round is over, create a new round []



# Round
Manage the round
- Receive a list of players [x]
- Shuffle the deck [x]
- Do an initial deal to all the players & dealer [x]
   * If dealer is showing a ten check for blackjack
   * If dealer is showing an ace, asks for insurance
- For each player in the list of players, ask them to hit/stand until they stand, bust, or hit 21 [x]
- The dealer will continue to hit until they reach (hard) 17 [x]
- Signal the Game class to switch to check wins []
- Signal to the Game class to payout the winners []
- Signal to the Game class that the round needs to be reset []


self.deal_list[*self.player_list, self.dealer]


