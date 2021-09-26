import datetime
import random
import sqlite3
from multiprocessing import Pipe, Process

from screen_core import CellsFieldImage
from variables import *

FPS = 1000
cells_field_image = CellsFieldImage()
parent_conn, child_conn = Pipe()


con = sqlite3.connect('cells.db')
cur = con.cursor()
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
        elif responce[0] == "bd":
            bd.append(responce[1])
        else:
            print("request_exception")
            print(responce)


if __name__ == "__main__":
    from core import start_game

    now = datetime.datetime.now()
    random_seed = 0
    for i in range(30):
        random_seed = random_seed * 10 + random.randint(0, 10)
    print(random_seed)
    random_seed = 956555860421311649120215809977
    #     random_seed = 1958475834730119261883859762763
    #     956555860421311649120215809977, размер 15

    # start_game()
    FLIP_INTERVAL = 120

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
            # if event.type == pygame.MOUSEBUTTONUP:
            #     pos = pygame.mouse.get_pos()
            #     parent_conn.send(pos)

        do_actions()
        if counter >= FLIP_INTERVAL:
            screen.blit(cells_field_image, (0, 0))
            cells_field_image.render()

            pygame.display.flip()
            counter = 0
        counter += 1
    game_process.kill()
    pygame.quit()

    bd_len = len(bd)
    for i in range(bd_len):
        cur.execute(f"""INSERT INTO cells VALUES ({bd[i]})""")
        con.commit()

    con.close()


