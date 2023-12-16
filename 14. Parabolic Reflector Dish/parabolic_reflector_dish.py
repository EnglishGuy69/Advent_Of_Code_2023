from Common.area import Area, AreaFromFile, Areas, ChangeCell

class ParabolicReflectorDish(AreaFromFile):
    ROUNDED_ROCKS = 'O'
    CUBE_ROCKS = '#'
    EMPTY_SPACE = '.'

    def __init__(self, filename):
        super().__init__(filename)

    def move_rock(self, x0, y0, x1, y1):
        c = self.get_cell(x0, y0)
        self.set_cell(x0,y0, self.EMPTY_SPACE)
        self.set_cell(x1, y1,  c)

    def _calc_min_max(self, dx: int, dy: int) -> (int, int, int, int):
        if dx != 0 and dy != 0:
            raise ValueError('dx and dy are both non-zero, only one can be non-zero')

        x_min = 0
        y_min = 0
        x_max = self.width
        y_max = self.height
        if dx > 0:
            x_min = self.width - 1
            x_max = -1
        elif dx < 0:
            x_min = 0
            x_max = self.width
        elif dy > 0:
            y_min = self.height - 1
            y_max = -1
        elif dy < 0:
            y_min = 0
            y_max = self.height
        else:
            raise ValueError('dx and dy are both 0')

        return x_min, x_max, y_min, y_max

    def find_empty_space(self, x, y, dx, dy) -> (int, int):
        if dx != 0 and dy != 0:
            raise ValueError('dx and dy are both non-zero, only one can be non-zero')

        x_ret = None
        y_ret = None
        if dx > 0:
            x0 = x+1
            x1 = self.width
        elif dx < 0:
            x0 = x-1
            x1 = -1
        else:
            x0 = x1 = x

        if dy > 0:
            y0 = y+1
            y1 = self.height
        elif dy < 0:
            y0 = y-1
            y1 = -1
        else:
            y0 = y1 = y

        if dy != 0:
            for y in range(y0, y1, dy):
                c = self.get_cell(x,y)
                if c == self.EMPTY_SPACE:
                    x_ret = x
                    y_ret = y
                else:
                    break

            if x_ret is None:
                return None, None
            else:
                return x_ret, y_ret
        elif dx != 0:
            for x in range(x0, x1, dx):
                c = self.get_cell(x, y)
                if c == self.EMPTY_SPACE:
                    x_ret = x
                    y_ret = y
                else:
                    break

            if x_ret is None:
                return None, None
            else:
                return x_ret, y_ret
        else:
            raise ValueError('dx and xy are both 0')

    def _tilt_direction_north_south(self, dx: int, dy: int):
        x_min, x_max, y_min, y_max = self._calc_min_max(dx, dy)
        for y in range(y_min, y_max, -dy or 1):
            for x in range(0, self.width):
                c = self.get_cell(x,y)
                if c == ParabolicReflectorDish.ROUNDED_ROCKS:
                    x_empty, y_empty = self.find_empty_space(x, y, dx, dy)
                    if x_empty is not None:
                        self.move_rock(x, y, x_empty, y_empty)

    def _tilt_direction_east_west(self, dx: int, dy: int):
        x_min, x_max, y_min, y_max = self._calc_min_max(dx, dy)
        for x in range(x_min, x_max, -dx or 1):
            for y in range(0, self.height):
                c = self.get_cell(x,y)
                if c == ParabolicReflectorDish.ROUNDED_ROCKS:
                    x_empty, y_empty = self.find_empty_space(x, y, dx, dy)
                    if x_empty is not None:
                        self.move_rock(x, y, x_empty, y_empty)

    def tilt_north(self):
        self._tilt_direction_north_south(dx=0, dy=-1)

    def tilt_south(self):
        self._tilt_direction_north_south(dx=0, dy=1)

    def tilt_east(self):
        self._tilt_direction_east_west(dx=1, dy=0)

    def tilt_west(self):
        self._tilt_direction_east_west(dx=-1, dy=0)

    def calculate(self):
        total = 0
        positions = self.find_cell_positions(ParabolicReflectorDish.ROUNDED_ROCKS)
        for pos in positions:
            total += (self.height-pos[1])

        return total

    def calculate_cycle(self, scores):
        score_cycle_frequency = None
        for i in range(1, len(scores)):
            cycle_0 = scores[-i:]
            cycle_1 = scores[-2*i:-i]
            cycle_2 = scores[-3*i:-2*i]
            if cycle_0 == cycle_1:
                score_cycle_frequency = i
                if cycle_2 == cycle_0:
                    break

        return score_cycle_frequency


    def calculate_after_cycles(self, n: int) -> int:
        scores = []
        score_cycle_frequency = None
        since_change = 0
        for i in range(0, n):
            self.tilt_north()
            self.tilt_west()
            self.tilt_south()
            self.tilt_east()
            scores.append(self.calculate())
            cycle_frequency = self.calculate_cycle(scores)
            if cycle_frequency is None or cycle_frequency != score_cycle_frequency:
                since_change = 0
            else:
                since_change += 1

            if cycle_frequency is not None and (score_cycle_frequency is None or cycle_frequency > score_cycle_frequency):
                score_cycle_frequency = cycle_frequency
                print(f'Frequency: {score_cycle_frequency}')

            if (score_cycle_frequency or 0) > 1 and since_change > score_cycle_frequency*10:
                cycle_scores = scores[-score_cycle_frequency:]
                pos = (n - (len(scores)-score_cycle_frequency)-1) % score_cycle_frequency
                return cycle_scores[pos]


if __name__ == '__main__':
    dish = ParabolicReflectorDish('sample.txt')
    dish.tilt_north()
    print(f'{str(dish)}')
    assert(dish.calculate() == 136)
    assert(dish.calculate_after_cycles(1000000000) == 64)

    dish = ParabolicReflectorDish('data.txt')
    dish.tilt_north()
    print(f"Part 1 Total: {dish.calculate()}")

    dish = ParabolicReflectorDish('data.txt')
    cycle_frequency = dish.calculate_after_cycles(1000000000)

    print(dish.calculate())



