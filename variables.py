from threading import Lock
import numpy
import pygame

background_color = (180, 180, 180)
border_color = (170, 170, 170)
window_width = 1800
window_height = 900

# cell_size = 3
cell_size = 35
cell_mutation_chance = 100

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
max_cell_energy = 150
genome_size = 64

stop_lock = Lock()
stop = False


def normalize_coords(*args):
    if len(args) == 1:
        args = [args[0][0], args[0][1]]
    x = args[0] % (window_width // cell_size)
    y = args[1]
    return [x, y]
