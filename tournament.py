from game import Game

class Tournament(object):
    def __init__(self, player1, player2, numberOfGames, alternateFirstPlayer=True):
        (self.player1,
         self.player2) = self.players = (player1, player2)
        self.numberOfGames = numberOfGames

        self.player1Wins = 0
        self.player2Wins = 0

        if alternateFirstPlayer:
            self.games = [Game(self.players[i % 2], self.players[(i + 1) % 2]) for i in xrange(self.numberOfGames)]
        else:
            self.games = [Game(*self.players) for i in xrange(self.numberOfGames)]

    @property
    def player1Losses(self):
        return self.player2Wins

    @property
    def player2Losses(self):
        return self.player1Wins

    def start(self):
        for game in self.games:
            winner, loser = game.playGame()

            if winner == self.player1:
                self.player1Wins += 1
            else:
                self.player2Wins += 1
