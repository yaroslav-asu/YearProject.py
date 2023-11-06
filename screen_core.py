from typing import Tuple

import numpy as np

from internal.variables import *


class CellsFieldImage(pygame.Surface):
    color = background_color
    grey_square = pygame.Surface((cell_size, cell_size))
    grey_square.fill(color)

    cells_cache = {}

    def __init__(self):
        super().__init__((window_width, window_height))
        self.fill(self.color)

        self.cells_data = np.zeros((window_width // cell_size, window_height // cell_size, 5),
                                   dtype=np.int32)
        for x, row in enumerate(self.cells_data):
            for y, cell in enumerate(row):
                self.cells_data[x, y] = (0, 0, 0, x, y)

        self.render_cache = None

    def move(self, start_x, start_y, end_x, end_y, center_color, border_color):
        self.delete(start_x, start_y)
        self.add(center_color, border_color, end_x, end_y)

    def add(self, center_color, border_color, x, y):
        self.cells_data[x, y] = (*center_color, x, y)

    def delete(self, x, y):
        self.cells_data[x, y] = (*self.color, x, y)

    @staticmethod
    def find_diff(arr1, arr2):
        color_sum1 = (arr1[:, :, 0] + arr1[:, :, 1] + arr1[:, :, 2])
        color_sum2 = (arr2[:, :, 0] + arr2[:, :, 1] + arr2[:, :, 2])
        diff_map: np.ndarray = color_sum1 != color_sum2

        diff = arr1[diff_map == True]
        return diff

    def render_cell(self, cell_info):
        cell_color: Tuple[int, int] = tuple(cell_info[:3])
        x, y = cell_info[3:]

        cached_cell = self.cells_cache.get(cell_color)
        if cached_cell:
            return cached_cell, (x * cell_size, y * cell_size)
        else:
            cell_image = pygame.Surface((cell_size, cell_size))
            pygame.draw.rect(cell_image, cell_color, (0, 0, cell_size, cell_size))

            self.cells_cache[cell_color] = cell_image

            return cell_image, (x * cell_size, y * cell_size)

    def render(self):
        to_blit = []
        if self.render_cache is not None:
            changed_cells = self.find_diff(self.cells_data, self.render_cache)
            for cell_info in changed_cells:
                to_blit.append(self.render_cell(cell_info))
        else:
            for row in self.cells_data:
                for cell_info in row:
                    cell_color = sum(cell_info[:3])
                    if cell_color:
                        to_blit.append(self.render_cell(cell_info))

        self.blits(to_blit)

        self.render_cache = self.cells_data.copy()
