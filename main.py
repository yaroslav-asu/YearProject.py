import threading
from pprint import pprint
from threading import Thread
import pygame
import numpy
from random import shuffle, randint, random

window_width = 900
window_height = 600

cell_energy_to_live = 3

cells_commands = [25]

fps = 60

thread_list = []


# background_image = pygame.Surface((window_width, window_height))
# field_cell_size = 10
# for i in range(window_width // field_cell_size + 1):
#     pygame.draw.rect(background_image, (40, 40, 40), pygame.Rect(field_cell_size * i, 0, 1,
#                                                                  window_height))
# for i in range(window_height // field_cell_size + 1):
#     pygame.draw.rect(background_image, (40, 40, 40),
#                      pygame.Rect(0, field_cell_size * i, window_width, 1))

class SpriteGroup(pygame.sprite.Group):
    def update(self, game):
        pygame.sprite.Group.update(self, game)

    def render(self, screen):
        self.draw(screen)


class DeadCell(pygame.sprite.Sprite):
    def __init__(self, coords, game):
        super().__init__()
        game.dead_cells_group.add(self)
        self.color = (150, 150, 150)
        self.border_color = (80, 80, 80)
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, self.border_color, (0, 0, 10, 10))
        pygame.draw.rect(self.image, self.color, (1, 1, 8, 8))

        self.x = coords[1]
        self.y = coords[0]
        self.rect = pygame.Rect(self.x * 10, self.y * 10, 10, 10)


class Cell(pygame.sprite.Sprite):
    def __init__(self, coords, game, parent=None, color=(20, 150, 0)):
        super().__init__()
        game.cells_group.add(self)
        self.x = coords[1]
        self.y = coords[0]
        self.color = color
        self.border_color = (80, 80, 80)
        self.game = game
        self.energy = 250
        self.max_energy = 500
        self.genome_id = 0
        self.image = pygame.Surface((10, 10))
        pygame.draw.rect(self.image, self.border_color, (0, 0, 10, 10))
        pygame.draw.rect(self.image, self.color, (1, 1, 8, 8))
        self.rect = pygame.Rect(self.x * 10, self.y * 10, 10, 10)
        # self.photosynthesized = 0
        # self.cells_eaten = 0

        directions = ['up', 'down', 'left', 'right']
        self.direction = directions[randint(0, 3)]

        if not parent:
            self.genome = numpy.array([25 for i in range(64)],
                                  numpy.int8)
        else:
            if random() < 0.25:
                self.genome = parent.genome
                self.genome[randint(0, 63)] = randint(0, 63)
            else:
                self.genome = parent.genome
        # pprint(self.genome)

    # def render(self, screen):


    def move(self):
        x, y = self.x, self.y
        if self.direction == 'left' and self.can_move(self.x - 1, self.y):
            self.x -= 1
        elif self.direction == 'right' and self.can_move(self.x + 1, self.y):
            self.x += 1
        elif self.direction == 'up' and self.can_move(self.x, self.y - 1):
            self.y -= 1
        elif self.direction == 'down' and self.can_move(self.x, self.y + 1):
            self.y += 1
        if x != self.x:
            self.rect.x = self.x * 10
        if x != self.y:
            self.rect.y = self.y * 10


    def can_move(self, x, y):
        if 0 <= x < window_width // 10 and 0 <= y < window_height // 10 and not \
            self.get_object_from_coords(x, y):
            return True
        else:
            return False

    def get_object_from_coords(self, x, y):
        if isinstance(self.game.cells_field[y][x], Cell):
            counter = 0
            for i in self.genome == self.game.cells_field[y][x]:
                if not i:
                    counter += 1
                    if counter > 1:
                        break
            if counter == 1:
                return 'Family_Cell'
            else:
                return 'Cell'
        elif isinstance(self.game.cells_field[y][x], DeadCell):
            return 'Dead'
        elif not self.game.cells_field[y][x]:
            return None

    def update(self, game):
        if self.energy >= self.max_energy:
            self.reproduce()
        elif self.energy <= 0:
            self.kill()
        if self.genome[self.genome_id] == 25:
            self.photosynthesize()
            self.genome_id = (self.genome_id + 1) % 64
            self.energy -= cell_energy_to_live
        elif self.genome[self.genome_id] == 26:
            counter = 0
            while counter < 5 and (self.genome[self.genome_id] == 26 or
                                   self.genome[(self.genome_id + 1) % 64] == 26 or
                                   (self.genome[(self.genome_id + 1) % 64] not in cells_commands
                                    and self.genome[(self.genome_id + self.genome[
                                           self.genome_id + 1]) % 64] == 26)):
                self.move()
                if self.genome[(self.genome_id + 1) % 64] == 26:
                    self.genome_id = (self.genome_id + 1) % 64
                else:
                    self.genome_id = (self.genome_id + self.genome[
                        self.genome_id + 1]) % 64
                counter += 1
            self.energy -= cell_energy_to_live
        elif self.genome[self.genome_id] not in cells_commands:
            self.genome_id = (self.genome_id + self.genome[self.genome_id]) % 64
        print(self.game.cells_group)

    def reproduce(self):
        coords_list = []
        for i in range(0, 2):
            x = self.x + (-1) ** i
            y = self.y + (-1) ** i
            if self.can_move(x, self.y):
                coords_list.append((self.y, x))
            if self.can_move(self.x, y):
                coords_list.append((y, self.x))
        if len(coords_list):
            coords = coords_list[randint(0, len(coords_list) - 1)]
            self.game.cells_field[coords[0]][coords[1]] = \
                Cell([coords[0], coords[1]], self.game, self)
        else:
            self.game.cells_group.remove(self)
            # super().kill()
            self.game.cells_field[self.y][self.x] = DeadCell((self.y, self.x), game)

            return
        self.energy = 250
        # self.kill()

    def photosynthesize(self):
        self.energy += game.energy_field[self.y][self.x]['photosynthesis']

    def kill(self):
        self.game.cells_field[self.y][self.x] = None
        super().kill()


def run_with_thread(func, *args, **kwargs):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()


def update_cells(sprites_list, *args, **kwargs):
    for cell in sprites_list:
        run_with_thread(cell.update, *args, **kwargs)


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("My Game")
        self.screen = pygame.display.set_mode((window_width, window_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 220
        self.energy_field = numpy.array([[{'photosynthesis': 5} for i in range(90)] for j in range(
            60)])
        self.cells_field = numpy.array([[None for i in range(window_width // 10)] for j in range(
            window_height // 10)])
        self.cells_group = SpriteGroup()

        # self.previous_cells_field = self.cells_field
        # self.generate_cells()
        # for i in range(40):
        #     self.cells_field[i][i + 1] = Cell((i, i + 1), self)
        self.cells_field[10][9] = Cell((10, 9), self)
        self.cells_field[9][10] = Cell((9, 10), self)
        self.cells_field[10][10] = Cell((10, 10), self)
        self.cells_field[11][10] = Cell((11, 10), self)
        self.cells_field[10][11] = Cell((10, 11), self)
        self.cells_field[11][11] = Cell((11, 11), self)
        self.dead_cells_group = SpriteGroup()
        self.dead_cells_field = pygame.Surface((window_width, window_height))
        self.dead_cells_field.fill((140, 140, 140))
        # for i in range(0, 2):
        #     self.cells_field[10][10 + (-1) ** i] = Cell((10, 10 + (-1) ** i), self)
        # for i in range(0, 2):
        #     self.cells_field[10 + (-1) ** i][10] = Cell((10 + (-1) ** i, 10), self)

    def generate_cells(self):
        for i in range(window_height // 10):
            for j in range(window_width // 10):
                if randint(0, 1):
                    self.cells_field[i][j] = Cell((i, j), self)

    def run(self):
        while self.running:
            self.draw()
            self.update()
            # self.previous_cells_field = self.cells_field
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            # self.clock.tick(self.fps)
            pygame.display.flip()

    def update(self):
        for cell in self.cells_group:
            cell.update(self)

    def draw(self):
        self.cells_group.draw(self.screen)
        self.dead_cells_group.draw(self.screen)


if __name__ == "__main__":
    game = Game()
    game.run()
pygame.quit()
