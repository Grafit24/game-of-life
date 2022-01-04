"""
Module realize Conway's Game of Life.
If you aren't familiar with this game:
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
"""
from itertools import product
from typing import List, Tuple
from templates import Singleton


__author__ = "Sergey Zelenovsky"
__email__ = "zelnovskiygoodman454@gmail.com"


class Cell:
    """Base unit of the Life Game."""
    def __init__(self, x: int, y: int, game_obj: "Game")-> None:
        self._x = x
        self._y = y
        self._game = game_obj
        if not isinstance(x , int) or not isinstance(y , int):
            raise ValueError("x, y arguments must be integer's objects.")
        self._neighbours = []

    def update_neighbours(self)-> None:
        self._neighbours = self._game.look_around(self.x, self.y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y
        
    @property
    def neighbours(self):
        return tuple(self._neighbours)

    @property
    def count(self):
        """Number of neighbours."""
        return len(self.neighbours)
        

class Game(metaclass=Singleton):
    """All Life Game logic.

    Args:
        init_cells: list of (x, y) tuples, where x, y 
        is coordinates of cell objects.
    """
    def init(self, init_cells):
        self._cells = {}
        for x, y in init_cells:
            self._cells[(x, y)] = Cell(x, y, self)
        
        for cell in self._cells.values():
            cell.update_neighbours()

    def update(self):
        """Go to the next step."""
        creating_objects = []
        removing_objects = []
        # preprocess
        for (x, y), cell in self._cells.items():
            # creating new cells with 3 neighbours
            for c in product([-1, 0, 1], repeat=2):
                dx, dy = c[0]+x, c[1]+y
                if not self._cells.get((dx, dy)):
                    hypoth_neighbours = self.look_around(dx, dy)
                    if len(hypoth_neighbours) == 3:
                        creating_objects.append(Cell(dx, dy, self))
            # removing old cells(x) with x<2 or x>3
            n_neighbours = len(self.look_around(cell.x, cell.y))
            if n_neighbours < 2 or n_neighbours > 3:
                removing_objects.append(cell)
        # update
        for new_cell in creating_objects:
            self._cells[(new_cell.x, new_cell.y)] = new_cell
        for old_cell in removing_objects:
            self._cells.pop((old_cell.x, old_cell.y))

        for cell in self._cells.values():
            cell.update_neighbours()

    def look_around(self, x, y)-> List[Cell]:
        """Detect all neighbours around cell (dead or alive no matter).
        Note. Maximum neighbours is eight.
        """
        neighbours = []
        for с in product([-1, 0, 1], repeat=2):
            dx, dy = с[0]+x, с[1]+y
            neighbour = self._cells.get((dx, dy))
            if (dx != x or dy != y) and neighbour:
                neighbours.append(neighbour)
        return neighbours

    def get_cells(self)-> Tuple[Tuple[int]]:
        """Return tuple of cell coordinates (x, y)."""
        return tuple(self._cells.keys())

    def clear(self)-> None:
        """Remove all cells."""
        self._cells = {}