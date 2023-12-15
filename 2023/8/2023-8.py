import re
import math

with open('input.txt') as file:
    lines = file.readlines()

instructions = [int(i == 'R') for i in lines[0].rstrip()]

nodes = [re.findall('[A-Z]+', line) for line in lines[2:]]
node_names = [n[0] for n in nodes]
left_right = [[node_names.index(l), node_names.index(r)] for _, l, r in nodes]

current = node_names.index('AAA')
LAST = node_names.index('ZZZ')
steps = 0
while current != LAST:
    current = left_right[current][instructions[steps % len(instructions)]]
    steps += 1
print(f'Part 1: {steps}')


current = [node_names.index(n) for n in node_names if re.search('A$', n)]
LAST = set(node_names.index(n) for n in node_names if re.search('Z$', n))


def steps_to_z(current: int) -> int:
    """Finds the number of steps it takes to get to a 'Z' node."""
    # All node sequences actually behave surprisingly well, i.e. they
    # eventually return to the first node and only encounter one 'Z' node
    # during one cycle and even as the last node.
    steps = 0
    while current not in LAST:
        i = steps % len(instructions)
        current = left_right[current][instructions[i]]
        steps += 1
    return steps


to_z = [steps_to_z(c) for c in current]
print(f'Part 2: {math.lcm(*to_z)}')
