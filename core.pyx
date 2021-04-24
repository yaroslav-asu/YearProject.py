from random import random
#
# # import numpy
# # from pygame.sprite import AbstractGroup
from operator import truth
#
# from cells import Cell
# # from pygame_classes import MySpriteGroup
from variables import *
# from pg cimport MySpriteGroup
from libcpp cimport bool
# cimport numpy
# import numpy

# from pygameclassesi cimport SpriteGroup

# class CursorImage(pygame.Surface):
#     def __init__(self):
#         super().__init__((window_width, window_height))
#         self.color = (255, 255, 0)
#         self.cursor_image = pygame.Surface((cell_size, cell_size))
#         # pygame.draw.rect(self.cursor_image, self.color, (0, 0, 10, 10))
#         create_border(self.cursor_image, self.color)
#         self.set_colorkey((0, 0, 0))
#         self.connected_cell = None
#         self.set_colorkey((0, 0, 0))
#
#     def connect_cell(self, sprite):
#         self.connected_cell = sprite
#
#     def clear(self):
#         self.fill((0, 0, 0))
#
#     def set_cursor_position(self, coords):
#         self.fill((0, 0, 0))
#         self.blit(self.cursor_image, (coords[0] // cell_size * cell_size, coords[1] // cell_size
#                                       * cell_size,
#                                       cell_size, cell_size))
#
#     def update(self):
#         import interface_logic
#         if self.connected_cell:
#             if self.connected_cell.groups():
#                 self.set_cursor_position(
#                     (self.connected_cell.x * cell_size, self.connected_cell.y * cell_size))
#             else:
#                 interface_logic.window.clear_window()
#                 self.clear()
#
#
# class CellsFieldImage(pygame.Surface):
#     def __init__(self):
#         super().__init__((window_width, window_height))
#         self.color = (140, 140, 140)
#         self.fill(self.color)
#         self.grey_square = pygame.Surface((cell_size, cell_size))
#         self.grey_square.fill(self.color)
#
#     def move(self, start_x, start_y, end_x, end_y, image):
#         self.delete(start_x, start_y)
#         self.add(image, end_x, end_y)
#
#     def add(self, image, x, y):
#         self.blit(image, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))
#
#     def delete(self, x, y):
#         self.blit(self.grey_square, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))





# cimport numpy
#
# cdef class A:
#     numpy.import_array()
#
#
#     cdef list b
#     def __init__(self):
#         self.b = [1, 'a', 0.2]
#         print(self.b)
from game cimport Game
cpdef start_game():
    cdef Game game = Game()
    game.run()
