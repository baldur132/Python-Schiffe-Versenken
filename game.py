""" Primary Game class, ties together the other classes """
import os
#import sys
import keyboard
#import ship
import player

class Game:
    """ Game class, creates a battleship instance """
    def __init__(self):
        """
        Game constructor
        :param num: number of players
        """
        #allow ansi escape codes
        os.system("color")
        self.players = []
        self.selection_pointer = 0
        self.selection_callbacks = []
        self.paused = False

        #image assets
        self.title = [
            r"     .─────────────────────────────────────────────────── ",
            r"    /     ____        __  __  __    _____ __    _         ",
            r"   /     / __ )____ _/ /_/ /_/ /__ / ___// /_  (_)___     ",
            r"  /     / __  / __ `/ __/ __/ / _ \\__ \/ __ \/ / __ \    ",
            r"       / /_/ / /_/ / /_/ /_/ /  __/__/ / / / / / /_/ /   /",
            r"      /_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/   / ",
            r"                                             /_/       /  ",
            r"   ───────────────────────────────────────────────────'   ",
        ]
        self.endcard = [
            r"     .────────────────────────────────────────────────────── ",
            r"    /   ______                        ____                   ",
            r"   /   / ____/___ _____ ___  ___     / __ \_   _____  _____  ",
            r"  /   / / __/ __ `/ __ `__ \/ _ \   / / / / | / / _ \/ ___/  ",
            r"     / /_/ / /_/ / / / / / /  __/  / /_/ /| |/ /  __/ /     /",
            r"     \____/\__,_/_/ /_/ /_/\___/   \____/ |___/\___/_/     / ",
            r"                                                          /  ",
            r"   ──────────────────────────────────────────────────────'   ",
        ]
        self.pause = [
            r"     .───────────────────────────────────── ",
            r"    /   ____                            __  ",
            r"   /   / __ \____ ___  __________  ____/ /  ",
            r"  /   / /_/ / __ `/ / / / ___/ _ \/ __  /   ",
            r"     / ____/ /_/ / /_/ (__  )  __/ /_/ /   /",
            r"    /_/    \__,_/\__,_/____/\___/\__,_/   / ",
            r"                                         /  ",
            r"   ─────────────────────────────────────'   ",
        ]
        self.hit = [
            r"    _   _   _____   _____            |__                   --_--              ",
            r"   │ │ │ │ │_   _│ │_   _│           |\/                (  -_    _).          ",
            r"   │ └ ┘ │  _│ │_    │ │             ---              ( ~       )   )         ",
            r"   │_│ │_│ │_____│   │_│             / | [          (( )  (    )  ()  )       ",
            r"                              !      | |||           (.   )) (       )        ",
            r"                            _/|     _/|-++'            ``..     ..``          ",
            r"                        +  +--|    |--|--|_ |-              | |               ",
            r"                     { /|__|  |/\__|  |--- |||__/         (=| |=)             ",
            r"                    +---------------___[}-_===_.'____       | |       /\      ",
            r"                ____`-' ||___-{]_| _[}-  |     |_[___\==(../( )\.))   \/   _  ",
            r" __..._____--==/___]_|__|_____________________________[___\==--____,------' .7",
            r"|                                                                     BB-61/  ",
            r" \_________________________________________________________________________|  "
        ]
        self.sink = [
            r"    ____   _____   _    _   _  __                                             ",
            r"   /  __/ │_   _│ │  \ │ │ │ │/ /                                             ",
            r"   \_ \     │ │   │   \│ │ │   /                                              ",
            r"   \____/ │_____│ │_|\___│ │_│\_\        (  .      )                          ",
            r"                                    (    .   )    )                           ",
            r"                               .  '   .   '  .  '  .                          ",
            r"       .      '            (    , )       (.   )  (   ',   ')                 ",
            r"       )  . (`     '`  .' )    ( . )    ,  ( ,     )   ( .         .      '   ",
            r"      ((  (  ;)    '  )''  ). ,( .   (  ) ( , ')  .' (  ,    )    )  . (`     ",
            r"  _' )_') (. _..( '. (_,) . ), ) _) _,')  (, ) '. )  ,. (' )  _.. ((  (  ;)   ",
            r" __..._____--==/___]_|__|_____________________________[___\==--____,------' .7",
            r"|                                                                     BB-61/  ",
            r" \_________________________________________________________________________|  "
        ]
        self.miss = [
            r"    _   _   _____   ____   ____      |__                                      ",
            r"   │ \ / │ │_   _│ /  __/ /  __/     |\/                                      ",
            r"   │  ^  │   │ │   \_ \   \_ \       ---                                      ",
            r"   │_│ │_│ │_____│ \____/ \____/     / | [                                    ",
            r"                                     | |||                                    ",
            r"                            _/|     _/|-++'                                   ",
            r"                        +  +--|    |--|--|_ |-                                ",
            r"                     { /|__|  |/\__|  |--- |||__/                             ",
            r"                    +---------------___[}-_===_.'____                 /\      ",
            r"                ____`-' ||___-{]_| _[}-  |     |_[___\==--            \/   _  ",
            r" __..._____--==/___]_|__|_____________________________[___\==--____,------' .7",
            r"|                                                                     BB-61/  ",
            r" \_________________________________________________________________________|  "
        ]
        self.select_box_head = r" .──────────────────────────────────────────────────────"
        self.select_box_foot = r"──────────────────────────────────────────────────────' "

    def build_options(self, padding, options):
        """
        builds string out of given options and padding parameters
        :param padding: int number of spaces per item to pad with
        :param options: array of strings containing the options
        @return string with distributed padding
        """
        item_num = len(options)
        options_string = ""
        if not padding % 2:
            # distribute to each string
            pad = " " * (padding // 2)
            #pad individual strings
            for num, option in enumerate(options):
                if num == self.selection_pointer:
                    options_string += pad + "\033[1;37m\033[4;37m" + option + "\033[0;0m\033[0;0m" + pad + " | "
                else:
                    options_string += pad + option + pad + " | "
            #cut off last separator
            options_string = options_string[:-3]
        else:
            # portion is odd. subtract one from each portion and use to pad
            unused = item_num
            pad = " " * ((padding - 1) // 2)
            #pad inividual options
            for num, option in enumerate(options):
                if num == self.selection_pointer:
                    options_string += pad + "\033[1;37m\033[4;37m" + option + "\033[0;0m\033[0;0m" + pad + " | "
                else:
                    options_string += pad + option + pad + " | "
            #cut off last separator
            options_string = options_string[:-3]
            #pad ends of options string
            options_string = (" " * (unused // 2)) + options_string + (" " * ((unused // 2 + 1) if unused % 2 else (unused // 2)))

        return options_string

    def draw_selection(self, key = None, box_options = None, title = False, endcard = False, pause = False):
        """
        prints the given box with the current selection underlined
        :param key: string containing pressed movement key
        :param box_options: array containing the box options to be printed
        @return bool true if box fill is successful
        """
        if box_options is None:
            return False

        #clear console
        os.system('cls' if os.name=='nt' else 'clear')

        if key == " ":
            #confirm selection
            self.select_option()
        else:
            # calculate formatting
            max_fillable = 54
            item_count = len(box_options)
            tot_internal_len = (item_count - 1) * 3
            for string in box_options:
                tot_internal_len += len(string)
            #sanity check
            if tot_internal_len > max_fillable:
                #box options are too big for selection box
                return False

            #set incrementation direction
            if key in ("a", "d"):
                direction = not key == "a"
                direction = (key == "d")
                #increment internal pointer
                self.selection_pointer = self.selection_pointer + 1 if direction else self.selection_pointer - 1
            #bound selection pointer between 0 and options
            self.selection_pointer = 0 if self.selection_pointer < 0 else self.selection_pointer
            self.selection_pointer = item_count - 1 if self.selection_pointer > item_count - 1 else self.selection_pointer

            #calculate and apply margins
            extra = max_fillable - tot_internal_len
            options_string = r""
            if not extra % item_count:
                #distribute equally if each string gets an even number of spaces
                options_string = self.build_options(extra // item_count, box_options)
                #add stoppers
                options_string = "/" + options_string + "/"
            else:
                if extra > item_count:
                    #distribute extra values normally, then pad edges with rest
                    distributable = extra - extra % item_count
                    excess = extra - distributable
                    options_string = self.build_options(distributable // item_count, box_options)
                    #add excess
                    options_string = (" " * (excess // 2)) + options_string + (" " * ((excess // 2 + 1) if excess % 2 else (excess // 2)))
                    #add stoppers
                    options_string = "/" + options_string + "/"
                else:
                    #not enough to distribute, pad edges
                    options_string = (" " * (extra // 2)) + options_string + (" " * ((extra // 2 + 1) if extra % 2 else (excess // 2)))
                    #add stoppers
                    options_string = "/" + options_string + "/"

            #print centered
            width = os.get_terminal_size().columns

            #print title
            if title:
                for line in self.title:
                    print(line.center(width))
            #print endcard
            if endcard:
                for line in self.endcard:
                    print(line.center(width))
            #print pause screen
            if pause:
                for line in self.pause:
                    print(line.center(width))

            #print selection box
            print(self.select_box_head.center(width))
            print((" " * (width // 2 - (len(options_string) - 24) // 2 + (2 if width % 2 else 1))) + options_string)
            print(self.select_box_foot.center(width))

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)
        return True

    def capture_input_select(self, box, title = False, endcard = False, pause = False):
        """
        responsible for menu input captures
        :param box: specifies the box options to be passed to callback
        """
        key_a = keyboard.on_press_key("a", lambda e : self.draw_selection("a", box, title, endcard, pause))
        key_d = keyboard.on_press_key("d", lambda e : self.draw_selection("d", box, title, endcard, pause))
        keyboard.wait(" ")
        keyboard.unhook_key(key_a)
        keyboard.unhook_key(key_d)
        self.draw_selection(key = " ", box_options = box)

    def captive_space(self, message = " Press [space] To Continue ", clear_console = False):
        """
        holds the player captive until spacebar is pressed
        :param message: string message to be displayed while player is held captive
        :param hide_name: bool if true does not print player name before message
        """
        if clear_console:
            os.system('cls' if os.name=='nt' else 'clear')

        print(message)
        keyboard.wait(" ")
        keyboard.press(0x0E)

    def capture_pause(self, key = None):
        """ sets up hotkeys to capture key events even during keyboard.wait() """
        if key is None:
            #set up hotkeys
            keyboard.add_hotkey("1", self.capture_pause, args = ["1"])
            keyboard.add_hotkey("2", self.capture_pause, args = ["2"])
            keyboard.add_hotkey("3", self.capture_pause, args = ["3"])
            keyboard.add_hotkey("p", self.display_pause)
        else:
            #run event
            if self.paused:
                if key == "1":
                    self.selection_pointer = 0
                elif key == "2":
                    self.selection_pointer = 1
                elif key == "3":
                    self.selection_pointer = 2

                self.draw_selection(box_options = ["[1]Resume", "[2]Save and Exit", "[3]Abandon Game"], pause = True)

        return False


    def select_option(self):
        """ selects option based off of internal selection values """
        if self.selection_callbacks[self.selection_pointer] is not False:
            self.selection_callbacks[self.selection_pointer]()

    def display_pause(self):
        """ dispay pause menu, to allow for saving and exiting game """
        if not self.paused:
            self.paused = True
            self.draw_selection(box_options = ["[1]Resume", "[2]Save and Exit", "[3]Abandon Game"], pause = True)
        else:
            self.paused = False

        keyboard.press(0x0E)

    def display_gameoptions(self):
        """ prints selectable game options """
        self.selection_pointer = 0
        self.selection_callbacks = [self.start_singleplayer, self.start_multiplayer, self.display_titlecard]
        self.draw_selection(box_options = ["Singleplayer", "1v1 Multiplayer", "Back"], title = True)
        self.capture_input_select(box = ["Singleplayer", "1v1 Multiplayer", "Back"], title = True)

    def display_titlecard(self):
        """ responsible for printing title card and start options"""
        self.selection_callbacks = [self.display_gameoptions, "", quit]
        self.draw_selection(box_options = ["Start New Game", "Resume Game", "Quit"], title = True)
        self.capture_input_select(box = ["Start New Game", "Resume Game", "Quit"], title = True)

    def display_endcard(self):
        """ responsible for printing end card and end options """
        self.selection_callbacks = [self.display_gameoptions, quit]
        self.draw_selection(box_options = ["Start New Game", "Quit"], endcard = True)
        self.capture_input_select(["Start New Game", "Quit"], endcard = True)


    def interpret_shot(self, value, user):
        """
        displays message according to value
        :param value: string expecting miss|hit|sunk|lost
        """
        width = os.get_terminal_size().columns
        #clear console
        os.system('cls' if os.name=='nt' else 'clear')

        if not value == "lost" and user.human:
            if value == "hit":
                #print hit message
                for line in self.hit:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has hit a ship! - Press [space] To Continue".center(width))
                self.captive_space(message = "")
            elif value == "sink":
                #print sunk message
                for line in self.sink:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has sunk a ship! - Press [space] To Continue".center(width))
                self.captive_space(message = "")
            elif value == "miss":
                #print miss message
                for line in self.miss:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has missed - Press [space] To Continue".center(width))
                self.captive_space(message = "")
        elif value == "lost":
            #end game
            self.captive_space(f"{ user.player_name } has won")
            self.display_endcard()

    def run_game(self, player_count = 1, board_size = 10):
        """
        starts battleship game
        :param player_count: int number of players
        :param board_size: int size of board (side length)
        """
        #set up pause
        self.capture_pause()

        if player_count == 1:
            # singleplayer game
            #initialize players
            plyrs = [
                player.Human(player_name = "Human Player", board_size = board_size),
                player.AI(player_name = "Computer Player", board_size = board_size)
            ]
            self.players = plyrs
            #set targets
            self.players[0].target = self.players[1]
            self.players[1].target = self.players[0]

            #pregame setup
            for user in self.players:
                user.place_ships(battleships = 1, cruisers = 0, destroyers = 1, submarines = 0)

            #run game
            play = True
            while play:
                for user in self.players:
                    value = user.shoot()
                    self.interpret_shot(value, user)
                    if value == "lost":
                        break
        else:
            # multiplayer game
            #initialize players
            plyrs = [""] * player_count
            for num in range(player_count):
                plyrs[num] = player.Human(player_name = f"Player { num + 1 }", board_size = board_size)
            self.players = plyrs

            #set targets
            for num, user in enumerate(self.players):
                if num + 1 == len(self.players):
                    user.target = self.players[0]
                else:
                    user.target = self.players[num + 1]

            #pregame setup
            for user in self.players:
                user.place_ships(battleships = 1, cruisers = 0, destroyers = 1, submarines = 0)

            #run game
            play = True
            while play:
                for user in self.players:
                    value = user.shoot()
                    self.interpret_shot(value, user)
                    if value == "lost":
                        break

    def start_singleplayer(self):
        """ Starts Singleplayer game against computer """
        self.run_game()

    def start_multiplayer(self):
        """ Starts 1v1 multiplayer game """
        self.run_game(player_count = 2)

    def start(self):
        """ Alias for display_titlecard, starts game menu """
        self.display_titlecard()

if __name__ == "__main__":
    newgame = Game()
    #newgame.draw_selection(box_options = ["Ente", "quack"])
    #newgame.start_game()
    newgame.display_titlecard()
