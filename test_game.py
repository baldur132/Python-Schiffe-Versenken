# pylint: skip-file
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
import os
import game
import player


class MyTestCase(TestCase):
    def setUp(self):
        self.game_object = game.Game()
        self.player_object = player.Human()
        self.options = ["Start New Game", "Resume Game", "Quit"]
        self.maxDiff = None

    def test_captive_space(self):
        expected_out = """ Press [space] To Continue 
"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            game.captive_space()
            self.assertEqual(fake_out.getvalue(), expected_out)
        with patch('sys.stdout', new=StringIO()) as fake_out_two:
            game.captive_space(clear_console=True)
            self.assertEqual(fake_out_two.getvalue(), expected_out)

    def test_build_options(self):
        padding = 6
        return_state = '   \x1b[1;37m\x1b[4;37mStart New Game\x1b[0;0m\x1b[0;0m    |    Resume Game    |    Quit   '
        return_state_two = '    [1;37m[4;37mStart New Game[0;0m[0;0m    |    Resume Game    |    Quit     '
        self.assertEqual(self.game_object.build_options(padding, self.options), return_state)
        self.assertEqual(self.game_object.build_options(7, self.options), return_state_two)

    def test_draw_selection(self):
        self.assertEqual(self.game_object.draw_selection(box_options=None), False)
        self.game_object.selection_callbacks = [self.game_object.display_pause]
        self.game_object.selection_pointer = 0
        self.assertEqual(self.game_object.draw_selection(key=" ", box_options=self.options), True)
        self.assertEqual(self.game_object.draw_selection(key="a", box_options=self.options), True)

    def test_capture_pause(self):
        expected_out = ""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.capture_pause(key=None)
            self.assertEqual(fake_out.getvalue(), expected_out)
        self.game_object.capture_pause(key="1")
        self.assertEqual(self.game_object.selection_pointer, 0)
        self.game_object.capture_pause(key="2")
        self.assertEqual(self.game_object.selection_pointer, 1)
        self.game_object.capture_pause(key="3")
        self.assertEqual(self.game_object.selection_pointer, 2)

    def test_save_game(self):
        self.game_object.saved = False
        self.assertEqual(self.game_object.save_game(), True)

    def test_load_game(self):
        self.assertEqual(self.game_object.load_game(), True)

    def test_display_titlecard(self):
        title = [
            r"     .─────────────────────────────────────────────────── ",
            r"    /     ____        __  __  __    _____ __    _         ",
            r"   /     / __ )____ _/ /_/ /_/ /__ / ___// /_  (_)___     ",
            r"  /     / __  / __ `/ __/ __/ / _ \\__ \/ __ \/ / __ \    ",
            r"       / /_/ / /_/ / /_/ /_/ /  __/__/ / / / / / /_/ /   /",
            r"      /_____/\__,_/\__/\__/_/\___/____/_/ /_/_/ .___/   / ",
            r"                                             /_/       /  ",
            r"   ───────────────────────────────────────────────────'   ",
        ]
        selection = [
            r" .──────────────────────────────────────────────────────",
            r"/   Start New Game    |    Resume Game    |    [1;37m[4;37mQuit[0;0m[0;0m    /",
            r"──────────────────────────────────────────────────────' ",
            r"Use [a] and [d] to move left and right, [space] to select",
        ]
        width = os.get_terminal_size().columns
        expected_out = ""
        for line in title:
            expected_out = expected_out + line.center(width) + "\n"
        for num, line in enumerate(selection):
            if num == 1:
                pad = " " * (width // 2 - (len(line) - 24) // 2 + (2 if width % 2 else 1))
                expected_out = expected_out + pad + line + "\n"
            else:
                expected_out = expected_out + line.center(width) + "\n"

        self.game_object.selection_pointer = 2

        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                self.game_object.display_titlecard()
            except SystemExit:
                pass
            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_display_endcard(self):
        endcard = [
            r"     .────────────────────────────────────────────────────── ",
            r"    /   ______                        ____                   ",
            r"   /   / ____/___ _____ ___  ___     / __ \_   _____  _____  ",
            r"  /   / / __/ __ `/ __ `__ \/ _ \   / / / / | / / _ \/ ___/  ",
            r"     / /_/ / /_/ / / / / / /  __/  / /_/ /| |/ /  __/ /     /",
            r"     \____/\__,_/_/ /_/ /_/\___/   \____/ |___/\___/_/     / ",
            r"                                                          /  ",
            r"   ──────────────────────────────────────────────────────'   ",
        ]
        selection = [
            r" .──────────────────────────────────────────────────────",
            r"/        Start New Game         |         [1;37m[4;37mQuit[0;0m[0;0m         /",
            r"──────────────────────────────────────────────────────' ",
        ]
        width = os.get_terminal_size().columns
        expected_out = ""
        for line in endcard:
            expected_out = expected_out + line.center(width) + "\n"
        for num, line in enumerate(selection):
            if num == 1:
                pad = " " * (width // 2 - (len(line) - 24) // 2 + (2 if width % 2 else 1))
                expected_out = expected_out + pad + line + "\n"
            else:
                expected_out = expected_out + line.center(width) + "\n"

        self.game_object.selection_pointer = 1

        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                self.game_object.display_endcard()
            except SystemExit:
                pass
            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_display_pause(self):
        pause = [
            r"     .───────────────────────────────────── ",
            r"    /   ____                            __  ",
            r"   /   / __ \____ ___  __________  ____/ /  ",
            r"  /   / /_/ / __ `/ / / / ___/ _ \/ __  /   ",
            r"     / ____/ /_/ / /_/ (__  )  __/ /_/ /   /",
            r"    /_/    \__,_/\__,_/____/\___/\__,_/   / ",
            r"                                         /  ",
            r"   ─────────────────────────────────────'   ",
        ]
        selection = [
            r" .──────────────────────────────────────────────────────",
            r"/  [1;37m[4;37m[1]Resume[0;0m[0;0m  |  [2]Save and Exit  |  [3]Abandon Game  /",
            r"──────────────────────────────────────────────────────' ",
            r"Select option with [1] [2] [3], confirm with [space]",
        ]
        width = os.get_terminal_size().columns
        expected_out = ""
        for line in pause:
            expected_out = expected_out + line.center(width) + "\n"
        for num, line in enumerate(selection):
            if num == 1:
                pad = " " * (width // 2 - (len(line) - 24) // 2 + (2 if width % 2 else 1))
                expected_out = expected_out + pad + line + "\n"
            else:
                expected_out = expected_out + line.center(width) + "\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.display_pause()
            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_interpret_shot(self):
        hit = [
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
        subtitle = "Unnamed Player has hit a ship! - Press [space] To Continue"
        
        width = os.get_terminal_size().columns
        expected_out = ""
        for line in hit:
            expected_out = expected_out + line.center(width) + "\n"
        expected_out += "\n" + subtitle.center(width) + "\n\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.interpret_shot("hit", self.player_object)
            self.assertEqual(fake_out.getvalue(), expected_out)

        sink = [
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
        subtitle = "Unnamed Player has sunk a ship! - Press [space] To Continue"

        expected_out = ""
        for line in sink:
            expected_out = expected_out + line.center(width) + "\n"
        expected_out += "\n" + subtitle.center(width) + "\n\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.interpret_shot("sink", self.player_object)
            self.assertEqual(fake_out.getvalue(), expected_out)

        miss = [
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
        subtitle = "Unnamed Player has missed - Press [space] To Continue"

        expected_out = ""
        for line in miss:
            expected_out = expected_out + line.center(width) + "\n"
        expected_out += "\n" + subtitle.center(width) + "\n\n"

        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.interpret_shot("miss", self.player_object)
            self.assertEqual(fake_out.getvalue(), expected_out)
