from battlePy.utils import docprop

(UP,
 DOWN,
 LEFT,
 RIGHT) = SHIP_ORIENTATIONS = range(4)
VECTOR_DICT = {UP: (0, 1),
               DOWN: (0, -1),
               LEFT: (-1, 0),
               RIGHT: (1, 0)}


class Ship(object):
    name = docprop('name', 'Name of the ship')
    size = docprop('size', 'Size of the ship')
    hits = docprop('hits', 'Set of current hit locations')
    locations = docprop('locations', 'Set of ship coordinates')
    game = docprop('game', 'The game this Ship belongs to')

    def __init__(self, name, size, game):
        self.name = name
        self.size = size
        self.hits = set()
        self.locations = set()
        self.game = game
        self.symbol = self.name[0]

    def __repr__(self):
        return "<%s %s %s>" % (self.__class__.__name__, id(self), self.name)

    def placeShip(self, location, orientation):
        self.locations = set()

        newLocation = location
        self.locations.add(newLocation)

        for i in range(self.size - 1):
            newLocation = (newLocation[0] + VECTOR_DICT[orientation][0],
                           newLocation[1] + VECTOR_DICT[orientation][1])
            self.locations.add(newLocation)

    def isPlacementValid(self):
        return self.game.isValidShipPlacement(self)

    def addHit(self, location):
        if location not in self.locations:
            return

        self.hits.add(location)

    def isSunk(self):
        return self.hits == self.locations

    def getProtoShip(self):
        return Ship(self.name, self.size)
