#!/usr/bin/env python

"""
Setup script for BattleshipSimulator.
"""

import setuptools

from battleship import __project__, __cli__

setuptools.setup(
    name=__project__,
    version='0.0.0',

    description="Simulates a Battleship AI using random sampling.",
    url='http://pypi.python.org/pypi/BattleshipSimulator',
    author='Jace Browning',
    author_email='jace.browning@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': [__cli__ + " = battleship.main:main"]},

    long_description=open('README.rst').read(),
    license='LGPL',

    install_requires=[],
)
