#!/usr/bin/env python

"""
Functions for interacting with Scilab for report generation and statistical analysis.
"""

import logging

import settings


GRAPH_CODE = """
// Generated code to display 3 graphs of Battleship simulation results

// Y coordinates
sample_sizes = [{sample_sizes}];

// X coordinates
guesses      = [{guesses}];
steps        = [{steps}];
durations    = [{durations}];

// Graph number of rounds vs. sample sizes
subplot(1, 3, 1);
title ("Algorithm Accuracy");
plot(sample_sizes, guesses, 'o', sample_sizes, mean(guesses, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [{min};{max}];
xlabel ("Monte Carlo Sample Size");
ylabel ("Number of Guesses Required");

// Graph algorithm steps vs. sample sizes
subplot(1, 3, 2);
title ("Algorithm Efficiency (Steps)");
plot(sample_sizes, steps, 'o', sample_sizes, mean(steps, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [{min};{max}];
xlabel ("Monte Carlo Sample Size");
ylabel ("Number Steps Per Game");

// Graph game duration vs. sample sizes
subplot(1, 3, 3);
title ("Algorithm Efficiency (Duration)");
plot(sample_sizes, durations, 'o', sample_sizes, mean(durations, 'r'));
axes = gca();
axes.sub_ticks = [0, 0];
axes.data_bounds(:,1) = [{min};{max}];
xlabel ("Monte Carlo Sample Size");
ylabel ("Simulation Duration (Seconds)");

// Close the window after a mouse click
xclick();
xdel(winsid());
""".strip()
GRAPH_INDENT = ';\n' + ' ' * 16

SAMPLE_CODE = """
// Generated code to display the Monte Carlo experiments for each round of a game
{rounds}

// Automatically clear the graph after each plot
da=gda();
da.auto_clear = 'on';

// Draw each round and wait for a mouse click
{draws}

// Close the window
messagebox("Simulation completed.");
xclick();
xdel(winsid());
""".strip()
SAMPLE_ROUND = "round_{number} = [{data}];"
SAMPLE_INDENT = '\n' + ' ' * 11
SAMPLE_DRAW = """
subplot(1, 2, 1);
title ("Round {number}: Algorithm Frequency Results");
hist3d(round_{number}, alpha=50, theta=25, flag=[1,1,0], ebox=[0,10,0,10,0,10]);
subplot(1, 2, 2);
title ("Previous Round Hits and Misses");
hist3d(round_{number} * -1/4, alpha=34.5, theta=45, flag=[1,1,0], ebox=[0,10,0,10,0,1]);
[ibutton,xcoord,yxcoord] = xclick();
if (ibutton == -1000) then
    abort
end
""".strip()


class StepCounter(object):
    """Basic counter to store the number of steps taken during an algorithm."""

    def __init__(self):
        self.steps = 0

    def __int__(self):
        return self.steps

    def increment(self):
        """Increment counter."""
        self.steps += 1

    def value(self):
        """Return counter's value."""
        return self.steps


def write_graph(results, path):
    """Create Scilab code to store simulation results.

    @param results: dictionary of results: {sample_size: [(guesses, steps, duration), ...]}
    @path path: Scilab file to create
    @return: indicates file was created
    """
    code = format_graph_code(results)

    with open(path, 'w') as graph:
        graph.write(code)

    return True


def format_graph_code(results):
    """Generate Scilab code to graph results data.

    @param results: dictionary of results: {sample_size: [(guesses, steps, duration), ...]}
    @return: Scilab code as text
    """

    sample_sizes_text = ''.join("{:<15}".format(key) for key in sorted(results.keys()))
    guesses_text = get_column_text(results, 0)
    steps_text = get_column_text(results, 1)
    durations_text = get_column_text(results, 2)

    code = GRAPH_CODE.format(sample_sizes=sample_sizes_text,
                             guesses=guesses_text,
                             steps=steps_text,
                             durations=durations_text,
                             min=min(results.keys()) - 5,
                             max=max(results.keys()) + 5)

    return code


def get_column_text(dictionary, column):
    """Generate a table of text for the specified column in the dictionary values.

    @param dictionary: data to convert to text
    @param column: index of the dictionary's values to format
    @return: text table
    """
    keys = sorted(dictionary.keys())
    count = len(dictionary[keys[0]])
    return GRAPH_INDENT.join(''.join('{:<15}'.format(dictionary[key][i][column]) for key in keys) for i in range(count))


def write_sample(log, path):
    """Create Scilab code to simulate a single game.

    @param log: list of frequency data to represent in 3D
    @path path: Scilab file to create
    @return: indicates file was created
    """
    code = format_sample_code(log)

    with open(path, 'w') as sample:
        sample.write(code)

    return True


def format_sample_code(log):
    """Generate Scilab code to run a game simulation.

    @param log: list of frequency data to represent in 3D
    @return: Scilab code as text
    """

    rounds_text = ""
    draws_text = ""
    for number, grid in enumerate(log, start=1):
        rounds_text += SAMPLE_ROUND.format(number=number,
                                           data=SAMPLE_INDENT.join(''.join('{:<4}'.format(c) for c in r)
                                                                   for r in grid.grid)) + '\n'
        draws_text += SAMPLE_DRAW.format(number=number) + '\n'

    code = SAMPLE_CODE.format(rounds=rounds_text, draws=draws_text)

    return code


if __name__ == '__main__':  # pragma: no cover
    logging.basicConfig(format=settings.DEFAULT_LOGGING_FORMAT, level=settings.DEFAULT_LOGGING_LEVEL)
