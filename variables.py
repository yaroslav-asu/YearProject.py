from threading import Lock

import pygame

window_width = 1800
window_height = 900

cell_energy_to_live = 3

# cells_commands = [25, 24, 26]

cells_number_of_available_actions = 5
actions_costs = {
    21: 1,  # посмотреть собственную энергию
    22: 1,  # посмотреть перед собой
    23: 1,  # повернуться
    24: 5,  # получение энергии из минералов
    25: 5,  # фотосинтез
    26: 1  # движение
}

energy_field_stats = {
    'sun': 5,
    'minerals': 4
}

start_cell_energy = 50
max_cell_energy = 100

stop_lock = Lock()
stop = False
fps = 100


def create_border(image, color):
    for pos in [((0, 0), (9, 0)), ((9, 0), (9, 9)), ((9, 9), (0, 9)), ((0, 9), (0, 0))]:
        pygame.draw.line(image, color, *pos, 1)
