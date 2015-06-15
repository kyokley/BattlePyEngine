from tournament import Tournament
from players.random_player import RandomPlayer

def main():
    tournament = Tournament(RandomPlayer(), RandomPlayer(), 100)
    tournament.start()
    tournament.printStats()

if __name__ == '__main__':
    main()
