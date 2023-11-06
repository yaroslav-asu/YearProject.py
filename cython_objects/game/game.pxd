from cython_objects.game.cell.myspritegroup.myspritegroup cimport  MySpriteGroup
cdef class Game:
    cdef bint running
    cdef unsigned long int cell_number
    cdef public list energy_field, cells_field
    cdef public object pipe
    cdef public object csv_writer

    cdef public MySpriteGroup cells_group, dead_cells_group
    cdef generate_cells(self)
    cdef public run(self)
    cdef update(self)
    cdef draw(self)
