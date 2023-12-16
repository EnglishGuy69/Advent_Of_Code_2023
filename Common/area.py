from __future__ import annotations

class Area:

    def __init__(self, rows, debug=False):
        self.rows = rows
        self._debug=debug


    def get_column(self, x: int):
        s = ''
        for row in self.rows:
            s += row[x]

        return s

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0])

    def get_cell(self, x: int, y: int):
        return self.rows[y][x]

    def set_cell(self, x: int, y: int, c: str):
        row = self.rows[y]
        self.rows[y] = row[:x] + c + row[x+1:]


    def find_cell_positions(self, c: str):
        cell_positions = []
        for y in range(0, self.height):
            for x in range(0, self. width):
                cell = self.get_cell(x,y)
                if cell == c:
                    cell_positions.append((x,y))

        return cell_positions

    def __str__(self):
        s = ''
        for row in self.rows:
            s += row + '\n'

        return s

class AreaFromFile(Area):
    def __init__(self, filename: str, debug=False):
        rows = []
        with open(filename) as f:
            for y, line in enumerate(f):
                line = line.strip()
                rows.append(self._create_row(y, line))

        super().__init__(rows, debug=debug)

    def _create_row(self, y:int, s: str) -> []|str:
        return s

class Areas:
    def __init__(self, filename: str):
        self._areas = []

        with open(filename) as f:
            self._read_headings(f)
            self._read_areas(f)

    def _read_headings(self, f):
        raise NotImplemented('Must be overridden in the derived class')

    def _read_areas(self, f):
        raise NotImplemented('Must be overridden in the derived class')

class Cell:
    def __init__(self, x:int, y:int, c:str):
        self.x = x
        self.y = y
        self.c = c


class ChangeCell:
    def __init__(self, area: Area, x: int, y: int, c: str):
        self._area = area
        self._x = x
        self._y = y
        self._c = c
        self._old_c = None

    def __enter__(self):
        self._old_c = self._area.get_cell(self._x, self._y)
        self._area.set_cell(self._x, self._y, self._c)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._area.set_cell(self._x, self._y, self._old_c)
        self._old_c = None