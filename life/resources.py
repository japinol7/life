"""Module resources."""
__author__ = 'Joan A. Pinol  (japinol)'

import os

import pygame as pg

from life.colors import Color
from life import constants as consts
from life import lib_graphics_jp as libg_jp
from life.settings import Settings, SCREEN_MIN_WIDTH, SCREEN_MIN_HEIGHT


def file_name_get(name, subname='', num=None, subnum=None, quality='',
                  folder=consts.BITMAPS_FOLDER):
    return os.path.join(folder,
                        '%s%s%s%s.%s' % (consts.FILE_NAMES['%s%s' % (name, subname)][0],
                                         quality,
                                         num and '_%02i' % num or '',
                                         subnum and '_%02i' % subnum or '',
                                         consts.FILE_NAMES['%s%s' % (name, subname)][1])
                        )


class Resource:
    """Some resources used in the game that do not have their own class."""
    images = {}
    txt_surfaces = {'game_paused': None,
                    'press_intro_to_continue': None,
                    }

    @classmethod
    def render_text_frequently_used(cls):
        # Render text
        libg_jp.render_text('PAUSED', 150 + Settings.screen_width // 2, Settings.screen_height // 2,
                            cls.txt_surfaces, 'game_paused', color=Color.RED,
                            size=int(196*Settings.font_pos_factor), align="center")
        libg_jp.render_text('– Press Escape to Exit –', Settings.screen_width // 2,
                            (Settings.screen_height // 2) - int(6 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'exit_current_game_confirm', color=Color.RED,
                            size=int(64*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text('– Press Enter to Continue –', Settings.screen_width // 2,
                            (Settings.screen_height // 2) + int(82 * Settings.font_pos_factor_t2),
                            cls.txt_surfaces, 'press_intro_to_continue', color=Color.RED,
                            size=int(64*Settings.font_pos_factor_t2), align="center")
        libg_jp.render_text("– GAME OVER. It's a Tie –", Settings.screen_width // 2,
                            Settings.screen_height // 2,
                            cls.txt_surfaces, 'game_tied', color=Color.RED,
                            size=int(80*Settings.font_pos_factor), align="center")

    @classmethod
    def load_and_render_background_images(cls):
        # Load and render background images and effects.
        img = pg.Surface((Settings.screen_width, Settings.screen_height)).convert_alpha()
        img.fill((0, 0, 0, 15))
        cls.images['dim_screen'] = img

        if Settings.screen_width == SCREEN_MIN_WIDTH and Settings.screen_height == SCREEN_MIN_HEIGHT:
            im_background = 'im_background'
            im_screen_help = 'im_screen_help'
        else:
            im_background = 'im_background_hd'
            im_screen_help = 'im_screen_help_hd'

        img = pg.image.load(file_name_get(name=im_background, subname='')).convert()
        cls.images['background'] = img

        img = pg.image.load(file_name_get(name=im_screen_help, subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width_adjusted,
                                             Settings.screen_height_adjusted))
        cls.images['screen_help'] = img

        img = pg.image.load(file_name_get(name='im_bg_gray1', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_gray1'] = img

        img = pg.image.load(file_name_get(name='im_bg_gray2', subname='')).convert()
        img = pg.transform.smoothscale(img, (Settings.screen_width, Settings.screen_height))
        cls.images['bg_gray2'] = img

        img = pg.image.load(file_name_get(name='im_help_key', subname='')).convert()
        img = pg.transform.smoothscale(img, (int((Settings.help_key_size.w)
                                                 * Settings.font_pos_factor_t2),
                                             int(Settings.help_key_size.h
                                                 * Settings.font_pos_factor_t2)))
        cls.images['help_key'] = img

        img = pg.image.load(file_name_get(name='im_logo_japinol', subname='')).convert()
        img = pg.transform.smoothscale(img, (int((Settings.logo_jp_std_size.w)
                                                 * Settings.font_pos_factor_t2),
                                             int(Settings.logo_jp_std_size.h
                                                 * Settings.font_pos_factor_t2)))
        cls.images['logo_jp'] = img
