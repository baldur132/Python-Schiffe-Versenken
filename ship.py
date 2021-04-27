""" Classes for Battleships """

class Ship:
    """ Parent class for all ships """
    def __init__(self, position = None, orientation = True, length = 5, letter = "B"):
        """
        constructor for ships
        :param position: position on board
        :param orientation: direction of ship either vertical(true) or horizontal(false)
        :param length: int defining length of the ship in squares
        :param letter: char used to print onto the board
        """
        self.position = [0, 0] if position is None else position
        self.orientation = orientation
        self.length = length
        self.letter = letter
        self.sunken = False
        self.placed = False

    def place(self, pos = None, orient = None, ships = None, board_size = 10, test = False):
        """
        places ships on board by setting their internal position values and/or checks placement validity
        :param pos: position to be placed (first square of ship on top or left)
        :param orient: direction of ship either vertical(true) or horizontal(false)
        :param ships: array of currently existing ships
        :param board_size: int needed to define board bounds to check for validity
        :param test: bool if true does not place the ship, only returns value
        @return bool value if true means that the ship is in a valid location on the board
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
            for shipper in ships:
                if shipper.placed:
                    #check for collisions with battleships
                    if nextpos_x == shipper.position[0] and nextpos_y == shipper.position[1]:
                        #head collision with battleship
                        #return False
                        return False #f"head collision at { nextpos_x } { nextpos_y }"
                    if shipper.orientation:
                        #check for body collisions on vertically oriented shipper
                        if nextpos_x == shipper.position[0] and shipper.position[1] <= nextpos_y < shipper.position[1] + shipper.length:
                            #ship intersects with another vertically oriented one
                            return False #f"vertical body collision at { nextpos_x } { nextpos_y }"
                    else:
                        if nextpos_y == shipper.position[1] and nextpos_x >= shipper.position[0] <= nextpos_x < shipper.position[0] + shipper.length:
                        #check for body collisions on horizontially oriented shipper
                            #ship intersects with with another differently oriented one
                            return False#f"Horizontal body collision at { nextpos_x } { nextpos_y }"

        if not test:
            self.placed = True
            self.position = [pos_x, pos_y]
            self.orientation = orient
        return True

    def get_hit(self, pos, markers):
        """
        checks if a hit is on itself
        :param pos: position of hit, expects len 2 array [n, n]
        @return bool when true, hit is successful when false, hit is not on ship
        """
        hit = False
        if self.placed and not self.sunken:
            if pos[0] == self.position[0] and pos[1] == self.position[1]:
                #hit position is on head
                hit = True
            else:
                if self.orientation:
                    #check for hit on vertically oriented body
                    if pos[0] == self.position[0] and pos[1] < self.position[1] + self.length and pos[1] >= self.position[1]:
                        #hit on body
                        hit = True
                else:
                    #check for hit on horizontally oriented body
                    if pos[1] == self.position[1] and pos[0] < self.position[0] + self.length and pos[0] >= self.position[0]:
                        #hit on bldy
                        hit = True

        if hit:
            hits = 0
            #check if ship is sunken
            for num in range(self.length):
                if self.orientation:
                    #cycle through vertical positions (inc y)
                    pos_str = str(self.position[0]) + str(self.position[1] + num)
                    if not pos_str in markers and pos_str != str(pos[0]) + str(pos[1]):
                        #hit marker does not exist at position, can assume that ship is not sunken
                        break
                    hits = hits + 1
                else:
                    #cycle through horizontal positions (inc x)
                    pos_str = str(self.position[0] + num) + str(self.position[1])
                    if not pos_str in markers and pos_str != str(pos[0]) + str(pos[1]):
                        #hit marker does not exist at position, can assume that the ship is not sunken
                        break
                    hits = hits + 1

            if hits == self.length:
                #because there are as many hits as ship squares, the ship must be sunken
                self.sunken = True

            #return true because ship has been hit
            return True

        return False
