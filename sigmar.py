#!/usr/bin/env python3
"""
This script solves the inside game Sigmar's Garden in the game Opus Magnum.
The script is meant to be called from the command line.
Input should be put in the variable LINES.
The format is one line per line on the board (so 11 lines in total), one character per tile.
The mapping character to element is in CHAR_TO_ELEM.
If the variable is set to None, input will be prompt on the command line.
"""

from enum import IntEnum
import itertools as it

LINES = [
    "teata4",
    "hhoooem",
    "aoaooeof",
    "eooaahooe",
    "vootoosoom",
    "efefo6ofm2v",
    "hoofooaooa",
    "vooftsoo1",
    "sovoofot",
    "tmooos5",
    "tfe3ht",
]

class Element(IntEnum):
    """ Enum for the different elements. """
    VOID = 0
    FIRE = 1
    EARTH = 2
    WATER = 3
    AIR = 4
    SALT = 5
    LIFE = 6
    DEATH = 7
    MERCURY = 8
    LEAD = 9
    TIN = 10
    IRON = 11
    COPPER = 12
    SILVER = 13
    GOLD = 14

    def is_metal(self):
        """ Return True if the element is a metal. """
        return self >= Element.LEAD


CHAR_TO_ELEM = {
    "o": Element.VOID,
    "f": Element.FIRE,
    "t": Element.EARTH,
    "e": Element.WATER,
    "a": Element.AIR,
    "s": Element.SALT,
    "v": Element.LIFE,
    "m": Element.DEATH,
    "h": Element.MERCURY,
    "1": Element.LEAD,
    "2": Element.TIN,
    "3": Element.IRON,
    "4": Element.COPPER,
    "5": Element.SILVER,
    "6": Element.GOLD,
}

class AxialCoordinates:
    """ Represents the axial coordinates of a tile on an hexagonal grid.
    Definition of axial coordinates for hexagonal grids and much more
    can be found on this outstanding webpage
    https://www.redblobgames.com/grids/hexagons/.
    """
    def __init__(self, axial_p, axial_q):
        self.axial_p = axial_p
        self.axial_q = axial_q

    @classmethod
    def from_lines(cls, line, offset):
        """ Create new axial coordinates from line coordinates.
        Lines coordinate consists of the line as it appears on the screen, 0 being the top line,
        and the offset, on the line, 0 being the leftmost tile.
        """
        axial_p = max(0, 5-line) + offset
        axial_q = line
        return AxialCoordinates(axial_p, axial_q)

    def to_lines(self):
        """ Convert axial coordinates to the more friendly line coordinates. """
        line = self.axial_q
        offset = self.axial_p - max(0, 5-line)
        return line, offset

    def __add__(self, other):
        """ Add two axial coordinates vectors. """
        new_axial_p = self.axial_p + other.axial_p
        new_axial_q = self.axial_q + other.axial_q
        return AxialCoordinates(new_axial_p, new_axial_q)

    def __eq__(self, other):
        return self.axial_p == other.axial_p and self.axial_q == other.axial_q

    def __hash__(self):
        return hash((self.axial_p, self.axial_q))

    def __repr__(self):
        return "AxialCoordinates(p:{}, q:{})".format(self.axial_p, self.axial_q)


ADJ_VECTORS = list(it.starmap(AxialCoordinates, [
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (0, -1),
    (1, -1),
]))

def can_combine(element1, element2):
    """ Return True if elements e1 and e2 can be combined per the rules of the game. """
    if element1 > element2:
        element1, element2 = element2, element1
    if 1 <= element1 <= 5:
        return element1 == element2 or element2 == 5
    if  element1 == 6:
        return element2 == 7
    if element1 == 8:
        return element2 < 14
    return False


class Grid:
    """ Represents the board of the game. """
    def __init__(self):
        self.grid = dict()
        self.current_metal = Element.LEAD
        self.last_ops = []
        self.elem_sets = dict()
        for elem in range(1, 9):
            self.elem_sets[elem] = set()
        for elem in range(9, 15):
            self.elem_sets[elem] = None

    def populate_from_lines_input(self, lines):
        """ Populate the board.
        Parameter lines is a list with the following format:
        each element of the list is a line on the board, starting from the top.
        Each character represents a tile, according the values defined in CHAR_TO_ELEM.
        """
        for index, line in enumerate(lines):
            for offset, char in enumerate(line):
                coord = AxialCoordinates.from_lines(index, offset)
                elem = CHAR_TO_ELEM[char]
                if elem == Element.VOID:
                    continue
                self.set_tile(coord, elem)

    def delete_tile(self, coord):
        """ Delete tile from the board. """
        elem = self.grid[coord]
        if elem.is_metal():
            self.elem_sets[elem] = None
        else:
            self.elem_sets[elem].remove(coord)
        del self.grid[coord]

    def set_tile(self, coord, elem):
        """ Set tile to an elem. """
        if elem.is_metal():
            self.elem_sets[elem] = coord
        else:
            self.elem_sets[elem].add(coord)
        self.grid[coord] = elem

    def remaining(self):
        """ Return the number of elements remaining on the grid. """
        return len(self.grid)

    def elem_count(self, elem):
        """ Return the number of elements of type elem remaining on the grid. """
        res = 0
        for value in self.grid.values():
            if value == elem:
                res += 1
        return res

    def is_active(self, coord):
        """ Return True if the element at coord can be played.
        An element can be played if it has 3 adjacent free tiles.
        """
        elem = self.grid.get(coord)
        if elem is None:
            return False
        if elem >= Element.LEAD and self.current_metal != elem:
            return False
        consec = 0
        for vec in ADJ_VECTORS:
            if coord + vec not in self.grid:
                consec += 1
            else:
                consec = 0
            if consec == 3:
                return True
        return False

    def feasible_ops(self):
        """ Return the feasible operations on the grid, as a list of couple of coordinates. """
        ops = []
        sels = filter(self.is_active, self.elem_sets[Element.SALT])
        ops.extend(it.combinations(sels, 2))
        for element in [1, 2, 3, 4]:
            active_elems = filter(self.is_active, self.elem_sets[element])
            ops.extend(it.combinations(active_elems, 2))
            for sel in sels:
                ops.extend(it.product(sel, active_elems))
        vie = filter(self.is_active, self.elem_sets[Element.LIFE])
        mort = filter(self.is_active, self.elem_sets[Element.DEATH])
        ops.extend(it.product(vie, mort))
        mercure = list(filter(self.is_active, self.elem_sets[Element.MERCURY]))
        if mercure:
            metal = self.elem_sets[self.current_metal]
            if metal:
                ops.extend(it.product([metal], mercure))
        if self.current_metal == Element.GOLD:
            gold_coords = self.elem_sets[Element.GOLD]
            if self.is_active(gold_coords):
                ops.append((gold_coords, gold_coords))
        return ops

    def is_solved(self):
        """ Return True if the grid is solved. """
        return not self.grid

    def apply_op(self, operation):
        """ Apply operation toe the grid, and append it the last_ops list.
        The last_ops list also remembers the elements.
        """
        coord1, coord2 = operation
        element1, element2 = self.grid[coord1], self.grid[coord2]
        self.last_ops.append([(coord1, coord2), (element1, element2)])
        if element1.is_metal() or element2.is_metal():
            self.current_metal += 1
        self.delete_tile(coord1)
        if coord1 != coord2:
            self.delete_tile(coord2)

    def reverse_last_op(self):
        """ Revert the last operation. """
        last_op = self.last_ops.pop()
        coord1, coord2 = last_op[0]
        element1, element2 = last_op[1]
        if element1.is_metal() or element2.is_metal():
            self.current_metal -= 1
        self.set_tile(coord1, element1)
        self.set_tile(coord2, element2)

    def __repr__(self):
        return str(self.grid)

    def solve(self):
        """ Solve the grid and return the operations required. """
        if self.is_solved():
            return []
        operations = self.feasible_ops()
        for operation in operations:
            op_values = self.grid[operation[0]], self.grid[operation[1]]
            self.apply_op(operation)
            res = self.solve()
            if res is not None:
                res.insert(0, (operation, op_values))
                return res
            self.reverse_last_op()
        return None


# LINES = [
#     "oooooo",
#     "ooooooo",
#     "oooooooo",
#     "ooooooooo",
#     "oooooooooo",
#     "eoooooooooe",
#     "oooooooooo",
#     "ooooooooo",
#     "oooooooo",
#     "ooooooo",
#     "eooooe",
# ]
if __name__ == "__main__":
    def solve_game(lines):
        """ Solve the game and print result. """
        grid = Grid()
        grid.populate_from_lines_input(lines)
        path = grid.solve()
        if not path:
            print("Unsolvable board.")
        else:
            for operation in path:
                coords, elems = operation
                coord1, coord2 = coords
                print(coord1.to_lines(), elems[0], coord2.to_lines(), elems[1])

    print("**** Solver for Sigmar's Garden ****")
    if LINES:
        print("Solving with provided input...")
        solve_game(LINES)
    else:
        print("I recommand to modify the variable LINES in the script,")
        print("it will be easier to correct if you make a mistake when typing the board.")
        LINES = []
        for i in range(11):
            LINES.append(input("Line {}".format(i+1)))
        solve_game(LINES)
