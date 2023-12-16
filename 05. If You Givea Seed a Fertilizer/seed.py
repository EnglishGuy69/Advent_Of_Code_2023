import sys
import os

class SeedRange:
    def __init__(self, seed_range_start: int, seed_range_length: int):
        self.seed_range_start = seed_range_start
        self.seed_range_length =seed_range_length

class RangeMap:
    def __init__(self, target_start:int, source_start:int, range_length):
        self.target_start = target_start
        self.source_start = source_start
        self.range_length = range_length

        s = str(self)
        pass

    @property
    def source_range_start(self):
        return self.source_start

    @property
    def source_range_end(self):
        return self.source_start + self.range_length - 1

    @property
    def target_range_start(self):
        return self.target_start

    @property
    def target_range_end(self):
        return self.target_start + self.range_length - 1

    def __str__(self):
        return f'({self.source_start}-{self.source_range_end} => {self.target_range_start}-{self.target_range_end})'

    def map_source_to_target(self, src: int) -> int:
        if self.source_range_start <= src <= self.source_range_end:
            return self.target_range_start + (src-self.source_range_start)
        else:
            return None


class RangeMaps:
    def __init__(self, map_type: str):
        self.map_type: str = map_type
        self.range_maps:[RangeMap] = []
        self.mru_range_map = None
        self.mru_hits = 0
        self.mru_misses = 0
        self.total_misses = 0

    def add_range_map(self, range_map: RangeMap):
        self.range_maps.append(range_map)

    def map_source_to_target(self, src: int):
        if self.mru_range_map:
            t = self.mru_range_map.map_source_to_target(src)
            if t is not None:
                self.mru_hits += 1
                return t

        for m in self.range_maps:  # type: RangeMap
            t = m.map_source_to_target(src)
            if t is not None:
                self.mru_range_map = m
                self.mru_misses += 1
                return t

        self.total_misses += 1

        return src

    def __str__(self):
        return f'{self.map_type}'


class RangeMapSystem:
    def __init__(self, filename):
        self.seeds = []
        self.range_maps_list:[RangeMaps] = []

        with open(filename, 'r') as f:
            seeds_row = f.readline()
            self._load_seeds(seeds_row.rstrip())
            _ = f.readline()

            range_maps = None
            for row in f.readlines():
                if range_maps == None and row.strip():
                    range_maps = self._create_range_maps(row.rstrip())
                else:
                    if row.strip() == '':
                        self.range_maps_list.append(range_maps)
                        range_maps = None
                    else:
                        range_map = self._create_range_map(row.strip())
                        range_maps.add_range_map(range_map)
            if range_maps:
                self.range_maps_list.append(range_maps)

    def _load_seeds(self, s) -> None:
        seed_pairs = [int(c) for c in s.split(':')[1].strip().split(' ')]
        while len(seed_pairs) > 0:
            start_seed = seed_pairs[0]
            num_seeds = seed_pairs[1]
            self.seeds.append(SeedRange(start_seed, num_seeds))
            seed_pairs = seed_pairs[2:]

    def _create_range_maps(self, s) -> RangeMaps:
        range_maps = RangeMaps(map_type=s.split(' ')[0])
        return range_maps

    def _create_range_map(self, s) -> RangeMap:
        dest_start, src_start, map_length = s.strip().split(' ')
        range_map = RangeMap(target_start=int(dest_start), source_start=int(src_start), range_length=int(map_length))
        return range_map

    def find_location(self, seed_number) -> int:
        n = seed_number
        for range_maps in self.range_maps_list:
            n = range_maps.map_source_to_target(n)

        return n

    # def _get_overlap(self, src_start, src_len, tgt_start, tgt_len) -> int:
    #     src_end = src_start + src_len - 1
    #     tgt_end = tgt_start + tgt_len - 1
    #
    #     # src |-----|
    #     # tgt    *-----|
    #     if src_start <= tgt_start and src_end >= tgt_start:
    #         return tgt_start
    #
    #     # src    *-----|
    #     # tgt |----|
    #     if src_start >= tgt_start and src_start <= src_end:
    #         return src_start

    def _find_nearest_location_step(self, seed_range, seed_start, seed_end, step_size, n_min) -> (int, int):
        n = n_min
        seed_min = seed_start

        if seed_end is None:
            seed_end = seed_range.seed_range_start+seed_range.seed_range_length

        for seed in range(seed_start, seed_end, step_size):
            location = self.find_location(seed)
            if (n is None  or location < n) and location is not None:
                n = min([n, location]) if n is not None else location
                if seed >= seed_start+step_size:
                    seed_min = seed

        return n, seed_min - 32768, seed_min + 32768

    def find_closest_location(self):
        n = None
        seed_to_soil_maps = self.range_maps_list[0]
        for seed_range in self.seeds:  # type: SeedRange
            print(f'Search (n={n or "None"})...')

            step_size = 1024
            seed_start = seed_range.seed_range_start
            seed_end = seed_range.seed_range_start+seed_range.seed_range_length
            while True:
                n, seed_start, seed_end = self._find_nearest_location_step(seed_range = seed_range,
                                                                           seed_start = seed_start,
                                                                           seed_end = seed_end,
                                                                           step_size = step_size,
                                                                           n_min = n)
                if step_size == 1:
                    break
                else:
                    step_size = int(step_size / 2)

        return n



if __name__ == '__main__':
#    system = RangeMapSystem('./sample.txt')
    system = RangeMapSystem('./data.txt')
    closest_location = system.find_closest_location()
    pass