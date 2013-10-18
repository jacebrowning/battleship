#!/usr/bin/env python

"""
Installer for the Battleship Algorithms package.

Run "python setup.py develop" to install script shortcuts and build executables.

Script creation requires setuptools: http://pypi.python.org/pypi/setuptools
Executable creation requires:
- PyInstaller: http://www.pyinstaller.org/
- Windows extensions: http://sourceforge.net/projects/pywin32/files/pywin32
"""

import os
import sys
import tempfile
import subprocess
from distutils.dir_util import copy_tree, remove_tree
from setuptools import setup, find_packages

from battleship import main

# Create Script Entry Point
setup(
name=main.__program__,
author='Jace Browning',
author_email='jacebrowning@gmail.com',
version=main.__version__,
description=("Simulates a game of Battleship using a Monte Carlo algorithm."),
packages=find_packages(),
entry_points={'console_scripts': [main.__program__ + " = battleship.main:main"]},
)


# Create Executable
PYINSTALLER = r"C:\Python27\pyinstaller-2.0\pyinstaller.py"
if os.path.isfile(PYINSTALLER):
    cwd = os.getcwd()
    tmp = tempfile.mkdtemp()
    src = os.path.abspath(os.path.join(os.path.dirname(__file__), 'battleship', 'main.py'))
    exe = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'executable'))
    os.chdir(tmp)
    if subprocess.call([sys.executable, PYINSTALLER, src, '--name=' + main.__program__]) == 0:
        if os.path.exists(exe):
            remove_tree(exe)
        copy_tree(os.path.join(tmp, 'dist', main.__program__), exe)
    os.chdir(cwd)
    remove_tree(tmp)
