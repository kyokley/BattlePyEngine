import time

import mock
import pytest

from battlePy.default_config import BOARD_HEIGHT, BOARD_WIDTH
from battlePy.game import Game
from battlePy.player import GameClockViolationException, Player
from battlePy.ship import DOWN, RIGHT, Ship


def generateLongRunningFunc(timeLength):
    def longRunningFunc(*args, **kwargs):
        time.sleep(timeLength + 0.001)

    return longRunningFunc


class TestShipsPlacedLegally:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips(
            [
                self.ship1,
                self.ship2,
                self.ship3,
            ]
        )

    def test_shipPlacedOffBoard(self):
        self.ship1.placeShip((0, 0), DOWN)
        result = self.testPlayer.isShipPlacedLegally(self.ship1)

        assert not result
        assert not self.testPlayer._allShipsPlacedLegally()

    def test_shipsOverlapping(self):
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((5, 5), RIGHT)

        result = self.testPlayer.isShipPlacedLegally(self.ship1)
        assert not result

        result = self.testPlayer.isShipPlacedLegally(self.ship2)
        assert result

        result = self.testPlayer.isShipPlacedLegally(self.ship3)
        assert not result
        assert not self.testPlayer._allShipsPlacedLegally()

    def test_shipsAreValid(self):
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

        result = self.testPlayer.isShipPlacedLegally(self.ship1)
        assert result

        result = self.testPlayer.isShipPlacedLegally(self.ship2)
        assert result

        result = self.testPlayer.isShipPlacedLegally(self.ship3)
        assert result
        assert self.testPlayer._allShipsPlacedLegally()


class TestCheckIsHit:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips(
            [
                self.ship1,
                self.ship2,
                self.ship3,
            ]
        )
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_checkIsMiss(self):
        shot = (1, 1)
        hit, hitShip = self.testPlayer._checkIsHit(shot)

        assert not hit
        assert hitShip is None

    def test_checkIsHit(self):
        shot = (5, 3)
        hit, hitShip = self.testPlayer._checkIsHit(shot)

        assert hit
        assert hitShip == self.ship1


class TestCheckAllShipsSunk:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.game = Game(self.testPlayer, self.mockPlayer)
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT
        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips(
            [
                self.ship1,
                self.ship2,
                self.ship3,
            ]
        )
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_noShipsSunk(self):
        assert not self.testPlayer._checkAllShipsSunk()

    def test_oneShipSunk(self):
        self.ship1.hits = self.ship1.locations
        assert not self.testPlayer._checkAllShipsSunk()

    def test_allShipsSunk(self):
        self.ship1.hits = self.ship1.locations
        self.ship2.hits = self.ship2.locations
        self.ship3.hits = self.ship3.locations

        assert self.testPlayer._checkAllShipsSunk()


class TestGameClockViolations:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.testPlayer = Player()
        self.mockPlayer = mock.MagicMock()
        self.timeoutLength = 0.01
        self.game = Game(
            self.testPlayer, self.mockPlayer, timeoutLength=self.timeoutLength
        )
        self.game.boardWidth = BOARD_WIDTH
        self.game.boardHeight = BOARD_HEIGHT

        self.testPlayer.currentGame = self.game

        self.ship1 = Ship('ship1', 3, self.game)
        self.ship2 = Ship('ship2', 4, self.game)
        self.ship3 = Ship('ship3', 2, self.game)
        self.testPlayer._setShips(
            [
                self.ship1,
                self.ship2,
                self.ship3,
            ]
        )
        self.ship1.placeShip((5, 5), DOWN)
        self.ship2.placeShip((0, 6), RIGHT)
        self.ship3.placeShip((6, 5), RIGHT)

    def test_newGame(self):
        self.testPlayer.newGame = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._newGame()

    def test_placeShips(self):
        self.testPlayer.placeShips = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._placeShips()

    def test_shotHit(self):
        self.testPlayer.shotHit = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._shotHit((0, 0), 'ship1')

    def test_shotMissed(self):
        self.testPlayer.shotMissed = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._shotMissed((0, 0))

    def test_shipSunk(self):
        self.testPlayer.shipSunk = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._shipSunk('ship1')

    def test_fireShot(self):
        self.testPlayer.fireShot = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._fireShot()

    def test_gameWon(self):
        self.testPlayer.gameWon = generateLongRunningFunc(self.timeoutLength)
        self.testPlayer._gameWon()

    def test_gameLost(self):
        self.testPlayer.gameLost = generateLongRunningFunc(self.timeoutLength)
        self.testPlayer._gameLost()

    def test_opponentShot(self):
        self.testPlayer.opponentShot = generateLongRunningFunc(self.timeoutLength)
        with pytest.raises(GameClockViolationException):
            self.testPlayer._opponentShot((0, 0))

    def test_isValidPoint(self):
        point1 = (0, 0)
        point2 = (self.game.boardWidth - 1, 0)
        point3 = (0, self.game.boardHeight - 1)
        point4 = (self.game.boardWidth - 1, self.game.boardHeight - 1)
        point5 = (-1, 0)
        point6 = (0, -1)
        point7 = (self.game.boardWidth, self.game.boardHeight)
        point8 = (-10, -10)

        assert self.testPlayer._isValidPoint(point1)
        assert self.testPlayer._isValidPoint(point2)
        assert self.testPlayer._isValidPoint(point3)
        assert self.testPlayer._isValidPoint(point4)

        assert not self.testPlayer._isValidPoint(point5)
        assert not self.testPlayer._isValidPoint(point6)
        assert not self.testPlayer._isValidPoint(point7)
        assert not self.testPlayer._isValidPoint(point8)
