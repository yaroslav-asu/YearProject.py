from pprint import pprint
from random import random

from Cython import typeof

from cython_objects.game.cell.cell cimport Cell
from cython_objects.configs.configs cimport GameConfig

cdef class Game:
    def __init__(self, object pipe, GameConfig config):
        self.running = True
        self.pipe = pipe
        self.cell_number = 0
        self.config = config
        cell_size = self.config.cell_config.cell_size

        self.energy_field = [[
            {
                'sun': 8 - j * cell_size // 128,
                'minerals': j * cell_size // 128
            }
            for i in range(1800 // cell_size)]
            for j in range(900 // cell_size)]
        self.cells_field = [[None for i in range(self.config.screen_config.window_width // cell_size)]
                            for j in range(self.config.screen_config.window_height // cell_size)]

        self.generate_cells()

    cdef generate_cells(self):
        cell_size = self.config.cell_config.cell_size
        for i in range(self.config.screen_config.window_height // cell_size):
            for j in range(self.config.screen_config.window_width // cell_size):
                if random() < 0.001:
                    self.cells_field[i][j] = Cell([i, j], self)

    cdef run(self):
        while self.running:
            self.update()

    cdef update(self):
        for i in range(self.config.screen_config.window_height // self.config.cell_config.cell_size):
            for j in range(self.config.screen_config.window_width // self.config.cell_config.cell_size):
                if self.cells_field[i][j] is not None:
                    if typeof(self.cells_field[i][j]) is Cell:
                        Cell.update(self.cells_field[i][j])

    cdef draw(self):
        pass
