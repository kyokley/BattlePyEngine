import unittest
from ship import Ship
from players.player import Player
from ship import DOWN, RIGHT

class TestShipsPlacedLegally(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.ship1 = Ship('ship1', 3)
        self.ship2 = Ship('ship2', 4)
        self.ship3 = Ship('ship3', 2)
        self.testPlayer._setShips([self.ship1,
                                   self.ship2,
                                   self.ship3,
                                   ])

    def test_shipPlacedOffBoard(self):
        self.ship1.placeShip((0, 0), DOWN)
        result = self.testPlayer.isShipPlacedLegally(self.ship1)

        self.assertFalse(result)
        self.assertFalse(self.testPlayer._allShipsPlacedLegally())

    def test_shipsOverlapping(self):
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((5, 5), RIGHT)

        result = self.testPlayer.isShipPlacedLegally(self.ship1)
        self.assertFalse(result)

        result = self.testPlayer.isShipPlacedLegally(self.ship2)
        self.assertTrue(result)

        result = self.testPlayer.isShipPlacedLegally(self.ship3)
        self.assertFalse(result)
        self.assertFalse(self.testPlayer._allShipsPlacedLegally())

    def test_shipsAreValid(self):
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

        result = self.testPlayer.isShipPlacedLegally(self.ship1)
        self.assertTrue(result)

        result = self.testPlayer.isShipPlacedLegally(self.ship2)
        self.assertTrue(result)

        result = self.testPlayer.isShipPlacedLegally(self.ship3)
        self.assertTrue(result)
        self.assertTrue(self.testPlayer._allShipsPlacedLegally())

class TestCheckIsHit(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.ship1 = Ship('ship1', 3)
        self.ship2 = Ship('ship2', 4)
        self.ship3 = Ship('ship3', 2)
        self.testPlayer._setShips([self.ship1,
                                   self.ship2,
                                   self.ship3,
                                   ])
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_checkIsMiss(self):
        shot = (1, 1)
        hit, hitShip = self.testPlayer._checkIsHit(shot)

        self.assertFalse(hit)
        self.assertEqual(hitShip, None)

    def test_checkIsHit(self):
        shot = (5, 3)
        hit, hitShip = self.testPlayer._checkIsHit(shot)

        self.assertTrue(hit)
        self.assertEqual(hitShip, self.ship1)
