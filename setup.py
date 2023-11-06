import numpy

from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("*", ["*.pyx"]),
]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()]
)
