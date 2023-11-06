from random import random
from variables import *

from myspritegroup cimport MySpriteGroup
from cell cimport Cell

cdef class Game:

    def __cinit__(self):
        self.running = True
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

    def __init__(self, object pipe, object csv_writer):
        self.pipe = pipe
        self.csv_writer = csv_writer
        self.generate_cells()
        self.cell_number = 0


    cdef generate_cells(self):
        for i in range(window_height // cell_size):
            for j in range(window_width // cell_size):
                if random() < 0.001:
                    self.cells_field[i][j] = Cell([i, j], self)

    cdef run(self):
        while self.running:
            self.update()

    cdef update(self):
        for cell in self.cells_group:
            Cell.update(cell)

    cdef draw(self):
        pass