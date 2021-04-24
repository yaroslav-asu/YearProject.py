import numpy

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(("core.pyx", "cells.pyx", "pg.pyx", "pg.pxd", "game.pyx", "game.pxd",
                           "pygame_classes.pyx")),
    include_dirs=[numpy.get_include()]
)
