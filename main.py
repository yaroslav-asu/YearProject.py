import csv
import datetime
import random
import sys
from multiprocessing import Pipe, Process

from PySide6.QtWidgets import QApplication, QLabel

from interface_logic import run_interface
from screen_core import CellsFieldImage
from variables import *

cells_field_image = CellsFieldImage()
parent_conn, child_conn = Pipe()


def proc():
    app = QApplication(sys.argv)
    label = QLabel("Hello World!")
    label.show()
    app.exec()


def get_from_queue():
    if parent_conn.poll(0.001):
        return parent_conn.recv()


def do_actions():
    global cells_field_image
    responce = get_from_queue()
    if responce:
        if responce[0] == "add_cell_to_screen":
            # print(responce)
            cells_field_image.add(*responce[1])
        elif responce[0] == "delete_cell_from_screen":
            cells_field_image.delete(*responce[1])
        elif responce[0] == "move_cell_on_screen":
            cells_field_image.move(*responce[1])
        else:
            print("request_exception")
            print(responce)


def save_seed_to_csv():
    with open('seeds.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y"), random_seed,
                         cell_size, cell_mutation_chance])


if __name__ == "__main__":
    from core import start_game

    random_seed = 0
    for i in range(30):
        random_seed = random_seed * 10 + random.randint(0, 10)
    print(random_seed)
    #     random_seed = 1958475834730119261883859762763
    #     956555860421311649120215809977, размер 15
    # 550503209342900385906100700873, 18
    random_seed = 192068908107884041056006111951
    save_seed_to_csv()
    FLIP_INTERVAL = 120

    interface_process = Process(target=run_interface)
    interface_process.start()

    game_process = Process(target=start_game, args=(child_conn, random_seed))
    game_process.start()
    pygame.init()
    pygame.mixer.init()

    pygame.display.set_caption("My Game")
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    running = True

    counter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        do_actions()
        if counter >= FLIP_INTERVAL:
            screen.blit(cells_field_image, (0, 0))
            cells_field_image.render()

            pygame.display.flip()
            counter = 0
        counter += 1
    interface_process.kill()
    game_process.kill()
    pygame.quit()
