#!/usr/bin/env python

"""
Unit tests for the main Battleship Algorithms functionality.
"""

import unittest
import tempfile
import logging

from battleship import main
from battleship import settings


class TestMain(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the main module."""

    def test_run(self):
        """Verify simulations can be run with graph generation."""
        temp = tempfile.NamedTemporaryFile()
        self.assertTrue(main.run([0, 1], 2, graph_path=temp.name))

    def test_run_logging(self):
        """Verify simulations can be run with sample generation."""
        temp = tempfile.NamedTemporaryFile()
        self.assertTrue(main.run([1], 1, sample_path=temp.name))

    def test_run_invalid(self):
        """Verify sample genreation can only be performed on a single game."""
        temp = tempfile.NamedTemporaryFile()
        self.assertFalse(main.run([1, 2, 3], 1, sample_path=temp.name))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
