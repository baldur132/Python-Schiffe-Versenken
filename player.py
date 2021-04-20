"""file for players"""
import os
import keyboard
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

    def print_battlefield(self, mode = "none", overlay = None):
        """
        Prints the player's own ships on the battlefield
        :param mode: print mode ("none", "ship", "markers")
        :param overlay: adds a ship to the print routine, expects array [pos, orient, len, letter, color]
        """
        board_size = 10

        #get all ship positions
        if mode == "ship":
            ships = self.ships["Battleships"] + self.ships["Cruisers"] + self.ships["Destroyers"] + self.ships["Submarines"]
            ship_pos = {}
            for shipper in ships:
                if shipper.placed:
                    for pos in range(shipper.length):
                        pos_x = str(shipper.position[0] + 1) if shipper.orientation else str(shipper.position[0] + pos + 1)
                        pos_y = str(shipper.position[1] + pos + 1) if shipper.orientation else str(shipper.position[1] + 1)
                        ship_pos[pos_x + pos_y] = shipper.letter

            if not overlay is None:
                for pos in range(overlay[2]):
                    pos_x = str(overlay[0][0] + 1) if overlay[1] else str(overlay[0][0] + pos + 1)
                    pos_y = str(overlay[0][1] + pos + 1) if overlay[1] else str(overlay[0][1] + 1)
                    ship_pos[pos_x + pos_y] = f"\033[0;{ overlay[4] };40m{ overlay[3] }\033[0;0m"

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
            #print final newlines
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

    def draw_place_ships(self, key = None, shipper = None):
        """
        callback for input capture from place_ships()
        :param key: pressed key, controls which direction the ship moves
        :param ship: ship object to move
        """
        if shipper is None:
            return False

        if key == " ":
            #verify ship place
            verify = shipper.place(ships = self.ships)
            if not verify:
                #retry the placement
                self.capture_input(shipper)
        elif not shipper.placed:
            #increment position of ship according to keypress
            key_map = {"w" : [0, -1], "a" : [-1, 0], "s" : [0, 1], "d" : [1, 0]}
            pos = shipper.position
            if key in key_map:
                pos_mod = key_map[key]
                pos[0] += pos_mod[0]
                pos[1] += pos_mod[1]

            if key == "r":
                shipper.orientation = not shipper.orientation

            #check if ship collides with others on board and set color
            valid = shipper.place(ships = self.ships, test = True)
            color = "37" if valid else "31"

            #clear console
            os.system('cls' if os.name=='nt' else 'clear')
            #print board with ship overlay
            self.print_battlefield(mode = "ship", overlay = [pos, shipper.orientation, shipper.length, shipper.letter, color])

        return True

    def capture_input(self, shipper):
        """
        method which captures inputs until space is pressed
        :param shipper: ship object passed through to draw_place_ships method
        """
        keyboard.on_press_key("w", lambda event: self.draw_place_ships("w", shipper))
        keyboard.on_press_key("a", lambda event: self.draw_place_ships("a", shipper))
        keyboard.on_press_key("s", lambda event: self.draw_place_ships("s", shipper))
        keyboard.on_press_key("d", lambda event: self.draw_place_ships("d", shipper))
        keyboard.on_press_key("r", lambda event: self.draw_place_ships("r", shipper))
        keyboard.wait(" ")
        self.draw_place_ships(" ", shipper)

    def place_ships(self, battleships = 1, cruisers = 2, destroyers = 3, submarines = 4):
        """
        enables human player to place ships before a game
        :param battleships: number of battleships to be created
        :param cruisers: number of cruisers to be created
        :param destroyers: number of destroyers to be created
        :param submarines: number of submarines to be created
        """
        #initialize ship objects and ship dict
        btlshp = [""] * battleships
        for num in range(battleships):
            btlshp[num] = ship.Battleship()
        self.ships["Battleships"] = btlshp

        crsr = [""] * cruisers
        for num in range(cruisers):
            crsr[num] = ship.Cruiser()
        self.ships["Cruisers"] = crsr

        dstr = [""] * destroyers
        for num in range(destroyers):
            dstr[num] = ship.Destroyer()
        self.ships["Destroyers"] = dstr

        subs = [""] * submarines
        for num in range(submarines):
            subs[num] = ship.Submarine()
        self.ships["Submarines"] = subs

        ships_all = btlshp + crsr + dstr + subs

        for num, shipper in enumerate(ships_all):
            self.draw_place_ships(shipper = shipper)
            self.capture_input(shipper)

class AI(Player):
    """class for AI player"""
    def shoot(self):
        """
        method to shoot
        """

if __name__ == "__main__":
    testplayer = Human("")
    #testplayer.ships["Battleships"] = [ship.Battleship()]
    #testplayer.ships["Battleships"][0].place([5,4], True, ships=testplayer.ships)
    testplayer.place_ships()
    testplayer.print_battlefield("ship")
