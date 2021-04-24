from myspritegroup cimport  MySpriteGroup
cdef class Game:
    cdef bint running
    cdef int fps
    #
    #
    #
    cdef list energy_field, cells_field

    cdef public MySpriteGroup cells_group, dead_cells_group
    cdef generate_cells(self)
    cdef run(self)
    cdef update(self)
    cdef draw(self)
