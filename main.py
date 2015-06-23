from tournament import Tournament
from players.random_player import RandomPlayer
from players.improved_random_player import ImprovedRandomPlayer
from custom.admiral import Admiral

def main():
    tournament = Tournament(Admiral(), ImprovedRandomPlayer(), 100)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
