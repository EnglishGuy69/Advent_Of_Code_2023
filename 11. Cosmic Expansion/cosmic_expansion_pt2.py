

class GalaxyMap:
    SPACE ='.'
    GALAXY = '#'

    def __init__(self, filename, expansion_rate=1000000, debug=False):
        self.rows = []
        self._debug=debug
        self._expansion_rate = expansion_rate

        with open(filename, 'r') as f:
            for row in f.readlines():
                self.rows.append(row.strip())

        self._empty_rows = self._find_empty_rows()
        self._empty_columns = self._find_empty_columns()

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0])

    def _find_empty_columns(self) -> [int]:
        empty_columns = []
        for x in range(0, self.width):
            if self._is_empty_column(x):
                empty_columns.append(x)
        return empty_columns

    def _find_empty_rows(self) -> [int]:
        empty_rows = []
        for y in range(0, self.height):
            if self._is_empty_row(y):
                empty_rows.append(y)
        return empty_rows

    def _is_empty_column(self, x: int) -> bool:
        for y in range(0, self.height):
            if self.rows[y][x] != GalaxyMap.SPACE:
                return False

        return True

    def _is_empty_row(self, y: int) -> bool:
        for x in range(0, self.width):
            if self.rows[y][x] != GalaxyMap.SPACE:
                return False

        return True


    def get(self, x: int, y: int) -> str:
        return self.rows[y][x]

    def count_empty_rows(self, y0: int, y1: int) -> int:
        if y1 < y0:
            y0, y1 = y1, y0

        empty_rows = [r for r in self._empty_rows if r >= y0 and r <= y1]
        return len(empty_rows)

    def count_empty_columns(self, x0: int, x1: int) -> int:
        if x1 < x0:
            x0, x1 = x1, x0

        empty_columns = [r for r in self._empty_columns if r >= x0 and r <= x1]
        return len(empty_columns)

    def find_galaxies(self):
        galaxies = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.get(x,y) == GalaxyMap.GALAXY:
                    galaxies.append((x,y))

        return galaxies

    def _calc_distance(self, x0:int, y0: int, x1: int, y1: int) -> int:
        distance = abs(x1 - x0) + abs(y1 - y0)
        expansion_rows = self.count_empty_rows(y0, y1)
        expansion_columns = self.count_empty_columns(x0, x1)
        return distance + (expansion_rows + expansion_columns) * (self._expansion_rate-1)

    def find_total_distances(self, galaxies: [(int, int)]) -> int:
        total = 0

        for i in range(0, len(galaxies)):
            for j in range(i+1, len(galaxies)):
                if i == j:  # exclude each galaxy with itself
                    continue

                x0 = galaxies[i][0]
                y0 = galaxies[i][1]

                x1 = galaxies[j][0]
                y1 = galaxies[j][1]

                galaxy_distance = self._calc_distance(x0, y0, x1, y1)
                if self._debug:
                    print(f'- Between galaxy {i+1} and {j+1}: {galaxy_distance}')

                total += galaxy_distance

        return total

if __name__ == '__main__':
    gm = GalaxyMap('sample.txt', expansion_rate=2, debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    assert(total_distance == 374)
    print(f'Sample Total Distance: {total_distance}')

    gm = GalaxyMap('sample.txt', expansion_rate=10, debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    assert(total_distance == 1030)
    print(f'Sample Total Distance (expansion = 10): {total_distance}')

    gm = GalaxyMap('sample.txt', expansion_rate=100, debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    assert(total_distance == 8410)
    print(f'Sample Total Distance (expansion = 10): {total_distance}')

    gm = GalaxyMap('data.txt', expansion_rate=2, debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    print(f'Part One Total Distance: {total_distance}')
    # 9312968

    gm = GalaxyMap('data.txt', expansion_rate=1000000, debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    print(f'Part One Total Distance: {total_distance}')

