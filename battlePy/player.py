from battlePy.utils import docprop

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
