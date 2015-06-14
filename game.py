from ship import Ship
from config import getDefaultShips

class PlayerException(Exception):
    pass

class Game(object):
    def __init__(self, player1, player2):
        (self.player1,
         self.player2) = self.players = (player1, player2)

    def newGame(self):
        # Step 1
        # Place ships for both players
        self._placeShips()
        raise NotImplemented

    def _placeShips(self):
        for player in self.players:
            for i in xrange(100):
                player.setShips(getDefaultShips())
                player.placeShips()

                if player.allShipsPlaced():
                    break
            else:
                raise PlayerException("%s failed to place ships after 100 tries" % player.name)

    def _takeTurn(self):
        raise NotImplemented
