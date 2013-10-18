#!/usr/bin/env python

"""
General settings for the Battleship simulator.
"""

import os
import logging

# Logging settings
DEFAULT_LOGGING_FORMAT = "%(levelname)s: %(message)s"
if os.path.splitext(__file__)[1] == '.py':  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s (%(filename)s:%(lineno)d)"
else:  # pragma: no cover
    VERBOSE_LOGGING_FORMAT = "%(levelname)s: %(message)s"
SPARSE_LOGGING_LEVEL = logging.WARNING
DEFAULT_LOGGING_LEVEL = logging.INFO
VERBOSE_LOGGING_LEVEL = logging.DEBUG
