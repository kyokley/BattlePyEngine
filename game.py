from config import getDefaultShips

class PlayerException(Exception):
    pass

class SystemException(Exception):
    pass

class Game(object):
    def __init__(self, player1, player2):
        (self.player1,
         self.player2) = self.players = (player1, player2)

        self.winner = None
        self.loser = None

        self.turns = None

    def playGame(self):
        try:
            for player in self.players:
                player.newGame()

            # Step 1
            # Place ships for both players
            self._placeShips()

            # Step 2
            # Take turns blowing ships out of the water
            self._takeTurns()
            return self.winner, self.loser
        except PlayerException, e:
            return self._gameOver(e.args[1], exception=e)

    def _placeShips(self):
        for player in self.players:
                for i in xrange(100):
                    player._setShips(getDefaultShips())
                    try:
                        player.placeShips()
                    except Exception, e:
                        print e
                        raise PlayerException(e, player)

                    if player._allShipsPlacedLegally():
                        break
                else:
                    raise PlayerException("%s failed to place ships after %s tries" % (player.name, i + 1), player)

    def _takeTurns(self):
        count = -1
        while True:
            count += 1

            offensivePlayer = self.players[count % 2]
            defensivePlayer = self.players[(count + 1) % 2]

            try:
                shot = offensivePlayer.fireShot()
            except Exception, e:
                raise PlayerException(e, offensivePlayer)

            hit, hitShip = defensivePlayer._checkIsHit(shot)
            defensivePlayer.opponentShot(shot)

            if hit:
                try:
                    offensivePlayer.shotHit(shot, hitShip)
                except Exception, e:
                    raise PlayerException(e, offensivePlayer)


                if hitShip.isSunk():
                    try:
                        offensivePlayer.shipSunk(hitShip)
                    except Exception, e:
                        raise PlayerException(e, offensivePlayer)
                    done = defensivePlayer._checkAllShipsSunk()
                    if done:
                        # Game Over
                        self._gameOver(defensivePlayer, turns=count + 1)
                        break
            else:
                try:
                    offensivePlayer.shotMissed(shot)
                except Exception, e:
                    raise PlayerException(e, offensivePlayer)

    def _gameOver(self,
                  loser,
                  turns=0,
                  exception=None):
        self.loser = loser
        self.winner = self.player1 if loser == self.player2 else self.player2
        self.turns = turns
        self.exception = exception

        self.winner.gameWon()
        self.loser.gameLost()
        return self.winner, self.loser
