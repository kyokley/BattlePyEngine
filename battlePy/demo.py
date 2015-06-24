from battlePy.tournament import Tournament
from battlePy.players.random_player import RandomPlayer

def play():
    tournament = Tournament(RandomPlayer(), RandomPlayer(), 100)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    play()
