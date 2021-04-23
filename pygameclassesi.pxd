from operator import truth
from libcpp cimport bool
import pygame

cdef class Sprite:
    cdef dict __g

    cdef add(self, group)

    cdef remove(self)

    cdef add_internal(self, group)

    cdef remove_internal(self, group)

    cdef kill(self)

    cdef groups(self)

    cdef alive(self)


cdef class AbstractGroup:
    cdef bool _spritegroup
    cdef dict spritedict
    cdef list lostsprites

    cdef  inline sprites(self):
        return list(self.spritedict)

    cdef  inline add_internal(self,
                     sprite)

    cdef  inline remove_internal(self, sprite)

    cdef inline has_internal(self, sprite)

    cdef inline copy(self)


    cdef inline add(self, sprite)

    cdef inline remove(self, sprite)

    cdef inline has(self, sprite)



    cdef inline draw(self, surface)

    cdef inline clear(self, surface, bgd)

    cdef inline empty(self)




cdef class Group(AbstractGroup)



cdef class SpriteGroup(Group):
    cdef render(self, screen)

