"""Module output_file."""
__author__ = 'Joan A. Pinol  (japinol)'

import logging

from life import constants as consts

# Errors
ERROR_OUT_FILE_OPEN = "!!! ERROR: Output file: %s. Program aborted !!!"
ERROR_OUT_FILE_WRITING = "!!! ERROR writing output file: %s. Some information has been lost!!!"
ERROR_OUT_FILE_MAX_TRIES = "!!! ERROR: Too much tries failed writing to the output file: %s!!!"
# Max writing errors when trying to write the buffer to the output file
MAX_ERRORS_OUT_FILE = 4


logging.basicConfig(format=consts.LOGGER_FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class OutputFile:
    """Manages information for output to file purposes."""

    def __init__(self, out_file):
        self._out_file = out_file
        self._str_out = ['']

        self._write_data_to_file(open_method='w')

    def write_buffer_before_exit(self):
        """Writes pending buffer to the output file.
        It is intended to be called before exit the application.
        """
        self._write_data_to_file()

    def write_buffer(self):
        self._write_data_to_file()

    def write_line(self, line):
        """Writes a line to the output file."""
        self._str_out.append(f'{line}\n')

    def _write_data_to_file(self, open_method='a'):
        """Writes the data still in the buffer to the output file."""
        if not self._str_out:
            return
        try:
            with open(self._out_file, open_method, encoding='utf-8') as out_file:
                for line in self._str_out:
                    out_file.write(line)
        except Exception:
            if open_method == 'w':
                logger.critical(ERROR_OUT_FILE_OPEN % self._out_file)
                exit()
            else:
                self._num_errors_out_file += 1
                if self._num_errors_out_file >= MAX_ERRORS_OUT_FILE:
                    logger.critical(ERROR_OUT_FILE_MAX_TRIES % self._out_file)
                    exit()
            return
        self._str_out = []
