from pg cimport MySprite
cdef class MySprite:
    def __init__(self):
        self.__g = {}

    cdef kill(self):
        for group in self.__g:
            group.remove_internal(self)
        self.__g.clear()

    cdef add_internal(self, group):
        self.__g[group] = 0

cdef class MySpriteGroup:
    def __init__(self):
        self.sprites = {}

    cdef public add(self, MySprite sprite):
        if isinstance(sprite, MySprite):
            if not self.has_internal(sprite):
                self.add_internal(sprite)
                sprite.add_internal(self)

    cdef add_internal(self, sprite):
        self.sprites[sprite] = 0

    cdef has_internal(self, sprite):
        return sprite in self.sprites

    cdef remove_internal(self, sprite):
        del self.sprites[sprite]

    def __iter__(self):
        return iter(self.sprites())