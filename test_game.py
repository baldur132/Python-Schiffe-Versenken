# pylint: disable=c
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
import game
import player


class MyTestCase(TestCase):
    def setUp(self):
        self.game_object = game.Game()
        self.player_object = player.Human()
        self.options = ["Start New Game", "Resume Game", "Quit"]

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

    """def test_interpret_shot(self):
        expected_out =                          _   _   _____   _____            |__                   --_--
                        │ │ │ │ │_   _│ │_   _│           |\/                (  -_    _).
                        │ └ ┘ │  _│ │_    │ │             ---              ( ~       )   )
                        │_│ │_│ │_____│   │_│             / | [          (( )  (    )  ()  )
                                                   !      | |||           (.   )) (       )
                                                 _/|     _/|-++'            ``..     ..``
                                             +  +--|    |--|--|_ |-              | |
                                          { /|__|  |/\__|  |--- |||__/         (=| |=)
                                         +---------------___[}-_===_.'____       | |       /\
                                     ____`-' ||___-{]_| _[}-  |     |_[___\==(../( )\.))   \/   _
                      __..._____--==/___]_|__|_____________________________[___\==--____,------' .7
                     |                                                                     BB-61/
                      \_________________________________________________________________________|

                               Unnamed Player has hit a ship! - Press [space] To Continue


        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.game_object.interpret_shot("hit", self.player_object)
            self.assertEqual(fake_out.getvalue(), expected_out)"""
