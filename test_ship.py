# pylint: skip-file
from unittest import TestCase
import ship


class MyTestCase(TestCase):
    def setUp(self):
        self.ship_object = ship.Ship()
        self.battleship = ship.Ship(position=[2, 2])
        self.cruiser = ship.Ship(position=[3, 2], length=4, letter="C")
        self.destroyer = ship.Ship(position=[4, 2], length=3, letter="D")
        self.ships = [self.battleship, self.cruiser, self.destroyer]
        self.shooting_range = {"45": "o", "23": "x", "11": "o"}

    def test_place(self):
        self.assertEqual(self.ship_object.place(ships=None), False)
        self.assertEqual(self.ship_object.place(pos=[12, 12], orient=True, ships=self.ships), False)
        self.assertEqual(self.ship_object.place(pos=[5, 2], orient=True, ships=self.ships), True)

    def test_get_hit(self):
        self.battleship.placed = True
        self.battleship.sunken = False
        self.assertEqual(self.battleship.get_hit([2, 2], self.shooting_range), True)
        self.assertEqual(self.battleship.get_hit([9, 2], self.shooting_range), False)
