"""file for players"""
import time as _time
from threading import Event as _UninterruptableEvent
import os
import sys
import random
import keyboard
import ship

class _Event(_UninterruptableEvent):
    def wait_stutter(self):
        """ method allows for Event to be interrupted, as this is normally not possible """
        while True:
            if _UninterruptableEvent.wait(self, 0.5):
                break

def two_wait(hotkey_a = None, hotkey_b = None, suppress = False, trigger_on_release = False):
    """
    Near identical copy of the wait function present in keyboard,
    but can take two hotkeys, allowing for custom global interrupts
    """
    if hotkey_a and hotkey_b:
        lock = _Event()
        # Pylint warns that the lambda may be unnecessary, but testing other cases shows that the program excepts without lambda
        # test cases included `lambda e: lock.set()` `lock.set()` `lock.set`
        # pylint: disable=unnecessary-lambda
        remove_a = keyboard.add_hotkey(hotkey_a, lambda: lock.set(), suppress = suppress, trigger_on_release = trigger_on_release)
        remove_b = keyboard.add_hotkey(hotkey_b, lambda: lock.set(), suppress = suppress, trigger_on_release = trigger_on_release)
        lock.wait_stutter()
        keyboard.remove_hotkey(remove_a)
        keyboard.remove_hotkey(remove_b)
    else:
        while True:
            _time.sleep(1e6)

def clear_console():
    """
    clears console
    """
    os.system('cls' if os.name=='nt' else 'clear')

class Player:
    """ parent class for players """

    def __init__(self, player_name = "Unnamed Player", board_size = 10):
        #allow ansi escape codes
        os.system("color" if os.name == "nt" else "")
        self.shooting_range = {}
        self.hit_markers = {}
        self.ships = []
        self.player_name = player_name
        self.board_size = board_size
        self.pause_mode = 0
        self.save_exit = False

    def set_pause_mode(self, mode = 1):
        """
        sets the value of pause_mode to value
        """
        self.pause_mode = mode
        keyboard.send(0x0E)

    def captive_pause(self):
        """ holds the player captive in pause menu and allows pause menu functionality """
        #keyboard handling
        key_1 = keyboard.on_press_key("1", lambda e: self.set_pause_mode(1))
        key_2 = keyboard.on_press_key("2", lambda e: self.set_pause_mode(2))
        key_3 = keyboard.on_press_key("3", lambda e: self.set_pause_mode(3))
        keyboard.wait(" ")
        keyboard.unhook_key(key_1)
        keyboard.unhook_key(key_2)
        keyboard.unhook_key(key_3)
        keyboard.send(0x0E)

        if self.pause_mode == 3:
            clear_console()
            sys.exit()
        elif self.pause_mode == 2:
            self.save_exit = True

    def check_sunken(self):
        """
        checks if all ships are sunken
        @return bool if true, all ships are sunken and player has lost
        """
        sunken = 0
        for shipper in self.ships:
            if shipper.sunken:
                sunken = sunken + 1

        if sunken >= len(self.ships):
            #all ships have been sunken
            return True
        return False

    def get_shot(self, coord, markers):
        """
        checks if a certain coordinate is populated and if the hit results in a sink
        :param coord location of hit
        @return string contains "hit", "miss", "sink", "lost"
        """
        for shipper in self.ships:
            if shipper.get_hit(coord, markers):
                #ship has been successfully hit
                if shipper.sunken:
                    #check if all ships have been sunken
                    if self.check_sunken():
                        self.hit_markers[str(coord[0]) + str(coord[1])] = "\033[0;31mx\033[0;0m"
                        return "lost"
                    #ship has been sunken
                    self.hit_markers[str(coord[0]) + str(coord[1])] = "\033[0;31mx\033[0;0m"
                    return "sink"
                #insert hit
                self.hit_markers[str(coord[0]) + str(coord[1])] = "\033[0;31mx\033[0;0m"
                #return hit
                return "hit"
        #no hit registered, can assume miss
        return "miss"

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

    def get_segment(self, nums, mode = "none", ship_pos = None, cursor = None):
        """
        returns a segment of the battlefield based on a given x and y value
        as well as other data. exists to appease the pylint god
        :param nums: array of two integers, position on board
        :param mode: mode of print, see print_battlefield
        :param ship_pos: dict of ship positions, see prepare_ships
        :param cursor: array of two integers, position of cursor on board
        """
        segment = ""
        numx = nums[0]
        numy = nums[1]
        if numy == 0:
            #print top index, avoiding top left blank
            letter = chr(ord("`") + numx)
            segment += "    |" if numx == 0 else f" { letter } |"
            return segment

        #print left hand index
        if numx == 0:
            #switch spacing for 2 character numbers
            segment += f" { numy } |" if numy > 9 else f"  { numy } |"
            return segment

        #print field body
        if mode in ("ship", "composite"):
            #print player ships
            if str(numx - 1) + str(numy - 1) in self.hit_markers and mode == "composite":
                segment += f" { self.hit_markers[str(numx - 1) + str(numy - 1)] } |"
            elif str(numx) + str(numy) in ship_pos:
                segment += f" { ship_pos[str(numx) + str(numy)] } |"
            else:
                segment += "   |"
            return segment

        if mode == "markers":
            #print hit/miss markers on board
            #draw cursor
            if cursor is not None and numx == cursor[0] + 1 and numy == cursor[1] + 1:
                if str(numx - 1) + str(numy - 1) in self.shooting_range:
                    segment += f"[{ self.shooting_range[str(numx - 1) + str(numy - 1)] }]|"
                else:
                    segment += "\033[0;32m[-]\033[0;0m|"
            else:
                if str(numx - 1) + str(numy - 1) in self.shooting_range:
                    segment += f" { self.shooting_range[str(numx - 1) + str(numy - 1)] } |"
                else:
                    segment += "   |"
            return segment

        #same as mode none
        segment += "   |"

        return segment

    def print_battlefield(self, mode = "none", title = None, aside = None, overlay = None, cursor = None):
        """
        Prints the player's own ships on the battlefield
        :param mode: print mode ("none", "ship", "markers", "composite")
            mode "none": prints an empty board of size self.board_size
            mode "ships": prints player's ships on the board
            mode "markers": prints the player's hits and misses on the board
            mode "composite": prints player ships and enemy hits on board
        :param title: string, text to be printed above the board
        :param aside: array of strings to be printed next to the board
        :param footer: string to be printed at the bottom of the board
        :param overlay: adds a ship to the print routine, expects array [pos, orient, len, letter, color]
        """

        #clear console
        clear_console()

        #get all ship positions
        if mode in ("ship", "composite"):
            ship_pos = self.prepare_ships(overlay = overlay)

        print(title + "\n" if title is not None else "", end="")

        #iterate through each row
        for numy in range(self.board_size + 1):
            #iterate through each column
            for numx in range(self.board_size + 1):
                if mode in ("ship", "composite"):
                    line = self.get_segment([numx, numy], mode, ship_pos, cursor)
                else:
                    line = self.get_segment([numx, numy], mode, cursor = cursor)
                print(line, end="")
            #print final newlines
            if aside is not None and numy < len(aside):
                print(aside[numy])
            else:
                print("")

class Human(Player):
    """class for human player"""
    def __init__(self, player_name = "Unnamed Player", board_size = 10):
        super().__init__(player_name = player_name, board_size = board_size)
        self.human = True
        self.target = Player()
        self.targeting = [0, 0]
        self.last_hit = ""

    def shoot(self, empty_call = True):
        """
        method to shoot at the enemy's ships
        @return string value of hit
        """
        if empty_call:
            #allows easy usage of player.shoot() method
            self.last_hit = ""
            self.complete_shoot()
            self.capture_input_shoot()
            value = self.last_hit
        else:
            value = self.target.get_shot(self.targeting, self.shooting_range)
            if value == "miss":
                self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;36mo\033[0;0m"
            elif value in ("hit", "sink", "lost"):
                self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;31mx\033[0;0m"

            self.last_hit = value
        return value

    def complete_shoot(self, key = None):
        """
        callback for input capture from input capture of shoot
        :param key: string containing pressed key
        """

        if key == " ":
            #fire shot at square
            self.last_hit = self.shoot(empty_call = False)
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
            if key == "q":
                title = f"\033[1;37m{ self.player_name } - Ship View\033[0;0m"
                helptext = [
                    "",
                    "",
                    "      Player Ship View:",
                    "",
                    "         W       -   return to Shooting Input",
                ]
                self.print_battlefield(mode = "composite", title = title, aside = helptext)
            else:
                title = f"\033[1;37m{ self.player_name } - Shoot Square\033[0;0m"
                helptext = [
                    "",
                    "",
                    "      Shooting Cursor Control:",
                    "",
                    "      Q  W     P -   show ship view / cursor up / pause",
                    "      A  S  D    -   move cursor left / down / right",
                    "      [Space]    -   shoot at square",
                ]
                self.print_battlefield(mode = "markers", title = title, aside = helptext, cursor = self.targeting)

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)

    def capture_input_shoot(self):
        """ method which captures inputs for shooting cursor until space is pressed """
        if not self.save_exit:
            key_w = keyboard.on_press_key("w", lambda e: self.complete_shoot("w"))
            key_a = keyboard.on_press_key("a", lambda e: self.complete_shoot("a"))
            key_s = keyboard.on_press_key("s", lambda e: self.complete_shoot("s"))
            key_d = keyboard.on_press_key("d", lambda e: self.complete_shoot("d"))
            key_q = keyboard.on_press_key("q", lambda e: self.complete_shoot("q"))
            key_p = keyboard.on_press_key("p", self.set_pause_mode)
            two_wait(" ", "p")
            keyboard.unhook_key(key_w)
            keyboard.unhook_key(key_a)
            keyboard.unhook_key(key_s)
            keyboard.unhook_key(key_d)
            keyboard.unhook_key(key_q)
            keyboard.unhook_key(key_p)

            if self.pause_mode:
                self.captive_pause()
                self.set_pause_mode(0)
                if not self.save_exit:
                    self.complete_shoot()
                    self.capture_input_shoot()
                else:
                    self.target.save_exit = True
            else:
                self.complete_shoot(" ")

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
            verify = shipper.place(ships = self.ships, board_size = self.board_size)
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
                "      Ship Placement Control:",
                "",
                "         W  R  P -   move ship up / rotate ship / pause",
                "      A  S  D    -   move ship left / down / right",
                "      [Space]    -   place ship (red ship is not placeable)",
            ]
            self.print_battlefield(mode = "ship", title = title, aside = helptext, overlay = overlay)

        return True

    def capture_input_place(self, shipper):
        """
        method which captures inputs for ship placement until space is pressed
        :param shipper: ship object passed through to draw_place_ships method
        """
        if not self.save_exit:
            key_w = keyboard.on_press_key("w", lambda e: self.draw_place_ships("w", shipper))
            key_a = keyboard.on_press_key("a", lambda e: self.draw_place_ships("a", shipper))
            key_s = keyboard.on_press_key("s", lambda e: self.draw_place_ships("s", shipper))
            key_d = keyboard.on_press_key("d", lambda e: self.draw_place_ships("d", shipper))
            key_r = keyboard.on_press_key("r", lambda e: self.draw_place_ships("r", shipper))
            key_p = keyboard.on_press_key("p", self.set_pause_mode)
            two_wait(" ", "p")
            keyboard.unhook_key(key_w)
            keyboard.unhook_key(key_a)
            keyboard.unhook_key(key_s)
            keyboard.unhook_key(key_d)
            keyboard.unhook_key(key_r)
            keyboard.unhook_key(key_p)
            keyboard.send(0x0E)

            if self.pause_mode:
                self.captive_pause()
                self.set_pause_mode(0)
                if not self.save_exit:
                    self.draw_place_ships(shipper = shipper)
                    self.capture_input_place(shipper)
                else:
                    self.target.save_exit = True
            else:
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

            if self.save_exit:
                break

class AI(Player):
    """class for AI player"""
    def __init__(self, player_name = "Unnamed Computer", board_size = 10):
        super().__init__(player_name = player_name, board_size = board_size)
        self.human = False
        self.target = Player()
        self.targeting = [0, 0]
        self.save_exit = False

    def shoot(self):
        """
        method to shoot, randomly chooses squares to shoot
        @return string value of hit
        """
        #randomize shooting location
        while str(self.targeting[0]) + str(self.targeting[1]) in self.shooting_range:
            self.targeting = [random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)]

        value = self.target.get_shot(self.targeting, self.shooting_range)
        if value == "miss":
            self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;36mo\033[0;0m"
        elif value in ("hit", "sink", "lost"):
            self.shooting_range[str(self.targeting[0]) + str(self.targeting[1])] = "\033[0;31mx\033[0;0m"

        return value

    def place_ships(self, battleships = 1, cruisers = 2, destroyers = 3, submarines = 4):
        """
        method places ships randomly, following placement rules
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
            value = False
            while not value:
                pos = [random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)]
                orient = bool(random.getrandbits(1))
                value = shipper.place(pos = pos, orient = orient, ships = self.ships, board_size = self.board_size)


