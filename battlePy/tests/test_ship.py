import unittest
import mock
from battlePy.ship import (Ship,
                           UP,
                           DOWN,
                           LEFT,
                           RIGHT,
                           )
from battlePy.game import Game


class TestPlaceShip(unittest.TestCase):
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_placeShipUp(self):
        self.testShip.placeShip((0, 0), UP)
        self.assertEquals(self.testShip.locations, set([(0, 0),
                                                        (0, 1),
                                                        (0, 2),
                                                        ]))

    def test_placeShipDown(self):
        self.testShip.placeShip((5, 5), DOWN)
        self.assertEquals(self.testShip.locations, set([(5, 5),
                                                        (5, 4),
                                                        (5, 3),
                                                        ]))

    def test_placeShipRight(self):
        self.testShip.placeShip((5, 2), RIGHT)
        self.assertEquals(self.testShip.locations, set([(5, 2),
                                                        (6, 2),
                                                        (7, 2),
                                                        ]))

    def test_placeShipLeft(self):
        self.testShip.placeShip((5, 2), LEFT)
        self.assertEquals(self.testShip.locations, set([(5, 2),
                                                        (4, 2),
                                                        (3, 2),
                                                        ]))


class TestIsPlacementValid(unittest.TestCase):
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_isPlacementValid(self):
        self.testShip.placeShip((0, 1), DOWN)
        self.assertFalse(self.testShip.isPlacementValid())

        self.testShip.placeShip((0, 2), LEFT)
        self.assertFalse(self.testShip.isPlacementValid())

        self.testShip.placeShip((10, 2), RIGHT)
        self.assertFalse(self.testShip.isPlacementValid())

        self.testShip.placeShip((5, 5), UP)
        self.assertTrue(self.testShip.isPlacementValid())

        self.testShip.placeShip((0, 0), UP)
        self.assertTrue(self.testShip.isPlacementValid())

        self.testShip.placeShip((9, 0), UP)
        self.assertTrue(self.testShip.isPlacementValid())


class TestAddHit(unittest.TestCase):
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_notAHit(self):
        self.testShip.placeShip((5, 5), UP)
        shot = (0, 0)
        self.testShip.addHit(shot)

        self.assertEquals(self.testShip.hits, set())

    def test_hit(self):
        self.testShip.placeShip((5, 5), UP)
        shot = (5, 7)
        self.testShip.addHit(shot)

        self.assertEquals(self.testShip.hits, set([(5, 7)]))


class TestIsSunk(unittest.TestCase):
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)
        self.testShip.placeShip((5, 5), UP)

    def test_notSunk(self):
        self.testShip.hits = set([(5, 5),
                                  (5, 6),
                                  ])
        self.assertFalse(self.testShip.isSunk())

    def test_sunk(self):
        self.testShip.hits = set([(5, 5),
                                  (5, 6),
                                  (5, 7),
                                  ])
        self.assertTrue(self.testShip.isSunk())
