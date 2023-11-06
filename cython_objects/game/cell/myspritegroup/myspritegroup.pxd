from cython_objects.game.cell.myspritegroup.mysprite.mysprite cimport MySprite

cdef class MySpriteGroup:
    cdef public dict sprites

    cdef public add(self, MySprite sprite)

    cdef add_internal(self, MySprite sprite)

    cdef has_internal(self, MySprite sprite)
    cdef public remove(self, MySprite sprite)
    cdef public remove_internal(self, MySprite sprite)