""" Primary Game class, ties together the other classes """
import os
import pickle
import keyboard
import player

def captive_space(message = " Press [space] To Continue ", clear_console = False):
    """
    holds the player captive until spacebar is pressed
    :param message: string message to be displayed while player is held captive
    :param hide_name: bool if true does not print player name before message
    """
    if clear_console:
        player.clear_console()

    print(message)
    keyboard.wait(" ")
    keyboard.press(0x0E)

#Pylint Comment: Too many local attributes (14/7)
#Explanation: the 8 image assets are stored as attributes of the Game class,
#    as this, in my opinion, is the easiest way to store them in a way which allows
#    for dynamic and usable access to the different images. The other two (reasonable)
#    options are to either store them as global variables or in the respective method
#    they are called in, but ultimately I feel as though both of these options are 
#    unneccessary work asking for confusion (as well as file specific globals). Considering
#    the fact that some image assets are used in multiple methods and that the image assets
#    can be externally changed as attributes (allowing game customization), I believe that 
#    it is justified to leave the image assets as attributes of the Game class.
class Game:
    """ Game class, creates a battleship instance """
    def __init__(self):
        """
        Game constructor
        :param num: number of players
        """
        #allow ansi escape codes
        os.system("color" if os.name == "nt" else "")
        self.players = []
        self.selection_pointer = 0
        self.selection_callbacks = []
        self.setup = True           #tracks current game phase
        self.current_player = 0     #tracks current active player
        self.saved = False          #ensures that save cannot be executed multiple times

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
        self.end = [
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

    def draw_selection(self, key = None, box_options = None, card = None, hint = None):
        """
        prints the given box with the current selection underlined
        :param key: string containing pressed movement key
        :param box_options: array containing the box options to be printed
        :param card: string containing the card to be printed, expects "title", "end", "pause"
        :param hint: string to be printed at the bottom of the menu, as a hint
        @return bool true if box fill is successful
        """
        if box_options is None:
            return False

        #clear console
        player.clear_console()

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
                #increment internal pointer
                self.selection_pointer = self.selection_pointer + 1 if key == "d" else self.selection_pointer - 1
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
                    options_string = (" " * (extra // 2)) + options_string + (" " * ((extra // 2 + 1) if extra % 2 else (extra // 2)))
                    #add stoppers
                    options_string = "/" + options_string + "/"

            #print centered
            width = os.get_terminal_size().columns

            #print card
            if card:
                for line in getattr(self, card, self.title):
                    print(line.center(width))

            #print selection box
            print(self.select_box_head.center(width))
            print((" " * (width // 2 - (len(options_string) - 24) // 2 + (2 if width % 2 else 1))) + options_string)
            print(self.select_box_foot.center(width))

            if hint:
                print(hint.center(width))

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)
        return True

    def capture_input_select(self, box, card):
        """
        responsible for menu input captures
        :param box: specifies the box options to be passed to callback
        """
        key_a = keyboard.on_press_key("a", lambda e : self.draw_selection("a", box, card))
        key_d = keyboard.on_press_key("d", lambda e : self.draw_selection("d", box, card))
        keyboard.wait(" ")
        keyboard.unhook_key(key_a)
        keyboard.unhook_key(key_d)
        self.draw_selection(key = " ", box_options = box)

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
            hint = None

            if key == "1":
                self.selection_pointer = 0
            elif key == "2":
                self.selection_pointer = 1
                hint = "Save game to file and exit"
            elif key == "3":
                self.selection_pointer = 2
                hint = "Stop game and exit - will NOT save game"

            self.draw_selection(box_options = ["[1]Resume", "[2]Save and Exit", "[3]Abandon Game"], card = "pause", hint = hint)
            keyboard.send(0x0E)

        return False


    def select_option(self):
        """ selects option based off of internal selection values """
        if self.selection_callbacks[self.selection_pointer] is not False:
            self.selection_callbacks[self.selection_pointer]()

    def display_pause(self):
        """ dispay pause menu, to allow for saving and exiting game """
        self.selection_pointer = 0
        hint = "Select option with [1] [2] [3], confirm with [space]"
        self.draw_selection(box_options = ["[1]Resume", "[2]Save and Exit", "[3]Abandon Game"], card = "pause", hint = hint)

    def display_gameoptions(self):
        """ prints selectable game options """
        self.selection_pointer = 0
        self.selection_callbacks = [self.start_singleplayer, self.start_multiplayer, self.display_titlecard]
        options = ["Singleplayer", "1v1 Multiplayer", "Back"]
        self.draw_selection(box_options = options, card = "title")
        self.capture_input_select(box = options, card = "title")

    def display_titlecard(self):
        """ responsible for printing title card and start options"""
        self.selection_callbacks = [self.display_gameoptions, self.resume_game, quit]
        options = ["Start New Game", "Resume Game", "Quit"]
        hint = "Use [a] and [d] to move left and right, [space] to select"
        self.draw_selection(box_options = options, card = "title", hint = hint)
        self.capture_input_select(box = options, card = "title")

    def display_endcard(self):
        """ responsible for printing end card and end options """
        self.selection_callbacks = [self.display_gameoptions, quit]
        self.draw_selection(box_options = ["Start New Game", "Quit"], card = "end")
        self.capture_input_select(["Start New Game", "Quit"], card = "end")


    def save_game(self):
        """
        Saves the game state in a json encoded file
        @return bool true if file was successfully written
        """
        if not self.saved:
            #try to open file and savewrite = True
            write = True
            if os.path.isfile("save_file.pickle"):
                #ask to overwrite file
                width = os.get_terminal_size().columns
                val = ""
                while val.lower() not in ("y", "yes", "n", "no"):
                    player.clear_console()
                    print("\033[1;37mFile Already Exists, Overwrite Current Save File?\033[0;0m ".center(width))
                    val = input(" " * (width // 2 - (33 if width % 2 else 32)) + "[y/n] >> ")

                write = bool(val.lower() in ("y", "yes"))

            if write:
                try:
                    file = open("save_file.pickle", "wb")
                    pickle.dump(self, file, pickle.HIGHEST_PROTOCOL)
                    file.close()

                    player.clear_console()
                    print("Game has been successfully saved.")

                except (IOError, OSError):
                    print("Game has failed to save")
                    return False

            return True

        return False

    def load_game(self):
        """
        Loads the game saved state into memory
        @return bool true if load was successful
        """
        if os.path.isfile("save_file.pickle"):
            try:
                file = open("save_file.pickle", "rb")
                data = pickle.load(file)
                self.players = data.players
                self.setup = data.setup
                self.current_player = data.current_player
                file.close()
                return True

            except (IOError, OSError):
                #file could not be accessed/read
                return False

        #save file does not exist
        return False


    def interpret_shot(self, value, user):
        """
        displays message according to value
        :param value: string expecting miss|hit|sunk|lost
        """
        width = os.get_terminal_size().columns
        #clear console
        player.clear_console()

        if not value == "lost" and user.human:
            if value == "hit":
                #print hit message
                for line in self.hit:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has hit a ship! - Press [space] To Continue".center(width))
                captive_space(message = "")
            elif value == "sink":
                #print sunk message
                for line in self.sink:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has sunk a ship! - Press [space] To Continue".center(width))
                captive_space(message = "")
            elif value == "miss":
                #print miss message
                for line in self.miss:
                    print(line.center(width))
                print()
                print(f"{ user.player_name } has missed - Press [space] To Continue".center(width))
                captive_space(message = "")
        elif value == "lost":
            #end game
            print("")
            print(self.select_box_head.center(width))
            print(f"{ user.player_name } is the Winner!".center(width))
            print(self.select_box_foot.center(width))

            captive_space("Press [space] to finish".center(width))
            self.display_endcard()

    def run_game(self, skip_setup = False):
        """ primary game loops """
        #pregame setup
        if not skip_setup:
            for num, user in enumerate(self.players):
                self.current_player = num
                user.place_ships(battleships = 1, cruisers = 0, destroyers = 1, submarines = 0)

                if user.save_exit:
                    self.save_game()
                    self.saved = True
                    play = False
                    return False

        #run game
        self.setup = False
        play = True
        while play:
            for num, user in enumerate(self.players):
                if user.save_exit:
                    self.save_game()
                    self.saved = True
                    play = False
                    break

                self.current_player = num

                value = user.shoot()
                self.interpret_shot(value, user)
                if value == "lost":
                    play = False
                    break

        return True

    def prepare_game(self, player_count = 1, board_size = 10):
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

            #run game
            self.run_game()
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

            #run game
            self.run_game()

    def resume_game(self):
        """ Attempts to start a game saved in a file """
        if self.load_game():
            width = os.get_terminal_size().columns
            print("Game has successfully been loaded...".center(width))

            #set up pause
            self.capture_pause()

            #reset save state
            for user in self.players:
                user.save_exit = False

            #finish pregame setup if applicable
            if self.setup:
                for num in range(self.current_player, len(self.players), 1):
                    self.players[num].place_ships(battleships = 1, cruisers = 0, destroyers = 1, submarines = 0)

                #run game normally
                self.run_game(skip_setup = True)
            else:
                # run game starting with last player
                if self.current_player != 0:
                    for num in range(self.current_player, len(self.players)):
                        self.current_player = num

                        if self.players[num].save_exit:
                            self.save_game()
                            self.saved = True
                            break

                        value = self.players[num].shoot()
                        self.interpret_shot(value, self.players[num])
                        if value == "lost":
                            break

                #continue game normally
                self.run_game(skip_setup = True)

    def start_singleplayer(self):
        """ Starts Singleplayer game against computer """
        self.prepare_game()

    def start_multiplayer(self):
        """ Starts 1v1 multiplayer game """
        self.prepare_game(player_count = 2)

    def start(self):
        """ Alias for display_titlecard, starts game menu """
        self.display_titlecard()
