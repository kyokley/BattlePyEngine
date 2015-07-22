from battlePy.default_config import (DEFAULT_SHIPS,
                                     BOARD_WIDTH,
                                     BOARD_HEIGHT,
                                     TIMEOUT_LENGTH,
                                     )
from battlePy.ship import Ship
from battlePy.utils import docprop
from time import sleep
import traceback as tb

class PlayerException(Exception):
    pass

class SystemException(Exception):
    pass

class Game(object):
    player1 = docprop('player1', 'First player')
    player2 = docprop('player2', 'Second player')
    winner = docprop('winner', 'Winner of the game')
    loser = docprop('loser', 'Loser of the game')
    turns = docprop('turns', 'Total number of turns taken by both players')
    debug = docprop('debug', 'Is debugging mode?')
    shipSpecs = docprop('shipSpecs', 'List of tuples containing pairs of ship names and sizes')
    boardWidth = docprop('boardWidth', 'Game board width')
    boardHeight = docprop('boardHeight', 'Game board height')

    def __init__(self,
                 player1,
                 player2,
                 debug=False,
                 shipSpecs=None,
                 boardWidth=None,
                 boardHeight=None,
                 timeoutLength=None,
                 showVisualization=False,
                 visualizationInterval=.01):
        (self.player1,
         self.player2) = self.players = (player1, player2)

        self.winner = None
        self.loser = None

        self.turns = None
        self.debug = debug
        self.shipSpecs = shipSpecs or DEFAULT_SHIPS

        self.boardWidth = boardWidth or BOARD_WIDTH
        self.boardHeight = boardHeight or BOARD_HEIGHT

        self.timeoutLength = timeoutLength or TIMEOUT_LENGTH

        self.showVisualization = showVisualization
        self.visualizationInterval = visualizationInterval

        self.exception = None
        self.traceback = None

        self.playerShots = {self.player1: set(),
                            self.player2: set()}

    def createShips(self):
        ''' Generate a list of ship objects based on the given ship specifications '''
        return [Ship(*x, game=self) for x in self.shipSpecs]

    def playGame(self):
        ''' Start the game '''
        try:
            for player in self.players:
                player.currentGame = self
                player._setShips(self.createShips())

                try:
                    player._newGame()
                except Exception, e:
                    self.traceback = tb.format_exc()
                    raise PlayerException(e, player)

            # Step 1
            # Place ships for both players
            self._placeShips()

            if self.showVisualization:
                for player in self.players:
                    player._initializeGameBoard()
                    player._displayShips()

            # Step 2
            # Take turns blowing ships out of the water
            self._takeTurns()
            return self.winner, self.loser
        except PlayerException, e:
            return self._gameOver(e.args[1], exception=e)

    def _placeShips(self):
        for player in self.players:
                for i in xrange(100):
                    try:
                        player._placeShips()
                    except Exception, e:
                        self.traceback = tb.format_exc()
                        raise PlayerException(e, player)

                    if player._allShipsPlacedLegally():
                        break
                else:
                    raise PlayerException("%s failed to place ships after %s tries" % (player.name, i + 1), player)

    def _takeTurns(self):
        count = -1
        while True:
            if self.showVisualization:
                sleep(self.visualizationInterval)
            count += 1

            offensivePlayer = self.players[count % 2]
            defensivePlayer = self.players[(count + 1) % 2]

            try:
                shot = offensivePlayer._fireShot()
                self.playerShots[offensivePlayer].add(shot)
            except Exception, e:
                self.traceback = tb.format_exc()
                raise PlayerException(e, offensivePlayer)

            hit, hitShip = defensivePlayer._checkIsHit(shot)

            try:
                defensivePlayer._opponentShot(shot)
            except Exception, e:
                self.traceback = tb.format_exc()
                raise PlayerException(e, defensivePlayer)

            if hit:
                try:
                    offensivePlayer._shotHit(shot, hitShip.name)
                except Exception, e:
                    self.traceback = tb.format_exc()
                    raise PlayerException(e, offensivePlayer)


                if hitShip.isSunk():
                    try:
                        offensivePlayer._shipSunk(hitShip.name)
                    except Exception, e:
                        self.traceback = tb.format_exc()
                        raise PlayerException(e, offensivePlayer)
                    done = defensivePlayer._checkAllShipsSunk()
                    if done:
                        # Game Over
                        self._gameOver(defensivePlayer, turns=count + 1)
                        break
            else:
                try:
                    offensivePlayer._shotMissed(shot)
                except Exception, e:
                    self.traceback = tb.format_exc()
                    raise PlayerException(e, offensivePlayer)

    def _gameOver(self,
                  loser,
                  turns=0,
                  exception=None):
        self.loser = loser
        self.winner = self.player1 if loser == self.player2 else self.player2
        self.turns = turns
        self.exception = exception

        if not self.exception:
            self.winner._numberOfWins += 1
            self.winner._shotsTakenPerWin += len(self.playerShots[self.winner])

        if self.showVisualization:
            try:
                self.player1.printBoard()
                self.player2.printBoard()
            except Exception, e:
                print 'Error displaying board: %s' % str(e)

        self.winner._gameWon()
        self.loser._gameLost()
        return self.winner, self.loser

    def isValidShipPlacement(self, ship):
        ''' Is ship placement valid for this game board? '''
        if not ship.locations:
            return False

        for location in ship.locations:
            if (location[0] < 0 or
                location[0] >= self.boardWidth or
                location[1] < 0 or
                location[1] >= self.boardHeight):
                return False

        return True
