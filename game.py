from ship import Ship

class Game(object):
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def newGame(self):
        # Step 1
        # Place ships for both players
        self._placeShips()
        raise NotImplemented

    def _placeShips(self):
        raise NotImplemented

    def _takeTurn(self):
        raise NotImplemented
