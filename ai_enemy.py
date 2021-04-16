"""
file for cpu enemy
"""


battlefield_cpu = [["\n", "  ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                   ["\n", "1 ", "B", "B", "B", "B", "B", " ", " ", " ", " ", " "],
                   ["\n", "2 ", " ", " ", " ", " ", " ", " ", "D", "D", "D", " "],
                   ["\n", "3 ", " ", "C", " ", "S", "S", " ", " ", " ", " ", "S"],
                   ["\n", "4 ", " ", "C", " ", " ", " ", " ", " ", " ", " ", "S"],
                   ["\n", "5 ", " ", "C", " ", " ", "D", " ", "S", "S", " ", " "],
                   ["\n", "6 ", " ", "C", " ", " ", "D", " ", " ", " ", " ", " "],
                   ["\n", "7 ", " ", " ", " ", " ", "D", " ", " ", "D", "D", "D"],
                   ["\n", "8 ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
                   ["\n", "9 ", " ", " ", "C", "C", "C", "C", " ", " ", " ", " "],
                   ["\n", "10", " ", " ", " ", " ", " ", " ", " ", "S", "S", " "]]


def get_shot_ai(y_coord, x_coord):
    """
    notices if one of player two's ships got hit
    :param y_coord: y-coordinate that is targeted by enemy
    :param x_coord: x-coordinate that is targeted by enemy
    :return: tells if the shot was a hit or miss
    """
    if battlefield_cpu[y_coord][x_coord] == " ":
        hit_or_not = "o"
        print("Miss!")
    else:
        hit_or_not = "x"
        print("Hit!")
    return hit_or_not
