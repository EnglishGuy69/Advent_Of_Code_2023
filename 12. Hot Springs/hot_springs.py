import re

class SpringData:
    OPERATIONAL ='.'
    DAMAGED = '#'
    UNDEFINED = '?'

    def __init__(self, data: str, damage_summary:[int], debug=False):
        self.data = data
        self.damage_summary = damage_summary
        self._debug = debug

    def __str__(self):
        return f'{self.data} {",".join(self.damage_summary)}'


    @staticmethod
    def _is_valid(data: str, damage_summary: [int]):
        groups = re.findall(r'[#]+', data)
        if len(groups) != len(damage_summary):
            return False

        for i, group in enumerate(groups):
            if len(group) != damage_summary[i]:
                return False

        return True

    def repair_data(self):
        total_valid_repairs = 0
        num_undefined = len([c for c in self.data if c == SpringData.UNDEFINED])
        initial_num_damaged = len([c for c in self.data if c == SpringData.DAMAGED])
        num_damaged = sum(self.damage_summary)
        required_num_damaged = num_damaged - initial_num_damaged
        for i in range((2**required_num_damaged-1), 2**num_undefined):
            data = self.data
            bin_number = bin(i)[2:]
            bin_number = '0'*(num_undefined - len(bin_number)) + bin_number # prepend '0' to get full number of digits
            total_damaged = initial_num_damaged
            for c in bin_number:
                if c == '0':
                    data = data.replace(SpringData.UNDEFINED,SpringData.OPERATIONAL, 1)
                else:
                    data = data.replace(SpringData.UNDEFINED, SpringData.DAMAGED, 1)
                    total_damaged += 1
                    if total_damaged > num_damaged:
                        break

            if SpringData._is_valid(data, self.damage_summary):
                if self._debug:
                    print(data)
                total_valid_repairs += 1

        return total_valid_repairs

class HotSprings:

    def __init__(self, filename, debug=False):
        self.rows = []
        self._debug=debug

        with open(filename, 'r') as f:
            for row in f.readlines():
                spring_data = row.split()[0]
                summary = [int(n) for n in row.strip().split()[1].split(',')]
                self.rows.append(SpringData(data=spring_data, damage_summary=summary, debug=debug))

    # @staticmethod
    # def validate

    @property
    def height(self):
        return len(self.rows)

    @property
    def width(self):
        return len(len(self.rows[0].data))

    def repair_data(self):
        total_valid_repairs = 0
        for i, row in enumerate(self.rows):
            total_valid_repairs += row.repair_data()
            if i % 100 == 0:
                print(f'{i} of {len(self.rows)}')

        return total_valid_repairs

if __name__ == '__main__':
    # m = re.findall("[#]+","###.##.#")
    # m = re.findall("[#]+","...###.##.#..")

    hs = HotSprings('sample.txt', debug=False)
    total_valid_repairs = hs.repair_data()
    assert(total_valid_repairs == 21)

    hs = HotSprings('data.txt', debug=False)
    total_valid_repairs = hs.repair_data()
    print(f'Part 1: {total_valid_repairs}')


