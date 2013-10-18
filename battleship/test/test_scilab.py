#!/usr/bin/env python

"""
Unit tests for the Scilab functions.
"""

import os
import unittest
import logging

from battleship import scilab
from battleship import montecarlo
from battleship import settings

FILES = os.path.join(os.path.dirname(__file__), 'files')
GRAPH_PATH = os.path.join(FILES, "graph.sce")
SAMPLE_PATH = os.path.join(FILES, "sample.sce")


class TestScilab(unittest.TestCase):  # pylint: disable=R0904
    """Unit tests for the Scilab module."""

    RESULTS = {0: [(60, 1000, 6),
                   (65, 1100, 5.1)],
               25: [(55, 2000, 10.5),
                    (54, 2100, 11)]}

    @classmethod
    def setUpClass(cls):  # pylint: disable=C0103
        """Delete generated files so they can be recreated."""
        if os.path.isfile(GRAPH_PATH):
            os.remove(GRAPH_PATH)
        if os.path.isfile(SAMPLE_PATH):
            os.remove(SAMPLE_PATH)

    def test_write_graph(self):
        """Verify graph code is written to a file."""
        self.assertTrue(scilab.write_graph(self.RESULTS, GRAPH_PATH))
        self.assertTrue(os.path.isfile(GRAPH_PATH))

    def test_write_sample(self):
        """Verify graph code is written to a file."""
        log = [montecarlo.FrequencyGrid(), montecarlo.FrequencyGrid(), montecarlo.FrequencyGrid()]
        log[0].increment(5, 5)
        log[1].set_guessed_cells([(5, 5)])
        self.assertTrue(scilab.write_sample(log, SAMPLE_PATH))
        self.assertTrue(os.path.isfile(SAMPLE_PATH))

    def test_get_matrix_text(self):
        """Verify matrix text if formatted correctly."""
        self.assertEqual("6              10.5           ;\n                5.1            11             ",
                         scilab.get_column_text(self.RESULTS, 2))

    def test_counter(self):
        """Verify the simple counter functions."""
        counter = scilab.StepCounter()
        counter.increment()
        counter.increment()
        self.assertEqual(2, int(counter))


if __name__ == '__main__':
    logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    unittest.main()
