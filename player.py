class Player(object):
    def __init__(self, name):
        self.ships = None
        self.name = name

    def _setShips(self, ships):
        self.ships = ships

    def placeShips(self):
        raise NotImplemented

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

    def shotHit(self, location):
        pass

    def shotMissed(self, location):
        pass

    def shipSunk(self, ship):
        pass

    def getShot(self):
        raise NotImplemented

    def gameWon(self):
        pass

    def gameLost(self):
        pass

    def _checkIsHit(self, location):
        hit = False
        sunk = None
        for ship in self.ships:
            if location in ship.locations:
                ship.addHit(location)
                hit = True
                if ship.isSunk():
                    sunk = ship
                break

        return hit, sunk

    def _checkAllShipsSunk(self):
        done = True
        for ship in self.ships:
            if not ship.isSunk():
                done = False
                break
        return done
