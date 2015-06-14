from player import Player
from config import (BOARD_WIDTH,
                    BOARD_HEIGHT)
from ship import SHIP_ORIENTATIONS
import random

class RandomPlayer(Player):
    def initPlayer(self):
        self.name = 'RandomPlayer'

    def placeShips(self):
        for ship in self.ships:
            location = (random.randint(0, BOARD_WIDTH - 1),
                        random.randint(0, BOARD_HEIGHT - 1))
            orientation = random.choice(SHIP_ORIENTATIONS)
            ship.placeShip(location, orientation)

    def getShot():
        return (random.randint(0, BOARD_WIDTH - 1),
                random.randint(0, BOARD_HEIGHT - 1))
