import ctypes
from threading import Lock
from multiprocessing import Queue, Array

import numpy as np
import pygame

window_width = 1800
window_height = 900

cell_size = 5

cell_energy_to_live = 3
energy_for_cell_eat = 20
# cells_commands = [25, 24, 26]

cells_number_of_available_actions = 5
actions_costs = {
    21: 1,  # посмотреть собственную энергию
    22: 1,  # посмотреть перед собой
    23: 1,  # повернуться
    24: 5,  # получение энергии из минералов
    25: 5,  # фотосинтез
    26: 1,  # движение
    27: 5  # съесть клетку
}

# energy_field_stats = {
#     'sun': 5,
#     'minerals': 4
# }

start_cell_energy = 50
max_cell_energy = 100

stop_lock = Lock()
stop = False
fps = 10


def create_border(image, color):
    for pos in [((0, 0), (cell_size - 1, 0)), ((cell_size - 1, 0), (cell_size - 1, cell_size - 1)),
                ((cell_size - 1, cell_size - 1), (0, cell_size - 1)), ((0, cell_size - 1), (0,
                                                                                            0))]:
        pygame.draw.line(image, color, *pos, 1)


base_color = (140, 140, 140)


"""
Инициализация массива, доступного между различными процессами
"""
array_size = (window_width // cell_size, window_height // cell_size, 5)
shared_array = Array(ctypes.c_int64, (array_size[0] * array_size[1] * array_size[2]))
_numpy_shared = np.frombuffer(shared_array.get_obj())

cells_data = _numpy_shared.reshape(array_size)
# заполнение массива базовым цветом
for x, row in enumerate(cells_data):
    for y, cell in enumerate(row):
        cells_data[x, y] = (*base_color, x, y)


def create_numpy_cell_data(shared_array:Array):
    _numpy_shared = np.frombuffer(shared_array.get_obj())
    cells_data = _numpy_shared.reshape(array_size)
    return cells_data
