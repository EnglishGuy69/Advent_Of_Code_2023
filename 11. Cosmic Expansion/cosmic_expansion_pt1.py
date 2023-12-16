

class GalaxyMap:
    SPACE ='.'
    GALAXY = '#'

    def __init__(self, filename, debug=False):
        self.rows = []
        self._debug=debug

        with open(filename, 'r') as f:
            for row in f.readlines():
                self.rows.append(row.strip())

        self._perform_expand()

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(self.rows[0])

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

    def _insert_empty_column(self, x: int) -> None:
        for y in range(0, self.height):
            self.rows[y] = self.rows[y][:x] + GalaxyMap.SPACE + self.rows[y][x:]

    def _insert_empty_row(self, y: int) -> None:
        self.rows.insert(y, GalaxyMap.SPACE*self.width)

    def _perform_expand(self):
        empty_rows = sorted([y for y in range(0, self.height) if self._is_empty_row(y)], reverse=True)
        empty_columns = sorted([x for x in range(0, self.width) if self._is_empty_column(x)], reverse=True)

        for y in empty_rows:  # must be in reverse order
            self._insert_empty_row(y)

        for x in empty_columns:  # must be in reverse order
            self._insert_empty_column(x)

    def get(self, x: int, y: int) -> str:
        return self.rows[y][x]

    def find_galaxies(self):
        galaxies = []
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.get(x,y) == GalaxyMap.GALAXY:
                    galaxies.append((x,y))

        return galaxies

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

                galaxy_distance = abs(x1-x0) + abs(y1-y0)
                if self._debug:
                    print(f'- Between galaxy {i+1} and {j+1}: {galaxy_distance}')

                total += galaxy_distance

        return total

if __name__ == '__main__':
    gm = GalaxyMap('sample.txt', debug=True)
    assert(gm.width == 13)
    assert(gm.height == 12)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    assert(total_distance == 374)
    print(f'Sample Total Distance: {total_distance}')

    gm = GalaxyMap('data.txt', debug=True)
    galaxies = gm.find_galaxies()
    total_distance = gm.find_total_distances(galaxies=galaxies)
    print(f'Part One Total Distance: {total_distance}')


