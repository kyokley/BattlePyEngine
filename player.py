class Player(object):
    def __init__(self, name):
        self.ships = None
        self.name = name

    def setShips(self, ships):
        self.ships = ships

    def allShipsPlaced(self):
        if not self.ships:
            return False

        for ship in self.ships:
            if not ship.isPlacementValid():
                return False
