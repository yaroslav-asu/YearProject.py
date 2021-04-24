from game cimport Game
from mysprite cimport MySprite

cdef class DeadCell(MySprite):
    def __init__(self, list coords, Game game):
        super().__init__()
        self.game = game
        self.x = coords[1]
        self.y = coords[0]
        self.game.dead_cells_group.add(self)
        # self.color = [150, 150, 150]
        self.color = [200, 200, 200]
        self.border_color = [80, 80, 80]
        # self.image = pygame.Surface((cell_size, cell_size))
        # self.rect = pygame.Rect(self.x, self.y, cell_size, cell_size)
        # pygame.draw.rect(self.image, self.color, (0, 0, cell_size, cell_size))
        # pygame.draw.rect(self.image, self.border_color, (0, 0, cell_size, cell_size))
        # pygame.draw.rect(self.image, self.color, (1, 1, cell_size - 2, cell_size - 2))
        # self.game.cells_field_image.add(self.image, self.x, self.y)
        # self.game.screen_queue.send(('add_cell_to_screen', (self.color, self.border_color, self.x,
        # self.y)))

    cdef kill(self):
        self.game.cells_field[self.y][self.x] = None
        # self.game.cells_field_image.delete(self.x, self.y)
        # self.game.screen_queue.send(('delete_cell_from_screen', (self.x, self.y)))
        super().kill()
