"""Tests package life.
This test suite tests 2 universes in their flat and toroidal versions.
They just create each universe, calculates the first N generations,
saves the results in the output file and compares these results
with previous output files that are correct.

It creates this 4 universes till generation 550:
    > A flat universe starting with the default seeds.
    > A toroidal universe starting with the default seeds.
    > A flat universe starting with the seed:
        > gosper_glider_gun 7 20, clock 75 100.
    > A toroidal universe starting with the seed:
        > gosper_glider_gun 7 20, clock 75 100.

They could be recreated this way:
    $ python -m life --stopafter 550 --auto --savetofile --statsnogui --exitauto
    $ python -m life --toroidaluniverse --stopafter 550 --auto --exitauto
                     --savetofile --statsnogui
    $ python -m life --seeds "gosper_glider_gun 7 20, clock 75 100" --stopafter 550
                     --auto --savetofile --statsnogui --exitauto
    $ python -m life --seeds "gosper_glider_gun 7 20, clock 75 100" --toroidaluniverse
                     --stopafter 550 --auto --savetofile --statsnogui --exitauto

"""

__author__ = 'Joan A. Pinol  (japinol)'

import difflib
import logging
import os
import sys
from zipfile import ZipFile

import pygame as pg

from life import constants as consts
from life.life_game import Game


DIFF_LINES_TO_PRINT = 110

STOP_AFTER_GENERATION = "550"


logging.basicConfig(format=consts.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TestLife():
    """Tests life for some generations."""

    def __init__(self):
        self.test_num = 0
        self.tests_passed = 0
        self.tests_total = 4

    def main(self):
        pg.init()
        self.setUp()

        self.test_flat_universe_seeds_default()
        self.test_toroidal_universe_seeds_default()
        self.test_flat_universe_seeds_g_glider_gun()
        self.test_toroidal_universe_seeds_g_glider_gun()

        logger.info(f"{'-' * 50}")
        logger.info(f"{self.tests_passed} tests passed of {self.tests_total}")

        pg.quit()

    def setUp(self):
        out_file_correct_zip = os.path.join('tests', 'files', 'calculated_tests', 'zip',
                                            'calculated_tests.zip')

        logger.info(f"Unzip correct test files")
        with ZipFile(out_file_correct_zip) as fin_correct_zip:
            fin_correct_zip.extractall(os.path.join('tests', 'files'))

    def test_flat_universe_seeds_default(self):
        test_name = "Game of Life with default seeds in a flat universe."
        out_file = os.path.join('tests', 'files', 'output1.txt')
        out_file_correct = os.path.join('tests', 'files', 'calculated_tests', 'output_flat_default.txt')

        self._test_head(test_name)
        Game.current_game = 0
        game = Game(starting_seeds=None,
                    toroidal_universe=False,
                    stop_after_generation=STOP_AFTER_GENERATION,
                    out_file=out_file,
                    save_to_out_file=True,
                    log_file=os.path.join('tests', 'files', 'log1.txt'),
                    auto_play=True,
                    time_in_out_file=False,
                    stats_no_middle_calc_gui=True,
                    exit_auto_when_auto_play=True)
        logger.info(f"Start Life and calculate the first {STOP_AFTER_GENERATION} generations.")
        game.start()

        logger.info("Compare differences from previous correct output file.")
        self._find_differences(out_file, out_file_correct)

    def test_toroidal_universe_seeds_default(self):
        test_name = "Game of Life with default seeds in a toroidal universe."
        out_file = os.path.join('tests', 'files', 'output2.txt')
        out_file_correct = os.path.join('tests', 'files', 'calculated_tests', 'output_toroidal_default.txt')

        self._test_head(test_name)
        Game.current_game = 0
        game = Game(starting_seeds=None,
                    toroidal_universe=True,
                    stop_after_generation=STOP_AFTER_GENERATION,
                    out_file=out_file,
                    save_to_out_file=True,
                    log_file=os.path.join('tests', 'files', 'log2.txt'),
                    auto_play=True,
                    time_in_out_file=False,
                    stats_no_middle_calc_gui=True,
                    exit_auto_when_auto_play=True)
        logger.info(f"Start Life and calculate the first {STOP_AFTER_GENERATION} generations.")
        game.start()

        logger.info("Compare differences from previous correct output file.")
        self._find_differences(out_file, out_file_correct)

    def test_flat_universe_seeds_g_glider_gun(self):
        test_name = "Game of Life with default seeds in a flat universe."
        out_file = os.path.join('tests', 'files', 'output3.txt')
        out_file_correct = os.path.join('tests', 'files', 'calculated_tests', 'output_flat_g_glider_gun.txt')

        self._test_head(test_name)
        Game.current_game = 0
        game = Game(starting_seeds="gosper_glider_gun 7 20, clock 75 100",
                    toroidal_universe=False,
                    stop_after_generation=STOP_AFTER_GENERATION,
                    out_file=out_file,
                    save_to_out_file=True,
                    log_file=os.path.join('tests', 'files', 'log3.txt'),
                    auto_play=True,
                    time_in_out_file=False,
                    stats_no_middle_calc_gui=True,
                    exit_auto_when_auto_play=True)
        logger.info(f"Start Life and calculate the first {STOP_AFTER_GENERATION} generations.")
        game.start()

        logger.info("Compare differences from previous correct output file.")
        self._find_differences(out_file, out_file_correct)

    def test_toroidal_universe_seeds_g_glider_gun(self):
        test_name = "Game of Life with default seeds in a toroidal universe."
        out_file = os.path.join('tests', 'files', 'output4.txt')
        out_file_correct = os.path.join('tests', 'files', 'calculated_tests', 'output_toroidal_g_glider_gun.txt')

        self._test_head(test_name)
        Game.current_game = 0
        game = Game(starting_seeds="gosper_glider_gun 7 20, clock 75 100",
                    toroidal_universe=True,
                    stop_after_generation=STOP_AFTER_GENERATION,
                    out_file=out_file,
                    save_to_out_file=True,
                    log_file=os.path.join('tests', 'files', 'log4.txt'),
                    auto_play=True,
                    time_in_out_file=False,
                    stats_no_middle_calc_gui=True,
                    exit_auto_when_auto_play=True)
        logger.info(f"Start Life and calculate the first {STOP_AFTER_GENERATION} generations.")
        game.start()

        logger.info("Compare differences from previous correct output file.")
        self._find_differences(out_file, out_file_correct)

    def _test_head(self, test_name):
        self.test_num += 1
        logger.info(f"{'-' * 50}")
        logger.info(f"Test {self.test_num:2} of {self.tests_total:2}")
        logger.info(f"Initialize {test_name}")

    def _find_differences(self, out_file, out_file_correct):
        with open(out_file, 'r', encoding='utf-8') as fin_test:
            with open(out_file_correct, 'r', encoding='utf-8') as fin_correct:
                diff = difflib.unified_diff(
                    fin_test.readlines(),
                    fin_correct.readlines(),
                    fromfile='fin_test',
                    tofile='fin_correct',
                )

                diff_found = False
                for i, line in enumerate(diff):
                    if i == 1:
                        logger.info(f"First differences found (with a max. of {DIFF_LINES_TO_PRINT}):")
                        diff_found = True
                    sys.stdout.write(line)
                    if i > DIFF_LINES_TO_PRINT:
                        break
                if not diff_found:
                    self.tests_passed += 1
                    logger.info("No differences found.")
                    logger.info("OK.")
                else:
                    logger.info("Failed.")
