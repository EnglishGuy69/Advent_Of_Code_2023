import os
import sys
import math

class NodeVisit:
    def __init__(self, node_key: str, step_number: int, instruction_number: int):
        self.step_number = step_number
        self.instruction_number = instruction_number
        self.node_key = node_key

    def __str__(self):
        return f'{self.node_key} - Step {self.step_number} - Instruction: {self.instruction_number}'

class Node:
    def __init__(self, node_key: str):
        self.node_key = node_key
        self.node_visits:[NodeVisit] = []
        self.repeating = False
        self.repeating_period = 0

    def add_node_visit(self, node_visit: NodeVisit):
        o: NodeVisit
        existing_node = [o for o in self.node_visits \
                         if o.node_key == node_visit.node_key \
                         and o.instruction_number == node_visit.instruction_number ]

        self.node_visits.append(node_visit)

        if len(existing_node) > 0:
            self.repeating = True
            self.repeating_period = self.node_visits[-1].step_number - self.node_visits[-2].step_number

    def __str__(self):
        return f'{self.node_key} ({len(self.node_visits)}{"- Repeating" if self.repeating else ""})'

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

    def get_starting_positions(self):
        return [n for n in list(self.nodes) if n[2] == 'A']

    def calc_answer(self, node_visits: [Node]):
        repeating_periods = [o.repeating_period for o in node_visits if o.repeating]
        if len(repeating_periods) < len(node_visits):
            return None

        from math import gcd
        lcm = 1
        for i in repeating_periods:
            lcm = lcm * i // gcd(lcm, i)

        return lcm

    def steps(self):
        node_keys = self.get_starting_positions()
        node_visits = [Node(k) for k in node_keys]

        steps = 0
        p = 0
        while True:
            instruction = self.instructions[p]
            for i, node_key in enumerate(node_keys):
                node = self.nodes[node_key]
                next_node_key = node[0] if instruction == 'L' else node[1]
                node_keys[i] = next_node_key

                if next_node_key[2] == 'Z':
                    node_visits[i].add_node_visit(NodeVisit(next_node_key, steps, p))

            p = (p + 1) % len(self.instructions)
            steps += 1

            num_ending_in_z = 0
            for i in range(0, len(node_keys)):
                if node_keys[i][2] != 'Z':
                    break
                num_ending_in_z += 1

            if num_ending_in_z == len(node_keys):
                break

            answer = self.calc_answer(node_visits)
            if answer:
                return answer

            if steps % 100000 == 0:
                print(f'{steps} - {str(node_keys)} ({num_ending_in_z})', end='\r')
        return steps


if __name__ == '__main__':
    # hw = HauntedWasteland('sample3.txt')
    # assert(hw.steps() == 6)

    hw = HauntedWasteland('data.txt')

    print(hw.steps())