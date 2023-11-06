from cython_objects.game.myspritegroup.mysprite.mysprite cimport MySprite

cdef class MySpriteGroup:
    def __init__(self):
        self.sprites = {}

    cdef public add(self, MySprite sprite):
        if isinstance(sprite, MySprite):
            if not self.has_internal(sprite):
                self.add_internal(sprite)
                sprite.add_internal(self)

    cdef add_internal(self, MySprite sprite):
        self.sprites[sprite] = 0

    cdef has_internal(self, MySprite  sprite):
        return sprite in self.sprites

    cdef public remove(self, MySprite sprite):
        if sprite in self.sprites:
            self.remove_internal(sprite)

    cdef public remove_internal(self, MySprite  sprite):
        del self.sprites[sprite]
        # pass

    def __iter__(self):
        return iter(self.sprites.copy())
