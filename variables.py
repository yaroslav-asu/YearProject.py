from threading import Lock

import pygame

background_color = (180, 180, 180)
border_color = (170, 170, 170)
dead_cell_color = ()
window_width = 1800
window_height = 900

cell_size = 2

cell_energy_to_live = 3
energy_for_cell_eat = 20

cells_number_of_available_actions = 5
actions_costs = {
    21: 1,  # посмотреть собственную энергию
    22: 1,  # посмотреть перед собой
    23: 1,  # повернуться
    24: 5,  # получение энергии из минералов
    25: 5,  # фотосинтез
    26: 1,  # движение
    27: 2  # съесть клетку
}


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


def normalize_coords(*args):
    if len(args) == 1:
        args = [args[0][0], args[0][1]]
    x = args[0] % (window_width // cell_size)
    y = args[1]
    return x, y
