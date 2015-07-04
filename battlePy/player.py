from battlePy.utils import docprop
from datetime import datetime
from blessings import Terminal

class GameClockViolationException(Exception):
    pass

def _gameClockTimedMethod(func):
    def func_wrapper(cls, *args, **kwargs):
        t0 = datetime.now()
        res = func(cls, *args, **kwargs)
        t1 = datetime.now()
        timediff = t1 - t0
        cls._gameTime += timediff.total_seconds() * 1000000
        if not cls.currentGame.debug:
            if cls._gameTime > cls.currentGame.timeoutLength:
                raise GameClockViolationException("Player has gone over allotted time.")
        return res
    return func_wrapper

class Player(object):
    ships = docprop('ships', "List of this player's ship objects")
    name = docprop('name', 'Player name')
    currentGame = docprop('currentGame', 'Game that is currently being played')

    def __init__(self):
        self.ships = None
        self.name = self.__class__.__name__
        self.currentGame = None
        self._gameTime = 0
        self._opponentMisses = set()
        self.hOffset = 0
        self.vOffset = 0
        self.initPlayer()

    def initPlayer(self):
        ''' Initialize this player '''
        pass

    def placeShips(self):
        ''' Determine where ships should be placed and place them on the game board '''
        raise NotImplementedError()

    def isShipPlacedLegally(self, refShip):
        ''' Determine if a ship has been placed legally '''
        if not refShip.isPlacementValid():
            return False

        for ship in self.ships:
            if refShip == ship:
                continue

            for location in refShip.locations:
                if location in ship.locations:
                    return False

        return True

    def shotHit(self, shot, shipName):
        ''' Method called when a ship is hit

        Args:
            shot (tuple): x, y pair of the shot location
            shipName (string): Name of the ship that was hit
        '''
        pass

    def shotMissed(self, shot):
        ''' Method called when a shot misses

        Args:
            shot (tuple): x, y pair of the shot location
        '''
        pass

    def shipSunk(self, shipName):
        ''' Method called when a ship is sunk

        Args:
            shipName (string): Name of the ship that was hit
        '''
        pass

    def fireShot(self):
        ''' Get an x, y coordinate pair for a shot location

        Yields:
            tuple: x, y coordinate pair
        '''
        raise NotImplementedError()

    def gameWon(self):
        pass


    def gameLost(self):
        pass

    def newGame(self):
        pass

    def opponentShot(self, shot):
        pass

    def _setShips(self, ships):
        self.ships = ships

    def _allShipsPlacedLegally(self):
        if not self.ships:
            return False

        for ship in self.ships:
            if not self.isShipPlacedLegally(ship):
                return False

        return True

    def _checkIsHit(self, shot):
        hit = False
        hitShip = None
        for ship in self.ships:
            if shot in ship.locations and shot not in ship.hits:
                ship.addHit(shot)
                hit = True
                hitShip = ship
                break

        return hit, hitShip

    def _checkAllShipsSunk(self):
        done = True
        for ship in self.ships:
            if not ship.isSunk():
                done = False
                break
        return done

    def _getInfo(self):
        print self.name
        print 'Ship Locations'
        for ship in self.ships:
            print '%s: %s Hits: %s' % (ship.name, sorted(list(ship.locations)), sorted(list(ship.hits)))

    @_gameClockTimedMethod
    def _placeShips(self):
        return self.placeShips()

    @_gameClockTimedMethod
    def _shotHit(self, shot, shipName):
        return self.shotHit(shot, shipName)

    @_gameClockTimedMethod
    def _shotMissed(self, shot):
        return self.shotMissed(shot)

    @_gameClockTimedMethod
    def _shipSunk(self, shipName):
        return self.shipSunk(shipName)

    @_gameClockTimedMethod
    def _fireShot(self):
        return self.fireShot()

    def _gameWon(self):
        return self.gameWon()

    def _gameLost(self):
        return self.gameLost()

    @_gameClockTimedMethod
    def _newGame(self):
        self._gameTime = 0
        self._opponentMisses = set()
        return self.newGame()

    @_gameClockTimedMethod
    def _opponentShot(self, shot):
        for ship in self.ships:
            if shot in ship.locations:
                break
        else:
            self._opponentMisses.add(shot)
        return self.opponentShot(shot)

    def printBoard(self):
        term = Terminal()

        print term.move(0 + self.vOffset, 0 + self.hOffset) + self.name[:12]
        for i in xrange(1, self.currentGame.boardWidth + 1):
            print term.move(1 + self.vOffset, i + self.hOffset) + '-'
            print term.move(self.currentGame.boardHeight + 2 + self.vOffset, i + self.hOffset) + '-'

        for i in xrange(1, self.currentGame.boardHeight + 1):
            print term.move(i + 1 + self.vOffset, 0 + self.hOffset) + '|'
            print term.move(i + 1 + self.vOffset, self.currentGame.boardWidth + 1 + self.hOffset) + '|'

        for ship in self.ships:
            for location in ship.locations:
                if location not in ship.hits:
                    x, y = location
                    print term.move(x + 2 + self.vOffset, y + 1 + self.hOffset) + term.green(ship.symbol)

            for location in ship.hits:
                x, y = location
                print term.move(x + 2 + self.vOffset, y + 1 + self.hOffset) + term.red('X')

        for location in self._opponentMisses:
            x, y = location
            print term.move(x + 2 + self.vOffset, y + 1 + self.hOffset) + term.white('.')
        print term.move(1 + self.vOffset, 0 + self.hOffset) + '+'
        print term.move(self.currentGame.boardWidth + 2 + self.vOffset, 0 + self.hOffset) + '+'
        print term.move(1 + self.vOffset, self.currentGame.boardHeight + 1 + self.hOffset) + '+'
        print term.move(self.currentGame.boardWidth + 2 + self.vOffset, self.currentGame.boardHeight + 1 + self.hOffset) + '+'
