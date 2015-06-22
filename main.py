from tournament import Tournament
from players.random_player import RandomPlayer
from players.improved_random_player import ImprovedRandomPlayer
from players.admiral import Admiral

def main():
    tournament = Tournament(Admiral(), ImprovedRandomPlayer(), 1000, debug=False)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
