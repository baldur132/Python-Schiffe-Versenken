""" Primary Game class, ties together the other classes """
#import ship

class Game:
    """ Game class, creates a battleship instance """
    def __init__(self, num):
        """
        Game constructor
        :param num: number of players
        """
        self.players_num = num
