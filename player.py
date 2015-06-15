
class Player(object):
    def __init__(self, name='player'):
        self.ships = None
        self.name = name
        self.initPlayer()

    def initPlayer(self):
        pass

    def placeShips(self):
        raise NotImplementedError()

    def isShipPlacedLegally(self, refShip):
        if not refShip.isPlacementValid():
            return False

        for ship in self.ships:
            if refShip == ship:
                continue

            for location in refShip.locations:
                if location in ship.locations:
                    return False

        return True

    def shotHit(self, location, ship):
        pass

    def shotMissed(self, location):
        pass

    def shipSunk(self, ship):
        pass

    def fireShot(self):
        raise NotImplementedError()

    def gameWon(self):
        pass

    def gameLost(self):
        pass

    def newGame(self):
        pass

    def _setShips(self, ships):
        self.ships = ships

    def _allShipsPlacedLegally(self):
        if not self.ships:
            return False

        allLocations = set()
        for ship in self.ships:
            if not ship.isPlacementValid():
                return False

            for location in ship.locations:
                if location in allLocations:
                    return False

            allLocations.update(ship.locations)

        return True

    def _checkIsHit(self, location):
        hit = False
        hitShip = None
        for ship in self.ships:
            if location in ship.locations and location not in ship.hits:
                ship.addHit(location)
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

    def getInfo(self):
        print 'Ship Locations'
        for ship in self.ships:
            print '%s: %s Hits: %s' % (ship.name, sorted(list(ship.locations)), sorted(list(ship.hits)))
