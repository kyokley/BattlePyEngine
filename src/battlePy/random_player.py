import random

from battlePy.default_config import BOARD_HEIGHT, BOARD_WIDTH
from battlePy.player import Player
from battlePy.ship import RIGHT, UP


class RandomPlayer(Player):
    def initPlayer(self):
        self.name = 'RandomPlayer'

    def placeShips(self):
        for ship in self.ships:
            isValid = False
            while not isValid:
                orientation = random.choice([UP, RIGHT])
                if orientation == UP:
                    location = (
                        random.randint(0, BOARD_WIDTH - 1),
                        random.randint(0, BOARD_HEIGHT - 1 - ship.size),
                    )
                else:
                    location = (
                        random.randint(0, BOARD_WIDTH - 1 - ship.size),
                        random.randint(0, BOARD_HEIGHT - 1),
                    )
                ship.placeShip(location, orientation)

                if self.isShipPlacedLegally(ship):
                    isValid = True

    def fireShot(self):
        return (random.randint(0, BOARD_WIDTH - 1), random.randint(0, BOARD_HEIGHT - 1))
