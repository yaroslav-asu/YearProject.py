from cython_objects.game.game cimport Game
from cython_objects.game.cell.myspritegroup.mysprite.mysprite cimport MySprite

cdef class DeadCell(MySprite):
    def __init__(self, list coords, Game game):
        super().__init__()
        self.game = game
        self.x = coords[1]
        self.y = coords[0]
        self.game.dead_cells_group.add(self)
        self.color = [200, 200, 200]
        self.border_color = [80, 80, 80]
        self.game.pipe.send(('add_cell_to_screen', (self.color, self.border_color, self.x,
                                                      self.y)))

    cdef public kill(self):
        self.game.cells_field[self.y][self.x] = None
        self.game.pipe.send(('delete_cell_from_screen', (self.x, self.y)))
        MySprite.kill(self)
