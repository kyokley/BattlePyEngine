import unittest
from battlePy.series import Series
from battlePy.random_player import RandomPlayer
from battlePy.improved_random_player import ImprovedRandomPlayer


class TestPlay(unittest.TestCase):
    def setUp(self):
        self.series = Series(RandomPlayer(),
                             ImprovedRandomPlayer(),
                             numberOfGames=11,
                             debug=False,
                             showVisualization=True,
                             visualizationInterval=.001)

    def test_play(self):
        self.series.start()
