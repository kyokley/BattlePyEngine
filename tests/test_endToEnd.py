import unittest

from battlePy.improved_random_player import ImprovedRandomPlayer
from battlePy.random_player import RandomPlayer
from battlePy.series import Series


class TestPlay(unittest.TestCase):
    def setUp(self):
        self.series = Series(
            RandomPlayer(),
            ImprovedRandomPlayer(),
            numberOfGames=11,
            debug=False,
            showVisualization=True,
            visualizationInterval=0.001,
        )

    def test_play(self):
        self.series.start()
