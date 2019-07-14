"""Module cells."""
__author__ = 'Joan A. Pinol  (japinol)'

import pygame as pg

from life import lib_jp
from life import resources
from life.settings import Settings


class CellBase(pg.sprite.Sprite):
    """Represents a Cell Base.
    It is not intended to be instantiated directly.
    """
    size = None
    added_size = lib_jp.Size(w=0, h=0)  # Added size to the defined cell size.
    sprite_images = {}
    CELL_AGES_MAX = 9
    CELL_AGE_MAX_OLD = 15
    CELL_AGE_ONE_COLOR = 7

    def __init__(self, x, y, game, age=1):
        super().__init__()
        self.x = x
        self.y = y
        self.age = age
        self.age_total = age
        self.game = game
        self.images_sprite_no = CellBase.CELL_AGES_MAX

        if not CellBase.sprite_images:
            for i in range(self.images_sprite_no):
                image = pg.image.load(resources.file_name_get(name='im_cell_age', num=i)).convert()
                image = pg.transform.smoothscale(image, CellBase.size)
                image_zoom = pg.transform.smoothscale(image, (Settings.cell_zoom_size, Settings.cell_zoom_size))
                CellBase.sprite_images[i] = (image, image_zoom)

        if Settings.cell_one_color:
            self.image = CellBase.sprite_images[CellBase.CELL_AGE_ONE_COLOR if self.age else 0][0]
        else:
            self.image = CellBase.sprite_images[self.age][0]

        self.rect = self.image.get_rect()

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.cell_size + cls.added_size.w,
                               h=Settings.cell_size + cls.added_size.h)


class Cell(CellBase):
    """Represents a Cell in the universe."""

    def __init__(self, x, y, game, age=1):
        super().__init__(x, y, game, age)
        self.rect.x = Settings.universe_pos.x + (x * Cell.size.w)
        self.rect.y = Settings.universe_pos.y + (y * Cell.size.h)

        # Add cell to the active sprite list
        self.game.active_sprites.add(self, layer=1)
        # Add cell to the group of all cells
        self.game.cells.add(self)

    def update(self):
        # Change the frame according to the cell's age
        if Settings.cell_one_color:
            self.image = Cell.sprite_images[Cell.CELL_AGE_ONE_COLOR if self.age else 0][0]
        else:
            self.image = Cell.sprite_images[self.age][0]


class CellZoom(CellBase):
    """Represents a zoom of a cell in the universe."""

    def __init__(self, x, y, game, age=1):
        super().__init__(x, y, game, age)
        self.rect.x = x
        self.rect.y = y

        # Add cell to the group of cell zooms
        self.game.cell_zooms.add(self)

    def update(self):
        # Change the frame according to the selected cell's age
        if Settings.cell_one_color:
            self.image = CellZoom.sprite_images[CellZoom.CELL_AGE_ONE_COLOR
                                            if self.game.universe.cell_selected_age() else 0][1]
        else:
            self.image = CellZoom.sprite_images[self.game.universe.cell_selected_age()][1]
