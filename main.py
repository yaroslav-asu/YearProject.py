import random
import subprocess
from multiprocessing import Pipe, Process


from cython_objects.configs.configs import GameConfig, ScreenConfig, CellConfig


class GameStarter:
    def __init__(self, config):
        self.config = config
        self.parent_conn, self.child_conn = Pipe()
        self.stop = False

    def get_from_queue(self):
        if self.parent_conn.poll(0.001):
            return self.parent_conn.recv()

    def do_actions(self):
        response = self.get_from_queue()
        if response:
            if response[0] == "add_cell_to_screen":
                # self.cells_field.add(*response[1])
                pass
            elif response[0] == "delete_cell_from_screen":
                pass
                # self.cells_field.delete(*response[1])
            elif response[0] == "move_cell_on_screen":
                pass
                # self.cells_field.move(*response[1])
            elif response[0] == "toggle_pause":
                self.stop = not self.stop
            else:
                print("request_exception")
                print(response)

    def start(self):
        from cython_objects.core import start_game

        game_process = Process(target=start_game, args=(self.child_conn, self.config))
        game_process.start()

        running = True
        counter = 0
        while running:
            self.do_actions()
            if self.stop:
                continue

            if counter >= self.config.flip_interval:
                # Send screen
                counter = 0
            counter += 1

        game_process.join()
        game_process.kill()


if __name__ == "__main__":
    subprocess.call("python setup.py build_ext --inplace", shell=True)
    game_config = GameConfig(
        seed=random.randint(0, 10 ** 5),
        cell_size=10,
    )

    game_starter = GameStarter(game_config)
    game_starter.start()
