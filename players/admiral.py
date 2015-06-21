from player import Player
from config import (BOARD_WIDTH,
                    BOARD_HEIGHT,
                    DEFAULT_SHIPS)
from ship import (UP,
                  RIGHT,
                  LEFT,
                  DOWN,
                  SHIP_ORIENTATIONS,
                  VECTOR_DICT,
                  )
import random, math

VERSION = 'v0.1'
(SEARCH,
 DESTROY,
 RANDOM) = OFFENSIVE_MODES = range(3)

def intToPoint(num):
    x = num % BOARD_WIDTH
    y = num / BOARD_WIDTH
    return x, y

def pointToInt(point):
    total = point[0] + BOARD_WIDTH * point[1]
    return total

def isValidPoint(point):
    return (0 <= point[0] < BOARD_WIDTH and
            0 <= point[1] < BOARD_HEIGHT)

class Admiral(Player):
    def initPlayer(self):
        self.name = 'Admiral %s' % VERSION
        self.shipSizes = dict(((x[0], x[1]) for x in DEFAULT_SHIPS))

    def newGame(self):
        self.shots = set()
        self.foundShips = dict(((x[0], []) for x in DEFAULT_SHIPS))
        self.searchMat = []
        self.killMats = dict(((x[0], set()) for x in DEFAULT_SHIPS))

        shipSizes = [x.size for x in self.ships]
        minShipSize = min(shipSizes)

        self.offense = SEARCH

        for i in xrange(BOARD_HEIGHT):
            if i % 2 == 0:
                for j in xrange(BOARD_WIDTH):
                    smallMod = (i % (minShipSize + 1))
                    if j % (minShipSize + 1) == smallMod:
                        self.searchMat.append((i, j))

        print self.searchMat

    @staticmethod
    def getDistance(x, y):
        dist = math.sqrt(x**2 + y**2) 
        return dist

    def findMinMaxPoint(self, points):
        minPoint = None
        maxPoint = None
        for point in points:
            if not maxPoint:
                maxPoint = point
            if not minPoint:
                minPoint = point
            maxDist = self.getDistance(maxPoint[0], maxPoint[1])
            minDist = self.getDistance(minPoint[0], minPoint[1])
            pointDist = self.getDistance(point[0], point[1])

            if pointDist > maxDist:
                maxPoint = point
            if pointDist < minDist:
                minPoint = point
        return maxPoint, minPoint

    def normalize(self, shot):
        if shot[0] > 0:
            x = 1
        elif shot[0] < 0:
            x = -1
        else:
            x = 0

        if shot[1] > 0:
            y = 1
        elif shot[1] < 0:
            y = -1
        else:
            y = 0

        return x, y

    def shotHit(self, shot, shipName):
        hitShip = self.foundShips[shipName]
        hitShip.append(shot)

        if len(hitShip) > 1:
            # Filter out impossible locations
            maxPoint, minPoint = self.findMinMaxPoint(hitShip)

            shipLine = self.normalize((maxPoint[0] - minPoint[0],
                                       maxPoint[1] - minPoint[1]))

            possibleLocations = []
            for i in xrange(1, self.shipSizes[shipName] - len(hitShip) + 1):
                possibleShot = (minPoint[0] - i * shipLine[0],
                                minPoint[1] - i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

                possibleShot = (maxPoint[0] + i * shipLine[0],
                                maxPoint[1] + i * shipLine[1])
                if isValidPoint(possibleShot):
                    possibleLocations.append(possibleShot)

            self.killMats[shipName] = set(possibleLocations)

        else:
            # Build out the full kill matrix
            for i in xrange(1, self.shipSizes[shipName] - 1):
                for direction in SHIP_ORIENTATIONS:
                    vector = (VECTOR_DICT[direction][0] * i,
                              VECTOR_DICT[direction][1] * i)
                    self.killMats[shipName].add((shot[0] + vector[0], shot[1] + vector[1]))

    def shipSunk(self, shipName):
        pass


    def placeShips(self):
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    location = (random.randint(0, BOARD_WIDTH - 1),
                                random.randint(0, BOARD_HEIGHT - 1 - ship.size))
                else:
                    location = (random.randint(0, BOARD_WIDTH - 1 - ship.size),
                                random.randint(0, BOARD_HEIGHT - 1))
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True

    def fireShot(self):
        shot = (random.randint(0, BOARD_WIDTH - 1),
                random.randint(0, BOARD_HEIGHT - 1))

        while shot in self.shots:
            shot = (random.randint(0, BOARD_WIDTH - 1),
                    random.randint(0, BOARD_HEIGHT - 1))
        self.shots.add(shot)
        return shot

