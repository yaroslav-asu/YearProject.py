from game cimport Game
from mysprite cimport MySprite

# from pygameclassesi cimport MySprite


cdef class Cell(MySprite):
    cdef int x, y, degree, energy, max_energy, genome_id, children_counter, recursion_counter, \
        actions_count, from_sun_energy_counter, from_cells_energy_counter, \
        from_minerals_energy_counter
    cdef list color, border_color, genome
    cdef Game game
    cdef dict actions_dict
    @staticmethod
    cdef check_recursion(list genome)
    cdef change_color(self)
    cdef bite(self)
    cdef do_action(self, int action_id)
    cdef in_front_position(self)
    cdef change_degree(self, int degree)
    cdef get_self_energy(self)
    cdef look_in_front(self)
    cdef move(self)
    cdef can_move(self, list args)
    cdef get_object_from_coords(self, list args)
    cdef update(self, Game game)
    cdef reproduce(self)
    cdef photosynthesize(self)
    cdef get_energy_from_mineral(self)
    cdef kill(self)
