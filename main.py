from tournament import Tournament
from random_player import RandomPlayer

def main():
    tournament = Tournament(RandomPlayer(), RandomPlayer(), 100)
    tournament.start()
    tournament.printStats()
