import pygame
import pyximport
import interface_logic
# pyximport.install()
from core import Game
import threading
import multiprocessing



# def start_game():

# multiprocessing.queues.Queue()
if __name__ == "__main__":
    # from core_c import start_game
    # start_game()
    # thread1 = threading.Thread(target=)
    game = Game()
    # game.run()

    thread2 = threading.Thread(target=game.run)
    thread2.daemon = True
    # thread2 = multiprocessing.Process(target=start_game)
    thread2.start()
    # thread1.start()
    # thread1.join()
    interface_logic.run_interface()
    thread2.join()

pygame.quit()
