"""file for players"""
import os
import keyboard
import ship

class Player:
    """
    parent class for players
    """

    def __init__(self, battlefield, player_name = "Unnamed Player", board_size = 10):
        #allow ansi escape codes
        os.system("color")
        self.shooting_range = {}
        self.ships = []
        self.battlefield = battlefield
        self.player_name = player_name
        self.board_size = board_size

    def get_shot(self, coord):
        """
        checks if a certain coordinate is populated and if the hit results in a sink
        :param coord
        @return string contains "hit", "miss", "sink"
        """
        for shipper in self.ships:
            if shipper.get_hit(coord, self.shooting_range):
                #ship has been successfully hit
                if shipper.sunken:
                    #ship has been sunken
                    return "sink"
                else:
                    #return hit
                    return "hit"
        #no hit registered, can assume miss
        return "miss"

    def captive_space(self, message = "- Press [space] To Continue ", hide_name = False):
        """
        holds the player captive until spacebar is pressed
        :param message: string message to be displayed while player is held captive
        :param hide_name: bool if true does not print player name before message
        """
        print(f"{ self.player_name }{ message if not hide_name else '' }")
        keyboard.wait(" ")

    def prepare_ships(self, overlay = None):
        """
        prepares a dictionary of squares which have a ship, as well as an overlay ship
        :param overlay: adds a ship to the print routine, expects array [pos, orient, len, letter, color]
        @return dictionary containing ship letters keyed with their board position
        """
        ship_pos = {}
        for shipper in self.ships:
            if shipper.placed:
                for pos in range(shipper.length):
                    pos_x = str(shipper.position[0] + 1) if shipper.orientation else str(shipper.position[0] + pos + 1)
                    pos_y = str(shipper.position[1] + pos + 1) if shipper.orientation else str(shipper.position[1] + 1)
                    ship_pos[pos_x + pos_y] = shipper.letter

        if not overlay is None:
            for pos in range(overlay[2]):
                pos_x = str(overlay[0][0] + 1) if overlay[1] else str(overlay[0][0] + pos + 1)
                pos_y = str(overlay[0][1] + pos + 1) if overlay[1] else str(overlay[0][1] + 1)
                ship_pos[pos_x + pos_y] = f"\033[0;{ overlay[4] }m{ overlay[3] }\033[0;0m"

        return ship_pos

    def print_battlefield(self, mode = "none", title = None, aside = None, footer = None, overlay = None, cursor = None):
        """
        Prints the player's own ships on the battlefield
        :param mode: print mode ("none", "ship", "markers")
        :param title: string, text to be printed above the board
        :param aside: array of strings to be printed next to the board
        :param footer: string to be printed at the bottom of the board
        :param overlay: adds a ship to the print routine, expects array [pos, orient, len, letter, color]
        """

        #clear console
        os.system('cls' if os.name=='nt' else 'clear')

        #get all ship positions
        if mode == "ship":
            ship_pos = self.prepare_ships(overlay = overlay)

        print(title + "\n" if title is not None else "", end="")

        #iterate through each row
        for numy in range(self.board_size + 1):
            #iterate through each column
            for numx in range(self.board_size + 1):
                if numy == 0:
                    #print top index, avoiding top left blank
                    letter = chr(ord("`") + numx)
                    print("    |" if numx == 0 else f" { letter } |", end="")
                else:
                    #print left hand index
                    if numx == 0:
                        #switch spacing for 2 character numbers
                        print(f" { numy } |" if numy > 9 else f"  { numy } |", end="")
                    else:
                        #print field body
                        if mode == "ship":
                            #print player ships
                            if str(numx) + str(numy) in ship_pos:
                                print(f" { ship_pos[str(numx) + str(numy)] } |", end="")
                            else:
                                print("   |", end="")
                        elif mode == "markers":
                            #print hit/miss markers on board
                            #draw cursor
                            if cursor is not None and numx == cursor[0] + 1 and numy == cursor[1] + 1:
                                if str(numx - 1) + str(numy - 1) in self.shooting_range:
                                    print(f"[{ self.shooting_range[str(numx - 1) + str(numy - 1)] }]|", end="")
                                else:
                                    print("\033[0;32m[-]\033[0;0m|", end="")
                            else:
                                if str(numx - 1) + str(numy - 1) in self.shooting_range:
                                    print(f" { self.shooting_range[str(numx - 1) + str(numy - 1)] } |", end="")
                                else:
                                    print("   |", end="")
                        else:
                            #same as mode none
                            print("   |", end="")
            #print final newlines
            if aside is not None and numy < len(aside):
                print(aside[numy])
            else:
                print("")

        print(footer + "\n" if footer is not None else "", end="")

class Human(Player):
    """class for human player"""
    def __init__(self, target, player_name = "Unnamed Player"):
        super().__init__({}, player_name = player_name)
        self.target = target
        self.targeting = [0, 0]

    def shoot(self):
        """ method to shoot at the enemy's ships """
        #letter = chr(ord("`") + self.targeting[0] + 1)
        #print(f"Shooting square: { letter }{ self.targeting[1] + 1 }")
        value = self.target.get_shot(self.targeting)
        if value == "hit":
            self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;31mx\033[0;0m"
        elif value == "sink":
            self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;31mx\033[0;0m"
        elif value == "miss":
            self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;36mo\033[0;0m"

    def complete_shoot(self, key = None):
        """
        callback for input capture from get_shoot()
        :param key: string containing pressed key
        """

        if key == " ":
            #fire shot at square
            self.shoot()
        else:
            #increment cursor
            key_map = {"w" : [0, -1], "a" : [-1, 0], "s" : [0, 1], "d" : [1, 0]}
            if key in key_map:
                pos_mod = key_map[key]
                self.targeting[0] += pos_mod[0]
                self.targeting[1] += pos_mod[1]
                self.targeting[0] = 0 if self.targeting[0] < 0 else self.targeting[0]
                self.targeting[1] = 0 if self.targeting[1] < 0 else self.targeting[1]
                self.targeting[0] = self.board_size - 1 if self.targeting[0] > self.board_size - 1 else self.targeting[0]
                self.targeting[1] = self.board_size - 1 if self.targeting[1] > self.board_size - 1 else self.targeting[1]

            #print battlefield with markers and cursor
            title = f"\033[1;37m{ self.player_name } - Shoot Square\033[0;0m"
            helptext = [
                "",
                "",
                "          Shooting Cursor Control:",
                "",
                "             W       -   move cursor up",
                "          A  S  D    -   move cursor left / down / right",
                "          [Space]    -   shoot at square",
            ]
            self.print_battlefield(mode = "markers", title = title, aside = helptext, cursor = self.targeting)

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)

    def capture_input_shoot(self):
        """ method which captures inputs for shooting cursor until space is pressed """
        keyboard.on_press_key("w", lambda event: self.complete_shoot("w"))
        keyboard.on_press_key("a", lambda event: self.complete_shoot("a"))
        keyboard.on_press_key("s", lambda event: self.complete_shoot("s"))
        keyboard.on_press_key("d", lambda event: self.complete_shoot("d"))
        keyboard.wait(" ")
        keyboard.unhook_all()
        self.complete_shoot(" ")

    def get_shoot(self):
        """ method to get user requested square to shoot """
        self.complete_shoot()
        self.capture_input_shoot()

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
                self.capture_input_place(shipper)
        elif not shipper.placed:
            #increment position of ship according to keypress
            key_map = {"w" : [0, -1], "a" : [-1, 0], "s" : [0, 1], "d" : [1, 0]}
            pos = shipper.position
            if key in key_map:
                pos_mod = key_map[key]
                pos[0] += pos_mod[0]
                pos[1] += pos_mod[1]
                pos[0] = 0 if pos[0] < 0 else pos[0]
                pos[1] = 0 if pos[1] < 0 else pos[1]
                if shipper.orientation:
                    pos[0] = self.board_size - 1 if pos[0] > self.board_size - 1 else pos[0]
                    pos[1] = self.board_size - shipper.length if pos[1] + shipper.length > self.board_size - 1 else pos[1]
                else:
                    pos[0] = self.board_size - shipper.length if pos[0] + shipper.length > self.board_size - 1 else pos[0]
                    pos[1] = self.board_size - 1 if pos[1] > self.board_size - 1 else pos[1]


            if key == "r":
                shipper.orientation = not shipper.orientation

            #check if ship collides with others on board and set color
            valid = shipper.place(ships = self.ships, test = True)
            color = "37" if valid else "31"

            #print board with title, ship overlay, and help text
            title = f"\033[1;37m{ self.player_name } - Place Ships\033[0;0m"
            overlay = [pos, shipper.orientation, shipper.length, shipper.letter, color]
            helptext = [
                "",
                "",
                "          Ship Placement Control:",
                "",
                "             W   R   -   move ship up / rotate ship",
                "          A  S  D    -   move ship left / down / right",
                "          [Space]    -   place ship (red ship is not placeable)",
            ]
            self.print_battlefield(mode = "ship", title = title, aside = helptext, overlay = overlay)

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)
        return True

    def capture_input_place(self, shipper):
        """
        method which captures inputs for ship placement until space is pressed
        :param shipper: ship object passed through to draw_place_ships method
        """
        keyboard.on_press_key("w", lambda event: self.draw_place_ships("w", shipper))
        keyboard.on_press_key("a", lambda event: self.draw_place_ships("a", shipper))
        keyboard.on_press_key("s", lambda event: self.draw_place_ships("s", shipper))
        keyboard.on_press_key("d", lambda event: self.draw_place_ships("d", shipper))
        keyboard.on_press_key("r", lambda event: self.draw_place_ships("r", shipper))
        keyboard.wait(" ")
        keyboard.unhook_all()
        self.draw_place_ships(" ", shipper)

    def place_ships(self, battleships = 1, cruisers = 2, destroyers = 3, submarines = 4):
        """
        enables human player to place ships before a game
        :param battleships: number of battleships to be created
        :param cruisers: number of cruisers to be created
        :param destroyers: number of destroyers to be created
        :param submarines: number of submarines to be created
        """
        #initialize ship objects and ship array
        count = 0
        self.ships = [""] * (battleships + cruisers + destroyers + submarines)
        for _ in range(battleships):
            self.ships[count] = ship.Ship(length = 5, letter = "B")
            count = count + 1

        for _ in range(cruisers):
            self.ships[count] = ship.Ship(length = 4, letter = "C")
            count = count + 1

        for _ in range(destroyers):
            self.ships[count] = ship.Ship(length = 3, letter = "D")
            count = count + 1

        for _ in range(submarines):
            self.ships[count] = ship.Ship(length = 2, letter="S")
            count = count + 1

        for _, shipper in enumerate(self.ships):
            self.draw_place_ships(shipper = shipper)
            self.capture_input_place(shipper)

class AI(Player):
    """class for AI player"""
    def shoot(self):
        """
        method to shoot
        """

if __name__ == "__main__":
    testtarget = Human("", player_name = "Cannon Fodder")
    testplayer = Human("", player_name = "Player One")
    testplayer.target = testtarget
    #testplayer.ships["Battleships"] = [ship.Battleship()]
    #testplayer.ships["Battleships"][0].place([5,4], True, ships=testplayer.ships)
    testtarget.place_ships()

    while True:
        try:
            testplayer.get_shoot()
            testplayer.print_battlefield(mode = "markers")
            testplayer.captive_space()
        except KeyboardInterrupt:
            quit()
