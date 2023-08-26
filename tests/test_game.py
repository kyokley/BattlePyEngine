import mock
import pytest

from battlePy.default_config import DEFAULT_SHIPS
from battlePy.game import Game, PlayerException


class TestPlayGame:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2, shipSpecs=DEFAULT_SHIPS)
        self.game._placeShips = mock.MagicMock()
        self.game._takeTurns = mock.MagicMock()
        self.game._gameOver = mock.MagicMock()

    def test_playGame(self):
        self.game.playGame()

        assert self.player1._newGame.called
        assert self.player2._newGame.called

        assert self.game._placeShips.called
        assert self.game._takeTurns.called


class TestPlaceShips:
    @pytest.fixture(autouse=True)
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2)

    def test_shipsPlacedLegally(self):
        self.player1._allShipsPlacedLegally.return_value = True
        self.player2._allShipsPlacedLegally.return_value = True

        self.game._placeShips()

        assert self.player1._placeShips.called
        assert self.player2._placeShips.called

        assert self.player1._allShipsPlacedLegally.called
        assert self.player2._allShipsPlacedLegally.called

    def test_shipsPlacedIllegally(self):
        self.player1._allShipsPlacedLegally.return_value = True
        self.player2._allShipsPlacedLegally.return_value = False

        try:
            self.game._placeShips()
        except Exception as e:
            exception = e

        assert self.player1._placeShips.called
        assert self.player2._placeShips.called

        assert self.player1._allShipsPlacedLegally.called
        assert self.player2._allShipsPlacedLegally.called

        assert self.player2 == exception.args[1]
        assert isinstance(exception, PlayerException)
