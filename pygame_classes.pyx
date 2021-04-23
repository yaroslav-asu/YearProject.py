from operator import truth

import pygame
from libcpp cimport bool

cdef class Sprite:
    cdef dict __g
    def __init__(self):
        self.__g = {}

    cdef add(self, group):
        has = self.__g.__contains__
        if hasattr(group, '_spritegroup'):
            if not has(group):
                group.add_internal(self)
                self.add_internal(group)
        else:
            self.add(group)

    cdef remove(self, groups):
        has = self.__g.__contains__
        for group in groups:
            if hasattr(group, '_spritegroup'):
                if has(group):
                    group.remove_internal(self)
                    self.remove_internal(group)
            else:
                self.remove(group)

    cdef add_internal(self, group):
        self.__g[group] = 0

    cdef remove_internal(self, group):
        del self.__g[group]

    cdef kill(self):
        for group in self.__g:
            group.remove_internal(self)
        self.__g.clear()

    cdef groups(self):
        return list(self.__g)

    cdef alive(self):
        return truth(self.__g)

    cdef __repr__(self):
        return "<%s Sprite(in %d groups)>" % (self.__class__.__name__,
                                              len(self.__g))

    @property
    cdef layer(self):
        return getattr(self, '_layer')

    @layer.setter
    cdef layer(self, value):
        if not self.alive():
            setattr(self, '_layer', value)
        else:
            raise AttributeError("Can't set layer directly after "
                                 "adding to group. Use "
                                 "group.change_layer(sprite, new_layer) "
                                 "instead.")

cdef class AbstractGroup:
    _spritegroup = True

    def __init__(self):
        self.spritedict = {}
        self.lostsprites = []

    cdef sprites(self):
        return list(self.spritedict)

    cdef add_internal(self,
                     sprite  # noqa pylint: disable=unused-argument; supporting legacy derived classes that override in non-pythonic way
                     ):
        self.spritedict[sprite] = 0

    cdef remove_internal(self, sprite):
        lost_rect = self.spritedict[sprite]
        if lost_rect:
            self.lostsprites.append(lost_rect)
        del self.spritedict[sprite]

    cdef has_internal(self, sprite):
        return sprite in self.spritedict

    cdef copy(self):
        return self.__class__(self.sprites()) # noqa pylint: disable=too-many-function-args; needed because copy() won't work on AbstractGroup

    cdef __iter__(self):
        return iter(self.sprites())

    cdef __contains__(self, sprite):
        return self.has(sprite)

    cdef add(self, sprite):
        if isinstance(sprite, Sprite):
            if not self.has_internal(sprite):
                self.add_internal(sprite)
                sprite.add_internal(self)
        else:
            try:
                self.add(sprite)
            except (TypeError, AttributeError):
                if hasattr(sprite, '_spritegroup'):
                    for spr in sprite.sprites():
                        if not self.has_internal(spr):
                            self.add_internal(spr)
                            spr.add_internal(self)
                elif not self.has_internal(sprite):
                    self.add_internal(sprite)
                    sprite.add_internal(self)

    cdef remove(self, sprite):

        if isinstance(sprite, Sprite):
            if self.has_internal(sprite):
                self.remove_internal(sprite)
                sprite.remove_internal(self)
        else:
            try:
                self.remove(sprite)
            except (TypeError, AttributeError):
                if hasattr(sprite, '_spritegroup'):
                    for spr in sprite.sprites():
                        if self.has_internal(spr):
                            self.remove_internal(spr)
                            spr.remove_internal(self)
                elif self.has_internal(sprite):
                    self.remove_internal(sprite)
                    sprite.remove_internal(self)

    cdef has(self, sprite):
        if not sprite:
            return False  # return False if no sprites passed in

        if isinstance(sprite, Sprite):
            # Check for Sprite instance's membership in this group
            if not self.has_internal(sprite):
                return False
        else:
            try:
                if not self.has(sprite):
                    return False
            except (TypeError, AttributeError):
                if hasattr(sprite, '_spritegroup'):
                    for spr in sprite.sprites():
                        if not self.has_internal(spr):
                            return False
                else:
                    if not self.has_internal(sprite):
                        return False

        return True

    cdef draw(self, surface):
        sprites = self.sprites()
        if hasattr(surface, "blits"):
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits((spr.image, spr.rect) for spr in sprites)
                )
            )
        else:
            for spr in sprites:
                self.spritedict[spr] = surface.blit(spr.image, spr.rect)
        self.lostsprites = []

    cdef clear(self, surface, bgd):
        if callable(bgd):
            for lost_clear_rect in self.lostsprites:
                bgd(surface, lost_clear_rect)
            for clear_rect in self.spritedict.values():
                if clear_rect:
                    bgd(surface, clear_rect)
        else:
            surface_blit = surface.blit
            for lost_clear_rect in self.lostsprites:
                surface_blit(bgd, lost_clear_rect, lost_clear_rect)
            for clear_rect in self.spritedict.values():
                if clear_rect:
                    surface_blit(bgd, clear_rect, clear_rect)

    cdef empty(self):
        for sprite in self.sprites():
            self.remove_internal(sprite)
            sprite.remove_internal(self)

    cdef __nonzero__(self):
        return truth(self.sprites())

    cdef __len__(self):
        return len(self.sprites())

    cdef __repr__(self):
        return "<%s(%d sprites)>" % (self.__class__.__name__, len(self))


cdef class Group(AbstractGroup):

    def __init__(self, sprites):
        AbstractGroup.__init__(self)
        self.add(sprites)



cdef class SpriteGroup(Group):

    cdef render(self, screen):
        self.draw(screen)


