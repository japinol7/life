"""Module life_game."""
__author__ = 'Joan A. Pinol  (japinol)'
__all__ = ["Game"]

import logging

import pygame as pg

from life.cells import CellBase, CellZoom
from life.cell_selectors import CellSelector
from life.colors import Color
from life import constants as consts
from life.debug_info import DebugInfo
from life.help_info import HelpInfo
from life import lib_graphics_jp as libg_jp
from life.output_info import OutputInfo
from life.settings import Settings, NextGenerationType, UniverseCalculationType
from life.resources import Resource
from life import screens
from life.universes import Universe

logging.basicConfig(format=consts.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Game:
    """Represents a Game Of Life game."""
    is_exit_game = False
    is_over = False
    is_first_game = True
    current_game = 0
    current_time = None
    active_sprites = None
    size = None
    screen = None
    screen_flags = None
    normal_screen_flags = None
    full_screen_flags = None

    def __init__(self, screen_width=None, screen_height=None,
                 full_screen=None, cell_size=None,
                 toroidal_universe=False, empty_universe=None,
                 cell_one_color=False, edit_not_allowed=False,
                 start_immediately=False, starting_seeds=None,
                 stop_after_generation=None,
                 save_to_out_file=False,
                 out_file=None, log_file=None,
                 auto_play=False,
                 time_in_out_file=False,
                 stats_deactivated=False,
                 stats_no_middle_calc_gui=False,
                 speed=None,
                 exit_auto_when_auto_play=False):
        self.name = "Life v 1.01"
        self.name_short = "Life"
        self.start_time = None
        self.universe = None
        self.cell_selector = None
        self.cell_zoom = None
        self.done = None
        self.next_generation = NextGenerationType.NONE
        self.is_paused = False
        self.is_full_screen_switch = False
        self.is_help_screen = False
        self.is_exit_curr_game_confirm = False
        self.calc_stats = False
        self.show_fps = False
        self.show_grid = False
        self.clock = None
        self.help_info = None
        self.debug_info = None
        self.output_info = None
        self.screen_exit_current_game = None
        self.screen_game_over = None
        self.screen_pause = None
        self.screen_help = None
        self.exit_auto = False
        self.is_exit_game_count = 0

        Game.is_exit_game = False
        if Game.current_game > 0:
            Game.is_first_game = False

        if Game.is_first_game:
            # Calculate settings
            pg_display_info = pg.display.Info()
            Settings.display_start_width = pg_display_info.current_w
            Settings.display_start_height = pg_display_info.current_h
            Settings.calculate_settings(screen_width=screen_width,
                                        screen_height=screen_height,
                                        full_screen=full_screen,
                                        cell_size=cell_size,
                                        empty_universe=empty_universe,
                                        toroidal_universe=toroidal_universe,
                                        cell_one_color=cell_one_color,
                                        edit_not_allowed=edit_not_allowed,
                                        start_immediately=start_immediately,
                                        starting_seeds=starting_seeds,
                                        stop_after_generation=stop_after_generation,
                                        out_file=out_file,
                                        save_to_out_file=save_to_out_file,
                                        log_file=log_file,
                                        auto_play=auto_play,
                                        time_in_out_file=time_in_out_file,
                                        stats_deactivated=stats_deactivated,
                                        stats_no_middle_calc_gui=stats_no_middle_calc_gui,
                                        speed=speed,
                                        exit_auto_when_auto_play=exit_auto_when_auto_play)
            # Set screen to the settings configuration
            Game.size = [Settings.screen_width, Settings.screen_height]
            Game.full_screen_flags = pg.FULLSCREEN | pg.DOUBLEBUF | pg.HWSURFACE
            Game.normal_screen_flags = pg.DOUBLEBUF | pg.HWSURFACE
            if Settings.is_full_screen:
                Game.screen_flags = Game.full_screen_flags
            else:
                Game.screen_flags = Game.normal_screen_flags
            Game.screen = pg.display.set_mode(Game.size, Game.screen_flags)
            # Load and render resources
            Resource.load_and_render_background_images()

            # Render characters in some colors to use it as a cache
            libg_jp.chars_render_text_tuple()

        # Initialize screens
        self.screen_exit_current_game = screens.ExitCurrentGame(self)
        self.screen_help = screens.Help(self)
        self.screen_pause = screens.Pause(self)
        self.screen_game_over = screens.GameOver(self)

        # Initialize groups of sprites
        self.active_sprites = pg.sprite.LayeredUpdates()
        self.cells = pg.sprite.Group()
        self.cell_selectors = pg.sprite.Group()
        self.cell_zooms = pg.sprite.Group()

    def set_is_exit_game(self, is_exit_game):
        Game.is_exit_game = is_exit_game

    def draw_grid(self):
        for x in range(self.universe.rect.x, self.universe.pos_limit.x, Settings.cell_size):
            pg.draw.line(Game.screen, Color.GRAY, (x, self.universe.rect.y),
                         (x, self.universe.pos_limit.y))
        for y in range(self.universe.rect.y, self.universe.pos_limit.y, Settings.cell_size):
            pg.draw.line(Game.screen, Color.GRAY, (self.universe.rect.x, y), (self.universe.pos_limit.x, y))

    def initialize_the_universe(self):
        # Initialize the universe
        Universe.init()
        CellSelector.init()
        CellBase.init()
        self.universe = Universe(game=self)
        self.cell_selector = CellSelector(self)
        self.cell_zoom = CellZoom(147, 782, self)

    def update_stats(self):
        pos_y = 374
        for i in range(1, 9):
            deads = self.universe.stats[f'deads_age{i}']
            alive = self.universe.stats[f'cells_age{i}']
            pos_y += 37
            libg_jp.draw_text_rendered(text=f'{deads if deads <= 9999999 else "#######"}',
                                       x=130, y=pos_y, screen=Game.screen, color=Color.BLUE)
            libg_jp.draw_text_rendered(text=f'{alive if alive <= 99999 else "#####"}',
                                       x=234, y=pos_y, screen=Game.screen, color=Color.BLUE)

        total_alive = self.universe.stats['cells_total']
        libg_jp.draw_text_rendered(text=f'{total_alive if total_alive <= 999999 else "######"}',
                                   x=222, y=714, screen=Game.screen, color=Color.BLUE)

    def update_screen(self):
        # Handle game screens
        if self.is_paused or self.is_full_screen_switch:
            self.screen_pause.start_up(is_full_screen_switch=self.is_full_screen_switch)
        if self.is_help_screen:
            self.screen_help.start_up()
        elif self.is_exit_curr_game_confirm:
            self.screen_exit_current_game.start_up()
        elif Game.is_over:
            self.screen_game_over.start_up()
            if not self.writen_info_game_over_to_file:
                self.write_game_over_info_to_file()
        else:
            if not Game.is_over:
                Game.screen.blit(Resource.images['background'], (0, 0))
            else:
                Game.screen.blit(Resource.images['bg_gray1'], (0, 0))

            if not Game.is_over:
                # Draw generation
                libg_jp.draw_text_rendered(text=f'{self.universe.generation}',
                                           x=215, y=315, screen=Game.screen, color=Color.BLUE)
                # Draw stats
                if (Settings.stats_activated
                    and (Settings.stats_middle_calc_gui or
                         self.next_generation != NextGenerationType.SEVERAL)):
                    self.update_stats()
                # Draw active sprites
                self.active_sprites.draw(Game.screen)
                if not Settings.cell_selector_hide:
                    self.cell_selectors.draw(Game.screen)
                    self.cell_zooms.draw(Game.screen)

            self.show_grid and self.draw_grid()

        self.show_fps and pg.display.set_caption(f"{self.clock.get_fps():.2f}")

    def start(self):
        Game.is_exit_game = False
        Game.is_over = False
        Game.current_game += 1
        pg.display.set_caption(self.name_short)
        self.clock = pg.time.Clock()
        self.start_time = pg.time.get_ticks()

        self.initialize_the_universe()

        # Render text frequently used only if it is the first game
        if Game.is_first_game:
            Resource.render_text_frequently_used()

        self.help_info = HelpInfo()
        self.debug_info = DebugInfo(self)
        self.output_info = OutputInfo(self)

        if not Settings.edit_allowed or not Settings.empty_universe:
            Settings.cell_selector_hide = True

        if Settings.start_immediately:
            self.next_generation = NextGenerationType.SEVERAL

        # Current game loop
        self.done = False
        while not self.done:
            self.current_time = pg.time.get_ticks()
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    if not Settings.auto_play:
                        self.is_exit_curr_game_confirm = True
                    else:
                        self.is_exit_game_count += 1
                        if self.is_exit_game_count >= 4:
                            self.done = True
                            Game.is_exit_game = True
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_p:
                        if not Settings.auto_play:
                            self.is_paused = True
                    elif event.key == pg.K_SPACE:
                        if not Settings.auto_play:
                            if self.next_generation == NextGenerationType.SEVERAL:
                                self.next_generation = NextGenerationType.NONE
                            else:
                                self.next_generation = NextGenerationType.SEVERAL
                                self.universe.start_time = pg.time.get_ticks()
                    elif event.key == pg.K_n:
                        if not Settings.auto_play:
                            if self.next_generation == NextGenerationType.ONE:
                                self.next_generation = NextGenerationType.NONE
                            else:
                                self.next_generation = NextGenerationType.ONE
                                self.universe.start_time = pg.time.get_ticks()
                    elif event.key == pg.K_LEFT:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.cell_selector.go_left(speed_mult=4)
                        else:
                            self.cell_selector.go_left()
                    elif event.key == pg.K_RIGHT:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.cell_selector.go_right(speed_mult=4)
                        else:
                            self.cell_selector.go_right()
                    elif event.key == pg.K_UP:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.cell_selector.go_up(speed_mult=4)
                        else:
                            self.cell_selector.go_up()
                    elif event.key == pg.K_DOWN:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.cell_selector.go_down(speed_mult=4)
                        else:
                            self.cell_selector.go_down()
                    elif event.key == pg.K_h:
                        if pg.key.get_mods() & pg.KMOD_LCTRL:
                            self.help_info.print_help_keys()
                            self.debug_info.print_help_keys()
                    elif event.key == pg.K_d:
                        if not Settings.auto_play:
                            if pg.key.get_mods() & pg.KMOD_LCTRL:
                                self.debug_info.print_debug_info()
                    elif event.key == pg.K_l:
                        if not Settings.auto_play:
                            if pg.key.get_mods() & pg.KMOD_LCTRL:
                                self.debug_info.print_debug_info(to_log_file=True)
                    elif event.key == pg.K_F1:
                        if not Settings.auto_play:
                            if not self.is_exit_curr_game_confirm:
                                self.is_help_screen = not self.is_help_screen
                    elif event.key == pg.K_s:
                        Settings.cell_selector_hide = not Settings.cell_selector_hide
                    elif event.key == pg.K_o:
                        if not Settings.auto_play:
                            Settings.cell_one_color = not Settings.cell_one_color
                            self.universe.set_universe_colors(Settings.cell_one_color)
                    elif event.key == pg.K_r:
                        if not Settings.auto_play:
                            Settings.empty_universe = False
                            Settings.start_immediately = Settings.start_immediately_initial_value
                            self.done = True
                    elif event.key == pg.K_c:
                        if not Settings.auto_play:
                            Settings.empty_universe = True
                            Settings.start_immediately = False
                            self.done = True
                    elif event.key == pg.K_t:
                        if not Settings.auto_play:
                            if Settings.toroidal_universe:
                                Settings.toroidal_universe = False
                                Settings.universe_calculation = UniverseCalculationType.TOROIDAL_LOOP
                            else:
                                Settings.toroidal_universe = True
                                Settings.universe_calculation = UniverseCalculationType.NON_TOROIDAL_FAST
                            self.universe.set_universe_calculate_generation()
                    elif event.key == pg.K_j:
                        if not Settings.auto_play:
                            self.output_info.change_state_manually(activated=not Settings.save_to_out_file)
                    elif event.key == pg.K_b:
                        if not Settings.auto_play:
                            if pg.key.get_mods() & pg.KMOD_LCTRL:
                                self.output_info.write_buffer()
                                self.debug_info.write_buffer()
                    elif event.key == pg.K_k:
                        if not Settings.auto_play:
                            if pg.key.get_mods() & pg.KMOD_LCTRL:
                                Settings.stats_activated and self.output_info.write_statistics()
                    elif event.key == pg.K_g:
                        if not Settings.auto_play:
                            if pg.key.get_mods() & pg.KMOD_LCTRL and pg.key.get_mods() & pg.KMOD_RALT:
                                self.show_grid = not self.show_grid
                    elif event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                        if pg.key.get_mods() & pg.KMOD_ALT:
                            if not Settings.auto_play:
                                self.is_paused = True
                                self.is_full_screen_switch = True
                        else:
                            if Settings.edit_allowed and not Settings.cell_selector_hide:
                                self.universe.switch_cell()
                elif event.type == pg.KEYUP:
                    self.cell_selector.stop()
                    if event.key == pg.K_F5:
                        self.show_fps = not self.show_fps

            # Update sprites
            if not self.is_paused:
                self.active_sprites.update()
                if not Settings.cell_selector_hide:
                    self.cell_selector.update()
                    self.cell_zoom.update()
            if self.exit_auto:
                self.done = True
                Game.is_exit_game = True
            self.update_screen()
            self.clock.tick(Settings.fps if self.next_generation != NextGenerationType.NONE else Settings.fps_paused)

            pg.display.flip()

        # Actions to take immediately before exiting the game
        self.debug_info.write_buffer_before_exit()
        self.output_info.write_buffer_before_exit()
