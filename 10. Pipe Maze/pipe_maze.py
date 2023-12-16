from __future__ import annotations

class Searcher:
    def __init__(self, maze:Maze, debug=False):
        self._maze = maze
        self._debug = debug
        self._path = []

    @staticmethod
    def _can_move(current_cell: Cell, next_cell: Cell) -> bool:
        return current_cell.does_connect_to(next_cell) and (next_cell.distance_from_start is None or
                                                        next_cell.distance_from_start > current_cell.distance_from_start)


    def _available_cells(self, current_cell: Cell):
        available_cells = []
        possible_directions = current_cell.cell_type()[1]
        for direction in possible_directions:
            x1 = current_cell.x + direction[0]
            y1 = current_cell.y + direction[1]
            next_cell: Cell = self._maze.get_cell(x1, y1)
            if next_cell is None or next_cell.c == Cell.GROUND[0]:
                continue

            if next_cell.distance_from_start is not None and next_cell.distance_from_start < current_cell.distance_from_start:
                continue

            if not current_cell.does_connect_to(next_cell):
                continue

            available_cells.append(next_cell)

        return available_cells

    def search(self, current_cell: Cell, distance_from_start: int) -> None:
        if current_cell.distance_from_start is None or current_cell.distance_from_start > distance_from_start:
            current_cell.distance_from_start = distance_from_start
        else:
            return

        d = distance_from_start
        available_cells = self._available_cells(current_cell)
        while len(available_cells) > 0:
            if len(available_cells) > 1:
                for cell in available_cells:
                    if self._debug:
                        self._maze.print_distance_from_start(current_cell.x, current_cell.y)
                    self.search(cell, d+1)
                break
            else:
                d += 1
                current_cell = available_cells[0]
                current_cell.distance_from_start = d
                available_cells = self._available_cells(current_cell)
                if self._debug:
                    self._maze.print_distance_from_start(current_cell.x, current_cell.y)


class Cell:
    START_CHAR = ('S',[(1,0),(-1,0),(0,1),(0,-1)])
    DIR_EW = ('-',[(1,0), (-1,0)])
    DIR_NS = ('|',[(0,1), (0,-1)])
    DIR_NE = ('L',[(0,-1), (1,0)])
    DIR_NW = ('J',[(0,-1),(-1,0)])
    DIR_SW = ('7',[(-1,0),(0,1)])
    DIR_SE = ('F',[(0,1),(1,0)])
    GROUND = ('.', [])
    ALL_CELL_TYPES = [START_CHAR,
                      DIR_EW,
                      DIR_NS,
                      DIR_NE,
                      DIR_NW,
                      DIR_SW,
                      DIR_SE,
                      GROUND]

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c
        self.distance_from_start = None

    @property
    def is_part_of_loop(self):
        return self.distance_from_start is not None

    def cell_type(self):
        for c in Cell.ALL_CELL_TYPES:
            if c[0] == self.c:
                return c
        raise ValueError(f'Unknown cell type "{self.c}"')

    def _contains_direction(self, direction:(int, int)):
        for d in self.cell_type()[1]:
            if d[0] == direction[0] and d[1] == direction[1]:
                return True
        return False


    def links_left(self):
        return self._contains_direction((-1, 0))

    def links_right(self):
        return self._contains_direction((1, 0))

    def links_up(self):
        return self._contains_direction((0, -1))

    def links_down(self):
        return self._contains_direction((0, 1))


    def is_above(self, cell:Cell):
        if self.y < cell.y:
            return True
        else:
            return False

    def is_below(self, cell:Cell):
        if self.y > cell.y:
            return True
        else:
            return False

    def is_left(self, cell:Cell):
        if self.x < cell.x:
            return True
        else:
            return False

    def is_right(self, cell:Cell):
        if self.x > cell.x:
            return True
        else:
            return False

    def does_connect_to(self, cell: Cell):
        if self.c == Cell.START_CHAR[0]:
            if (self.is_below(cell) and cell.links_down()) or \
                    (self.is_above(cell) and cell.links_up()):
                return True
            elif (self.is_right(cell) and cell.links_right() ) or \
                    (self.is_left(cell) and cell.links_left()):
                return True
            else:
                return False

        if (self.is_right(cell) and self.links_left() and cell.links_right()) or \
                (self.is_left(cell) and self.links_right() and cell.links_left()) or \
                (self.is_below(cell) and self.links_up() and cell.links_down()) or \
                (self.is_above(cell) and self.links_down() and cell.links_up()):
            print(f'')
            return True
        else:
            return False

    def __str__(self):
        return f'[{self.x},{self.y}] {self.c} ({self.distance_from_start if self.distance_from_start is not None else "-"})'

    @staticmethod
    def diagnostics():
        for ct1 in Cell.ALL_CELL_TYPES:
            for ct2 in Cell.ALL_CELL_TYPES:
                if ct2[0] == 'S':
                    continue
                cell1 = Cell(10,10, ct1[0])
                cell2u = Cell(10, 9, ct2[0])
                cell2d = Cell(10, 11, ct2[0])
                cell2l = Cell(9, 10, ct2[0])
                cell2r = Cell(11, 10, ct2[0])

                print(f'{cell2u.c}')
                print(f'{cell1.c} connected:{cell1.does_connect_to(cell2u)}')
                print('')

                print(f'{cell1.c} connected:{cell1.does_connect_to(cell2d)}')
                print(f'{cell2d.c}')
                print('')

                print(f'{cell2l.c} {cell1.c} connected:{cell1.does_connect_to(cell2l)}')
                print('')

                print(f'{cell1.c} {cell2r.c} connected:{cell1.does_connect_to(cell2r)}')
                print('')

class Maze:
    def __init__(self, filename, debug=True):
        self.rows = []
        self._debug = debug

        with open(filename, 'r') as f:
            for y, row in enumerate(f.readlines()):
                row_list = []
                for x, c in enumerate(row.strip()):
                    row_list.append(Cell(x,y,c))
                self.rows.append(row_list)

        self.populate_distance_from_start()

    @property
    def width(self):
        return len(self.rows[0])

    @property
    def height(self):
        return len(self.rows)

    def get_cell(self, x: int, y: int) -> Cell:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return None
        else:
            return self.rows[y][x]

    def find_start(self) -> (int, int):
        for y, r in enumerate(self.rows):
            cell: Cell
            for x, cell in enumerate(r):
                if cell.c == Cell.START_CHAR[0]:
                    return x, y
        return None, None

    def print_distance_from_start(self, x=None, y=None, w=6, h=6):
        y_min = 0
        y_max = self.height
        x_min = 0
        x_max = self.width

        if x is not None and y is not None:
            x_min = max([x-(w // 2), 0])
            x_max = min([x+(w // 2),self.width-1])
            y_min = max([y-(h // 2), 0])
            y_max = min([y+(h // 2),self.height-1])

        for y in range(y_min,y_max):
            for x in range(x_min, x_max):
                distance_from_start = self.get_cell(x,y).distance_from_start
                if distance_from_start:
                    print(f'{distance_from_start:03} ', end='')
                else:
                    print(' -  ', end='')

            print('      ', end='')
            for x in range(x_min, x_max):
                print(f'{self.get_cell(x,y).c:3} ', end='')
            print('')

        for y in range(y_min, y_max):
            print('')

        if x is not None and y is not None:
            input('')


    def __str__(self):
        s = ''
        for y in range(0, self.height):
            for x in range(0, self.width):
                s = s + self.get_cell(x,y).c

            s == '\n'

        return s

    def populate_distance_from_start(self):
        x, y = self.find_start()
        assert(x is not None and y is not None)
        start_cell = self.get_cell(x,y)
        start_cell.distance_from_start = 0
        searcher = Searcher(self, debug=self._debug)
        searcher.search(start_cell, 0)

    def max_distance(self):
        d = None
        for y in range(0, self.height):
            for x in range(0, self.width):
                new_d = self.get_cell(x,y).distance_from_start
                if d is None or (new_d is not None and d < new_d):
                    d = new_d

        return d

if __name__ == '__main__':

#    Cell.diagnostics()
#     m = Maze('sample_1.txt')
# #    m.print_distance_from_start()
#     assert(m.max_distance() == 4)
#
#     m = Maze('sample_2.txt')
#     assert(m.max_distance() == 8)

    m = Maze('data.txt', debug=False)
    m.print_distance_from_start()
    print(m.max_distance())


