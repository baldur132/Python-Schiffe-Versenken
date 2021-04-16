"""
functions needed for the game that are not part of a class
"""
from os import system, name


def clear():
    """
    clears command shell/terminal
    """
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


def pause():
    """
    pauses the command shell
    """
    _ = system('pause')


def translate_column(column):
    """
    translates letter for columns to numbers
    :param column: the letter to be translated
    :return: translation of the letter
    """
    x_coordinate = 0
    if column in ("a", "A"):
        x_coordinate = 2
    elif column in ("b", "B"):
        x_coordinate = 3
    elif column in ("c", "C"):
        x_coordinate = 4
    elif column in ("d", "D"):
        x_coordinate = 5
    elif column in ("e", "E"):
        x_coordinate = 6
    elif column in ("f", "F"):
        x_coordinate = 7
    elif column in ("g", "G"):
        x_coordinate = 8
    elif column in ("h", "H"):
        x_coordinate = 9
    elif column in ("i", "I"):
        x_coordinate = 10
    elif column in ("j", "J"):
        x_coordinate = 11
    else:
        print(column + "is not part of the battlefield!")
    return x_coordinate
