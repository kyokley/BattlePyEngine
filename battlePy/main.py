from battlePy.tournament import Tournament
from battlePy.players.random_player import RandomPlayer
from battlePy.players.improved_random_player import ImprovedRandomPlayer
from battlePy.custom.admiral import Admiral

def main():
    tournament = Tournament(Admiral(), ImprovedRandomPlayer(), 100)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
