import sys
from threading import Lock

import pygame

window_width = 900
window_height = 600

cell_energy_to_live = 3

cells_commands = [25]

number_of_available_actions = 5
actions_costs = {
    25: 5, 26: 1
}
stop_lock = Lock()
stop = False
fps = 60


def create_border(image, color):
    for pos in [((0, 0), (9, 0)), ((9, 0), (9, 9)), ((9, 9), (0, 9)), ((0, 9), (0, 0))]:
        pygame.draw.line(image, color, *pos, 1)
