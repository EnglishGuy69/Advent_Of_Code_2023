import io

class Race:
    def __init__(self, duration: int, distance: int):
        self.duration = duration
        self.distance = distance

    def calc_winning_combos(self):
        cnt = 0
        for i in range(1, self.duration):
            d = i + (self.duration-(i+1))*i
            print(f'{100.0 * i / self.duration:002f}%', end='\r')
            if d > self.distance:
                cnt += 1

        return cnt


class Races:
    def __init__(self, filename: str):
        self.races = []
        with open(filename, 'r') as f:
            times = [int(t) for t in f.readline().strip().split(':')[1].split(' ') if t != '']
            distances = [int(d) for d in f.readline().strip().split(':')[1].split(' ') if d != '']

            for i, t in enumerate(times):
                race = Race(t, distances[i])
                self.races.append(race)
        pass

    def calculate_combos(self):
        total = 1
        for race in self.races:
            n = race.calc_winning_combos()
            total *= n

        return total

if __name__ == '__main__':
#    r = Races('./sample.txt')
#    r = Races('./sample_2.txt')
#    r = Races('./data.txt')
    r = Races('./data_2.txt')
    print(r.calculate_combos())