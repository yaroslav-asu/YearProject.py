import numpy

from setuptools import setup
from Cython.Build import cythonize
sp = []
file_names = [
    "cell",
    "game",
    "game",
    "deadcell",
    "mysprite",
    "myspritegroup"
]
for i in file_names:
    sp.append(i + ".pyx")
    sp.append(i + ".pxd")

setup(
    ext_modules=cythonize(sp + ["core.pyx"]),
    include_dirs=[numpy.get_include()]
)
