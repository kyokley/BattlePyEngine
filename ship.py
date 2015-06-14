from config import (BOARD_WIDTH,
                    BOARD_HEIGHT,
                    )
(UP,
 DOWN,
 LEFT,
 RIGHT) = SHIP_ORIENTATIONS = xrange(4)

class Ship(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = set()
        self.locations = set()

    def placeShip(self, location, orientation):
        refDict = {UP: (0, 1),
                   DOWN: (0, -1),
                   LEFT: (-1, 0),
                   RIGHT: (1, 0)}

        newLocation = location
        self.locations.add(newLocation)

        for i in xrange(self.size):
            newLocation = (newLocation[0] + refDict[orientation][0],
                            newLocation[1] + refDict[orientation][1])
            self.locations.add(newLocation)

    def isPlacementValid(self):
        if not self.locations:
            return False

        for location in self.locations:
            if (location[0] < 0 or
                location[0] >= BOARD_WIDTH or
                location[1] < 0 or
                location[1] >= BOARD_HEIGHT):
                return False

        return True

    def addHit(self, location):
        if location not in self.locations:
            return

        self.hits.add(location)

    def isSunk(self):
        return self.hits == self.locations
