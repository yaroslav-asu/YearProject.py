from cython_objects.game.game cimport Game

cdef class DeadCell:
    def __init__(self, list coords, Game game):
        super().__init__()
        self.game = game
        self.y, self.x = coords
        self.game.pipe.send(('add_cell_to_screen', (self.x, self.y)))

    cdef public kill(self):
        self.game.cells_field[self.y][self.x] = None
        self.game.pipe.send(('delete_cell_from_screen', (self.x, self.y)))
