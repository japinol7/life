"""Module constants."""
__author__ = 'Joan A. Pinol  (japinol)'

import os
import sys


LOGGER_FORMAT = '%(asctime)s %(levelname)s %(name)s: %(message)s'


# If the code is frozen, use this path:
if getattr(sys, 'frozen', False):
    CURRENT_PATH = sys._MEIPASS
    BITMAPS_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'img')
    FONT_FOLDER = os.path.join(CURRENT_PATH, 'assets', 'data')
    FONT_DEFAULT_NAME = os.path.join(FONT_FOLDER, 'sans.ttf')
else:
    BITMAPS_FOLDER = os.path.join('assets', 'img')
    FONT_DEFAULT_NAME = os.path.join('assets', 'data', 'sans.ttf')


FILE_NAMES = {
                'im_cell_age': ('cell_age', 'png'),
                'im_cell_selector': ('cell_selector', 'png'),
                'im_bg_start_game': ('bg_start_game', 'png'),
                'im_background': ('background', 'png'),
                'im_background_hd': ('background_1920', 'png'),
                'im_bg_gray1': ('background_gray1', 'png'),
                'im_bg_gray2': ('background_gray2', 'png'),
                'im_bg_blue_t1': ('bg_blue_t1', 'png'),
                'im_bg_blue_t2': ('bg_blue_t2', 'png'),
                'im_bg_black_t1': ('bg_black_t1', 'png'),
                'im_universe': ('universe', 'png'),
                'im_screen_help': ('screen_help_01', 'png'),
                'im_screen_help_hd': ('screen_help_01_1920', 'png'),
                'im_logo_japinol': ('logo_japinol', 'png'),
                'im_help_key': ('help_key', 'png'),
                'im_bg_color': ('background_gray1', 'png'),
            }
