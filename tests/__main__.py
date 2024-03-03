"""Module __main__. Entry point for the test suite."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging
import traceback

from life import constants as consts
from tests.test_life import TestLife

logging.basicConfig(format=consts.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    try:
        test_life = TestLife()
        test_life.main()
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        logger.critical(f'Error: {e}')


if __name__ == '__main__':
    main()
