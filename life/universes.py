"""Module universes."""
__author__ = 'Joan A. Pinol  (japinol)'

from random import randint

import numpy as np
from numpy.lib.stride_tricks import as_strided

import pygame as pg

from life.cells import Cell
from life import lib_jp
from life import resources
from life import seeds
from life.settings import Settings, UniverseCalculationType, NextGenerationType


INVISIBLE_DEAD_CELLS_ALLOWED = 5


class Universe(pg.sprite.Sprite):
    """Represents a universe."""
    size = None     # The size of the sprite of the universe
    sprite_image = None

    def __init__(self, game):
        super().__init__()
        self.id = game.current_game
        self.cells = None  # The matrix of cells
        # Dictionary of the cells used for their graphic representation on the board
        self.cells_board = {}
        self.size_u = lib_jp.Size(w=Settings.universe_size.w, h=Settings.universe_size.h)
        self.game = game
        self.start_time = 0
        self.stop_time = 0
        self.generation = 0
        self.stats = {'cells_total': 0,
                      'cells_age1': 0,
                      'cells_age2': 0,
                      'cells_age3': 0,
                      'cells_age4': 0,
                      'cells_age5': 0,
                      'cells_age6': 0,
                      'cells_age7': 0,
                      'cells_age8': 0,
                      'deads_age1': 0,
                      'deads_age2': 0,
                      'deads_age3': 0,
                      'deads_age4': 0,
                      'deads_age5': 0,
                      'deads_age6': 0,
                      'deads_age7': 0,
                      'deads_age8': 0,
                      }

        self.set_universe_calculate_generation()
        self.set_cells_board_update_calculation()
        self.set_universe_colors(Settings.cell_one_color)

        self.clean()

        if not Universe.sprite_image:
            image = pg.image.load(resources.file_name_get(name='im_universe')).convert()
            image = pg.transform.smoothscale(image, Universe.size)
            Universe.sprite_image = image
        else:
            image = Universe.sprite_image

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = Settings.universe_pos.x
        self.rect.y = Settings.universe_pos.y
        self.pos_limit = lib_jp.Point(x=self.rect.x + Universe.size.w,
                                      y=self.rect.y + Universe.size.h)

        # Add universe to the active sprite list
        self.game.active_sprites.add(self)

    def update(self):
        if not self.game.next_generation or self.game.next_generation == NextGenerationType.NONE:
            return

        self.next_generation()

        # Clean the graphic board of dead cells
        if len(self.game.cells) > self.stats['cells_total'] + INVISIBLE_DEAD_CELLS_ALLOWED:
            self._clean_board_of_dead_cells()

        if self.game.next_generation == NextGenerationType.ONE:
            self.game.next_generation = NextGenerationType.NONE
        elif self.game.next_generation == NextGenerationType.SEVERAL:
            if Settings.stop_after_generation and self.generation == Settings.stop_after_generation:
                self.stop_time = pg.time.get_ticks()
                self.game.next_generation = NextGenerationType.NONE
                if Settings.exit_auto_when_auto_play:
                    self.game.exit_auto = True

    def clean(self):
        self.generation = 1
        self.cells = np.array([[0] * self.size_u.w for _ in range(self.size_u.h)], dtype=np.uint8)
        nd_slice = (slice(1, -1),) * len(self.size_u)
        self.cells_slice = self.cells[nd_slice]
        self.n_dims = len(self.cells_slice.shape)
        self.cells_board = {}

        cells_old = self.cells.copy()

        self.stats.update((k, 0) for k in self.stats)
        self._reset_population()

        self.start_time = pg.time.get_ticks()
        # Change the graphic cells on the board according to the matrix of cells
        self._cells_board_update(cells_old)

    def set_universe_calculate_generation(self):
        """Sets the calculation function of the universe a toroidal one
        or a flat one according to settings.
        """
        if Settings.universe_calculation == UniverseCalculationType.NON_TOROIDAL_FAST:
            self._calculate_generation = self._calculate_generation_fast
        elif Settings.universe_calculation == UniverseCalculationType.TOROIDAL_LOOP:
            self._calculate_generation = self._calculate_generation_toroidal_with_loop
        elif Settings.universe_calculation == UniverseCalculationType.NON_TOROIDAL_LOOP:
            self._calculate_generation = self._calculate_generation_with_loop

    def set_cells_board_update_calculation(self):
        """Sets the calculation function of cells on the board with and without statistics."""
        if Settings.stats_activated:
            self._cells_board_update = self._cells_board_update_with_stats
        else:
            self._cells_board_update = self._cells_board_update_standard

    def set_universe_colors(self, cell_one_color):
        """Sets the representation of the universe to one color for each age
        when cell_one_color is False; sets it to only on color despite the age if True.
        """
        if cell_one_color:
            self.pprint_to_string = self.pprint_to_string_board_one_color
        else:
            self.pprint_to_string = self.pprint_to_string_board_age

    def next_generation(self):
        if self.generation == 1:
            self.game.output_info.write_head()
            self.game.debug_info.write_head()
            if Settings.save_to_out_file:
                self.game.output_info.write_generation()

        self.generation += 1

        # Copy the old generation
        cells_old = self.cells.copy()
        # Calculate generation
        self._calculate_generation(cells_old)
        # Change the graphic cells on the board according to the array of cells
        self._cells_board_update(cells_old)

        if Settings.save_to_out_file:
            self.game.output_info.write_generation()

    def _cells_board_update_standard(self, cells_old):
        # Change the graphic cells on the board according to the array of cells
        for i, rows in enumerate(self.cells):
            for j, cell in enumerate(rows):
                cell_board = self.cells_board.get((j, i))
                if cell_board:
                    if cell == 1 and cells_old[i, j] == 1:
                        cell_board.age = min(cell_board.age + 1, Cell.CELL_AGES_MAX - 1)
                        cell_board.age_total += 1
                    else:
                        cell_board.age = cell
                        if not cell and cells_old[i, j] == 1:
                            self.stats['cells_total'] -= 1
                        elif cell == 1 and not cells_old[i, j]:
                            self.stats['cells_total'] += 1
                elif cell:
                    self.add_cell_to_board(j, i, age=cell)
                    self.stats['cells_total'] += 1

    def _cells_board_update_with_stats(self, cells_old):
        """Change the graphic cells on the board according to the array of cells.
        Also calculates statistics for total age dead cells and cells currently alive.
        """
        for i, rows in enumerate(self.cells):
            for j, cell in enumerate(rows):
                cell_board = self.cells_board.get((j, i))
                if cell_board:
                    if cell == 1 and cells_old[i, j] == 1:
                        self.stats[f'cells_age{cell_board.age}'] -= 1
                        cell_board.age = min(cell_board.age + 1, Cell.CELL_AGES_MAX - 1)
                        cell_board.age_total += 1
                        self.stats[f'cells_age{cell_board.age}'] += 1
                    else:
                        if not cell and cells_old[i, j] == 1:
                            self.stats['cells_total'] -= 1
                            self.stats[f'deads_age{cell_board.age}'] += 1
                            self.stats[f'cells_age{cell_board.age}'] -= 1
                        elif cell == 1 and not cells_old[i, j]:
                            self.stats['cells_total'] += 1
                            self.stats['cells_age1'] += 1
                        cell_board.age = cell
                elif cell:
                    self.add_cell_to_board(j, i, age=cell)
                    self.stats['cells_total'] += 1
                    self.stats[f'cells_age{cell}'] += 1

    def _clean_board_of_dead_cells(self):
        for key, cell_board in tuple(self.cells_board.items()):
            if cell_board.age == 0:
                cell_board.kill()
                del self.cells_board[key]

    def _calculate_generation_fast(self, _):
        """Calculates the next generation for each cell
        in a non-toroidal universe.
        This is a faster method that takes advantage of numpy.
        """
        # Calculate the number of neighbors in a non toroidal universe
        rule_of_life_alive = np.zeros(8 + 1, np.uint8)
        rule_of_life_dead = np.zeros(8 + 1, np.uint8)
        # If it is alive and has less than 2 neighbors, it dies by under-population.
        # Also, if it has more than 3 neighbors, it dies by over-population.
        # That is, only the cells alive with 2 or 3 neighbors survive
        rule_of_life_alive[[2, 3]] = 1
        # If the cell is dead but has exactly 3 neighbors, a new cell is born by reproduction.
        rule_of_life_dead[3] = 1

        # Calculate the neighborhoods and apply the rules
        neighborhoods = Universe._grid_n_dims(self.cells)
        sum_over = tuple(-(i+1) for i in range(self.n_dims))
        neighbors_no = np.sum(neighborhoods, sum_over) - self.cells_slice
        self.cells_slice[:] = np.where(self.cells_slice, rule_of_life_alive[neighbors_no],
                                       rule_of_life_dead[neighbors_no])

    def _calculate_generation_toroidal_with_loop(self, cells_old):
        """Calculates the next generation for each cell
        in a toroidal universe.
        """
        cells_ne = cells_old.copy()
        cells_ne = Universe._neighborhood(cells_ne)
        for x, rows in enumerate(cells_old):
            for y, _ in enumerate(rows):
                if cells_old[x, y] and not 2 <= cells_ne[x, y] <= 3:
                    # If it is alive and has less than 2 neighbors, it dies by under-population.
                    # Also, if it has more than 3 neighbors, it dies by over-population.
                    self.cells[x, y] = 0
                elif cells_ne[x, y] == 3:
                    # If it has exactly 3 neighbors, it lives.
                    # Also, if it is dead, a new cell is born by reproduction.
                    self.cells[x, y] = 1

    def _calculate_generation_with_loop(self, cells_old):
        """Calculates the next generation for each cell
        in a non-toroidal universe.
        This is a slower method than the one used.
        It can be used to test faster methods.
        """
        for x, rows in enumerate(cells_old):
            for y, _ in enumerate(rows):
                # Calculate the number of neighbors in a no toroidal universe
                neighbors_no = np.sum(cells_old[x - 1: x + 2, y - 1: y + 2]) - cells_old[x, y]
                if cells_old[x, y] and not 2 <= neighbors_no <= 3:
                    # If it is alive and has less than 2 neighbors, it dies by under-population.
                    # Also, if it has more than 3 neighbors, it dies by over-population.
                    self.cells[x, y] = 0
                elif neighbors_no == 3:
                    # If it has exactly 3 neighbors, it lives.
                    # Also, if it is dead, a new cell is born by reproduction.
                    self.cells[x, y] = 1

    @staticmethod
    def _grid_n_dims(arr):
        """Calculates a sub-array for a given array and return it with a customized shape,
        so we can get the neighborhoods of a cell.
        """
        assert all(_len > 2 for _len in arr.shape)
        n_dims = len(arr.shape)
        new_shape = [_len - 2 for _len in arr.shape]
        new_shape.extend([3] * n_dims)
        new_strides = arr.strides + arr.strides
        # Return the sub-array with our neighborhoods and a convenient way to move through them
        return as_strided(arr, shape=new_shape, strides=new_strides)

    @staticmethod
    def _neighborhood(arr):
        """Calculates the number of neighbors for each cell of a toroidal array.
        To do so, it rotates the array in each direction.
        Returns and array with this information.
        """
        return (np.roll(np.roll(arr, 1, 1), 1, 0) +  # Top, left
                np.roll(arr, 1, 0) +  # Top
                np.roll(np.roll(arr, -1, 1), 1, 0) +  # Top, right
                np.roll(arr, -1, 1) +  # Right
                np.roll(np.roll(arr, -1, 1), -1, 0) +  # Bottom, right
                np.roll(arr, -1, 0) +  # Bottom
                np.roll(np.roll(arr, 1, 1), -1, 0) +  # Bottom, left
                np.roll(arr, 1, 1)  # Left
                )

    def switch_cell(self):
        if not Settings.edit_allowed:
            return
        x, y = self._cell_selected_coords()
        self.cells[y, x] = 1 if not self.cells[y, x] else 0
        self.stats['cells_total'] += 1 if self.cells[y, x] else -1
        self.stats['cells_age1'] += 1 if self.cells[y, x] else -1

        cell_board = self.cells_board.get((x, y))
        if cell_board:
            cell_board.age = self.cells[y, x]
        else:
            self.add_cell_to_board(x, y, age=self.cells[y, x])

    def _cell_selected_coords(self):
        x = (self.game.cell_selector.rect.x - Settings.universe_pos.x) // Settings.cell_size
        y = (self.game.cell_selector.rect.y - Settings.universe_pos.y) // Settings.cell_size
        return x, y

    def cell_selected_age(self):
        x, y = self._cell_selected_coords()
        cell_board = self.cells_board.get((x, y))
        if cell_board:
            return cell_board.age
        else:
            return 0

    def add_cell_to_board(self, x, y, age):
        cell = Cell(x, y, self.game, age=age)
        self.cells_board[x, y] = cell

    def add_cells_seed(self, x, y, seed):
        seed_array = np.array(seeds.seeds[seed])
        x_end, y_end = x + seed_array.shape[0], y + seed_array.shape[1]
        self.cells[x:x_end, y:y_end] = seed_array

    def add_cells_random(self, n_cells):
        for _ in range(n_cells):
            added = False
            while not added:
                cell_pos_x = randint(0, self.size_u.w - 1)
                cell_pos_y = randint(0, self.size_u.h - 1)
                if self.cells[cell_pos_y, cell_pos_x]:
                    continue
                self.cells[cell_pos_y, cell_pos_x] = 1
                self.cells_alive += 1
                added = True
                self.add_cell_to_board(cell_pos_x, cell_pos_y)

    def pprint_to_string_one_color(self):
        res = []
        for rows in self.cells:
            for cell in rows:
                res += [str(cell) if cell != 0 else '·']
            res += ['\n']
        return ''.join(res)

    def pprint_to_string_board_age(self):
        res = []
        for i, rows in enumerate(self.cells):
            for j, _ in enumerate(rows):
                cell_board = self.cells_board.get((j, i))
                if cell_board:
                    res += [str(cell_board.age) if cell_board.age != 0 else '·']
                else:
                    res += ['·']
            res += ['\n']
        return ''.join(res)

    def pprint_to_string_board_one_color(self):
        res = []
        for i, rows in enumerate(self.cells):
            for j, _ in enumerate(rows):
                cell_board = self.cells_board.get((j, i))
                if cell_board:
                    res += ['1' if cell_board.age != 0 else '·']
                else:
                    res += ['·']
            res += ['\n']
        return ''.join(res)

    def _reset_population(self):
        if Settings.empty_universe:
            return

        if Settings.starting_seeds:
            for seed, pos in Settings.starting_seeds:
                self.add_cells_seed(pos[0], pos[1], seed)
            return

    @classmethod
    def init(cls):
        cls.size = lib_jp.Size(w=Settings.universe_size.w * Settings.cell_size,
                               h=Settings.universe_size.h * Settings.cell_size)
