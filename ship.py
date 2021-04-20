""" Classes for Battleships """

class Ship:
    """ Parent class for all ships """
    def __init__(self, position = None, orientation = True, length = 5):
        """
        constructor for ships
        :param position: position on board
        :param orientation: direction of ship either vertical(true) or horizontal(false)
        """
        self.position = [0, 0] if position is None else position
        self.orientation = orientation
        self.length = length
        self.sunken = False
        self.placed = False

    def place(self, pos = None, orient = None, ships = None, board_size = 9, test = False):
        """
        places ships on board by setting their internal position values and
        checks placement validity
        :param pos: position to be placed (first square of ship on top or left)
        :param orient: direction of ship either vertical(true) or horizontal(false)
        :param ships: dict of currently existing ships
        """
        pos = self.position if pos is None else pos
        orient = self.orientation if orient is None else orient
        if ships is None:
            return False

        pos_x = pos[0]
        pos_y = pos[1]

        if (not orient and pos_x + self.length > board_size) or (orient and pos_y + self.length > board_size):
            #ship overhangs on board
            return False #f"board overhang as { pos_x + self.length } and  { pos_y + self.length }"

        for i in range(self.length):
            #find next position
            nextpos_x = pos_x if orient else pos_x + i
            nextpos_y = pos_y + i if orient else pos_y

            #loop through all ship objects
            ships_all = ships["Battleships"] + ships["Cruisers"] + ships["Destroyers"] + ships["Submarines"]

            for shipper in ships_all:
                if shipper.placed:
                    #check for collisions with battleships
                    if nextpos_x == shipper.position[0] and nextpos_y == shipper.position[1]:
                        #head collision with battleship
                        #return False
                        return False #f"head collision at { nextpos_x } { nextpos_y }"
                    if orient:
                        #check for body collisions on vertically oriented ship
                        if nextpos_x == shipper.position[0] and nextpos_y < shipper.position[1] + shipper.length:
                            #ship is on top of the body of an already existing ship
                            return False #f"vertical body collision at { nextpos_x } { nextpos_y }"
                    else:
                        #check for body collisions on horizontially oriented ship
                        if nextpos_y == shipper.position[1] and nextpos_x < shipper.position[0] + shipper.length:
                            #ship intersects with with another differently oriented one
                            return False#f"Horizontal body collision at { nextpos_x } { nextpos_y }"

        if not test:
            self.placed = True
            self.position = [pos_x, pos_y]
            self.orientation = orient
        return True

class Battleship(Ship):
    """ Class for Battleship """
    def __init__(self, position = None, orientation = True):
        #self.position = [0, 0] if position is None else position
        super().__init__(position = position, orientation = orientation, length = 5)
        self.placed = False if position is None else True
        self.length = 5
        self.letter = "B"

class Cruiser(Ship):
    """ Class for Cruiser """
    def __init__(self, position = None, orientation = True):
        super().__init__(position = position, orientation = orientation, length = 4)
        self.placed = False if position is None else True
        self.length = 4
        self.letter = "C"

class Destroyer(Ship):
    """ Class for Destroyer """
    def __init__(self, position = None, orientation = True):
        super().__init__(position = position, orientation = orientation, length = 3)
        self.placed = False if position is None else True
        self.length = 3
        self.letter = "D"

class Submarine(Ship):
    """ Class for Submarine """
    def __init__(self, position = None, orientation = True):
        super().__init__(position = position, orientation = orientation, length = 2)
        self.placed = False if position is None else True
        self.length = 2
        self.letter = "S"
