from random import random

from cython_objects.game.myspritegroup.myspritegroup cimport MySpriteGroup
from cython_objects.game.cell.cell cimport Cell
from cython_objects.configs.configs cimport GameConfig, CellConfig

cdef class Game:
    def __cinit__(self):
        self.running = True
        self.cells_group = MySpriteGroup()
        self.dead_cells_group = MySpriteGroup()

    def __init__(self, object pipe, GameConfig config):
        self.pipe = pipe
        self.cell_number = 0
        self.config = config
        cell_size = self.config.cell_config.cell_size

        self.energy_field = [[
            {
                'sun': 8 - j * cell_size // 128,
                'minerals': j * cell_size // 128
            }
            for i in range(self.config.cell_config.max_x_id)]
            for j in range(self.config.cell_config.max_y_id)]
        self.cells_field = [[None for i in range(self.config.cell_config.max_x_id)]
                            for j in range(self.config.cell_config.max_y_id)]

        self.generate_cells()

    cdef generate_cells(self):
        cell_size = self.config.cell_config.cell_size
        for i in range(self.config.cell_config.max_y_id):
            for j in range(self.config.cell_config.max_x_id):
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
