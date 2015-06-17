import unittest, mock
from game import Game

class TestPlayGame(unittest.TestCase):
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2)
        self.game._placeShips = mock.MagicMock()
        self.game._takeTurns = mock.MagicMock()
        self.game._gameOver = mock.MagicMock()

    def test_playGame(self):
        self.game.playGame()

        self.assertTrue(self.player1.newGame.called)
        self.assertTrue(self.player2.newGame.called)

        self.assertTrue(self.game._placeShips.called)
        self.assertTrue(self.game._takeTurns.called)

class TestPlaceShips(unittest.TestCase):
    def setUp(self):
        self.player1 = mock.MagicMock()
        self.player2 = mock.MagicMock()

        self.game = Game(self.player1, self.player2)
