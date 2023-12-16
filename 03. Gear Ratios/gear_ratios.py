import os
import re

NON_SYMBOLS='0123456789.'

class MatchingNumber:
    def __init__(self, number: int, y: int, x0: int, x1: int):
        self.number = number
        self.y = y
        self.x0 = x0
        self.x1 = x1

class MatchingSymbol:
    def __init__(self, symbol: str, y: int, x: int):
        self.symbol = symbol
        self.y = y
        self.x = x

    def is_adjacent(self, matching_number: MatchingNumber):
        if abs(matching_number.y - self.y) > 1:
            return False

        # to the left or right
        if matching_number.y == self.y:
            if matching_number.x1 == self.x - 1 or matching_number.x0 == self.x + 1:
                return True

        # above or below
        if matching_number.x1 < self.x-1 or matching_number.x0 > self.x + 1:
            return False
        else:
            return True

class PartSchematic:
    def __init__(self, filename):
        self._rows = []
        self._load_schematic(filename)

    @property
    def width(self):
        return len(self._rows[0])

    @property
    def height(self):
        return len(self._rows)

    def _load_schematic(self, filename):
        with open(filename, 'r') as f:
            for row in f.readlines():
                self._rows.append(row.rstrip())

    def is_symbol(self, x, y):
        if x < 0 or y < 0 or x >= self.width or y >= self.width:
            return False
        else:
            return self._rows[y][x] not in NON_SYMBOLS


    def display_symbols(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.is_symbol(x,y):
                    print(self._rows[y][x], end='')
                else:
                    print(' ', end='')
            print('')

    def _look_for_symbols(self, y:int, x_start:int , x_end:int):
        if y < 0 or y >=self.height:
            return False

        if x_start < 0:
            x_start = 0
        if x_end >= self.width:
            x_end = self.width-1

        s = self._rows[y][x_start:x_end+1]
        symbols = [c for c in s if not c in NON_SYMBOLS]
        return len(symbols) > 0

    def find_part_numbers(self):
        part_numbers = []
        for y in range(0, self.height):
            row = self._rows[y]
            for p in re.finditer('[0-9]+', row):
                x0 = p.span()[0]
                x1 = p.span()[1]-1

                symbols_above = self._look_for_symbols(y - 1, x0 - 1, x1 + 1)
                symbols_below = self._look_for_symbols(y + 1, x0 - 1, x1 + 1)
                symbols_end = self._look_for_symbols(y,       x0 - 1, x1 + 1)
                if symbols_above or symbols_below or symbols_end:
                    part_numbers.append(row[x0:x1+1])

        return part_numbers

    def find_all_symbols(self):
        matching_symbols = []
        for y in range(0, self.height):
            row = self._rows[y]
            for x in range(0, self.width):
                c = row[x]
                if c not in NON_SYMBOLS:
                    matching_symbols.append(MatchingSymbol(symbol=c, y=y, x=x))

        return matching_symbols

    def find_all_numbers(self):
        matching_numbers = []
        for y in range(0, self.height):
            row = self._rows[y]

            for p in re.finditer('[0-9]+', row):
                x0 = p.span()[0]
                x1 = p.span()[1]-1
                matching_numbers.append(MatchingNumber(number=int(row[x0:x1+1]),y=y, x0=x0, x1=x1))

        return matching_numbers

    def find_adjacent_numbers(self, matching_symbol: MatchingSymbol, matching_numbers: [MatchingNumber]) -> [MatchingNumber]:
        adjacent_numbers = []
        for matching_number in matching_numbers:
            if matching_symbol.is_adjacent(matching_number):
                adjacent_numbers.append(matching_number)

        return adjacent_numbers


    def find_gears(self):
        all_symbols = self.find_all_symbols()
        all_numbers = self.find_all_numbers()
        gear_ratios = []
        for symbol in all_symbols:
            adjacent_numbers = self.find_adjacent_numbers(symbol, all_numbers)  # type: [MatchingNumber]
            if len(adjacent_numbers) == 2:
                gear_ratios.append(adjacent_numbers[0].number * adjacent_numbers[1].number)

        return sum(gear_ratios)


if __name__ == '__main__':
    # ps = PartSchematic('sample_1.txt')
    # part_numbers = ps.find_part_numbers()
    # total = sum([int(s) for s in part_numbers])


    ps = PartSchematic('data_1.txt')
    part_numbers = ps.find_part_numbers()
    total = sum([int(s) for s in part_numbers])
    print(total)
    gear_total = ps.find_gears()
    pass