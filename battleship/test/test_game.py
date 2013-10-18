#!/usr/bin/env python

"""
Unit tests for the battleship game classes.
"""

import unittest
import logging

from battleship import game
from battleship import settings

SAMPLE_2X3_GRID = r"""
/---\
|   |
|   |
\---/
""".strip()


class TestGrid(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the Grid class."""

    def test_grid_to_text(self):
        """Verify a grid can be displayed."""
        self.assertEqual(SAMPLE_2X3_GRID, str(game.Grid(2, 3)))

    def test_indexing(self):
        """Verify IndexErrors are raised."""
        grid = game.Grid()
        self.assertRaises(IndexError, grid.set_cell, 0, 0, 0)
        self.assertRaises(IndexError, grid.set_cell, 11, 11, 0)
        grid.set_cell(5, 5, 1)
        self.assertEqual(1, grid.get_cell(5, 5))


class TestPlacementGrid(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the PlacementGrid class."""

    def test_randomize_empty(self):
        """Verify random placement is working."""
        grid = game.PlacementGrid()
        self.assertTrue(grid.initialize())

    def test_randomize_full(self):
        """Verify placement fails on a full grid."""
        grid = game.PlacementGrid()
        for row in range(10):
            for col in range(10):
                grid.set_cell(row + 1, col + 1, grid.PLACEMENT)
        self.assertFalse(grid.initialize())  # no more open spaces

    def test_placement(self):
        """Verify a grid placements are working."""
        grid = game.PlacementGrid()
        self.assertTrue(grid.place(1, 1, 3, 0))
        self.assertFalse(grid.place(1, 1, 3, 0))  # same placement
        self.assertFalse(grid.place(1, 1, 3, 270))  # overlapping placement
        self.assertTrue(grid.place(2, 1, 3, 0))
        self.assertFalse(grid.place(3, 1, 3, 180))  # off the grid
        self.assertFalse(grid.place(0, 0, 2, 0))  # invalid row and column


class TestShotsGrid(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the ShotGrid class."""

    def test_miss(self):
        """Verify an empty grid always misses."""
        placements = game.PlacementGrid()
        shots = game.ShotsGrid()
        self.assertFalse(shots.guess(1, 1, placements))
        self.assertFalse(shots.guess(5, 5, placements))
        self.assertFalse(shots.guess(8, 2, placements))

    def test_hit(self):
        """Verify a hit is detected."""
        placements = game.PlacementGrid()
        placements.place(1, 1, 5, 0)
        shots = game.ShotsGrid()
        self.assertTrue(shots.guess(1, 1, placements))
        self.assertTrue(shots.guess(1, 5, placements))
        self.assertFalse(shots.guess(1, 6, placements))

    def test_winning(self):
        """Verify a game can be won."""
        placements = game.PlacementGrid()
        placements.initialize()
        shots = game.ShotsGrid()
        guesses = 0
        for row in range(10):
            for col in range(10):
                shots.guess(row + 1, col + 1, placements)
                guesses += 1
                if guesses < 17:
                    self.assertFalse(shots.is_won())
        self.assertTrue(shots.is_won())
        self.assertEqual(100, len(shots.get_guessed_cells()))
        self.assertEqual(0, len(shots.get_unguessed_cells()))
        self.assertEqual(100 - 17, len(shots.get_missed_cells()))

    def test_targeting(self):
        """Verify adjacent cells are selected around hits."""
        placements = game.PlacementGrid()
        placements.set_cell(1, 1, game.PlacementGrid.PLACEMENT)
        placements.set_cell(5, 5, game.PlacementGrid.PLACEMENT)
        shots = game.ShotsGrid()
        shots.guess(1, 1, placements)
        shots.guess(5, 5, placements)
        shots.guess(9, 9, placements)
        self.assertEqual(6, len(shots.get_target_cells()))

    def test_remaining_ships(self):
        """Verify the remaining ships can be guessed."""
        shots = game.ShotsGrid()
        self.assertEqual(17, sum(shots.get_remaining_ships()))
        shots.set_cell(1, 1, shots.HIT)
        shots.set_cell(1, 2, shots.HIT)
        self.assertEqual(17 - 2, sum(shots.get_remaining_ships()))
        shots.set_cell(2, 1, shots.HIT)
        shots.set_cell(2, 2, shots.HIT)
        shots.set_cell(2, 3, shots.HIT)
        self.assertEqual(17 - 2 - 3, sum(shots.get_remaining_ships()))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
