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

    def print_battlefield(self, mode = "ship"):
        """
        Prints the player's own ships on the battlefield
        :param mode: print mode ("none", "ship", "markers")

        """
        board_size = 10

        #get all ship positions
        if mode == "ship":
            ships = self.ships["Battleships"] + self.ships["Cruisers"] + self.ships["Destroyers"] + self.ships["Submarines"]
            ship_pos = {}
            for shipper in ships:
                if shipper.placed:
                    for pos in range(shipper.length):
                        pos_x = str(shipper.position[0]) if shipper.orientation else str(shipper.position[0] + pos)
                        pos_y = str(shipper.position[1] + pos) if shipper.orientation else str(shipper.position[1])
                        ship_pos[pos_x + pos_y] = shipper.letter

        #iterate through each row
        for numy in range(board_size + 1):
            #iterate through each column
            for numx in range(board_size + 1):
                if numy == 0:
                    #print top index, avoiding top left blank
                    if numx == 0:
                        print("    |", end="")
                    else:
                        letter = chr(ord("`") + numx)
                        print(f" { letter } |", end="")
                else:
                    #print left hand index
                    if numx == 0:
                        #switch spacing for 2 character numbers
                        if numy > 9:
                            print(f" { numy } |", end="")
                        else:
                            print(f"  { numy } |", end="")
                    else:
                        #print field body
                        if mode == "ship":
                            #print player ships
                            if str(numx) + str(numy) in ship_pos:
                                print(f" { ship_pos[str(numx) + str(numy)] } |", end="")
                            else:
                                print("   |", end="")
                        elif mode == "markers":
                            print("   |", end="")
                        else:
                            #same as mode none
                            print("   |", end="")
            #print final newline
            print("")

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

if __name__ == "__main__":
    testplayer = Player("")
    testplayer.ships["Battleships"] = [ship.Battleship()]
    testplayer.ships["Battleships"][0].place([5,4], True, ships=testplayer.ships)

    testplayer.print_battlefield("ship")
