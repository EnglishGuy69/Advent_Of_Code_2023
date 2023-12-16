
def perform_hash(s: str) -> int:
    h = 0
    for c in s:
        h += ord(c)
        h = (h * 17) % 256

    return h

def calculate(s_list: [str]) -> int:
    total = 0
    for s in s_list:
        total += perform_hash(s)

    return total
def load_file(filename: str) -> [str]:
    s_list = []
    with open(filename, 'r') as f:
        for row in f.readlines():
            s_list += row.strip().split(',')

    return s_list

class Instruction:
    EXCHANGE = '='
    REMOVE = '-'

    def __init__(self, s: str):
        if s.find(Instruction.EXCHANGE) != -1:
            self.label = s.split(Instruction.EXCHANGE)[0]
            self.action = Instruction.EXCHANGE
            self.focal_length = int(s.split(Instruction.EXCHANGE)[1])
            self.box = perform_hash(self.label)
        else:
            self.label = s.split(Instruction.REMOVE)[0]
            self.action = Instruction.REMOVE
            self.focal_length = None
            self.box = perform_hash(self.label)

    def __str__(self):
        return f'[{self.box}] {self.label} {self.action} {self.focal_length or ""}'


class Lens:
    def __init__(self, label: str, focal_length: int):
        self.label=label
        self.focal_length=focal_length

    def __str__(self):
        return f'{self.label} {self.focal_length}'

class LensBoxes:
    def __init__(self, filename):
        self.lens_boxes:[[Lens]] = []

        for i in range(0, 256):
            self.lens_boxes.append([])

        self.instructions = []

        s_list = []
        with open(filename, 'r') as f:
            for row in f.readlines():
                s_list += row.strip().split(',')

        for s in s_list:
            self.instructions.append(Instruction(s))

    def exchange_lens(self, instruction: Instruction):
        assert(instruction.action == Instruction.EXCHANGE)
        box = self.lens_boxes[instruction.box]
        focal_length = instruction.focal_length
        for i, lens in enumerate(box):
            if lens.label == instruction.label:
                box[i] = Lens(lens.label, focal_length)
                return

        box.append(Lens(instruction.label, focal_length))

    def remove_lens(self, instruction: Instruction):
        assert(instruction.action == Instruction.REMOVE)
        box = self.lens_boxes[instruction.box]  # type: [Lens]

        for i, lens in enumerate(box):
            if lens.label == instruction.label:
                box.pop(i)
                break


    def run_instructions(self):
        for instruction in self.instructions:
            if instruction.action == Instruction.EXCHANGE:
                self.exchange_lens(instruction)
            else:
                self.remove_lens(instruction)


    def calculate_score(self):
        score = 0
        for i, box in enumerate(self.lens_boxes):
            for j, lens in enumerate(box):
                score += (i+1) * (j+1) * lens.focal_length

        return score

if __name__ == '__main__':
    assert(perform_hash('HASH') == 52)
    s_list = load_file('sample.txt')
    assert(calculate(s_list) == 1320)

    s_list = load_file('data.txt')
    print(f'Part 1: {calculate(s_list)}')

    # Part 2
    assert(perform_hash('rn') == 0)
    assert(perform_hash('qp') == 1)

    lens_boxes = LensBoxes('sample.txt')
    lens_boxes.run_instructions()
    assert(lens_boxes.calculate_score() == 145)

    lens_boxes = LensBoxes('data.txt')
    lens_boxes.run_instructions()
    print(f'Part 2: {lens_boxes.calculate_score()}')

