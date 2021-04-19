"""file for players"""
import ship

class Player:
    """
    parent class for players
    """

    def __init__(self, battlefield):
        self.shooting_range = {}
        self.ships = {"Battleships": [], "Cruisers": [], "Destroyers": [], "Submarines": []}
        self.battlefield = battlefield

    def get_shot(self, coord):
        """
        notices if one of player's ships got hit
        :param y_coord: y-coordinate that is targeted by enemy
        :param x_coord: x-coordinate that is targeted by enemy
        :return: tells if the shot was a hit or miss
        """
        if self.battlefield[coord] is not None:
            shot_statement = "x"
        else:
            shot_statement = "o"
        return shot_statement

    def translate_column(self, column):
        """
        translates letter for columns to numbers
        :param column: the letter to be translated
        :return: translation of the letter
        """
        x_coordinate = 0
        x_coordinate = (ord(column.lower()) - 96) + 1
        if x_coordinate < 2 or x_coordinate > 11:
            print(column + "is not part of the battlefield!")
        return x_coordinate

class Human(Player):
    """class for human player"""
    def __init__(self, enemy):
        super().__init__({})
        self.enemy = enemy

    def shoot(self):
        """
        method to shoot at the enemy's ships
        """
        print("Where do you want to shoot, captain?")
        #print_shooting_range()


    def place_ships(self):
        """
        enables human player to place ships before a game
        """
        self.ships["Battleships"][0] = ship.Battleship()
        self.ships["Battleships"][0].place()
        for i in range(2):
            self.ships["Cruisers"][i] = ship.Cruiser()
            self.ships["Cruisers"][i].place()
        for i in range(3):
            self.ships["Destroyers"][i] = ship.Destroyer()
            self.ships["Destroyers"][i].place()
        for i in range(4):
            self.ships["Submarine"][i] = ship.Submarine()
            self.ships["Submarines"][i].place()

class AI(Player):
    """class for AI player"""
    def shoot(self):
        """
        method to shoot
        """
        pass
        
