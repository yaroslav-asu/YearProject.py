from random import randint, random

from cython_objects.game.cell.dead_cell.deadcell cimport DeadCell
from cython_objects.game.myspritegroup.myspritegroup cimport MySpriteGroup
from cython_objects.configs.configs cimport CellConfig, ScreenConfig

cdef class Cell(MySprite):
    def __cinit__(self):

        self.genome_id: int = 0
        self.degree = randint(0, 7) * 45
        self.children_counter = 0
        self.recursion_counter = 0
        self.from_sun_energy_counter = 0
        self.from_cells_energy_counter = 0
        self.from_minerals_energy_counter = 0

    def __init__(self, list coords, Game game, Cell parent=None, color=[20, 150, 20]):
        super().__init__()
        game.cells_group.add(self)

        self.energy = game.config.cell_config.start_cell_energy
        self.max_energy = game.config.cell_config.max_cell_energy
        self.actions_count = game.config.cell_config.cells_available_actions_count
        self.config = game.config.cell_config

        self.actions_dict = {
            21: self.get_self_energy,
            22: self.look_in_front,
            23: self.change_degree,
            24: self.get_energy_from_mineral,
            25: self.photosynthesize,
            26: self.move,
            27: self.bite
        }
        self.x = coords[1]
        self.y = coords[0]
        self.color = color
        self.border_color = color
        self.game = game
        self.game.pipe.send(('add_cell_to_screen', (self.color, self.border_color, self.x, self.y)))

        if not parent:
            self.genome = [25 for i in range(64)]
        else:
            self.genome = parent.genome.copy()
            if random() < self.config.cell_mutation_chance / 100:
                self.genome[randint(0, 63)] = randint(1, 63)

        self.number = self.game.cell_number
        self.game.cell_number += 1
        if parent:
            parent_num = parent.number
        else:
            parent_num = -1

        self.game.cells_group.add(self)

    cdef public change_color(self):
        sum = self.from_cells_energy_counter + self.from_sun_energy_counter + \
              self.from_minerals_energy_counter
        if all([self.from_cells_energy_counter,
                self.from_sun_energy_counter,
                self.from_minerals_energy_counter]):
            self.color = [
                int(self.from_cells_energy_counter / sum * 250),
                int(self.from_sun_energy_counter / sum * 250),
                int(self.from_minerals_energy_counter / sum * 250)
            ]

    cdef bite(self):
        cdef bint bitten = False
        in_front_coords = self.in_front_position()
        in_front_obj = self.get_object_from_coords(in_front_coords)
        if in_front_obj == 'Cell':
            Cell.kill(self.game.cells_field[in_front_coords[1]][in_front_coords[0]])
            bitten = True
        elif in_front_obj == 'DeadCell':
            DeadCell.kill(self.game.cells_field[in_front_coords[1]][in_front_coords[0]])
            bitten = True
        if bitten:
            self.energy += self.config.eat_gain_energy
            self.from_cells_energy_counter += 1

    cdef do_action(self, int action_id):
        self.recursion_counter += 1
        if self.recursion_counter > 15:
            self.kill()
            return
        try:
            if action_id in self.actions_dict.keys():
                if self.actions_count - self.config.actions_costs[action_id] >= 0:
                    self.actions_dict[action_id](self)

                    self.actions_count -= self.config.actions_costs[action_id]
                    self.genome_id = (self.genome_id + 1) % 64
                    self.do_action(self.genome[self.genome_id])

                else:
                    self.energy -= self.config.cell_energy_to_live
                    self.actions_count = self.config.cells_available_actions_count
            else:
                self.genome_id = (self.genome_id + self.genome[(self.genome_id + 1) % 64]) % 64
                self.do_action(self.genome[self.genome_id])

        except RecursionError:
            print("recErr", self.recursion_counter)
            self.kill()
            return

    cdef in_front_position(self):
        cdef x_delta = 0
        cdef y_delta = 0
        if 0 < self.degree < 180:
            y_delta = 1
        elif 180 < self.degree < 360:
            y_delta = -1

        if self.degree < 90 or 270 < self.degree:
            x_delta = 1
        elif 90 < self.degree < 270:
            x_delta = -1
        return self.normalize_coords([self.x + x_delta, self.y + y_delta])

    cdef change_degree(self):
        self.degree = (self.degree + (self.genome[(self.genome_id + 1) % 64] % 8) * 45) % 360

    cdef get_self_energy(self):
        if self.energy < self.genome[(self.genome_id + 1) % 64]:
            self.do_action(25)
        else:
            self.genome_id = (self.genome_id + 1) % 64
            self.do_action(self.genome_id)

    cdef look_in_front(self):
        coords = self.in_front_position()
        in_front_obj = self.get_object_from_coords(coords)
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

    cdef move(self):
        start_x, start_y = self.x, self.y
        self.change_degree()
        in_front_coords = self.in_front_position()
        if self.can_move(in_front_coords):
            self.x, self.y = in_front_coords
        if start_x != self.x or start_y != self.y:
            self.game.pipe.send(('move_cell_on_screen', (start_x, start_y, self.x, self.y,
                                                         self.color, self.border_color
                                                         )))
            self.game.cells_field[start_y][start_x] = None
            self.game.cells_field[self.y][self.x] = self

    cdef can_move(self, list args):
        if len(args) == 1:
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]

        if 0 <= y < self.config.max_y_id and \
                not self.get_object_from_coords([x % (self.config.max_x_id), y]):
            return True
        else:
            return False

    cdef get_object_from_coords(self, list args):
        if len(args) == 1:
            x, y = args[0][0], args[0][1]
        else:
            x, y = args[0], args[1]

        if y < 0 or y >= (self.config.max_y_id):
            return 'Wall'
        if isinstance(self.game.cells_field[y][x], Cell):
            counter = 0
            for i in range(self.config.genome_size):
                if self.genome[i] != self.game.cells_field[y][x].genome[i]:
                    counter += 1
                    if counter > 1:
                        break
            if counter <= 1:
                return 'FamilyCell'
            else:
                return 'Cell'
        elif isinstance(self.game.cells_field[y][x], DeadCell):
            return 'DeadCell'
        elif not self.game.cells_field[y][x]:
            return None

    cdef public update(self):
        self.change_color()
        if self.energy >= self.max_energy:
            self.reproduce()
            pass
        elif self.energy <= 0:
            self.kill()
            return
        self.do_action(self.genome[self.genome_id])
        self.recursion_counter = 0

    cdef reproduce(self):
        coords_list = []
        for i in range(0, 2):
            x = (self.x + (-1) ** i + self.config.max_x_id) % (self.config.max_x_id)
            y = self.y + (-1) ** i
            if self.can_move([x, self.y]):
                coords_list.append((self.y, x))
            if self.can_move([self.x, y]):
                coords_list.append((y, self.x))
        if len(coords_list):
            coords = coords_list[randint(0, len(coords_list) - 1)]
            self.game.cells_field[coords[0]][coords[1]] = \
                Cell([coords[0], coords[1]], self.game, self, self.color)
        else:
            MySpriteGroup.remove(self.game.cells_group, self)
            # super().kill()
            self.game.cells_field[self.y][self.x] = DeadCell([self.y, self.x], self.game)
            return
        self.energy = self.config.start_cell_energy

        self.children_counter += 1
        if self.children_counter == 4:
            self.kill()
            return

    cdef photosynthesize(self):
        self.energy += self.game.energy_field[self.y][self.x]['sun']
        self.from_sun_energy_counter += 1

    cdef get_energy_from_mineral(self):
        self.energy += self.game.energy_field[self.y][self.x]['minerals']
        self.from_minerals_energy_counter += 1

    cdef public kill(self):
        self.game.cells_field[self.y][self.x] = None
        self.game.pipe.send(('delete_cell_from_screen', (self.x, self.y)))
        MySprite.kill(self)

    def normalize_coords(self, list args):
        if len(args) == 1:
            args = [args[0][0], args[0][1]]
        cdef int x = args[0] % (self.config.max_x_id)
        cdef int y = args[1]
        return [x, y]
