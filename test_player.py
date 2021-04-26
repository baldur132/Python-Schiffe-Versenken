# pylint: skip-file
from io import StringIO
from unittest import TestCase
from unittest.mock import patch
import player
import ship


class MyTestCase(TestCase):
    def setUp(self):
        self.player_object = player.Player()
        self.human_object = player.Human()
        self.AI_object = player.AI()
        self.battleship = ship.Ship(position=[2, 2])
        self.cruiser = ship.Ship(position=[3, 2], length=4, letter="C")
        self.player_object.ships = [self.battleship, self.cruiser]
        self.shooting_range = {"45": "o", "23": "x", "11": "o"}

    def test_clear_console(self):
        expected_out = ""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            player.clear_console()
            self.assertEqual(fake_out.getvalue(), expected_out)

    def test_set_pause(self):
        self.player_object.set_pause()
        self.assertEqual(self.player_object.pause, True)

    def test_set_pause_mode(self):
        self.player_object.set_pause_mode(2)
        self.assertEqual(self.player_object.pause_mode, 2)

    def test_check_sunken(self):
        self.assertEqual(self.player_object.check_sunken(), False)
        self.battleship.sunken = True
        self.cruiser.sunken = True
        self.assertEqual(self.player_object.check_sunken(), True)

    def test_get_shot(self):
        self.battleship.placed = True
        self.battleship.sunken = False
        self.assertEqual(self.player_object.get_shot([2, 2], self.shooting_range), "hit")
        self.assertEqual(self.player_object.get_shot([9, 2], self.shooting_range), "miss")
        self.battleship.length = 1
        self.assertEqual(self.player_object.get_shot([2, 2], self.shooting_range), "sink")
        self.cruiser.length = 1
        self.cruiser.placed = True
        self.cruiser.sunken = False
        self.assertEqual(self.player_object.get_shot([3, 2], self.shooting_range), "lost")

    def test_prepare_ships(self):
        self.battleship.length = 1
        self.battleship.placed = True
        self.cruiser.length = 1
        self.cruiser.placed = True
        self.assertEqual(self.player_object.prepare_ships(), {'33': 'B', '43': 'C'})

    def test_print_battlefield(self):
        expected_battlefield = """    | a | b | c | d | e | f | g | h | i | j |
  1 |   |   |   |   |   |   |   |   |   |   |
  2 |   |   |   |   |   |   |   |   |   |   |
  3 |   |   |   |   |   |   |   |   |   |   |
  4 |   |   |   |   |   |   |   |   |   |   |
  5 |   |   |   |   |   |   |   |   |   |   |
  6 |   |   |   |   |   |   |   |   |   |   |
  7 |   |   |   |   |   |   |   |   |   |   |
  8 |   |   |   |   |   |   |   |   |   |   |
  9 |   |   |   |   |   |   |   |   |   |   |
 10 |   |   |   |   |   |   |   |   |   |   |
"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.player_object.print_battlefield(mode="none")
            self.assertEqual(fake_out.getvalue(), expected_battlefield)
        self.shooting_range = {}
        with patch('sys.stdout', new=StringIO()) as fake_out_two:
            self.player_object.print_battlefield(mode="markers")
            self.assertEqual(fake_out_two.getvalue(), expected_battlefield)

    def test_human_shoot(self):
        self.assertEqual(self.human_object.shoot(), "miss")

    def test_complete_shoot(self):
        expected_out = ""
        expected_out_two = """[1;37mUnnamed Player - Shoot Square[0;0m
    | a | b | c | d | e | f | g | h | i | j |
  1 |[[0;36mo[0;0m]|   |   |   |   |   |   |   |   |   |
  2 |   |   |   |   |   |   |   |   |   |   |          Shooting Cursor Control:
  3 |   |   |   |   |   |   |   |   |   |   |
  4 |   |   |   |   |   |   |   |   |   |   |             W       -   move cursor up
  5 |   |   |   |   |   |   |   |   |   |   |          A  S  D    -   move cursor left / down / right
  6 |   |   |   |   |   |   |   |   |   |   |          [Space]    -   shoot at square
  7 |   |   |   |   |   |   |   |   |   |   |
  8 |   |   |   |   |   |   |   |   |   |   |
  9 |   |   |   |   |   |   |   |   |   |   |
 10 |   |   |   |   |   |   |   |   |   |   |
"""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.human_object.complete_shoot(key=" ")
            self.assertEqual(fake_out.getvalue(), expected_out)
        with patch('sys.stdout', new=StringIO()) as fake_out_two:
            self.human_object.complete_shoot()
            self.assertEqual(fake_out_two.getvalue(), expected_out_two)
        with patch('sys.stdout', new=StringIO()) as fake_out_three:
            self.human_object.complete_shoot(key="w")
            self.assertEqual(fake_out_three.getvalue(), expected_out_two)

    def test_draw_place_ships(self):
        self.assertEqual(self.human_object.draw_place_ships(), False)
        self.assertEqual(self.human_object.draw_place_ships(key=" ", shipper=self.battleship), True)
        self.ships = None
        self.assertEqual(self.human_object.draw_place_ships(key=" ", shipper=self.battleship), True)
        self.battleship.orientation = True
        self.assertEqual(self.human_object.draw_place_ships(key="w", shipper=self.battleship), True)
        self.battleship.placed = False
        self.assertEqual(self.human_object.draw_place_ships(shipper=self.battleship), True)
        self.assertEqual(self.human_object.draw_place_ships(key="r", shipper=self.battleship), True)
        self.assertEqual(self.human_object.draw_place_ships(key="w", shipper=self.battleship), True)
        self.battleship.orientation = False
        self.assertEqual(self.human_object.draw_place_ships(key="w", shipper=self.battleship), True)

    def test_capture_input_place(self):
        self.human_object.pause = True
        self.human_object.capture_input_place(self.battleship)
        self.assertEqual(self.human_object.pause, False)

    def test_AI_shoot(self):
        self.assertEqual(self.AI_object.shoot(), "miss")
