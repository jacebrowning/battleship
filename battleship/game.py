#!/usr/bin/env python

"""
Simulation of the battleship board game.
"""

import random
import logging

import settings

# Battleship constants
ROWS = 10
COLS = 10
SHIPS = (5, 4, 3, 3, 2)
ROTATION = (0, 90, 180, 270)


class Grid(object):
    """Generic Battleship grid. The top left corner is (1,1)."""

    EMPTY = 0
    FORMAT = {EMPTY: ' '}

    def __init__(self, rows=ROWS, cols=COLS):
        """Create a new grid."""
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def __str__(self):
        """Format the grid as text."""
        text = '/' + '-' * self.cols + '\\' + '\n'
        for row in self.grid:
            text += '|'
            for value in row:
                if value in self.FORMAT:
                    text += self.FORMAT[value]
                else:
                    text += chr(min(value, 255 - ord('0')) + ord('0'))  # show numbers over 9 as ASCII
            text += '|' + '\n'
        text += '\\' + '-' * self.cols + '/'
        return text

    def __iter__(self):
        """Iterate through cells and values."""
        for row, row_value in enumerate(self.grid, start=1):
            for col, cell_value in enumerate(row_value, start=1):
                yield (row, col), cell_value

    def get_cell(self, row, col):
        """Return value of cell (index starts at 1)."""
        if row < 1 or col < 1:
            raise IndexError
        return self.grid[row - 1][col - 1]

    def set_cell(self, row, col, value):
        """Set value of cell (index starts at 1)."""
        if row < 1 or col < 1:
            raise IndexError
        self.grid[row - 1][col - 1] = value

    def is_empty(self, row, col):
        """Determine if cell is empty (index starts at 1)."""
        return self.get_cell(row, col) == self.EMPTY


class PlacementGrid(Grid):
    """Representation of a Battleship field containing randomly placed ships."""

    SKIP = -1
    EMPTY, PLACEMENT = range(2)
    FORMAT = {SKIP: ' ',
              EMPTY: ' ',
              PLACEMENT: 'O'}
    MAX_PLACEMENT_ATTEMPTS = 100

    def initialize(self):
        """Create a new playing field.

        @return: indicates initial board could be created"""
        for length in SHIPS:
            attempts = 0
            while attempts < self.MAX_PLACEMENT_ATTEMPTS:
                attempts += 1
                row = random.randint(1, self.rows)
                col = random.randint(1, self.cols)
                rotation = random.choice(ROTATION)
                if self.place(row, col, length, rotation):
                    break
            else:
                logging.error("could not place a ship after {0} attempts".format(attempts))
                return False
        logging.info("random ship placement:\n{0}".format(self))

        return True

    def sample(self, ships):
        """Attempt to place more ships for sampling algorithms.

        @param ships: lengths of remaining ships to place
        """
        for length in ships:
            attempts = 0
            while attempts < self.MAX_PLACEMENT_ATTEMPTS:
                attempts += 1
                row = random.randint(1, self.rows)
                col = random.randint(1, self.cols)
                rotation = random.choice(ROTATION)
                if self.place(row, col, length, rotation):
                    break
        logging.debug("random sample placement:\n{0}".format(self))

    def place(self, row, col, length, rotation=0):
        """Place a ship with the given length and rotation.

        @param row: 1-indexed row for ship placement
        @param col: 1-indexed column for ship placement
        @param length: number of cells occupied by the ship
        @param rotation: angle to place the ship: 0, 90, 180, 270
        @return: indicates ship could be placed at the given location
        """
        free = False
        logging.debug("attempting {length}-cell ship at ({row}, {col}) rotated {rotation}".format(length=length,
                                                                                                  row=row, col=col,
                                                                                                  rotation=rotation))
        # Determine rotation
        assert rotation in ROTATION
        if rotation == 90:
            row_step = -1
            col_step = 0
        elif rotation == 180:
            row_step = 0
            col_step = -1
        elif rotation == 270:
            row_step = 1
            col_step = 0
        else:
            row_step = 0
            col_step = 1
        # Determine cells to occupy
        cells = [(row, col)]
        for index in range(1, length):
            _row = cells[-1][0] + row_step
            _col = cells[-1][1] + col_step
            cells.append((_row, _col))
            logging.debug("cell {count} will occupy ({row}, {col})".format(count=index + 1, row=_row, col=_col))
        # Verify cells are empty
        try:
            free = all(self.is_empty(_row, _col) for _row, _col in cells)
            if not free:
                logging.debug("one or more cells is already occupied")
        except IndexError:
            logging.debug("one or more cells is off the grid")
        # Place ship
        if free:
            for _row, _col in cells:
                self.set_cell(_row, _col, self.PLACEMENT)
            logging.debug("placed {length}-cell ship at ({row}, {col}) rotated {rotation}".format(length=length,
                                                                                                  row=row, col=col,
                                                                                                  rotation=rotation))
        return free


class ShotsGrid(Grid):
    """Representation of a shots taken against a Battleship field."""

    UNGUESSED, HIT, MISS = range(3)
    FORMAT = {UNGUESSED: ' ',
              HIT: 'X',
              MISS: '*'}

    def get_hit_cells(self):
        """Return a list of hit cells."""
        return [cell for cell, value in self if value == self.HIT]

    def get_missed_cells(self):
        """Return a list of missed cells."""
        return [cell for cell, value in self if value == self.MISS]

    def get_guessed_cells(self):
        """Return a list of guessed cells."""
        return self.get_hit_cells() + self.get_missed_cells()

    def get_unguessed_cells(self):
        """Return a list of unguessed cells."""
        return [cell for cell, _value in self if cell not in self.get_guessed_cells()]

    def get_target_cells(self):
        """Return a list of unguessed cells adjacent to hit cells."""
        target_cells = []
        unguessed_cells = self.get_unguessed_cells()
        for row, col in self.get_hit_cells():
            for adjacent_cell in ((row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)):
                if adjacent_cell in unguessed_cells:
                    target_cells.append(adjacent_cell)
        return target_cells

    def guess(self, row, col, grid):
        """Guess a cell in the opponent's grid.

        @param row: 1-indexed row for ship guess
        @param col: 1-indexed column for ship guess
        @param grid: reference to opponent's grid
        @return: indicates a ship was hit
        """
        if grid.is_empty(row, col):
            logging.info("guessed ({row},{col}) and it was a miss".format(row=row, col=col))
            self.set_cell(row, col, self.MISS)
            hit = False
        else:
            logging.info("guessed ({row},{col}) and it was a hit".format(row=row, col=col))
            self.set_cell(row, col, self.HIT)
            hit = True
        logging.info("current guesses:\n{0}".format(self))
        return hit

    def get_remaining_ships(self):
        """Guess which ships could be remaining based on the number of hits."""
        hits = len(self.get_hit_cells())
        if hits:
            for _attempt in range(999):
                remaining_ships = list(SHIPS)
                hit_ships = []
                for _count in range(len(SHIPS) - 1):
                    hit_ships.append(remaining_ships.pop(random.randrange(len(remaining_ships))))
                    if sum(hit_ships) == hits:
                        return remaining_ships
        return SHIPS

    def is_won(self):
        """Determine if all ships have been hit."""
        return len(self.get_hit_cells()) >= sum(SHIPS)


if __name__ == '__main__':  # pragma: no cover
    logging.basicConfig(format=settings.DEFAULT_LOGGING_FORMAT, level=settings.DEFAULT_LOGGING_LEVEL)
    _PLACEMENT = PlacementGrid()
    _PLACEMENT.initialize()
    print("Placement grid:")
    print(_PLACEMENT)
    _SHOTS = ShotsGrid()
    for _COUNT in range(50):
        _SHOTS.guess(random.randint(1, ROWS), random.randint(1, COLS), _PLACEMENT)
    print("Shots grid:")
    print(_SHOTS)
