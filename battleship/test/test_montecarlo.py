#!/usr/bin/env python

"""
Unit tests for the Monte Carlo algorithm.
"""

import unittest
import logging

from battleship import montecarlo
from battleship import game
from battleship import scilab
from battleship import settings


class TestMonteCarlo(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the Monte Carlo module."""

    def test_player_targeting(self):
        """Verify a computer player guesses the right cell using targeting."""
        shots = game.ShotsGrid()
        shots.set_cell(1, 1, game.ShotsGrid.HIT)
        shots.set_cell(2, 1, game.ShotsGrid.MISS)
        player = montecarlo.Player(5)
        self.assertEqual((1, 2), player.get_guess(shots, scilab.StepCounter()))

    def test_player_sampling(self):
        """Verify a computer player guesses the right cell using sampling."""
        #shots = game.ShotsGrid()
        #player = montecarlo.Player(5)
        # TODO: complete test case

    def test_get_best_cells(self):
        """Verify the best cells are returned."""
        frequencies = montecarlo.FrequencyGrid()
        frequencies.set_cell(1, 1, 1)
        frequencies.set_cell(5, 5, 2)
        frequencies.set_cell(9, 9, 2)
        self.assertEqual(2, len(frequencies.get_best_cells()))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
