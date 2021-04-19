class Ship:
    """ Parent class for all ships """
    def __init__(self, position = [0, 0], orientation = True, length):
        """
        constructor for ships
        :param position: position on board
        :param orientation: direction of ship either vertical(true) or horizontal(false)
        """
        self.position
        self.orientation
        self.length
        self.sunken = False
        self.placed = False
        
    def place(self, pos, orient, ships):
        """
        places ships on board by setting their internal position values and
        checks placement validity
        :param pos: position to be placed (first square of ship on top or left)
        :param orient: direction of ship either vertical(true) or horizontal(false)
        :param ships: dict of currently existing ships
        """
        pos_x = pos[0]
        pos_y = pos[1]

        if pos_x + self.length > 9 or pos_y + self.length > 9:
            #ship overhangs on board
            return False

        for i in range(self.length):
            #find next position
            nextpos_x = pos_x if orient else pos_x + i
            nextpos_y = pos_y + i if orient else pos_y

            #loop through all ship objects
            ships_all = ships[Battleships] + ships[Cruisers] + ships[Destroyers] + ships[Submarines]

            for e in range(len(ships_all)):
                if e.placed:
                    #check for collisions with battleships
                    if nextpos_x == e.position[0] and nextpos_y == e.position[1]:
                        #head collision with battleship
                        return False
                    if orient:
                        #check for body collisions on vertically oriented ship
                        if nextpos_x == e.position[0] and nextpos_y < e.position[1] + e.length:
                            #ship is on top of the body of an already existing ship
                            return False
                    elif:
                        #check for body collisions on horizontially oriented ship
                        if nextpos_y == e.position[1] and nextpos_x < e.position[0] + e.length:
                            #ship intersects with with another differently oriented one
                            return False
                            
        

class Battleship(Ship):
    """ Class for Battleship """
    def __init__(self, position = [0, 0], orientation = True):
        super().__init__(self, position = [0, 0], orientation = True, 5)
        self.length = 5

    def get_hit(self, x, y):
        pass

class Cruiser(Ship):
    """ Class for Cruiser """
    def __init__(self, position = [0, 0], orientation = True):
        super().__init__(self, position = [0, 0], orientation = True, 4)
        self.length = 4

class Destroyer(Ship):
    """ Class for Destroyer """
    def __init__(self, position = [0, 0], orientation = True):
        super().__init__(self, position = [0, 0], orientation = True, 3)
        self.length = 3

class Submarine(Ship):
    """ Class for Submarine """
    def __init__(self, position = [0, 0], orientation = True):
        super().__init__(self, position = [0, 0], orientation = True, 2)
        self.length = 2
        
