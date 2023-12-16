import os
import sys

class HauntedWasteland:
    FIRST_NODE = 'AAA'
    LAST_NODE = 'ZZZ'

    def __init__(self, filename: str):
        with open(filename, 'r') as f:
            self.instructions = f.readline().strip()
            self.nodes = {}

            _ = f.readline()  # skip empty line
            for row in f.readlines():
                start_node = row.split('=')[0].strip()
                left_node, right_node = row.split('(')[1].split(')')[0].split(', ')
                self.nodes[start_node] = (left_node, right_node)

    def steps(self):
        steps = 0
        node = self.nodes[HauntedWasteland.FIRST_NODE]
        p = 0
        while True:
            instruction = self.instructions[p]
            next_node = node[0] if instruction == 'L' else node[1]
            node = self.nodes[next_node]
            p = (p + 1) % len(self.instructions)
            steps += 1
            if next_node == HauntedWasteland.LAST_NODE:
                break
        return steps


if __name__ == '__main__':
    hw = HauntedWasteland('sample.txt')
    assert(hw.steps() == 2)

    hw = HauntedWasteland('sample2.txt')
    assert(hw.steps() == 6)

    hw = HauntedWasteland('data.txt')

    print(hw.steps())