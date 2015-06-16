import unittest
from ship import Ship
from players.player import Player
from ship import DOWN

class TestIsShipPlacedLegally(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.ship1 = Ship('ship1', 3)
        self.ship2 = Ship('ship2', 4)
        self.ship3 = Ship('ship3', 2)
        self.testPlayer._setShips([self.ship1,
                                   self.ship2,
                                   ])

    def test_shipPlacedOffBoard(self):
        self.ship1.placeShip((0, 0), DOWN)
        result = self.testPlayer.isShipPlacedLegally(self.ship1)

        self.assertFalse(result)
