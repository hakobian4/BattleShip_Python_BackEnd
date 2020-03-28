from player import Player
import numpy as np

class Game():
    def __init__(self):
        self.player1 = None
        self.player2 = None

    def registration(self, name1 = "Player1", name2 = "Player2"):
        self.player1 = Player(name1)
        self.player2 = Player(name2)
    
    def starting(self):
        player_list = [self.player1.name, self.player2.name]
        return np.random.choice(player_list)

