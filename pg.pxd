cdef class MySprite:
    cdef dict __g

    cdef kill(self)

    cdef add_internal(self, group)


cdef class MySpriteGroup:
    cdef dict sprites

    cdef public add(self, MySprite sprite)

    cdef add_internal(self, sprite)

    cdef has_internal(self, sprite)

    cdef remove_internal(self, sprite)