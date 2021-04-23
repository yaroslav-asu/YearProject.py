import os
import sys
from multiprocessing import Process
from multiprocessing import Queue, Pipe

import pygame

# pyximport.install()
from core import Game, start_game
from screen_core import CellsFieldImage
from variables import window_width, window_height

FPS = 1000
cells_field_image = CellsFieldImage()
parent_conn, child_conn = Pipe()


# def get_from_queue():
#     return screen_game_queue.get()
def get_from_queue():
    if parent_conn.poll(0.001):
        return parent_conn.recv()
    # else:
    #     print('no data')


def do_actions():
    global cells_field_image
    responce = get_from_queue()
    if responce:
        if responce[0] == "add_cell_to_screen":
            cells_field_image.add(*responce[1])
        elif responce[0] == "delete_cell_from_screen":
            cells_field_image.delete(*responce[1])
        elif responce[0] == "move_cell_on_screen":
            cells_field_image.move(*responce[1])
        else:
            print("request_exception")


if __name__ == "__main__":
    FLIP_INTERVAL = 120

    game_process = Process(target=start_game, args=(child_conn,))
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
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                parent_conn.send(pos)

        do_actions()
        # clock.tick(FPS)
        if counter >= FLIP_INTERVAL:

            screen.blit(cells_field_image, (0, 0))
            cells_field_image.render()

            pygame.display.flip()
            counter = 0
        counter += 1

    game_process.kill()
    pygame.quit()

    # game.run()
    # game_screen.cells_field_image.add((0, 0, 0), (0, 0, 0), 0, 0)
    # game_screen.run()
    #

    # game_process.join()
    # thread2 = threading.Thread(target=game.run)
    # thread2.daemon = True
    # # thread2 = multiprocessing.Process(target=start_game)
    # thread2.start()
    # # thread1.start()
    # # thread1.join()
    # interface_logic.run_interface()
    # thread2.join()
