#!/usr/bin/env python

"""
Package for BattleshipSimulator.
"""

from pkg_resources import get_distribution, DistributionNotFound

__project__ = 'BattleshipSimulator'
__version__ = None  # required for initial installation

__cli__ = 'battleship'

try:
    __version__ = get_distribution(__project__).version  # pylint: disable=E1103
except DistributionNotFound:  # pragma: no cover, manual test
    VERSION = __project__ + '-' + '(local)'
else:
    VERSION = __project__ + '-' + __version__
