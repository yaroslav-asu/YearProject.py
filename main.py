import csv
import datetime
import random
import subprocess
from multiprocessing import Pipe, Process

from screen_core import CellsFieldImage
from internal.variables import *

cells_field_image = CellsFieldImage()
parent_conn, child_conn = Pipe()


def get_from_queue():
    if parent_conn.poll(0.001):
        return parent_conn.recv()


def do_actions():
    global cells_field_image, stop
    response = get_from_queue()
    if response:
        if response[0] == "add_cell_to_screen":
            cells_field_image.add(*response[1])
        elif response[0] == "delete_cell_from_screen":
            cells_field_image.delete(*response[1])
        elif response[0] == "move_cell_on_screen":
            cells_field_image.move(*response[1])
        elif response[0] == "toggle_pause":
            stop = not stop
        else:
            print("request_exception")
            print(response)


def save_seed_to_csv():
    with open('seeds.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"), random_seed,
                         cell_size, cell_mutation_chance])


def set_seed(start_seed=None, seed_length=30):
    global random_seed
    if not start_seed:
        for i in range(seed_length):
            random_seed = random_seed * 10 + random.randint(0, 10)
    else:
        random_seed = start_seed
    save_seed_to_csv()


if __name__ == "__main__":

    from cython_objects.core import start_game
    from internal.variables import stop

    random_seed = 0
    FLIP_INTERVAL = 120

    game_process = Process(target=start_game, args=(child_conn, random_seed))
    game_process.start()

    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("Game")
    screen = pygame.display.set_mode((window_width, window_height))
    running = True

    counter = 0
    while running:

        while stop:
            do_actions()
        do_actions()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if counter >= FLIP_INTERVAL:
            screen.blit(cells_field_image, (0, 0))
            cells_field_image.render()

            pygame.display.flip()
            counter = 0
        counter += 1

    game_process.join()
    game_process.kill()

    pygame.quit()
