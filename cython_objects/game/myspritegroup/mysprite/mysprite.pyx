from cython_objects.game.myspritegroup.myspritegroup cimport MySpriteGroup

cdef class MySprite:
    def __init__(self):
        self.__g = {}

    cdef kill(self):
        for group in self.__g:
            MySpriteGroup.remove(group, self)
        self.__g.clear()

    cdef add_internal(self, group):
        self.__g[group] = 0
