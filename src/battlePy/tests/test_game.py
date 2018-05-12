import unittest, mock
from battlePy.game import Game, PlayerException
from battlePy.default_config import DEFAULT_SHIPS

class TestPlayGame(unittest.TestCase):
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2, shipSpecs=DEFAULT_SHIPS)
        self.game._placeShips = mock.MagicMock()
        self.game._takeTurns = mock.MagicMock()
        self.game._gameOver = mock.MagicMock()

    def test_playGame(self):
        self.game.playGame()

        self.assertTrue(self.player1._newGame.called)
        self.assertTrue(self.player2._newGame.called)

        self.assertTrue(self.game._placeShips.called)
        self.assertTrue(self.game._takeTurns.called)

class TestPlaceShips(unittest.TestCase):
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2)

    def test_shipsPlacedLegally(self):
        self.player1._allShipsPlacedLegally.return_value = True
        self.player2._allShipsPlacedLegally.return_value = True

        self.game._placeShips()

        self.assertTrue(self.player1._placeShips.called)
        self.assertTrue(self.player2._placeShips.called)

        self.assertTrue(self.player1._allShipsPlacedLegally.called)
        self.assertTrue(self.player2._allShipsPlacedLegally.called)

    def test_shipsPlacedIllegally(self):
        self.player1._allShipsPlacedLegally.return_value = True
        self.player2._allShipsPlacedLegally.return_value = False

        try:
            self.game._placeShips()
        except Exception as e:
            exception = e

        self.assertTrue(self.player1._placeShips.called)
        self.assertTrue(self.player2._placeShips.called)

        self.assertTrue(self.player1._allShipsPlacedLegally.called)
        self.assertTrue(self.player2._allShipsPlacedLegally.called)

        self.assertEquals(self.player2, exception.args[1])
        self.assertTrue(isinstance(exception, PlayerException))
