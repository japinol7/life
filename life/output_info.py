"""Module output_info."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import OrderedDict
from datetime import datetime

from life import lib_jp
from life.output_file import OutputFile
from life.settings import Settings


class OutputInfo(OutputFile):
    """Manages information for output to file purposes."""

    def __init__(self, game):
        self._out_file = Settings.out_file
        super().__init__(self._out_file)
        self.game = game
        self.write_time = Settings.time_in_out_file
        self.generations_to_save = 0
        self._num_errors_out_file = 0

    def write_head(self):
        out_dict = OrderedDict([
                    ('time', str(datetime.now()) if self.write_time else "<deactivated>"),
                    ('full screen', Settings.is_full_screen),
                    ('screen size', self.game.size),
                    ('speed', Settings.fps),
                    ('toroidal universe', Settings.toroidal_universe),
                    ('one color', Settings.cell_one_color),
                    ('cell size', Settings.cell_size),
                    ('dimensions', self.game.universe.size_u),
        ])
        out_info_title = "Conway's Game of Life with colors"
        out_info = '%s%s %s %s\n' % ('\n\n\n', '-' * 25, out_info_title, '-' * 25)
        out_info = '%s%s%s\n' % (out_info, lib_jp.pretty_dict_to_string(out_dict, with_last_new_line=True),
                                 '-' * (25 + len(out_info_title) + 25))
        self.write_line(out_info)
        self._write_data_to_file()

    def write_generation(self):
        out_dict = OrderedDict([
                    ('time', str(datetime.now()) if self.write_time else "<deactivated>"),
                    ('full screen', Settings.is_full_screen),
                    ('toroidal universe', Settings.toroidal_universe),
                    ('one color', Settings.cell_one_color),
                    ('cells', self.game.universe.stats['cells_total']),
                    ('dimensions', self.game.universe.size_u),
                    ('universe', ''.join(['\n', self.game.universe.pprint_to_string()])),
                    ('generation', self.game.universe.generation),
        ])
        out_info_title = 'Current game stats'
        out_info = '%s%s%s%s\n' % ('\n\n\n', '-' * 25, out_info_title, '-' * 25)
        out_info = '%s%s%s\n' % (out_info, lib_jp.pretty_dict_to_string(out_dict, with_last_new_line=True),
                                 '-' * (25 + len(out_info_title) + 25))

        self.write_line(out_info)
        self.generations_to_save += 1
        if self.generations_to_save >= Settings.save_file_buffer_n_iterations:
            self.generations_to_save = 0
            self._write_data_to_file()

    def write_statistics(self):
        out_info = [f"\n{' ' * 3} {'-' * 37}",
                    f"{' ' * 16} Statistics ",
                    f"{' ' * 3} {'-' * 37}",
                    f"{' ' * 5} Last Generation:{self.game.universe.generation:7}\n",
                    f"{' ' * 12} Total Deads     Cells Alive",
                    f"{' ' * 12} -----------     -----------",
                    f"{' ' * 4} Age 1: {self.game.universe.stats['deads_age1']:12}    {self.game.universe.stats['cells_age1']:12}",
                    f"{' ' * 4} Age 2: {self.game.universe.stats['deads_age2']:12}    {self.game.universe.stats['cells_age2']:12}",
                    f"{' ' * 4} Age 3: {self.game.universe.stats['deads_age3']:12}    {self.game.universe.stats['cells_age3']:12}",
                    f"{' ' * 4} Age 4: {self.game.universe.stats['deads_age4']:12}    {self.game.universe.stats['cells_age4']:12}",
                    f"{' ' * 4} Age 5: {self.game.universe.stats['deads_age5']:12}    {self.game.universe.stats['cells_age5']:12}",
                    f"{' ' * 4} Age 6: {self.game.universe.stats['deads_age6']:12}    {self.game.universe.stats['cells_age6']:12}",
                    f"{' ' * 4} Age 7: {self.game.universe.stats['deads_age7']:12}    {self.game.universe.stats['cells_age7']:12}",
                    f"{' ' * 4} Age 8+:{self.game.universe.stats['deads_age8']:12}    {self.game.universe.stats['cells_age8']:12}",
                    f"{' ' * 29}-----------",
                    f"{' ' * 8} Total cells alive: {self.game.universe.stats['cells_total']:12}",
                    f"{' ' * 3} {'-' * 37}",
                    ]
        self.write_line('\n'.join(out_info))

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
        if Settings.stats_activated:
            self.write_statistics()
        super().write_buffer_before_exit()

    def change_state_manually(self, activated):
        Settings.save_to_out_file = activated
        if activated:
            self.write_line("-**- Activated manually -**-\n")
        else:
            self.write_line("-**- Deactivated manually -**-\n")
