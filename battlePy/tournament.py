from series import Series
from itertools import combinations
from blessings import Terminal
from tabulate import tabulate

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
        self.term = Terminal()

    def run(self):
        self.results = dict([(player, [{'win': 0,
                                        'lose': 0,
                                        'draw': 0}, []]) for player in self.players])
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
            if self.showVisualization:
                print self.term.clear
            result = series.start()
            if result is not None:
                self.results[type(result[0])][0]['win'] += 1
                self.results[type(result[1])][0]['lose'] += 1

                self.results[type(result[0])][1].append(type(result[1]).__name__)
            else:
                # A null result means we got a draw
                self.results[type(result[0])][0]['draw'] += 1
                self.results[type(result[1])][0]['draw'] += 1

            self.displayLeaderBoard()

        self.finalResults()

    def displayLeaderBoard(self):
        rankings = sorted(self.results.items(), key=lambda x: -x[1][0]['win'])
        data = []
        for idx, ranking in enumerate(rankings):
            data.append(('%s: %s' % (idx + 1, ranking[0].__name__),
                         ranking[1][0]['win'],
                         ranking[1][0]['lose'],
                         ranking[1][0]['draw'],))
        table = tabulate(data, headers=['Player', 'Wins', 'Losses', 'Draws'])
        print table

    def finalResults(self):
        rankings = sorted(self.results.items(), key=lambda x: -x[1][0]['win'])
        for idx, ranking in enumerate(rankings):
            print '%s: %s' % (idx + 1, ranking[0].__name__)
            print '   with wins against %s' % ranking[1][1]
