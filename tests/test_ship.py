import mock
import pytest

from battlePy.game import Game
from battlePy.ship import DOWN, LEFT, RIGHT, UP, Ship


class TestPlaceShip:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_placeShipUp(self):
        self.testShip.placeShip((0, 0), UP)
        assert self.testShip.locations == set(
            [
                (0, 0),
                (0, 1),
                (0, 2),
            ]
        )

    def test_placeShipDown(self):
        self.testShip.placeShip((5, 5), DOWN)
        assert self.testShip.locations == set(
            [
                (5, 5),
                (5, 4),
                (5, 3),
            ]
        )

    def test_placeShipRight(self):
        self.testShip.placeShip((5, 2), RIGHT)
        assert self.testShip.locations == set(
            [
                (5, 2),
                (6, 2),
                (7, 2),
            ]
        )

    def test_placeShipLeft(self):
        self.testShip.placeShip((5, 2), LEFT)
        assert self.testShip.locations == set(
            [
                (5, 2),
                (4, 2),
                (3, 2),
            ]
        )


class TestIsPlacementValid:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_isPlacementValid(self):
        self.testShip.placeShip((0, 1), DOWN)
        assert not self.testShip.isPlacementValid()

        self.testShip.placeShip((0, 2), LEFT)
        assert not self.testShip.isPlacementValid()

        self.testShip.placeShip((10, 2), RIGHT)
        assert not self.testShip.isPlacementValid()

        self.testShip.placeShip((5, 5), UP)
        assert self.testShip.isPlacementValid()

        self.testShip.placeShip((0, 0), UP)
        assert self.testShip.isPlacementValid()

        self.testShip.placeShip((9, 0), UP)
        assert self.testShip.isPlacementValid()


class TestAddHit:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)

    def test_notAHit(self):
        self.testShip.placeShip((5, 5), UP)
        shot = (0, 0)
        self.testShip.addHit(shot)

        assert self.testShip.hits == set()

    def test_hit(self):
        self.testShip.placeShip((5, 5), UP)
        shot = (5, 7)
        self.testShip.addHit(shot)

        assert self.testShip.hits == set([(5, 7)])


class TestIsSunk:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.game = Game(mock.MagicMock(), mock.MagicMock())
        self.testShip = Ship('testShip1', 3, self.game)
        self.testShip.placeShip((5, 5), UP)

    def test_notSunk(self):
        self.testShip.hits = set(
            [
                (5, 5),
                (5, 6),
            ]
        )
        assert not self.testShip.isSunk()

    def test_sunk(self):
        self.testShip.hits = set(
            [
                (5, 5),
                (5, 6),
                (5, 7),
            ]
        )
        assert self.testShip.isSunk()
