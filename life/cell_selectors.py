"""Module cell_selectors."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from life import lib_jp
from life import resources
from life.settings import Settings


class CellSelector(pg.sprite.Sprite):
    """Represents a cell selector."""
    size = None
    added_size = lib_jp.Size(w=0, h=0)  # Added size to the defined cell size.
    sprite_image = None

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.change_x = 0
        self.change_y = 0
        self.speed = Settings.cell_size

        if not CellSelector.sprite_image:
            image = pg.image.load(resources.file_name_get(name='im_cell_selector')).convert()
            image = pg.transform.smoothscale(image, CellSelector.size)
            CellSelector.sprite_image = image
        else:
            image = CellSelector.sprite_image

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = Settings.universe_pos.x
        self.rect.y = Settings.universe_pos.y
        self.pos_limit_top = lib_jp.Point(x=self.game.universe.rect.x, y=self.game.universe.rect.y)
        self.pos_limit_bottom = lib_jp.Point(x=self.game.universe.pos_limit.x - self.rect.w,
                                             y=self.game.universe.pos_limit.y - self.rect.h)

        # Add cell selector to the cell selectors list
        self.game.cell_selectors.add(self)

    def update(self):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        self.stop()

        # Control universe's limits
        if self.rect.x > self.pos_limit_bottom.x:
            self.rect.x = self.pos_limit_top.x
        elif self.rect.x < self.pos_limit_top.x:
            self.rect.x = self.pos_limit_bottom.x
        if self.rect.y > self.pos_limit_bottom.y:
            self.rect.y = self.pos_limit_top.y
        elif self.rect.y < self.pos_limit_top.y:
            self.rect.y = self.pos_limit_bottom.y

    def go_left(self, speed_mult=1):
        self.change_x = -self.speed * speed_mult
        self.change_y = 0

    def go_right(self, speed_mult=1):
        self.change_x = self.speed * speed_mult
        self.change_y = 0

    def go_up(self, speed_mult=1):
        self.change_y = -self.speed * speed_mult
        self.change_x = 0

    def go_down(self, speed_mult=1):
        self.change_y = self.speed * speed_mult
        self.change_x = 0

    def stop(self):
        self.change_x = 0
        self.change_y = 0

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.added_size.w,
                               h=Settings.cell_size + cls.added_size.h)
