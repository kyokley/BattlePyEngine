from ship import Ship

def getDefaultShips():
    return [Ship('Carrier', 5),
            Ship('Battleship', 4),
            Ship('Destroyer', 3),
            Ship('Submarine', 3),
            Ship('Patrol Boat', 2)
            ]

class Game(object):
    def __init__(self, player1, player2, board=None, ships=None):
        pass
