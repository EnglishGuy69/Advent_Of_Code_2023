from __future__ import annotations
from Common.area import Area, AreaFromFile, Cell

class Beam:
    _id = 1
    reflections = {'N/': 'E',
                   'N\\': 'W',
                   'S/': 'W',
                   'S\\': 'E',
                   'E/': 'N',
                   'E\\': 'S',
                   'W/': 'S',
                   'W\\': 'N'}

    def __init__(self, direction: str):
        self.id = Beam._id
        Beam._id += 1
        self.direction = direction
        if direction == 'N':
            self.dx = 0
            self.dy = -1
        elif direction == 'S':
            self.dx = 0
            self.dy = 1
        elif direction == 'E':
            self.dx = 1
            self.dy = 0
        elif direction == 'W':
            self.dx = -1
            self.dy = 0

    def split_beam(self, splitter: str) -> [Beam]:
        if self.direction in ['N', 'S'] and splitter == '-':
            beam1 = Beam('E')
            beam2 = Beam('W')
            return [beam1, beam2]
        elif self.direction in ['E', 'W'] and splitter == '|':
            beam1 = Beam('N')
            beam2 = Beam('S')
            return [beam1, beam2]
        else:
            return [self]

    def reflect_beam(self, mirror: str) -> [Beam]:
        new_direction = Beam.reflections[self.direction + mirror]
        return [Beam(new_direction)]

    def process_beam(self, c: str):
        if c in ['|','-']:
            return self.split_beam(c)
        elif c in ['/','\\']:
            return self.reflect_beam(c)
        else:
            return []

    def __str__(self):
        if self.direction == 'N':
            return '^'
        elif self.direction == 'S':
            return 'v'
        elif self.direction == 'E':
            return '>'
        elif self.direction == 'W':
            return '<'

class BeamPosition:
    def __init__(self, x: int, y: int, beam: Beam, max_x: int, max_y: int):
        self.beam = beam
        self.x = x
        self.y = y
        self.max_x = max_x
        self.max_y = max_y
        self.deleted = False

    def move(self):
        self.x += self.beam.dx
        self.y += self.beam.dy

        if self.x < 0 or self.x >= self.max_x:
            self.deleted = True
        if self.y < 0 or self.y >= self.max_y:
            self.deleted = True

class Tile(Cell):
    def __init__(self, x: int, y: int, c: str):
        super().__init__(x, y, c)
        self.beams = []

    def find_beam(self, direction:str) -> Beam|None:
        for beam in self.beams:
            if beam.direction == direction:
                return beam
        return None

    def find_beam_with_id(self, id: int) -> Beam|None:
        for beam in self.beams:
            if beam.id == id:
                return beam
        return None

    def add_beam(self, beam: Beam):
        if self.find_beam_with_id(beam.id):
            return
        else:
            self.beams.append(beam)

    def __str__(self):
        return f'{self.c}'


class Cave(AreaFromFile):
    def __init__(self, filename: str):
        super().__init__(filename)

    def _create_row(self, y: int, s: str) -> []|str:
        row = []
        for x, c in enumerate(s):
            tile = Tile(x, y, c)
            row.append(tile)
        return row

    def _is_beam_position_in_area(self, beam_pos:BeamPosition):
        if  beam_pos.x < 0 or beam_pos.x >= self.width:
            return False
        elif beam_pos.y < 0 or beam_pos.y >= self.height:
            return False
        else:
            return True

    def print_cave(self):
        for y in range(self.height):
            n = 0
            for x in range(self.width):
                tile = self.get_cell(x,y)
                if tile.c != '.':
                    print(f' {tile.c}', end='')
                elif len(tile.beams) > 1:
                    print(f' {len(tile.beams)}', end='')
                elif len(tile.beams) == 1:
                    print(f' {tile.beams[0]}', end='')
                else:
                    print(f' {tile.c}', end='')

            print(f'')
            pass

    def print_energized(self):
        for y in range(self.height):
            n = 0
            for x in range(self.width):
                tile = self.get_cell(x,y)
                if len(tile.beams) > 0:
                    print(f' #', end='')
                else:
                    print(f' .', end='')

            print(f'')

    @staticmethod
    def _beam_positions_contain(beam_positions:[BeamPosition], beam: Beam):
        return len([bp for bp in beam_positions if bp.beam.id == beam.id]) == 1

    @staticmethod
    def _beams_contain(beams:[Beam], beam: Beam):
        return len([b for b in beams if b.id == beam.id]) == 1

    def _shine(self, beam_position: BeamPosition) -> [Beam]:
        beam_positions = []
        while not beam_position.deleted:
            tile = self.get_cell(beam_position.x, beam_position.y)  # type: Tile

            # If we see our beam matches one that already came past in this direction, end the beam...
            if tile.find_beam(beam_position.beam.direction):
                beam_position.deleted = True
                break
            else:
                tile.add_beam(beam_position.beam)

            new_beams = beam_position.beam.process_beam(tile.c)

            if len(new_beams) == 0:     # no new beams means, keep going
                beam_position.move()
            elif len(new_beams) == 1:   # one new beam means, reflection, replace old beam with new
                beam_position = BeamPosition(beam_position.x, beam_position.y, new_beams[0], self.width, self.height)
                beam_position.move()
            elif len(new_beams) == 2:   # two new beams means, split, add beams to list and return
                beam_position_1 = BeamPosition(beam_position.x, beam_position.y, new_beams[0], self.width, self.height)
                beam_position_1.move()
                if not beam_position_1.deleted:
                    beam_positions.append(beam_position_1)

                beam_position_2 = BeamPosition(beam_position.x, beam_position.y, new_beams[1], self.width, self.height)
                beam_position_2.move()
                if not beam_position_2.deleted:
                    beam_positions.append(beam_position_2)

                beam_position.deleted = True  # After a split, delete and break
                break

            if beam_position.deleted:
                break

        return beam_positions

    def shine(self,x: int, y: int, beam: Beam):
        beam_positions = [BeamPosition(x, y, beam, self.width, self.height)]

        while len(beam_positions) > 0:
            new_beam_positions = []
            for beam_position in beam_positions:
                new_beam_positions.extend(self._shine(beam_position))
            beam_positions = new_beam_positions
            if self._debug:
                self.print_cave()
                print('')
            pass

    def reset(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_cell(x,y)
                tile.beams = []

    def calculate_score(self):
        total = 0
        for y in range(self.height):
            for x in range(self.width):
                tile = self.get_cell(x,y)
                if len(tile.beams) > 0:
                    total += 1

        return total

    def search_for_optimal_beam(self) -> int:
        max_score = None
        for y in range(0, self.height):
            for x in range(0, self.width):

                if y != 0 and y != self.height-1:
                    if x != 0 and x != self.width-1:
                        continue

                directions = []
                if x == 0:
                    directions.append('E')
                elif x == self.width-1:
                    directions.append('W')

                if y == 0:
                    directions.append('S')
                elif y == self.height-1:
                    directions.append('N')

                for d in directions:
                    self.reset()
                    self.shine(x,y, Beam(d))
                    new_score = self.calculate_score()
                    if max_score is None or new_score > max_score:
                        max_score = new_score

        return max_score

if __name__ == '__main__':
    cave = Cave('sample.txt')
    cave.shine(0,0, Beam('E'))
    cave.print_cave()
    print('')
    cave.print_energized()
    assert(cave.calculate_score() == 46)
    assert(cave.search_for_optimal_beam() == 51)


    cave = Cave('data.txt')
    cave.shine(0,0, Beam('E'))
    print(f'Part 1: {cave.calculate_score()}')
    print(f'Part 2: {cave.search_for_optimal_beam()}')
