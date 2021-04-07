from random import randint, random

import numpy
import pygame
from variables import *


class DeadCell(pygame.sprite.Sprite):
    def __init__(self, coords, game):
        super().__init__()
        self.game = game
        self.x = coords[1]
        self.y = coords[0]
        self.game.dead_cells_group.add(self)
        self.color = (150, 150, 150)
        self.border_color = (80, 80, 80)
        self.image = pygame.Surface((10, 10))
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        pygame.draw.rect(self.image, self.border_color, (0, 0, 10, 10))
        pygame.draw.rect(self.image, self.color, (1, 1, 8, 8))
        self.game.cells_field_image.add(self.image, self.x, self.y)


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
        self.actions_count = number_of_available_actions
        self.image = pygame.Surface((10, 10))
        create_border(self.image, self.border_color)
        # pygame.draw.rect(self.image, self.border_color, (0, 0, 10, 10))
        pygame.draw.rect(self.image, self.color, (1, 1, 8, 8))
        self.rect = pygame.Rect(self.x * 10, self.y * 10, 10, 10)

        self.game.cells_field_image.add(self.image, self.x, self.y)
        # self.photosynthesized = 0
        # self.cells_eaten = 0
        self.actions_dict = {
            25: self.photosynthesize,
            26: self.move
        }

        directions = ['up', 'down', 'left', 'right']
        self.direction = directions[randint(0, 3)]

        if not parent:
            self.genome = numpy.array([25 for i in range(64)], numpy.int8)
            # self.genome = numpy.array([randint(0, 64) for i in range(64)], numpy.int8)
        else:
            if random() < 0.25:
                self.genome = parent.genome
                # self.genome[randint(0, 63)] = randint(0, 63)
                self.genome[randint(0, 63)] = randint(25, 26)
            else:
                self.genome = parent.genome

    def do_action(self, action_id):
        try:
            if action_id in self.actions_dict.keys():
                if self.actions_count - actions_costs[action_id] >= 0:
                    self.actions_dict[action_id]()
                    self.genome_id = (self.genome_id + 1) % 64
                    self.actions_count -= actions_costs[action_id]
                    self.do_action(self.genome[self.genome_id])
                else:
                    self.energy -= cell_energy_to_live
                self.actions_count = number_of_available_actions
            else:
                self.genome_id = (self.genome_id + self.genome[(self.genome_id + 1) % 64]) % 64
                self.do_action(self.genome[self.genome_id])
        except RecursionError:
            print('RecErr')

    def move(self):
        start_x, start_y = self.x, self.y
        # print(self.x, self.y, self.game.cells_field.size())
        self.game.cells_field[self.y][self.x] = None
        if self.direction == 'left' and self.can_move(self.x - 1, self.y):
            # self.x = (self.x + window_width // 10 - 1) % (window_width // 10)
            self.x = (self.x - 1) % (window_width // 10)
        elif self.direction == 'right' and self.can_move(self.x + 1, self.y):
            self.x = (self.x + 1) % (window_width // 10)
        elif self.direction == 'up' and self.can_move(self.x, self.y - 1):
            self.y -= 1
        elif self.direction == 'down' and self.can_move(self.x, self.y + 1):
            self.y += 1
        if start_x != self.x or start_y != self.y:
            self.game.cells_field_image.move(start_x, start_y, self.x, self.y, self.image)
        self.rect.x, self.rect.y = self.x * 10, self.y * 10
        self.game.cells_field[self.y][self.x] = self

    def can_move(self, x, y):
        if 0 <= y < window_height // 10 and \
            not self.get_object_from_coords(x % (window_width // 10), y):
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
        self.do_action(self.genome[self.genome_id])

    def reproduce(self):
        coords_list = []
        for i in range(0, 2):
            x = (self.x + (-1) ** i + window_width // 10) % (window_width // 10)
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
            self.game.cells_field[self.y][self.x] = DeadCell((self.y, self.x), self.game)

            return
        self.energy = 250
        # self.kill()

    def photosynthesize(self):
        self.energy += self.game.energy_field[self.y][self.x]['photosynthesis']

    def kill(self):
        self.game.cells_field[self.y][self.x] = None
        self.game.cells_field_image.delete(self.x, self.y)
        super().kill()
