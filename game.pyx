from random import random
from variables import *

from myspritegroup cimport MySpriteGroup
from cell cimport Cell

cdef class Game:

    def __cinit__(self):
        self.running = True
        self.fps = fps
        self.energy_field = [[
            {
                'sun': 8 - j * cell_size // 128,
                'minerals': j * cell_size // 128
            }
            for i in range(1800 // cell_size)]
            for j in range(900 // cell_size)]
        self.cells_field = [[None for i in range(window_width // cell_size)]
                                        for j in range(window_height // cell_size)]

        self.cells_group = MySpriteGroup()
        self.dead_cells_group = MySpriteGroup()

    def __init__(self, object pipe):
        self.pipe = pipe
        cdef Cell cell = Cell((10, 10), self)
        print(cell.x, cell.update)
        self.cells_group.add(cell)
        # self.cells_field[10][10] = cell
        # self.generate_cells()


    cdef generate_cells(self):
        for i in range(window_height // cell_size):
            for j in range(window_width // cell_size):
                if random() < 0.001:
                    self.cells_field[i][j] = Cell((i, j), self)

    cdef run(self):
        while True:
            self.update()

    cdef update(self):
        for cell in self.cells_group:
            cell.update(self)

    cdef draw(self):
        pass