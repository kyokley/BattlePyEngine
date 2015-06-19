from config import (BOARD_WIDTH,
                    BOARD_HEIGHT,
                    )
(UP,
 DOWN,
 LEFT,
 RIGHT) = SHIP_ORIENTATIONS = xrange(4)
VECTOR_DICT = {UP: (0, 1),
               DOWN: (0, -1),
               LEFT: (-1, 0),
               RIGHT: (1, 0)}

class Ship(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.hits = set()
        self.locations = set()

    def placeShip(self, location, orientation):
        self.locations = set()

        newLocation = location
        self.locations.add(newLocation)

        for i in xrange(self.size - 1):
            newLocation = (newLocation[0] + VECTOR_DICT[orientation][0],
                            newLocation[1] + VECTOR_DICT[orientation][1])
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

    def getProtoShip(self):
        return Ship(self.name, self.size)
