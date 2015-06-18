from tournament import Tournament
from players.random_player import RandomPlayer
from players.improved_random_player import ImprovedRandomPlayer

def main():
    tournament = Tournament(ImprovedRandomPlayer(), ImprovedRandomPlayer(), 100)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
