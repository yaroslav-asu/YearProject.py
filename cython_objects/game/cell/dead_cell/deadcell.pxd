from cython_objects.game.game cimport Game
from cython_objects.game.myspritegroup.mysprite.mysprite cimport MySprite

cdef class DeadCell(MySprite):
    cdef Game game
    cdef int x, y
    cdef list border_color, color
    cdef public kill(self)
