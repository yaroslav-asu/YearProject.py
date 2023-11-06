import numpy

from setuptools import setup, Extension
from Cython.Build import cythonize
import os

dirs = []
extensions = [

]
w = os.walk("cython_objects")
for (dirpath, dirnames, filenames) in w:
    if "__pycache__" in dirpath:
        continue
    extensions.append(Extension("*", [f"{dirpath}/*.pyx"]))
    dirs.append(dirpath)

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include(), *dirs]
)
