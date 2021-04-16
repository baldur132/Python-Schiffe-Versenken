"""
file for the game class
"""
import global_funcs as func


class Game:
    """
    contains complete game engine except for shooting
    """
    player_number = 0

    battleship_one = {"name": "battleship", "length": 5, "amount": 1}
    cruiser_one = {"name": "cruiser", "length": 4, "amount": 2}
    destroyer_one = {"name": "destroyer", "length": 3, "amount": 3}
    submarine_one = {"name": "submarine", "length": 2, "amount": 4}

    battleship_two = {"name": "battleship", "length": 5, "amount": 1}
    cruiser_two = {"name": "cruiser", "length": 4, "amount": 2}
    destroyer_two = {"name": "destroyer", "length": 3, "amount": 3}
    submarine_two = {"name": "submarine", "length": 2, "amount": 4}

    def __init__(self, index):
        """
        constructor for class 'Game'
        :param index: tells who's 'logged in'
        """
        self.player_number = index

    battlefield_one = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                       ["\n", "1 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "2 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "3 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "4 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "5 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "6 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "7 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "8 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "9 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "10", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    battlefield_two = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                       ["\n", "1 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "2 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "3 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "4 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "5 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "6 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "7 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "8 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "9 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                       ["\n", "10", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]]

    def print_battlefield(self):
        """
        prints battlefield of player 1 or 2 depending on who is 'logged in'
        """
        if self.player_number == 1:
            for i in range(len(self.battlefield_one)):

                for j in range(len(self.battlefield_one[i])):
                    print(self.battlefield_one[i][j], end='|')

            print('\n')
        elif self.player_number == 2:
            for i in range(len(self.battlefield_two)):

                for j in range(len(self.battlefield_two[i])):
                    print(self.battlefield_two[i][j], end='|')

            print('\n')

    def print_ships(self):
        """
        prints ships with their amount and length
        """
        if self.player_number == 1:
            print(self.battleship_one)
            print(self.cruiser_one)
            print(self.destroyer_one)
            print(self.submarine_one)
        elif self.player_number == 2:
            print(self.battleship_two)
            print(self.cruiser_two)
            print(self.destroyer_two)
            print(self.submarine_two)

    def place_battleship(self, y_coord, x_coord_letter, direct, battlefield):
        """
        places battleship on the battlefield given
        :param y_coord: y-coordinate of the ship
        :param x_coord_letter: x-coordinate of the ship
        :param direct: direction of the ship (vertical or horizontal)
        :param battlefield: battlefield on which the ship is placed
        """
        x_coord = func.translate_column(x_coord_letter)
        if direct in ("1", "(1)", "vertical") and 1 < x_coord < 12 and 0 < y_coord < 7:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord+1][x_coord] == " "
               and battlefield[y_coord+2][x_coord] == " " and battlefield[y_coord+3][x_coord] == " "
               and battlefield[y_coord+4][x_coord] == " "):
                battlefield[y_coord][x_coord] = "B"
                battlefield[y_coord+1][x_coord] = "B"
                battlefield[y_coord+2][x_coord] = "B"
                battlefield[y_coord+3][x_coord] = "B"
                battlefield[y_coord+4][x_coord] = "B"
                if self.player_number == 1:
                    self.battleship_one["amount"] -= 1
                elif self.player_number == 2:
                    self.battleship_two["amount"] -= 1
            else:
                print("Column not available!")
        elif direct in ("2", "(2)", "horizontal") and 1 < x_coord < 8 and 0 < y_coord < 11:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord][x_coord+1] == " "
               and battlefield[y_coord][x_coord+2] == " " and battlefield[y_coord][x_coord+3] == " "
               and battlefield[y_coord][x_coord+4] == " "):
                battlefield[y_coord][x_coord] = "B"
                battlefield[y_coord][x_coord+1] = "B"
                battlefield[y_coord][x_coord+2] = "B"
                battlefield[y_coord][x_coord+3] = "B"
                battlefield[y_coord][x_coord+4] = "B"
                if self.player_number == 1:
                    self.battleship_one["amount"] -= 1
                elif self.player_number == 2:
                    self.battleship_two["amount"] -= 1
            else:
                print("Row not available!")

    def place_cruiser(self, y_coord, x_coord_letter, direct, battlefield):
        """
        places cruiser on the battlefield given
        :param y_coord: y-coordinate of the ship
        :param x_coord_letter: x-coordinate of the ship
        :param direct: direction of the ship (vertical or horizontal)
        :param battlefield: battlefield on which the ship is placed
        """
        x_coord = func.translate_column(x_coord_letter)
        if direct in ("1", "(1)", "vertical") and 1 < x_coord < 12 and 0 < y_coord < 8:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord+1][x_coord] == " "
               and battlefield[y_coord+2][x_coord] == " "
               and battlefield[y_coord+3][x_coord] == " "):
                battlefield[y_coord][x_coord] = "C"
                battlefield[y_coord+1][x_coord] = "C"
                battlefield[y_coord+2][x_coord] = "C"
                battlefield[y_coord+3][x_coord] = "C"
                if self.player_number == 1:
                    self.cruiser_one["amount"] -= 1
                elif self.player_number == 2:
                    self.cruiser_two["amount"] -= 1
            else:
                print("Column not available!")
        elif direct in ("2", "(2)", "horizontal") and 1 < x_coord < 9 and 0 < y_coord < 11:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord][x_coord+1] == " "
               and battlefield[y_coord][x_coord+2] == " "
               and battlefield[y_coord][x_coord+3] == " "):
                battlefield[y_coord][x_coord] = "C"
                battlefield[y_coord][x_coord+1] = "C"
                battlefield[y_coord][x_coord+2] = "C"
                battlefield[y_coord][x_coord+3] = "C"
                if self.player_number == 1:
                    self.cruiser_one["amount"] -= 1
                elif self.player_number == 2:
                    self.cruiser_two["amount"] -= 1
            else:
                print("Row not available!")

    def place_destroyer(self, y_coord, x_coord_letter, direct, battlefield):
        """
        places destroyer on the battlefield given
        :param y_coord: y-coordinate of the ship
        :param x_coord_letter: x-coordinate of the ship
        :param direct: direction of the ship (vertical or horizontal)
        :param battlefield: battlefield on which the ship is placed
        """
        x_coord = func.translate_column(x_coord_letter)
        if direct in ("1", "(1)", "vertical") and 1 < x_coord < 12 and 0 < y_coord < 9:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord+1][x_coord] == " "
               and battlefield[y_coord+2][x_coord] == " "):
                battlefield[y_coord][x_coord] = "D"
                battlefield[y_coord+1][x_coord] = "D"
                battlefield[y_coord+2][x_coord] = "D"
                if self.player_number == 1:
                    self.destroyer_one["amount"] -= 1
                elif self.player_number == 2:
                    self.destroyer_two["amount"] -= 1
            else:
                print("Column not available!")
        elif direct in ("2", "(2)", "horizontal") and 1 < x_coord < 10 and 0 < y_coord < 11:
            if(battlefield[y_coord][x_coord] == " " and battlefield[y_coord][x_coord+1] == " "
               and battlefield[y_coord][x_coord+2] == " "):
                battlefield[y_coord][x_coord] = "D"
                battlefield[y_coord][x_coord+1] = "D"
                battlefield[y_coord][x_coord+2] = "D"
                if self.player_number == 1:
                    self.destroyer_one["amount"] -= 1
                elif self.player_number == 2:
                    self.destroyer_two["amount"] -= 1
            else:
                print("Row not available!")

    def place_submarine(self, y_coord, x_coord_letter, direct, battlefield):
        """
        places submarine on the battlefield given
        :param y_coord: y-coordinate of the ship
        :param x_coord_letter: x-coordinate of the ship
        :param direct: direction of the ship (vertical or horizontal)
        :param battlefield: battlefield on which the ship is placed
        """
        x_coord = func.translate_column(x_coord_letter)
        if direct in ("1", "(1)", "vertical") and 1 < x_coord < 12 and 0 < y_coord < 10:
            if battlefield[y_coord][x_coord] == " " and battlefield[y_coord+1][x_coord] == " ":
                battlefield[y_coord][x_coord] = "S"
                battlefield[y_coord+1][x_coord] = "S"
                if self.player_number == 1:
                    self.submarine_one["amount"] -= 1
                elif self.player_number == 2:
                    self.submarine_two["amount"] -= 1
            else:
                print("Column not available!")
        elif direct in ("2", "(2)", "horizontal") and 1 < x_coord < 11 and 0 < y_coord < 11:
            if battlefield[y_coord][x_coord] == " " and battlefield[y_coord][x_coord+1] == " ":
                battlefield[y_coord][x_coord] = "S"
                battlefield[y_coord][x_coord+1] = "S"
                if self.player_number == 1:
                    self.submarine_one["amount"] -= 1
                elif self.player_number == 2:
                    self.submarine_two["amount"] -= 1
            else:
                print("Row not available!")

    def place_ships_one(self):
        """
        enables player 1 to place ships before a game
        """
        while (self.battleship_one["amount"] != 0 or self.cruiser_one["amount"] != 0
                or self.destroyer_one["amount"] != 0 or self.submarine_one["amount"] != 0):
            self.print_ships()
            self.print_battlefield()
            ship = input("Which ship would you like to place: ")
            try:
                y_coord = int(input("In which row: "))
                x_coord = input("In which column: ")
                direction = input("(1)vertical or (2)horizontal: ")
                if ship in ("Battleship", "battleship") and self.battleship_one["amount"] > 0:
                    self.place_battleship(y_coord, x_coord, direction, self.battlefield_one)
                elif ship in ("Cruiser", "cruiser") and self.cruiser_one["amount"] > 0:
                    self.place_cruiser(y_coord, x_coord, direction, self.battlefield_one)
                elif ship in ("Destroyer", "destroyer") and self.destroyer_one["amount"] > 0:
                    self.place_destroyer(y_coord, x_coord, direction, self.battlefield_one)
                elif ship in ("Submarine", "submarine") and self.submarine_one["amount"] > 0:
                    self.place_submarine(y_coord, x_coord, direction, self.battlefield_one)
                else:
                    print("Ship not available!")
                    func.pause()
            except ValueError:
                print("Invalid number!")
                func.pause()
            func.clear()

    def place_ships_two(self):
        """
        enables player 2 to place ships before a game
        """
        while (self.battleship_two["amount"] != 0 or self.cruiser_two["amount"] != 0
                or self.destroyer_two["amount"] != 0 or self.submarine_two["amount"] != 0):
            self.print_ships()
            self.print_battlefield()
            ship = input("Which ship would you like to place: ")
            try:
                y_coord = int(input("In which row: "))
                x_coord = input("In which column: ")
                direction = input("(1)vertical or (2)horizontal: ")
                if ship in ("Battleship", "battleship") and self.battleship_two["amount"] > 0:
                    self.place_battleship(y_coord, x_coord, direction, self.battlefield_two)
                elif ship in ("Cruiser", "cruiser") and self.cruiser_two["amount"] > 0:
                    self.place_cruiser(y_coord, x_coord, direction, self.battlefield_two)
                elif ship in ("Destroyer", "destroyer") and self.destroyer_two["amount"] > 0:
                    self.place_destroyer(y_coord, x_coord, direction, self.battlefield_two)
                elif ship in ("Submarine", "submarine") and self.submarine_two["amount"] > 0:
                    self.place_submarine(y_coord, x_coord, direction, self.battlefield_two)
                else:
                    print("Ship not available!")
                    func.pause()
            except ValueError:
                print("Invalid number!")
                func.pause()
            func.clear()

    def get_shot_one(self, y_coord, x_coord):
        """
        notices if one of player one's ships got hit
        :param y_coord: y-coordinate that is targeted by enemy
        :param x_coord: x-coordinate that is targeted by enemy
        :return: tells if the shot was a hit or miss
        """
        if self.battlefield_one[y_coord][x_coord] == " ":
            hit_or_not = "o"
            print("Miss!")
        else:
            hit_or_not = "x"
            print("Hit!")
        return hit_or_not

    def get_shot_two(self, y_coord, x_coord):
        """
        notices if one of player two's ships got hit
        :param y_coord: y-coordinate that is targeted by enemy
        :param x_coord: x-coordinate that is targeted by enemy
        :return: tells if the shot was a hit or miss
        """
        if self.battlefield_two[y_coord][x_coord] == " ":
            hit_or_not = "o"
            print("Miss!")
        else:
            hit_or_not = "x"
            print("Hit!")
        return hit_or_not
