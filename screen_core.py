import os

from variables import *


class CursorImage(pygame.Surface):
    def __init__(self):
        super().__init__((window_width, window_height))
        self.color = (255, 255, 0)
        self.cursor_image = pygame.Surface((cell_size, cell_size))
        # pygame.draw.rect(self.cursor_image, self.color, (0, 0, 10, 10))
        create_border(self.cursor_image, self.color)
        self.set_colorkey((0, 0, 0))
        self.connected_cell = None
        self.set_colorkey((0, 0, 0))

    def connect_cell(self, sprite):
        self.connected_cell = sprite

    def clear(self):
        self.fill((0, 0, 0))

    def set_cursor_position(self, coords):
        self.fill((0, 0, 0))
        self.blit(self.cursor_image, (coords[0] // cell_size * cell_size, coords[1] // cell_size
                                      * cell_size,
                                      cell_size, cell_size))

    def update(self):
        import interface_logic
        if self.connected_cell:
            if self.connected_cell.groups():
                self.set_cursor_position(
                    (self.connected_cell.x * cell_size, self.connected_cell.y * cell_size))
            else:
                interface_logic.window.clear_window()
                self.clear()


class CellsFieldImage(pygame.Surface):
    def __init__(self):
        super().__init__((window_width, window_height))
        self.color = (140, 140, 140)
        self.fill(self.color)
        self.grey_square = pygame.Surface((cell_size, cell_size))
        self.grey_square.fill(self.color)

    def move(self, start_x, start_y, end_x, end_y, center_color, border_color):
        self.delete(start_x, start_y)
        self.add(center_color, border_color, end_x, end_y)

    def add(self, center_color, border_color, x, y):
        cell_image = pygame.Surface((cell_size, cell_size))
        create_border(cell_image, border_color)
        pygame.draw.rect(cell_image, center_color, (1, 1, cell_size - 1, cell_size - 1))
        self.blit(cell_image, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

    def delete(self, x, y):
        self.blit(self.grey_square, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))


class GameScreen:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = fps

        self.cells_field_image = CellsFieldImage()
        # self.cursor_image = CursorImage()

    @staticmethod
    def get_from_queue():
        return screen_game_queue.get()

    def do_actions(self):
        responce = self.get_from_queue()
        if responce:
            if responce[0] == "add_cell_to_screen":
                self.cells_field_image.add(*responce[1])
            elif responce[0] == "delete_cell_from_screen":
                self.cells_field_image.delete(*responce[1])
            elif responce[0] == "move_cell_on_screen":
                self.cells_field_image.move(*responce[1])
            else:
                print("request_exception")

    def run(self):
        while True:
            self.do_actions()
            self.screen.blit(self.cells_field_image, (0, 0))
            # self.clock.tick(self.fps)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    os._exit(1)
            #     # if event.type == pygame.K_SPACE:
            #     #     with stop_lock:
            #     #         variables.stop = not variables.stop
            #     # if event.type == pygame.MOUSEBUTTONUP:
            #     #     pos = pygame.mouse.get_pos()
            #     #     clicked_sprites = [sprite for sprite in list(self.cells_group) +
            #     #                        list(self.dead_cells_group)
            #     #                        if sprite.rect.collidepoint(pos)]
            #     #     if clicked_sprites:
            #     #         window.fill_window(clicked_sprites[0])
            #     #         self.cursor_image.connect_cell(clicked_sprites[0])
            #
            # # with stop_lock:
            # #     if variables.stop:
            # #         self.screen.blit(self.cells_field_image, (0, 0))
            # #         self.screen.blit(self.cursor_image, (0, 0))
            # #         self.cursor_image.update()
            # #         self.clock.tick(self.fps)
            # #         pygame.display.flip()
            # #         continue
            #
            # # self.screen.blit(self.cursor_image, (0, 0))
            # # self.cursor_image.update()
            # # window.update(self)
            # # self.previous_cells_field = self.cells_field
            #
