""" Primary Game class, ties together the other classes """
import os
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

    def draw_selection(self, key = None, box_options = None, title = False):
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
            pass
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

            #print selection box
            print(self.select_box_head.center(width))
            print((" " * (width // 2 - (len(options_string) - 24) // 2 + 1)) + options_string)
            print(self.select_box_foot.center(width))

        #send backspace to prevent command line getting filled
        keyboard.send(0x0E)
        return True

    def capture_input_select(self, box, title):
        """
        responsible for menu input captures
        :param box: specifies the box options to be passed to callback
        """
        keyboard.on_press_key("a", lambda e : self.draw_selection(key = "a", box_options = box, title = title))
        keyboard.on_press_key("d", lambda e : self.draw_selection(key = "d", box_options = box, title = title))
        keyboard.wait(" ")
        keyboard.unhook_all()
        self.draw_selection(key = " ", box_options = box)

    def display_titlecard(self):
        """ responsible for printing title card """
        self.draw_selection(box_options = ["Start New Game", "Resume Game", "Quit"], title = True)
        self.capture_input_select(box = ["Start New Game", "Resume Game", "Quit"], title = True)

    def start_game(self, player_count = 1, board_size = 10):
        """
        starts battleship game
        :param player_count: int number of players
        :param board_size: int size of board (side length)
        """
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
                user.place_ships(battleships = 0, cruisers = 0, destroyers = 1, submarines = 0)

            #run game
            play = True
            while play:
                for user in self.players:
                    value = user.shoot()
                    if value == "lost":
                        #game has hit end condition
                        winner = user
                        play = False
                        break
                    if user.human:
                        if value == "miss":
                            #print miss screen
                            print("miss")
                            user.captive_space()
                        elif value == "hit":
                            #print hit screen
                            print("hit")
                            user.captive_space()
                        elif value == "sunk":
                            #print sunk screen
                            print("sunk")
                            user.captive_space()

            #finish game
            print(f"game has ended, { winner.player_name } has won")

if __name__ == "__main__":
    newgame = Game()
    #newgame.draw_selection(box_options = ["Ente", "quack", "quark"])
    newgame.start_game()
    #newgame.display_titlecard()
