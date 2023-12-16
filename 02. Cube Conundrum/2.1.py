
class Cube:
    def __init__(self, color):
        self.color = color


class CubeGroup:
    def __init__(self):
        self.group = {}

    def __str__(self):
        s = ', '.join([f'{g}:{self.group[g]}' for g in self.group.keys()])
        return s

    def add_group(self, color:str, count:int):
        self.group[color] = count

    def is_game_possible(self, color:str, count:int):
        if color in self.group and self.group[color] > count:
            return False
        else:
            return True

class Game:
    def __init__(self, id:int):
        self.id:int = id
        self.groups = []

    def __str__(self):
        return f'{self.id} ({len(self.groups)} groups)'

    def add_group(self, group:CubeGroup):
        self.groups.append(group)

    def is_game_possible(self, check_game:[(str,int)]):
        for group in self.groups:  #type: CubeGroup
            for (color, count) in check_game:
                if not group.is_game_possible(color, count):
                    return False

        return True

    def calc_power(self) -> int:
        min_cubes = {}
        for group in self.groups:  # type: CubeGroup
            for color in group.group.keys():
                if color not in min_cubes:
                    min_cubes[color] = group.group[color]
                elif group.group[color] > min_cubes[color]:
                    min_cubes[color] = group.group[color]

        power_total = 1
        for color in min_cubes.keys():
            power_total *= min_cubes[color]

        return power_total

class Games:
    def __init__(self, filename):
        self.games = []

        with open(filename, 'r') as f:
            for row in f.readlines():
                game_data = row.rstrip().split(':')
                game_id = int(game_data[0].split(' ')[1])
                game = Game(game_id)
                self.games.append(game)
                game_rounds = game_data[1].split(';')
                for game_round in game_rounds:
                    cube_data = game_round.split(',')
                    cube_group = CubeGroup()
                    for cube_datum in cube_data:
                        color_count = cube_datum.strip().split(' ')
                        cube_group.add_group(color_count[1], int(color_count[0]))
                    game.add_group(cube_group)

    def possible_games(self, check_games: []):
        games = []
        for game in self.games:  # type: Game
            if game.is_game_possible(check_games):
                games.append(game)

        return games

    def power_total(self) -> int:
        power_total = 0
        for game in self.games:
            power_total += game.calc_power()

        return power_total

if __name__ == '__main__':
    def sample_1():
        games = Games('sample-1.txt')
        check_games = [('red', 12),('green', 13),('blue', 14)]
        total_possible_games = sum([g.id for g in games.possible_games(check_games)])
        assert(total_possible_games == 8)
        assert(games.power_total() == 2286)

    def test_1():
        games = Games('data-1.txt')
        check_games = [('red', 12),('green', 13),('blue', 14)]
        total_possible_games = sum([g.id for g in games.possible_games(check_games)])
        print(f'Total Possible Games: {total_possible_games}')
        print(f'Power Total: {games.power_total()}')


    sample_1()
    test_1()