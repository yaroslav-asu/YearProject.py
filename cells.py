from random import randint, random

import numpy

from variables import *


def normalize_coords(*args):
    if len(args) == 1:
        args = args[0][0], args[0][1]
    x = args[0] % (window_width // cell_size)
    y = args[1]
    return x, y


class DeadCell(pygame.sprite.Sprite):
    def __init__(self, coords, game):
        super().__init__()
        self.game = game
        self.x = coords[1]
        self.y = coords[0]
        self.game.dead_cells_group.add(self)
        # self.color = [150, 150, 150]
        self.color = [190, 190, 190]
        self.border_color = (80, 80, 80)
        self.image = pygame.Surface((cell_size, cell_size))
        self.rect = pygame.Rect(self.x, self.y, cell_size, cell_size)
        pygame.draw.rect(self.image, self.color, (0, 0, cell_size, cell_size))
        # pygame.draw.rect(self.image, self.border_color, (0, 0, cell_size, cell_size))
        # pygame.draw.rect(self.image, self.color, (1, 1, cell_size - 2, cell_size - 2))
        # self.game.cells_field_image.add(self.image, self.x, self.y)
        self.game.screen_queue.send(('add_cell_to_screen', (self.color, self.border_color, self.x,
                                                      self.y)))

    def kill(self):
        self.game.cells_field[self.y][self.x] = None
        # self.game.cells_field_image.delete(self.x, self.y)
        self.game.screen_queue.send(('delete_cell_from_screen', (self.x, self.y)))
        super().kill()


class Cell(pygame.sprite.Sprite):
    genome: numpy.array

    def __init__(self, coords, game, parent=None, color=[20, 150, 20]):
        super().__init__()
        game.cells_group.add(self)
        self.x = coords[1]
        self.y = coords[0]
        self.color = color
        # self.border_color = (80, 80, 80)
        self.border_color = color
        self.game = game
        self.energy = start_cell_energy
        self.max_energy = max_cell_energy
        self.genome_id: int = 0
        self.degree = randint(0, 7) * 45
        self.children_counter = 0
        self.recursion_counter = 0

        self.actions_count = cells_number_of_available_actions
        self.image = pygame.Surface((cell_size, cell_size))
        create_border(self.image, self.border_color)
        pygame.draw.rect(self.image, self.color, (1, 1, cell_size - 2, cell_size - 2))
        self.rect = pygame.Rect(self.x * cell_size, self.y * cell_size, cell_size, cell_size)

        # self.game.cells_field_image.add(self.image, self.x, self.y)
        self.game.screen_queue.send(('add_cell_to_screen', (self.color, self.border_color, self.x,
                                                     self.y)))
        self.from_sun_energy_counter = 0
        self.from_cells_energy_counter = 0
        self.from_minerals_energy_counter = 0

        self.actions_dict = {
            21: self.get_self_energy,
            22: self.look_in_front,
            23: self.change_degree,
            24: self.get_energy_from_mineral,
            25: self.photosynthesize,
            26: self.move,
            27: self.bite
        }

        if not parent:
            self.genome = numpy.array([25 for i in range(64)], numpy.int8)
            # self.genome = numpy.array([randint(0, 64) for i in range(64)], numpy.int8)
        else:
            self.genome = parent.genome.copy()
            if random() < 0.25:
                self.genome[randint(0, 63)] = randint(1, 63)

            # main_genome = parent.genome.copy()
            # genome = main_genome.copy()
            # if random() < 0.9:
            #     counter = 0
            #     genome[randint(0, 63)] = randint(1, 63)
            #     while self.check_recursion(genome):
            #         genome = main_genome.copy()
            #         genome[randint(0, 63)] = randint(1, 63)
            #         counter += 1
            #     if counter:
            #         print(counter)
            # self.genome = genome

    @staticmethod
    def check_recursion(genome):
        was_ids = set()
        was_actions = set()
        action_id = 0
        while action_id not in was_ids:
            was_ids.add(action_id)
            if genome[action_id] in [24, 25, 27]:
                was_actions.add(action_id)
                action_id = (action_id + 1) % 64
            else:
                action_id = (genome[action_id] + action_id) % 64
        if was_actions:
            return False
        else:
            return True

    def change_color(self):
        maximum_color_id = 0
        colors = [self.from_cells_energy_counter,
                  self.from_sun_energy_counter,
                  self.from_minerals_energy_counter]
        if any(colors):
            for color_id in range(0, 3):
                if colors[color_id] > colors[maximum_color_id]:
                    maximum_color_id = color_id
            self.color[maximum_color_id] = 150
            for color_id in list({0, 1, 2} - {maximum_color_id}):
                self.color[color_id] = int(colors[color_id] / colors[maximum_color_id] * 150)

    def bite(self):
        in_front_coords = self.in_front_position()
        in_front_obj = self.get_object_from_coords(in_front_coords)
        if in_front_obj == 'Cell' or in_front_obj == 'DeadCell' or in_front_obj == 'FamilyCell':
            self.game.cells_field[in_front_coords[1]][in_front_coords[0]].kill()
            self.energy += energy_for_cell_eat
            self.from_cells_energy_counter += 1

    def do_action(self, action_id):
        self.recursion_counter += 1
        if self.recursion_counter > 15:
            self.kill()
            return
        try:
            if action_id in self.actions_dict.keys():
                if self.actions_count - actions_costs[action_id] >= 0:
                    if action_id == 23:
                        self.actions_dict[action_id]((self.genome[(self.genome_id + 1) % 64] % 8)
                                                     * 45)
                    else:
                        self.actions_dict[action_id]()

                    self.actions_count -= actions_costs[action_id]
                    self.genome_id = (self.genome_id + 1) % 64
                    self.do_action(self.genome[self.genome_id])

                else:
                    self.energy -= cell_energy_to_live
                    self.actions_count = cells_number_of_available_actions
            else:
                self.genome_id = (self.genome_id + self.genome[(self.genome_id + 1) % 64]) % 64
                self.do_action(self.genome[self.genome_id])

        except RecursionError:
            print("recErr", self.recursion_counter)
            print(self.genome)
            self.kill()
            return
        # self.recursion_counter = 0

    def in_front_position(self):
        if self.degree == 0:
            coords = normalize_coords(self.x + 1, self.y)
        elif self.degree == 1 * 45:
            coords = normalize_coords(self.x + 1, self.y + 1)
        elif self.degree == 2 * 45:
            coords = normalize_coords(self.x, self.y + 1)
        elif self.degree == 3 * 45:
            coords = normalize_coords(self.x - 1, self.y + 1)
        elif self.degree == 4 * 45:
            coords = normalize_coords(self.x - 1, self.y)
        elif self.degree == 5 * 45:
            coords = normalize_coords(self.x - 1, self.y - 1)
        elif self.degree == 6 * 45:
            coords = normalize_coords(self.x, self.y - 1)
        elif self.degree == 7 * 45:
            coords = normalize_coords(self.x + 1, self.y - 1)
        return coords

    def change_degree(self, degree):
        self.degree = (self.degree + degree) % 360

    def get_self_energy(self):
        if self.energy < self.genome[(self.genome_id + 1) % 64]:
            self.do_action(25)
        else:
            self.genome_id = (self.genome_id + 1) % 64
            self.do_action(self.genome_id)

    def look_in_front(self):
        coords = self.in_front_position()
        in_front_obj = self.get_object_from_coords(*coords)
        if in_front_obj == 'Cell':
            coefficient = 2
        elif in_front_obj == 'DeadCell':
            coefficient = 3
        elif in_front_obj == 'FamilyCell':
            coefficient = 4
        elif in_front_obj == 'Wall':
            coefficient = 5
        elif not in_front_obj:
            coefficient = 6
        action_id = self.genome[(self.genome_id + coefficient) % 64]
        self.do_action(action_id)

    def move(self):
        start_x, start_y = self.x, self.y
        self.change_degree((self.genome[(self.genome_id + 1) % 64] % 8) * 45)
        in_front_coords = self.in_front_position()
        if self.can_move(in_front_coords):
            self.x, self.y = in_front_coords
        if start_x != self.x or start_y != self.y:
            # self.game.cells_field_image.move(start_x, start_y, self.x, self.y, self.image)
            self.game.screen_queue.send(('move_cell_on_screen', (start_x, start_y, self.x, self.y,
                                                                self.color, self.border_color
                                                                )))
            self.rect.x, self.rect.y = self.x * cell_size, self.y * cell_size
            self.game.cells_field[start_y][start_x] = None
            self.game.cells_field[self.y][self.x] = self

    def can_move(self, *args):
        if len(args) == 1:
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]

        if 0 <= y < window_height // cell_size and \
            not self.get_object_from_coords(x % (window_width // cell_size), y):
            return True
        else:
            return False

    def get_object_from_coords(self, *args):
        if len(args) == 1:
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]

        if y < 0 or y >= (window_height // cell_size):
            return 'Wall'
        if isinstance(self.game.cells_field[y][x], Cell):
            counter = 0
            for i in self.genome == self.game.cells_field[y][x]:
                if not i:
                    counter += 1
                    if counter > 1:
                        break
            if counter == 1:
                return 'FamilyCell'
            else:
                return 'Cell'
        elif isinstance(self.game.cells_field[y][x], DeadCell):
            return 'DeadCell'
        elif not self.game.cells_field[y][x]:
            return None

    def update(self, game):
        self.change_color()
        if self.energy >= self.max_energy:
            self.reproduce()
            pass
        elif self.energy <= 0:
            self.kill()
            return
        # self.change_color()
        self.do_action(self.genome[self.genome_id])
        self.recursion_counter = 0

    def reproduce(self):
        coords_list = []
        for i in range(0, 2):
            x = (self.x + (-1) ** i + window_width // cell_size) % (window_width // cell_size)
            y = self.y + (-1) ** i
            if self.can_move(x, self.y):
                coords_list.append((self.y, x))
            if self.can_move(self.x, y):
                coords_list.append((y, self.x))
        if len(coords_list):
            coords = coords_list[randint(0, len(coords_list) - 1)]
            self.game.cells_field[coords[0]][coords[1]] = \
                Cell([coords[0], coords[1]], self.game, self, self.color)
        else:
            self.game.cells_group.remove(self)
            # super().kill()
            self.game.cells_field[self.y][self.x] = DeadCell((self.y, self.x), self.game)
            return
        self.energy = start_cell_energy

        self.children_counter += 1
        if self.children_counter == 4:
            self.kill()
            return

    def photosynthesize(self):
        self.energy += self.game.energy_field[self.y][self.x]['sun']
        self.from_sun_energy_counter += 1

    def get_energy_from_mineral(self):
        self.energy += self.game.energy_field[self.y][self.x]['minerals']
        self.from_minerals_energy_counter += 1

    def kill(self):
        self.game.cells_field[self.y][self.x] = None
        self.game.screen_queue.send(('delete_cell_from_screen', (self.x, self.y)))
        super().kill()
