"""Module settings."""
__author__ = 'Joan A. Pinol  (japinol)'

from enum import Enum, auto
import os

from life import lib_jp
from life.seeds import seeds as seeds_seeds

SCREEN_MAX_WIDTH = 1920
SCREEN_MAX_HEIGHT = 1080
SCREEN_MIN_WIDTH = 1700
SCREEN_MIN_HEIGHT = 959

CELL_DEFAULT_SIZE = 10
CELL_MAX_SIZE = 10
CELL_MIN_SIZE = 4
CELL_ZOOM_DEFAULT_SIZE = 19

FPS_DEFAULT = 400
FPS_MIN = 15
FPS_MAX = 500

OUT_FILE_DEFAULT = os.path.join('output', 'output.txt')
LOG_FILE_DEFAULT = os.path.join('files', 'log.txt')


STARTING_SEEDS_DEFAULT = [
    ['sparker_101', (4, 3)],
    ['boat', (5, 55)],
    ['beacon', (24, 6)],
    ['diehard', (37, 18)],
    ['pentomino_o', (8, 46)],
    ['pentomino_v', (30, 44)],
    ['clock', (34, 6)],
    ['block_switch_engine', (18, 34)],
    ['spaceship_25p3h1v0.1', (40, 44)],
    ['blinkers_bit_pole', (55, 60)],
    ['explode_small', (58, 88)],
    ['pentomino_u', (42, 92)],
    ['circle_of_fire', (6, 84)],
    ['quad_pole', (26, 86)],
    ['pulsar', (60, 105)],
    ['spaceship_heavy', (78, 107)],
    ['pentomino_w', (16, 114)],
    ['clock', (85, 4)],
]


class UniverseCalculationType(Enum):
    """Generation calculation types."""
    NON_TOROIDAL_FAST = auto()
    TOROIDAL_LOOP = auto()
    NON_TOROIDAL_LOOP = auto()


class NextGenerationType(Enum):
    """Next generation types."""
    NONE = auto()
    ONE = auto()
    SEVERAL = auto()


class SettingsException(Exception):
    pass


class Settings:
    """Settings of the game."""
    screen_width = None
    screen_height = None
    screen_aspect_ratio = None
    screen_height_adjusted = None
    screen_width_adjusted = None
    display_start_width = None    # max. width of the user's initial display mode
    display_start_height = None   # max. height of the user's initial display mode
    cell_size = None
    cell_zoom_size = None
    universe_pos = None
    universe_size = None
    universe_calculation = None
    toroidal_universe = None
    empty_universe = None
    cell_one_color = None
    cell_selector_hide = False
    edit_allowed = True
    out_file = None
    save_to_out_file = False
    auto_play = False
    time_in_out_file = False
    log_file = None
    save_file_buffer_n_iterations = None
    fps = None
    fps_paused = None
    start_immediately = False
    start_immediately_initial_value = False
    exit_auto_when_auto_play = False
    starting_seeds = None
    stop_after_generation = None
    stats_activated = True
    stats_middle_calc_gui = True
    is_full_screen = False
    screen_near_top = None
    screen_near_bottom = None
    screen_near_right = None
    grid_width = None
    grid_height = None
    font_size1 = None
    font_size2 = None
    font_spc_btn_chars1 = None
    font_spc_btn_chars2 = None
    font_pos_factor = None
    font_pos_factor_t2 = None
    logo_jp_std_size = None
    help_key_size = None

    @classmethod
    def clean(cls):
        cls.screen_width = 1700
        cls.screen_height = 959
        cls.screen_aspect_ratio = cls.screen_width / cls.screen_height
        cls.screen_height_adjusted = None
        cls.screen_width_adjusted = None
        cls.universe_pos = lib_jp.Point(x=320, y=55)
        cls.universe_size = lib_jp.Size(w=137, h=90)
        cls.universe_calculation = UniverseCalculationType.NON_TOROIDAL_FAST
        cls.toroidal_universe = False
        cls.empty_universe = False
        cls.cell_one_color = False
        cls.cell_selector_hide = False
        cls.cell_size = CELL_DEFAULT_SIZE
        cls.cell_zoom_size = CELL_ZOOM_DEFAULT_SIZE
        cls.cell_size_ratio = cls.screen_width * cls.screen_height / CELL_DEFAULT_SIZE
        cls.edit_allowed = True
        cls.out_file = OUT_FILE_DEFAULT
        cls.save_to_out_file = False
        cls.auto_play = False
        cls.time_in_out_file = False
        cls.log_file = LOG_FILE_DEFAULT
        cls.save_file_buffer_n_iterations = 150
        cls.fps = FPS_DEFAULT
        cls.fps_paused = 15
        cls.start_immediately = False
        cls.start_immediately_initial_value = False
        cls.exit_auto_when_auto_play = False
        cls.starting_seeds = None
        cls.stop_after_generation = 0
        cls.stats_activated = True
        cls.stats_middle_calc_gui = True
        cls.is_full_screen = False
        cls.screen_near_top = None
        cls.screen_near_bottom = None
        cls.screen_near_right = None
        cls.grid_width = None
        cls.grid_height = None
        cls.logo_jp_std_size = lib_jp.Size(w=244, h=55)
        cls.help_key_size = lib_jp.Size(w=218, h=57)
        cls.font_size1 = None
        cls.font_size2 = None
        cls.font_spc_btn_chars1 = None
        cls.font_spc_btn_chars2 = None
        cls.font_pos_factor = 1                   # position or size factor for some text to render
        cls.font_pos_factor_t2 = 1                # position or size factor for some other text to render
        cls.logo_jp_std_size = lib_jp.Size(w=244, h=55)
        cls.help_key_size = lib_jp.Size(w=218, h=57)

    @classmethod
    def calculate_settings(cls, screen_width=None,
                           screen_height=None,
                           full_screen=None,
                           cell_size=None,
                           toroidal_universe=False,
                           empty_universe=False,
                           cell_one_color=False,
                           edit_not_allowed=False,
                           out_file=None,
                           save_to_out_file=False,
                           auto_play=False,
                           time_in_out_file=False,
                           log_file=None,
                           start_immediately=False,
                           starting_seeds=None,
                           stop_after_generation=None,
                           stats_deactivated=False,
                           stats_no_middle_calc_gui=False,
                           speed=None,
                           exit_auto_when_auto_play=False):

        def _calculate_max_screen_size(screen_width, screen_height):
            screen_max_width = min([SCREEN_MAX_WIDTH, cls.display_start_width])
            screen_max_height = min([SCREEN_MAX_HEIGHT, cls.display_start_height])
            if screen_width and screen_width.isdigit():
                cls.screen_width = int(screen_width)
                if cls.screen_width < SCREEN_MIN_WIDTH:
                    cls.screen_width = SCREEN_MIN_WIDTH
                elif cls.screen_width > screen_max_width:
                    cls.screen_width = screen_max_width
                if not screen_height or not screen_height.isdigit():
                    cls.screen_height = int(cls.screen_width / cls.screen_aspect_ratio)
                    if cls.screen_height > screen_max_height:
                        cls.screen_height = screen_max_height
            if screen_height and screen_height.isdigit():
                cls.screen_height = int(screen_height)
                if cls.screen_height < SCREEN_MIN_HEIGHT:
                    cls.screen_height = SCREEN_MIN_HEIGHT
                elif cls.screen_height > screen_max_height:
                    cls.screen_height = screen_max_height
                    cls.screen_width = int(cls.screen_height * cls.screen_aspect_ratio)
                if not screen_width or not screen_width.isdigit():
                    cls.screen_width = int(cls.screen_height * cls.screen_aspect_ratio)

        def validate_starting_seeds(starting_seeds):
            res = []
            seeds_with_pos = starting_seeds.strip().split(',')
            for seed_with_pos in seeds_with_pos:
                seeds = seed_with_pos.strip().split()
                if not seeds_seeds.get(seeds[0]):
                    raise SettingsException(f"Starting seed not found: {seeds[0]}")
                try:
                    pos_y = int(seeds[1])
                    pos_x = int(seeds[2])
                except Exception as _:
                    raise SettingsException(f'coordinates for seed {seeds[0]} '
                                            'must be integers. Example: {seeds[0]} 10 20')

                seed_h = len(seeds_seeds[seeds[0]])
                seed_w = len(seeds_seeds[seeds[0]][0])
                pos_h = pos_y + seed_h
                pos_w = pos_x + seed_w
                if pos_y < 0 or pos_h > cls.universe_size.h:
                    raise SettingsException(f'y coordinate for seed {seeds[0]} must be '
                                            f'between 0 and {cls.universe_size.h-seed_h}. Example: {seeds[0]} 10 20')
                if pos_x < 0 or pos_w > cls.universe_size.w:
                    raise SettingsException(f'y coordinate for seed {seeds[0]} must be '
                                            f'between 0 and {cls.universe_size.w-seed_w}. Example: {seeds[0]} 10 20')
                res += [[seeds[0], (pos_y, pos_x)]]
            return res

        cls.clean()
        # Define screen values to resize the screen and images if necessary
        _calculate_max_screen_size(screen_width, screen_height)
        cls.screen_width_adjusted = int(cls.screen_height * cls.screen_aspect_ratio)
        cls.screen_height_adjusted = cls.screen_height
        # Resize adjusted screen values for images if they are too high
        if cls.screen_height_adjusted > cls.screen_height:
            cls.screen_width_adjusted -= cls.screen_height_adjusted - cls.screen_height
            cls.screen_height_adjusted -= cls.screen_height_adjusted - cls.screen_height
        if cls.screen_width_adjusted > cls.screen_width:
            cls.screen_height_adjusted -= cls.screen_width_adjusted - cls.screen_width
            cls.screen_width_adjusted -= cls.screen_width_adjusted - cls.screen_width
        # Set full screen or windowed screen
        cls.is_full_screen = True if full_screen else False
        # Resize cell
        if cell_size and cell_size.isdigit():
            cls.cell_size = int(cell_size)
            if cls.cell_size < CELL_MIN_SIZE:
                cls.cell_size = CELL_MIN_SIZE
            elif cls.cell_size > CELL_MAX_SIZE:
                cls.cell_size = CELL_MAX_SIZE
            # Calculate universe size for the current cell size
            cls.universe_size = lib_jp.Size(w=cls.universe_size.w * CELL_DEFAULT_SIZE // cls.cell_size,
                                            h=cls.universe_size.h * CELL_DEFAULT_SIZE // cls.cell_size)

        cls.cell_one_color = cell_one_color

        cls.toroidal_universe = toroidal_universe
        if cls.toroidal_universe:
            cls.universe_calculation = UniverseCalculationType.TOROIDAL_LOOP

        cls.empty_universe = empty_universe
        cls.edit_allowed = not edit_not_allowed
        cls.start_immediately = start_immediately
        cls.save_to_out_file = save_to_out_file
        cls.auto_play = auto_play
        cls.time_in_out_file = time_in_out_file
        cls.stats_activated = not stats_deactivated
        cls.stats_middle_calc_gui = not stats_no_middle_calc_gui

        if cls.auto_play:
            cls.edit_allowed = False
            cls.start_immediately = True
            cls.exit_auto_when_auto_play = exit_auto_when_auto_play

        if starting_seeds:
            cls.starting_seeds = validate_starting_seeds(starting_seeds)
            cls.empty_universe = False

        if not cls.empty_universe and not cls.starting_seeds:
            cls.starting_seeds = STARTING_SEEDS_DEFAULT

        if out_file and str(out_file).strip():
            cls.out_file = str(out_file).strip()

        if log_file and str(log_file).strip():
            cls.log_file = str(log_file).strip()

        if stop_after_generation and stop_after_generation.isdigit():
            cls.stop_after_generation = int(stop_after_generation)

        if not cls.stats_activated:
            cls.stats_middle_calc_gui = False

        if cls.empty_universe:
            cls.stop_after_generation = 0
            cls.auto_play = False
            cls.edit_allowed = True
            cls.start_immediately = False

        cls.start_immediately_initial_value = cls.start_immediately

        # Set fps
        if speed and speed.isdigit():
            cls.fps = int(speed)
            if cls.fps < FPS_MIN:
                cls.fps = FPS_MIN
            elif cls.fps > FPS_MAX:
                cls.fps = FPS_MAX

        # Font sizes for scores, etc
        cls.font_size1 = 18
        cls.font_size2 = 36
        cls.font_spc_btn_chars1 = 12
        cls.font_spc_btn_chars2 = 21
