#!/usr/bin/env python

"""
Implementation of a Monte Carlo algorithm to select the next most likely hit in a Battleship game.
"""

import random
import logging

from game import Grid, PlacementGrid
import settings


class Player(object):
    """Computer player utilizing Monte Carlo sampling to select each play.

    The algorithm:
    1. if cells have been hit, target surrounding cells first
    2. based on the specified sample size (N), generate N random ship placements in the free spaces
    3. randomly select from the cells most likely to contain part of a ship

    If the sample size is 0, no Monte Carlo sampling will occur and randomly guessing will be applied.
    """

    def __init__(self, sample_size=0):
        """Create new computer player.

        @param sample_size: number of steps in the Monte Carlo method, 0 for purely random guessing
        """
        self.sample_size = sample_size

    def get_guess(self, shots, counter, frequency_log=None):
        """Return next cell to guess based on targeting (if applicable) or using Monte Carlo sampling.

        @param shots: ShotsGrid of shots already taken
        @return: next cell to guess
        """
        # Target cells surrounding hits first
        target_cells = shots.get_target_cells()
        if target_cells:
            return self.get_random_guess(shots, target_cells, counter, frequency_log=frequency_log)

        # Use Monte Carlo sampling to select the best cell
        return self.get_monte_carlo_guess(shots, counter, frequency_log=frequency_log)

    def get_random_guess(self, shots, target_cells, counter, frequency_log=None):
        """Return next cell to guess from the available target cells.

        @param shots: ShotsGrid of shots already taken
        @param target_cells: list of unguessed cells adjacent to hits
        @return: next random cell to guess
        """
        logging.debug("selecting from target cells: {0}".format(target_cells))
        if frequency_log:
            frequencies = FrequencyGrid()
            frequencies.set_guessed_cells(shots.get_guessed_cells())
            for row, col in target_cells:
                frequencies.increment(row, col)
            frequency_log.append(frequencies)
        counter.increment()
        return random.choice(target_cells)

    def get_monte_carlo_guess(self, shots, counter, frequency_log=None):
        """Return next cell to guess based on Monte Carlo sampling.

        @param shots: ShotsGrid of shots already taken
        @return: next best cell to guess
        """
        # Create grid to store frequency totals for all samples
        frequencies = FrequencyGrid()
        frequencies.set_guessed_cells(shots.get_guessed_cells())
        # Guess which ships could be remaining
        ships = shots.get_remaining_ships()
        logging.info("estimated remaining ships: {0}".format(ships))
        # Create placement samples
        for sample in range(self.sample_size):
            logging.info("computing Monte Carlo sample {0} of {1}...".format(sample + 1, self.sample_size))
            counter.increment()
            placements = PlacementGrid()
            # Mark already guessed cells
            for row, col in shots.get_guessed_cells():
                placements.set_cell(row, col, PlacementGrid.SKIP)
            # Randomly place remaining ships
            placements.sample(ships)
            # Update frequencies
            for (row, col), value in placements:
                if value == PlacementGrid.PLACEMENT:
                    frequencies.increment(row, col)
        logging.info("frequencies after sampling:\n{0}".format(frequencies))
        if frequency_log is not None:
            frequency_log.append(frequencies)
        # Select the best cell using the measured frequencies
        best_cells = frequencies.get_best_cells()
        logging.debug("selecting from best probability cells: {0}".format(best_cells))
        return random.choice(best_cells)


class FrequencyGrid(Grid):
    """Stores the frequency each cells contain a ship during Monte Carlo sampling."""

    GUESSED = -1
    HIT = -4

    FORMAT = {GUESSED: ' ',
              HIT: ' '}

    def set_guessed_cells(self, cells):
        """Set probability in cells that have already been guessed."""
        for row, col in cells:
            self.set_cell(row, col, self.GUESSED)

    def set_hit_cells(self, cells):
        """Mark hit cells for logging purposes."""
        for row, col in cells:
            self.set_cell(row, col, self.HIT)

    def increment(self, row, col):
        """Increment frequency at the specified cell."""
        self.set_cell(row, col, self.get_cell(row, col) + 1)

    def get_best_cells(self):
        """Return of list of cells with the highest probability."""
        # Find highest probability
        best = max((value for _cell, value in self))
        logging.info("current highest frequency: {0}".format(best))
        # Find cells with the highest probability
        return [cell for cell, value in self if value >= best]


if __name__ == '__main__':  # pragma: no cover
    logging.basicConfig(format=settings.DEFAULT_LOGGING_FORMAT, level=settings.DEFAULT_LOGGING_LEVEL)
