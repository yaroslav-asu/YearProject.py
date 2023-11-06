import random

from cython_objects.game.game cimport Game
from cython_objects.configs.configs cimport GameConfig

def start_game(pipe, GameConfig game_config):
    random.seed(game_config.seed)
    game = Game(pipe, game_config)
    game.run()