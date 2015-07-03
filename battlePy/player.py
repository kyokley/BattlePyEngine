from battlePy.utils import docprop
from datetime import datetime

def _gameClockTimedMethod(func):
    def func_wrapper(cls, *args, **kwargs):
        t0 = datetime.now()
        res = func(cls, *args, **kwargs)
        t1 = datetime.now()
        timediff = t1 - t0
        cls._gameTime += timediff.total_seconds() * 1000000
        if not cls.currentGame.debug:
            if cls._gameTime > cls.currentGame.timeoutLength:
                raise Exception("Player has gone over allotted time.")
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
        self.initPlayer()

    def initPlayer(self):
        ''' Initialize this player '''
        pass

    @_gameClockTimedMethod
    def _placeShips(self):
        return self.placeShips()

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

    @_gameClockTimedMethod
    def _shotHit(self, shot, shipName):
        return self.shotHit(shot, shipName)

    def shotHit(self, shot, shipName):
        ''' Method called when a ship is hit

        Args:
            shot (tuple): x, y pair of the shot location
            shipName (string): Name of the ship that was hit
        '''
        pass

    @_gameClockTimedMethod
    def _shotMissed(self, shot):
        return self.shotMissed(shot)

    def shotMissed(self, shot):
        ''' Method called when a shot misses

        Args:
            shot (tuple): x, y pair of the shot location
        '''
        pass

    @_gameClockTimedMethod
    def _shipSunk(self, shipName):
        return self.shipSunk(shipName)

    def shipSunk(self, shipName):
        ''' Method called when a ship is sunk

        Args:
            shipName (string): Name of the ship that was hit
        '''
        pass

    @_gameClockTimedMethod
    def _fireShot(self):
        return self.fireShot()

    def fireShot(self):
        ''' Get an x, y coordinate pair for a shot location

        Yields:
            tuple: x, y coordinate pair
        '''
        raise NotImplementedError()

    @_gameClockTimedMethod
    def _gameWon(self):
        return self.gameWon()

    def gameWon(self):
        pass

    @_gameClockTimedMethod
    def _gameLost(self):
        return self.gameLost()

    def gameLost(self):
        pass

    @_gameClockTimedMethod
    def _newGame(self):
        self._gameTime = 0
        return self.newGame()

    def newGame(self):
        pass

    @_gameClockTimedMethod
    def _opponentShot(self, shot):
        return self.opponentShot(shot)

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

