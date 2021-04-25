# pylint: disabled
from unittest import TestCase
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
    
    def test_human_shoot(self):
        self.assertEqual(self.human_object.shoot(), "miss")

    def test_draw_place_ships(self):
        self.assertEqual(self.human_object.draw_place_ships(), False)
        self.assertEqual(self.human_object.draw_place_ships(key=" ", shipper=self.battleship), True)
        self.battleship.placed = False
        self.assertEqual(self.human_object.draw_place_ships(shipper=self.battleship), True)
        self.assertEqual(self.human_object.draw_place_ships(key="r", shipper=self.battleship), True)
        self.assertEqual(self.human_object.draw_place_ships(key="w", shipper=self.battleship), True)
        self.battleship.orientation = False
        self.assertEqual(self.human_object.draw_place_ships(key="w", shipper=self.battleship), True)

    def test_AI_shoot(self):
        self.assertEqual(self.AI_object.shoot(), "miss")
