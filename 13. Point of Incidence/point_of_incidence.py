from __future__ import annotations
from Common.area import Area, ChangeCell
class SandArea(Area):
    ROCK = '#'
    SAND = '.'

    def __init__(self, rows, debug=False):
        super().__init__(rows=rows, debug=debug)

    def is_mirror(self, left: str, right: str):
        if len(left) > len(right):
            left = left[len(left)-len(right):]
        elif len(right) > len(left):
            right = right[:len(left)]

        right = right[::-1]
        return left == right

    def _find_lines_of_reflections_in_string(self, s: str):
        reflection_points = []
        for p in range(1, len(s)):
            left, right = s[:p], s[p:]
            if self.is_mirror(left, right):
                reflection_points.append(p)

        return reflection_points

    def find_line_of_reflection_columns(self):
        reflection_lines = None
        for y in range(0, self.height):
            row = self.rows[y]
            ror = self._find_lines_of_reflections_in_string(row)
            if reflection_lines is None:
                reflection_lines = ror
            else:
                reflection_lines = [p for p in reflection_lines if p in ror]
                if len(reflection_lines) == 0:
                    return reflection_lines

        return reflection_lines

    def find_line_of_reflection_rows(self):
        reflection_lines = None
        for x in range(0, self.width):
            col = self.get_column(x)
            ror = self._find_lines_of_reflections_in_string(col)
            if reflection_lines is None:
                reflection_lines = ror
            else:
                reflection_lines = [p for p in reflection_lines if p in ror]
                if len(reflection_lines) == 0:
                    return reflection_lines

        return reflection_lines

    def find_lines_of_reflection_with_smudges(self) -> int:
        original_reflection_lines = self.find_lines_of_reflection()
        rock_positions = self.find_cell_positions(SandArea.ROCK)
        for rock_position in rock_positions:
            x = rock_position[0]
            y = rock_position[1]

            with ChangeCell(area=self, x=x,y=y,c=SandArea.SAND):
                test_positions = self.find_lines_of_reflection()
                for pos in test_positions:
                    if pos != original_reflection_lines[0]:
                        return pos[1] * (1 if pos[0] == 'col' else 100)


    def find_lines_of_reflection(self):
        ror_row = self.find_line_of_reflection_rows()
        ror_col = self.find_line_of_reflection_columns()

        lines_of_reflection = []
        lines_of_reflection += [('row',r) for r in ror_row]
        lines_of_reflection += [('col',c) for c in ror_col]

        return lines_of_reflection

    def find_line_of_reflection(self):
        ror_row = self.find_line_of_reflection_rows()
        ror_col = self.find_line_of_reflection_columns()
        if ror_row:
            return ror_row[0] * 100
        elif ror_col:
            return ror_col[0]
        else:
            return None


class PointOfIncidence:
    def __init__(self, filename, debug=False):
        self.sand_areas = []
        self._debug=debug

        with open(filename, 'r') as f:
            rows = []
            for row in f.readlines():
                if row.strip() == '':
                    self.sand_areas.append(SandArea(rows, self._debug))
                    rows = []
                else:
                    rows.append(row.strip())

        if len(rows) > 0:
            self.sand_areas.append(SandArea(rows, self._debug))

    def find_total_lines_of_reflection(self):
        total = 0
        for sand_area in self.sand_areas:
            line_of_reflection_score = sand_area.find_line_of_reflection()
            if line_of_reflection_score:
                total += line_of_reflection_score

        return total

    def find_total_lines_of_reflection_with_smudges(self):
        total = 0
        for sand_area in self.sand_areas:
            Line_of_reflection_score = sand_area.find_lines_of_reflection_with_smudges()
            if Line_of_reflection_score:
                total += Line_of_reflection_score

        return total


if __name__ == '__main__':
    poi = PointOfIncidence('sample.txt', debug=True)
    assert(poi.find_total_lines_of_reflection() == 405)
    reflection_total = poi.find_total_lines_of_reflection_with_smudges()
    poi = PointOfIncidence('data.txt', debug=True)
    print(poi.find_total_lines_of_reflection_with_smudges())
