﻿"""Module lib_jp."""
__author__ = 'Joan A. Pinol  (japinol)'

from collections import namedtuple
from functools import wraps
import time

from life.colors import Color


Point = namedtuple('Point', ['x', 'y'])
Size = namedtuple('Size', ['w', 'h'])


def pretty_dict_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent, str(key), '-->', end='')
        if isinstance(value, dict):
            print('')
            pretty_dict_print(value, indent + 1)
        else:
            print('\t' * (indent + 1), '{:>10}'.format(str(value)))


def pretty_dict_to_string(d, indent=0, with_last_new_line=False, res='', firt_time=True):
    for key, value in d.items():
        res = '%s%s%s%s' % (res, '\t' * indent, str(key), '-->')
        if isinstance(value, dict):
            res = '%s\n' % res
            res = '%s%s' % (res, pretty_dict_to_string(value, indent + 1, res='', firt_time=False))
        else:
            res = '{}{}{:>10}\n'.format(res, '\t' * (indent + 1), str(value))
    if firt_time and not with_last_new_line:
        res = res[:-1]
    return res


def write_list_to_file(file, value, open_method='a'):
    with open(file, open_method, encoding='utf-8') as fout:
        for line in value:
            fout.write(line)
    value = []


def file_read_list(file_name, lines_to_read):
    res = []
    try:
        with open(file_name, "r") as file_in:
            i = 0
            for line in file_in:
                if i <= lines_to_read:
                    res.append(line.lower().replace('\n', '').replace(' ', ''))
                i += 1
    except FileNotFoundError:
        res = False
        print("File does not exist: %s" % file_name)
    except Exception:
        res = False
    return res


def map_color_to_img_num(color):
    res = 0
    if color == Color.GREEN:
        res = 1
    elif color == Color.YELLOW:
        res = 2
    elif color == Color.BLUE:
        res = 3
    elif color == Color.RED:
        res = 4
    elif color == Color.BLACK:
        res = 5
    return res


def map_color_num_to_name_txt(color):
    res = ''
    if color == 1:
        res = 'Green'
    elif color == 2:
        res = 'Yellow'
    elif color == 3:
        res = 'Blue'
    elif color == 4:
        res = 'Red'
    elif color == 5:
        res = 'Black'
    return res


def time_it(func, *args, **kwargs):
    """Benchmarks a given function."""
    start = time.perf_counter()
    res = func(*args, **kwargs)
    print(f'{func.__name__} t: {time.perf_counter() - start:.{8}f} s')
    return res


def time_it_dec(func):
    """Benchmarks a given function. It is intended to be used as a decorator."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print(f'{func.__name__} t: {time.perf_counter() - start:.8f} s')
        return res
    return wrapper
