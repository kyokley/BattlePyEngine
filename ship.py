(UP,
 DOWN,
 LEFT,
 RIGHT) = xrange(4)

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


    def _buildLocationList(self):
        pass
