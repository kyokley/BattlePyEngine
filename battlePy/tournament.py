from series import Series
from itertools import combinations

class Tournament(object):
    def __init__(self,
                 players,
                 numberOfGames,
                 alternateFirstPlayer=True,
                 debug=False,
                 boardWidth=None,
                 boardHeight=None,
                 showVisualization=False,
                 visualizationInterval=.01,
                 clearBoardOnException=False):
        self.players = players
        self.numberOfGames = numberOfGames
        self.alternateFirstPlayer = alternateFirstPlayer
        self.debug = debug
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.showVisualization = showVisualization
        self.visualizationInterval = visualizationInterval
        self.clearBoardOnException = clearBoardOnException

    def run(self):
        self.results = dict([(player, [0, []]) for player in self.players])
        self.series = [Series(x[0](),
                              x[1](),
                              self.numberOfGames,
                              alternateFirstPlayer=self.alternateFirstPlayer,
                              debug=self.debug,
                              boardWidth=self.boardWidth,
                              boardHeight=self.boardHeight,
                              showVisualization=self.showVisualization,
                              visualizationInterval=self.visualizationInterval,
                              clearBoardOnException=self.clearBoardOnException)
                            for x in combinations(self.players, 2)]

        for series in self.series:
            result = series.start()
            if result:
                self.results[type(result[0])][0] += 1
                self.results[type(result[0])][1].append(type(result[1]).__name__)

        self.displayResults()

    def displayResults(self):
        rankings = sorted(self.results.items(), key=lambda x: -x[1][0])
        for idx, ranking in enumerate(rankings):
            print '%s: %s' % (idx + 1, ranking[0].__name__)
            print '   with wins against %s' % ranking[1][1]
