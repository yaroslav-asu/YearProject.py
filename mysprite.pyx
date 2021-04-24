cdef class MySprite:
    def __init__(self):
        self.__g = {}

    cdef kill(self):
        for group in self.__g:
            group.remove_internal(self)
        self.__g.clear()

    cdef add_internal(self, group):
        self.__g[group] = 0