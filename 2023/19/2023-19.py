from operator import gt, lt
from collections import deque
from copy import deepcopy
from functools import reduce
import re


def read_numbers(text: str) -> list[int]:
    """Returns all numbers from a string as a list of integers"""
    return [int(n) for n in re.findall('[0-9]+', text)]


def apply_workflow(part, wf):
    for rule in wf:
        if isinstance(rule, str):  # last rule
            return rule

        xmas, op, n, target = rule
        if op(part[xmas], n):
            return target


with open('input.txt') as file:
    lines = file.read().splitlines()

# read workflows
xmas_to_i = {'x': 0, 'm': 1, 'a': 2, 's': 3}
workflows = dict()
i = 0
while l := lines[i]:
    name, rules = l[:-1].split('{')
    rules = rules.split(',')
    wf = []
    for rule in rules:
        if ':' in rule:
            cond, target = rule.split(':')
            xmas, _, *num = cond
            wf.append([xmas_to_i[xmas], gt if '>' in cond else lt, int(''.join(num)), target])
        else:
            wf.append(rule)
    workflows[name] = wf
    i += 1

i += 1
total = 0
for l in lines[i:]:
    part = read_numbers(l)
    wf = 'in'
    while wf not in ['A', 'R']:
        wf = apply_workflow(part, workflows[wf])
    if wf == 'A':
        total += sum(part)

print(f'Part 1: {total}')

accepted = 0
todo = deque()
todo.append(['in', [[1, 4000] for _ in range(4)]])
while todo:
    wf, ranges = todo.popleft()
    if wf in ['A', 'R']:
        if wf == 'A':
            accepted += reduce(lambda x, y: x * (y[1] - y[0] + 1), ranges, 1)
    else:
        wf = workflows[wf]
        for rule in wf:
            if isinstance(rule, str):
                if rule != 'R':
                    todo.append([rule, ranges])
            else:
                ranges_true = deepcopy(ranges)
                xmas, op, n, target = rule
                if op == gt:
                    ranges_true[xmas][0] = n + 1
                    ranges[xmas][1] = n
                else:
                    ranges_true[xmas][1] = n - 1
                    ranges[xmas][0] = n
                todo.append([target, ranges_true])

print(f'Part 2: {accepted}')



