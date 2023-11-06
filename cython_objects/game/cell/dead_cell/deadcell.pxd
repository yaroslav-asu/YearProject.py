from cython_objects.game.game cimport Game

cdef class DeadCell:
    cdef Game game
    cdef int x, y
    cdef public kill(self)