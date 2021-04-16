"""
contains class 'Shooting'
"""
from random import randint
import game_class as game
import global_funcs as func
import ai_enemy as ai


class Shooting:
    """
    provides all functions to shoot at the enemy's' battlefield
    """
    game_friend = game.Game(0)
    player_number = 0
    shooting_range_one = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
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

    shooting_range_two = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
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

    shooting_range = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
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

    def __init__(self, ongoing_game, index):
        """
        constructor for class 'Shooting'
        :param ongoing_game: object of class 'Game' from module game_class.py
        :param index: says which player is about to shoot
        """
        self.game_friend = ongoing_game
        self.player_number = index

    def print_shooting_range(self):
        """
        prints the shooting range depending on which players' turn it is
        """
        if self.player_number == 1:
            for i in range(len(self.shooting_range_one)):
                for j in range(len(self.shooting_range_one[i])):
                    print(self.shooting_range_one[i][j], end='|')

            print('\n')
        elif self.player_number == 2:
            for i in range(len(self.shooting_range_two)):
                for j in range(len(self.shooting_range_two[i])):
                    print(self.shooting_range_two[i][j], end='|')

            print('\n')
        elif self.player_number == 3:
            for i in range(len(self.shooting_range)):
                for j in range(len(self.shooting_range[i])):
                    print(self.shooting_range[i][j], end='|')

            print('\n')

    def shoot(self):
        """
        function to shoot at the enemy's ships
        """
        print("Where do you want to shoot, captain?")
        try:
            y_coord = int(input("Row: "))
            x_coord_letter = input("Column: ")
            x_coord = func.translate_column(x_coord_letter)
            if 0 < y_coord < 11 and 1 < x_coord < 12:
                if self.player_number == 1:
                    self.print_shooting_range()
                    if self.shooting_range_one[y_coord][x_coord] == " ":
                        func.clear()
                        self.shooting_range_one[y_coord][x_coord] = \
                            self.game_friend.get_shot_two(y_coord, x_coord)
                        self.print_shooting_range()
                        func.pause()
                        func.clear()
                elif self.player_number == 2:
                    self.print_shooting_range()
                    if self.shooting_range_two[y_coord][x_coord] == " ":
                        func.clear()
                        self.shooting_range_two[y_coord][x_coord] = \
                            self.game_friend.get_shot_one(y_coord, x_coord)
                        self.print_shooting_range()
                        func.pause()
                        func.clear()
        except ValueError:
            print("Not a number!")

    def shooting_ai(self):
        """
        function for automated shots by ai
        """
        stop_loop = 1
        while stop_loop == 1:
            x_coord = randint(2, 11)
            y_coord = randint(1, 10)
            if self.shooting_range[y_coord][x_coord] == " ":
                self.shooting_range[y_coord][x_coord] = \
                    self.game_friend.get_shot_one(y_coord, x_coord)
                self.print_shooting_range()
                func.pause()
                func.clear()
                stop_loop = 0
            else:
                stop_loop = 1

    def shoot_at_ai(self):
        """
        function to shoot at ai's ships
        """
        self.print_shooting_range()
        print("Where do you want to shoot, captain?")
        try:
            y_coord = int(input("Row: "))
            x_coord_letter = input("Column: ")
            x_coord = func.translate_column(x_coord_letter)
            if 0 < y_coord < 11 and 1 < x_coord < 12:
                self.print_shooting_range()
                if self.shooting_range_one[y_coord][x_coord] == " ":
                    func.clear()
                    self.shooting_range_one[y_coord][x_coord] = \
                        ai.get_shot_ai(y_coord, x_coord)
                    self.print_shooting_range()
                    func.pause()
                    func.clear()
        except ValueError:
            print("Not a number!")

    def game_winner(self):
        """
        notices when someone has destroyed every ship
        :return: signal to end the game
        """
        counter_one = 0
        counter_two = 0
        counter_three = 0
        stop_game = 0
        for i in range(len(self.shooting_range_one)):
            for j in range(len(self.shooting_range_one[i])):
                if self.shooting_range_one[i][j] == "x":
                    counter_one += 1
        for i in range(len(self.shooting_range_two)):
            for j in range(len(self.shooting_range_two[i])):
                if self.shooting_range_two[i][j] == "x":
                    counter_two += 1
        for i in range(len(self.shooting_range)):
            for j in range(len(self.shooting_range[i])):
                if self.shooting_range[i][j] == "x":
                    counter_three += 1
        if counter_one == 30:
            print("Player 1 wins!")
            func.pause()
            stop_game = 1
        elif counter_two == 30:
            print("Player 2 wins!")
            func.pause()
            stop_game = 2
        elif counter_three == 30:
            print("CPU wins!")
            func.pause()
            stop_game = 3
        return stop_game
