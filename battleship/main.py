#!/usr/bin/env python

"""
Main entry point for the statistical analysis of Battleship algorithms.
"""

import sys
import time
import argparse
import logging

import game
import montecarlo
import scilab
import settings

__program__ = 'battleship'
__version__ = '0.0.1'


def main():  # pragma: no cover
    """Process command-line arguments and run program.
    """
    # Get arguments
    parser = argparse.ArgumentParser(prog=__program__, description=__doc__)
    parser.add_argument('-r', '--random', action='store_true', help="randomly guessing algorithm")
    parser.add_argument('-m', '--montecarlo', metavar='N', type=split, help="Monte Carlo with given sample sizes")
    parser.add_argument('repeat', type=int, default=1, nargs='?', help="number of times to repeat each simulation")
    parser.add_argument('--graph', metavar='FILENAME', help="generate Scilab code to graph results")
    parser.add_argument('--sample', metavar='FILENAME', help="generate Scilab code to show sample game")
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-x', '--verbose', action='store_true', help="enable verbose logging")
    args = parser.parse_args()
    if not any((args.random, args.montecarlo)):
        parser.error("specify which algorithm to use")

    # Set logging level
    if args.verbose:
        logging.basicConfig(format=settings.VERBOSE_LOGGING_FORMAT, level=settings.VERBOSE_LOGGING_LEVEL)
    elif args.graph or args.sample:
        logging.basicConfig(format=settings.DEFAULT_LOGGING_FORMAT, level=settings.SPARSE_LOGGING_LEVEL)
    else:
        logging.basicConfig(format=settings.DEFAULT_LOGGING_FORMAT, level=settings.DEFAULT_LOGGING_LEVEL)

    # Set sample sizes to use for algorithms
    sample_sizes = []
    if args.random:
        sample_sizes.append(0)
    if args.montecarlo:
        sample_sizes.extend(args.montecarlo)

    # Run program
    try:
        if run(sample_sizes, args.repeat, args.graph, args.sample):
            sys.exit(0)
    except KeyboardInterrupt:
        logging.warning("user cancelled simulations")
    finally:
        sys.exit(1)


def split(text):
    """Split a list of comma separated sample sizes.

    >>> split("1,2,3")
    [1, 2, 3]
    """
    return [int(number) for number in text.split(',')]


def run(sample_sizes, repetitions, graph_path=None, sample_path=None):
    """Run simulations of a battleship game using the desired options.

    @param sample_sizes: list of sample sizes the Monte Carlo algorithm (size 0 represents random guessing)
    @param repetitions: number of times to run each algorithm
    @param graph_path: path to write Scilab graph code
    @param sample_path: path to write Scilab sample game code
    @return: indication that simulations completed successfully
    """
    results = {}
    if sample_path:
        if len(sample_sizes) > 1:
            logging.error("specify only one sample size to generate a sample game")
            return False
        frequency_log = []
    else:
        frequency_log = None

    # Run simulations for each sample size
    for index, sample_size in enumerate(sample_sizes):

        results[sample_size] = []

        # Repeat each simulation a number of times
        logging.info("running algorithm sample size {0} of {1}...".format(index + 1, len(sample_sizes)))
        for index2 in range(repetitions):

            # Run simulation and log results
            logging.info("running simulation {0} of {1}...".format(index2 + 1, repetitions))
            guesses, steps, duration = simulation(sample_size, frequency_log=frequency_log)
            results[sample_size].append((guesses, steps, duration))

            # Show only basic progress when generating Scilab data
            if graph_path:
                sys.stderr.write('.')
                sys.stderr.flush()

    # Generate Scilab code
    if graph_path:
        sys.stderr.write('\n')
        if not scilab.write_graph(results, graph_path):  # pragma: no cover
            return False
    if sample_path:
        if not scilab.write_sample(frequency_log, sample_path):  # pragma: no cover
            return False

    return True


def simulation(samples, frequency_log=None):
    """Run a simulation of a battleship game using the desired options.

    @param samples: number of samples for the Monte Carlo algorithm, 0 for random guessing
    @param frequency_log: object to log frequency data for each simulation
    @return: number of guesses required to win the game, number of algorithm steps, duration in seconds
    """
    start = time.time()
    counter = scilab.StepCounter()

    # Create a random playing field
    placements = game.PlacementGrid()
    placements.initialize()

    # Create a grid to store guesses
    shots = game.ShotsGrid()

    # Create a computer player
    player = montecarlo.Player(samples)

    # Run game simulation
    while not shots.is_won():
        row, col = player.get_guess(shots, counter, frequency_log=frequency_log)
        if frequency_log:
            frequency_log[-1].set_guessed_cells(shots.get_guessed_cells())
            frequency_log[-1].set_hit_cells(shots.get_hit_cells())
        shots.guess(row, col, placements)

    # Return number of guesses required
    guesses = len(shots.get_guessed_cells())
    logging.info("the game was won after {0} guesses".format(guesses))
    return guesses, counter.value(), time.time() - start


if __name__ == '__main__':  # pragma: no cover
    main()
