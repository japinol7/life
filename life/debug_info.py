"""Module debug_info."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import OrderedDict
from datetime import datetime

from life import lib_jp
from life.output_file import OutputFile
from life.settings import Settings


class DebugInfo(OutputFile):
    """Manages information used for debug and log purposes."""

    def __init__(self, game):
        self._out_file = Settings.log_file
        super().__init__(self._out_file)
        self.game = game
        self.text_blocks_to_save = 0

    def print_help_keys(self):
        print('  ^;: \t ^ñ interactive debug output (not available)\n'
              '  ^d: \t print debug information to console\n'
              '  ^l: \t write debug information to log file\n'
              )

    def write_head(self):
        debug_dict = OrderedDict([
                    ('time', str(datetime.now())),
                    ('full screen', Settings.is_full_screen),
                    ('screen size', self.game.size),
                    ('speed', Settings.fps),
                    ('toroidal universe', Settings.toroidal_universe),
                    ('one color', Settings.cell_one_color),
                    ('cell size', Settings.cell_size),
                    ('dimensions', self.game.universe.size_u),
        ])
        debug_info_title = "Conway's Game of Life with colors"
        debug_info = '%s%s %s %s\n' % ('Log file.\n\n\n', '-' * 25, debug_info_title, '-' * 25)
        debug_info = '%s%s%s\n' % (debug_info, lib_jp.pretty_dict_to_string(debug_dict, with_last_new_line=True),
                                   '-' * (25 + len(debug_info_title) + 25))
        self.write_line(debug_info)
        self._write_data_to_file()

    def print_debug_info(self, to_log_file=False):
        debug_dict = OrderedDict([
                    ('time', str(datetime.now())),
                    ('full screen', Settings.is_full_screen),
                    ('screen size', self.game.size),
                    ('speed', Settings.fps),
                    ('toroidal universe', Settings.toroidal_universe),
                    ('one color', Settings.cell_one_color),
                    ('cells_sprites', self.game.cells),
                    ('cells', self.game.universe.stats['cells_total']),
                    ('cell size', Settings.cell_size),
                    ('dimensions', self.game.universe.size_u),
                    ('-----' * 3, ''),
                    ('universe', ''.join(['\n', self.game.universe.pprint_to_string()])),
                    ('generation', self.game.universe.generation),
        ])
        debug_info_title = "Current Game of Life's stats"
        debug_info = '%s%s%s%s\n' % ('\n\n\n', '-' * 25, debug_info_title, '-' * 25)
        debug_info = '%s%s%s\n' % (debug_info, lib_jp.pretty_dict_to_string(debug_dict, with_last_new_line=True),
                                   '-' * (25 + len(debug_info_title) + 25))
        if to_log_file:
            self.write_line(debug_info)
            self.text_blocks_to_save += 1
            if self.text_blocks_to_save >= Settings.save_file_buffer_n_iterations:
                self.text_blocks_to_save = 0
                self._write_data_to_file()
        else:
            print(debug_info)

    def write_buffer_before_exit(self):
        """Writes pending buffer to the output file.
        It is intended to be called before exit the application.
        """
        if (self.game.universe.stop_time and Settings.stop_after_generation
                and Settings.auto_play and Settings.start_immediately
                and Settings.time_in_out_file):
            self.write_line("-**- total_nano_seconds since last start: "
                            f"{self.game.universe.stop_time - self.game.universe.start_time:,}"
                            f"   :: Last generation: {self.game.universe.generation}  -**-\n")
        super().write_buffer_before_exit()
