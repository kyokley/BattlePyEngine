import unittest, mock, time
from battlePy.ship import Ship
from battlePy.player import Player
from battlePy.ship import DOWN, RIGHT
from battlePy.default_config import (BOARD_WIDTH,
                                     BOARD_HEIGHT,
                                     )
from battlePy.game import Game

def generateLongRunningFunc(timeLength):
    def longRunningFunc(*args, **kwargs):
        time.sleep(timeLength + .001)
    return longRunningFunc

class TestShipsPlacedLegally(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
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
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
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

class TestCheckAllShipsSunk(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips([self.ship1,
                                   self.ship2,
                                   self.ship3,
                                   ])
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_noShipsSunk(self):
        self.assertFalse(self.testPlayer._checkAllShipsSunk())

    def test_oneShipSunk(self):
        self.ship1.hits = self.ship1.locations
        self.assertFalse(self.testPlayer._checkAllShipsSunk())

    def test_allShipsSunk(self):
        self.ship1.hits = self.ship1.locations
        self.ship2.hits = self.ship2.locations
        self.ship3.hits = self.ship3.locations

        self.assertTrue(self.testPlayer._checkAllShipsSunk())

class TestGameClockViolations(unittest.TestCase):
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.timeoutLength = .01
        self.game = Game(self.testPlayer, self.mockPlayer, timeoutLength=self.timeoutLength)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips([self.ship1,
                                   self.ship2,
                                   self.ship3,
                                   ])
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_newGame(self):
        self.testPlayer.newGame = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._newGame)

    def test_placeShips(self):
        self.testPlayer.placeShips = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._placeShips)

    def test_shotHit(self):
        self.testPlayer.shotHit = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._shotHit)

    def test_shotMissed(self):
        self.testPlayer.shotMissed = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._shotMissed)

    def test_shipSunk(self):
        self.testPlayer.shipSunk = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._shipSunk)

    def test_fireShot(self):
        self.testPlayer.fireShot = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._fireShot)

    def test_gameWon(self):
        self.testPlayer.gameWon = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._gameWon)

    def test_gameLost(self):
        self.testPlayer.gameLost = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._gameLost)

    def test_opponentShot(self):
        self.testPlayer.opponentShot = generateLongRunningFunc(self.timeoutLength)
        self.assertRaises(Exception, self.testPlayer._opponentShot)
