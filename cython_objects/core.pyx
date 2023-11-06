import random
import csv
from cython_objects.game.game cimport Game

def start_game(pipe, random_seed):
    random.seed(random_seed)
    with open(f'{random_seed}.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        game = Game(pipe, csv_writer)
        game.run()
