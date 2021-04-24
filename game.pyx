from random import random
#
# # import numpy
# # from pygame.sprite import AbstractGroup
from operator import truth
#
from cell import Cell
# # from pygame_classes import MySpriteGroup
from variables import *
from myspritegroup cimport MySpriteGroup
from mysprite cimport MySprite
from libcpp cimport bool
# cimport numpy
# import numpy
cdef class Game:
    # cdef multiprocessing.Pipe screen_queue


    def __cinit__(self):
        self.running = True
        print(self.running)
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
        print(self.cells_group.add)
        self.dead_cells_group = MySpriteGroup()

        # self.cells_field[80][100] = Cell((80, 100), self)
        # self.cells_field[20][100] = Cell((20, 100), self)
    def __init__(self):
        self.cells_field[10][10] = Cell((10, 10), self)
        # self.cells_field[11][10] = Cell((11, 10), self)
        # self.cells_field[10][11] = Cell((10, 11), self)
        # self.cells_field[11][11] = Cell((11, 11), self)
        # self.generate_cells()
    # def __init__(self):


    cdef generate_cells(self):
        for i in range(window_height // cell_size):
            for j in range(window_width // cell_size):
                if random() < 0.1:
                    self.cells_field[i][j] = Cell((i, j), self)

    cdef run(self):
        while True:
            self.update()

    cdef update(self):
        # for cell in self.cells_group:
        #     cell.update(self)
        pass

    cdef draw(self):
        pass