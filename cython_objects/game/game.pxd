from cython_objects.game.myspritegroup.myspritegroup cimport  MySpriteGroup
from cython_objects.configs.configs cimport GameConfig

cdef class Game:
    cdef bint running
    cdef unsigned long int cell_number
    cdef public list energy_field, cells_field
    cdef public object pipe
    cdef GameConfig config

    cdef public MySpriteGroup cells_group, dead_cells_group
    cdef generate_cells(self)
    cdef public run(self)
    cdef update(self)
    cdef draw(self)
