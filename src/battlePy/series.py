import math

from blessings import Terminal

from battlePy.game import Game


class Series(object):
    def __init__(
        self,
        player1,
        player2,
        numberOfGames,
        alternateFirstPlayer=True,
        debug=False,
        boardWidth=None,
        boardHeight=None,
        showVisualization=False,
        visualizationInterval=0.01,
        clearBoardOnException=False,
        showStatistics=False,
        tournament=None,
    ):
        self.debug = debug
        self.clearBoardOnException = clearBoardOnException
        (self.player1, self.player2) = self.players = (player1, player2)

        if self.player1.name == self.player2.name:
            self.player1Alias = self.player1.name + ' #1'
            self.player2Alias = self.player2.name + ' #2'
        else:
            self.player1Alias = self.player1.name
            self.player2Alias = self.player2.name

        self.numberOfGames = numberOfGames

        self.player1Wins = 0
        self.player2Wins = 0

        self.player1.hOffset = 0
        self.player2.hOffset = 20

        self.showVisualization = showVisualization
        self.visualizationInterval = visualizationInterval
        self.showStatistics = showStatistics

        if alternateFirstPlayer:
            self.games = [
                Game(
                    self.players[i % 2],
                    self.players[(i + 1) % 2],
                    debug=debug,
                    boardWidth=boardWidth,
                    boardHeight=boardHeight,
                    showVisualization=self.showVisualization,
                    visualizationInterval=self.visualizationInterval,
                )
                for i in range(self.numberOfGames)
            ]
        else:
            self.games = [
                Game(
                    *self.players,
                    debug=debug,
                    boardWidth=boardWidth,
                    boardHeight=boardHeight,
                    showVisualization=self.showVisualization,
                    visualizationInterval=self.visualizationInterval
                )
                for i in range(self.numberOfGames)
            ]

        self.player1.currentGame = self.games[0]
        self.player2.currentGame = self.games[0]
        self.player1.totalTurns = 0
        self.player1.averageTurns = 0
        self.player1.minTurns = 0
        self.player1.maxTurns = 0
        self.player2.totalTurns = 0
        self.player2.averageTurns = 0
        self.player2.minTurns = 0
        self.player2.maxTurns = 0

        self.tournament = tournament

        self.term = Terminal()
        if not self.tournament:
            print(self.term.clear)

    @property
    def player1Losses(self):
        return self.player2Wins

    @property
    def player2Losses(self):
        return self.player1Wins

    def start(self):
        for game in self.games:
            winner, loser, turns = game.playGame()

            if winner == self.player1:
                self.player1Wins += 1
                self.player1.totalTurns += math.ceil(turns / 2.0)
                if (
                    math.ceil(turns / 2.0) < self.player1.minTurns
                    or self.player1.minTurns == 0
                ):
                    self.player1.minTurns = math.ceil(turns / 2.0)
                if math.ceil(turns / 2.0) > self.player1.maxTurns:
                    self.player1.maxTurns = math.ceil(turns / 2.0)
                self.player1.averageTurns = self.player1.totalTurns / self.player1Wins

            else:
                self.player2Wins += 1
                self.player2.totalTurns += math.ceil(turns / 2.0)
                if (
                    math.ceil(turns / 2.0) < self.player2.minTurns
                    or self.player2.minTurns == 0
                ):
                    self.player2.minTurns = math.ceil(turns / 2.0)
                if math.ceil(turns / 2.0) > self.player2.maxTurns:
                    self.player2.maxTurns = math.ceil(turns / 2.0)
                self.player2.averageTurns = self.player2.totalTurns / self.player2Wins

            if self.showVisualization:
                self.printStats()
                if game.exception:
                    if self.clearBoardOnException:
                        print(self.term.clear)
                    print('%s threw an exception' % loser.name)
                    print(game.exception)
                    print()
                if game.exception and self.debug:
                    print()
                    print(game.traceback)
                    print()
                    break
            else:
                with self.term.location():
                    self.printStats()
                    if game.exception:
                        print('%s threw an exception' % loser.name)
                        print(game.exception)
                        print()

                if game.exception and self.debug:
                    print()
                    print(game.traceback)
                    print()
                    break

            if (
                self.player1Wins == math.floor(len(self.games) / 2.0) + 1
                or self.player2Wins == math.floor(len(self.games) / 2.0) + 1
            ):
                break
        else:
            if not self.showVisualization:
                # (For some reason I need to print one more time to keep the final results around)
                # May want to come back and clean this up at some point in the future
                self.printStats()

        if self.player1Wins > self.player2Wins:
            return self.player1, self.player2
        elif self.player2Wins > self.player1Wins:
            return self.player2, self.player1
        else:
            return None

    def printStats(self):
        print()
        print()
        print(self.term.bold('Current Matchup:'))
        print('Series games played: %s' % (self.player1Wins + self.player2Wins,))
        print('Player1 (%s) series wins: %s' % (self.player1Alias, self.player1Wins))
        if self.player1._lossesByException:
            print(
                'Player1 (%s) losses by exception: %s'
                % (self.player1Alias, self.player1._lossesByException)
            )
        if self.showStatistics:
            print(
                'Player1 (%s) average turns to win: %.2f'
                % (self.player1Alias, self.player1.averageTurns)
            )
            print(
                'Player1 (%s) minimum turns to win: %s'
                % (self.player1Alias, self.player1.minTurns)
            )
            print(
                'Player1 (%s) maximum turns to win: %s'
                % (self.player1Alias, self.player1.maxTurns)
            )
        print()
        print('Player2 (%s) series wins: %s' % (self.player2Alias, self.player2Wins))
        if self.player2._lossesByException:
            print(
                'Player2 (%s) losses by exception: %s'
                % (self.player2Alias, self.player2._lossesByException)
            )
        if self.showStatistics:
            print(
                'Player2 (%s) average turns to win: %.2f'
                % (self.player2Alias, self.player2.averageTurns)
            )
            print(
                'Player2 (%s) minimum turns to win: %s'
                % (self.player2Alias, self.player2.minTurns)
            )
            print(
                'Player2 (%s) maximum turns to win: %s'
                % (self.player2Alias, self.player2.maxTurns)
            )
        print()
