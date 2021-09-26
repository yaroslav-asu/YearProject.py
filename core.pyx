import random


# class CPipe:
#     def __init__(self, pipe):
#         self.pipe = pipe
#     def recv(self):
#         return self.pipe.recv()
#
#     def send(self, arg):
#         self.pipe.send(arg)

from game cimport Game

def start_game(pipe, random_seed):
    # cpipe = CPipe(pipe)
    random.seed(random_seed)
    cdef Game game = Game(pipe)
    game.run()
