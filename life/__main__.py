"""Module __main__. Entry point."""
__author__ = 'Joan A. Pinol  (japinol)'
__version__ = '1.0.1'

from argparse import ArgumentParser
import gc
import logging
import traceback

import pygame as pg

from life import constants as consts
from life.life_game import Game
from life.settings import (
    SCREEN_MIN_WIDTH,
    SCREEN_MIN_HEIGHT,
    SCREEN_MAX_WIDTH,
    SCREEN_MAX_HEIGHT,
    CELL_MIN_SIZE,
    CELL_MAX_SIZE,
    )
from life.seeds import seeds
from tests.test_life import TestLife


logging.basicConfig(format=consts.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    """Entry point of the Life program."""
    # Parse optional arguments from the command line
    parser = ArgumentParser(description="Conway's Game of Life with colors.",
                            prog="life",
                            usage="%(prog)s [-h] [-c CELLSIZE] [-m] [-o] [-u] [-w WIDTHSCREEN]\n"
                            f"{' '*12}[-e HEIGHTSCREEN] [-f] [-s SPEED] [-n] [-i] [-k SEEDS]\n"
                            f"{' '*12}[-v OUTFILE] [-x] [-l LOGFILE] [-a] [-j] [-p STOPAFTER]\n"
                            f"{' '*12}[-y] [-z] [-zz] [-t] [-ts]\n")
    parser.add_argument('-c', '--cellsize', default=None,
                        help='the size of each cell. '
                             f'Must be between {CELL_MIN_SIZE} and {CELL_MAX_SIZE}.')
    parser.add_argument('-m', '--emptyuniverse', default=False, action='store_true',
                        help='start with an empty universe.')
    parser.add_argument('-o', '--onecolor', default=False, action='store_true',
                        help='use one color, the way the classic Conway\'s Game of Life does.')
    parser.add_argument('-u', '--toroidaluniverse', default=False, action='store_true',
                        help='the universe is represented by a toroidal array instead of a flat one.')
    parser.add_argument('-w', '--widthscreen', default=None,
                        help='the width of the screen. \n'
                             f'Must be between {SCREEN_MIN_WIDTH} and {SCREEN_MAX_WIDTH}.')
    parser.add_argument('-e', '--heightscreen', default=None,
                        help='the height of the screen.\n'
                             f'Must be between {SCREEN_MIN_HEIGHT} and {SCREEN_MAX_HEIGHT}.')
    parser.add_argument('-f', '--fullscreen', default=False, action='store_true',
                        help='start the game in full screen mode.')
    parser.add_argument('-s', '--speed', default=None,
                        help='change the speed of each generation. \n'
                             'It will calculate a generation every N seconds if possible.')
    parser.add_argument('-n', '--editnotallowed', default=False, action='store_true',
                        help='will not allow edit the universe by changing the value of a cell.')
    parser.add_argument('-i', '--startimmediately', default=False, action='store_true',
                        help='start calculating generations with the initial seed/s immediately.')
    parser.add_argument('-k', '--seeds', default=None,
                        help='use specified starting seeds and their positions. \n'
                              f'Usage: --seeds "SEED1 Y_POS X_POS, SEED2 Y_POS X_POS" \n'
                              f'Example: --seeds "beacon 10 15, clock 20 15" \n'
                              f"You can use these seeds: \n"
                              f"{', '.join([x for x in seeds])}.")
    parser.add_argument('-v', '--outfile', default=None,
                        help='output file where there will be written the results \n'
                              'when -save generations to file- is activated.')
    parser.add_argument('-x', '--savetofile', default=False, action='store_true',
                        help='save generations to output file.')
    parser.add_argument('-l', '--logfile', default=None,
                        help='output log file where the results will be written.')
    parser.add_argument('-a', '--auto', default=False, action='store_true',
                        help='automatic mode. The following actions are not allowed: \n'
                             'Stop generations, pause generations, calculate \n'
                             'only the next generation, show graphic help screen, \n'
                             'edit the board, change the shape of the universe, \n'
                             'clean or reset the universe, change full/normal screen... \n'
                             'Also, you must press ESC or Quit 4 times to exit the life game. \n'
                             'Also, activates start immediately flag. \n'
                             'This option it is useful for benchmark purposes and more.')
    parser.add_argument('-j', '--exitauto', default=False, action='store_true',
                        help='exit immediately if the automatic mode is on.')
    parser.add_argument('-p', '--stopafter', default=None,
                        help='stop generations after the N one.')
    parser.add_argument('-y', '--timeinoutfile', default=False, action='store_true',
                        help='save current time in output file for each generation.')
    parser.add_argument('-z', '--statsoff', default=False, action='store_true',
                        help='deactivate statistics for total dead cells and current cells alive.')
    parser.add_argument('-zz', '--statsnogui', default=False, action='store_true',
                        help='even if statistics are activated, do not reflect the middle '
                             'calculations on the GUI. Only draw the last one.')
    parser.add_argument('-t', '--debugtraces', default=False, action='store_true',
                        help='show debug back traces information when something goes wrong.')
    parser.add_argument('-ts', '--testsuite', default=False, action='store_true',
                        help='execute the test suite and exit. \n'
                             'This test suite tests 2 universes in their flat and toroidal versions. \n'
                             'They just create each universe, calculate the first 550 generations, \n'
                             'save the results in the output file and compare these results \n'
                             'with previous output files that are correct.')
    args = parser.parse_args()

    if args.testsuite:
        # Run the test suite
        try:
            test_life = TestLife()
            test_life.main()
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            logger.critical(f'Error: {e}')
        return

    pg.init()
    # Multiple games loop
    while not Game.is_exit_game:
        try:
            game = Game(screen_width=args.widthscreen,
                        screen_height=args.heightscreen,
                        full_screen=args.fullscreen,
                        cell_size=args.cellsize,
                        toroidal_universe=args.toroidaluniverse,
                        empty_universe=args.emptyuniverse,
                        cell_one_color=args.onecolor,
                        edit_not_allowed=args.editnotallowed,
                        start_immediately=args.startimmediately,
                        starting_seeds=args.seeds,
                        stop_after_generation=args.stopafter,
                        out_file=args.outfile,
                        save_to_out_file=args.savetofile,
                        log_file=args.logfile,
                        auto_play=args.auto,
                        time_in_out_file=args.timeinoutfile,
                        stats_deactivated=args.statsoff,
                        stats_no_middle_calc_gui=args.statsnogui,
                        speed=args.speed,
                        exit_auto_when_auto_play=args.exitauto)
            if not Game.is_exit_game:
                game.start()
                del game
                gc.collect()
        except FileNotFoundError as e:
            if args.debugtraces:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'File not found error: {e}')
            break
        except Exception as e:
            if args.debugtraces:
                traceback.print_tb(e.__traceback__)
            logger.critical(f'Error: {e}')
            break
    pg.quit()


if __name__ == '__main__':
    logger.info(consts.LOG_START_APP_MSG)
    main()
    logger.info(consts.LOG_END_APP_MSG)
