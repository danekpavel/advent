from collections import defaultdict

with open('input.txt') as file:
    lines = file.read().splitlines()

""" naive approach
import re
from itertools import combinations
import numpy as np

def split_into(n: int, into: int) -> list[np.ndarray]:
    combs = list(combinations(range(1, n), into - 1))
    return [np.diff([0] + list(c) + [n]) for c in combs]


def place_dots(n: int, damaged: list[int]) -> list[str]:
    seq = []
    # sequences starting and ending with a dot:  .#.#.
    if n > len(damaged):
        # combs = list(combinations(range(1, n), len(damaged)))
        # combs = [np.diff([0] + list(c) + [n]) for c in combs]
        combs = split_into(n, len(damaged) + 1)
        for c in combs:
            seq.append(''.join('#' * damaged[i // 2] if i % 2 else '.' * c[i // 2]
                               for i in range(2 * len(damaged) + 1)))
    # sequences starting or ending with a dot:  .#.#  or  #.#.
    if n >= len(damaged):
        combs = split_into(n, len(damaged))
        for c in combs:
            #  .#.#
            seq.append(''.join('#' * damaged[i // 2] if i % 2 else '.' * c[i // 2]
                               for i in range(2 * len(damaged))))
            #  #.#.
            seq.append(''.join('#' * damaged[i // 2] if not i % 2 else '.' * c[i // 2]
                               for i in range(2 * len(damaged))))

    # dots only between '#':  #.#
    combs = split_into(n, len(damaged) - 1)
    for c in combs:
        seq.append(''.join('.' * c[i // 2] if i % 2 else '#' * damaged[i // 2]
                           for i in range(2 * len(damaged) - 1)))

    return seq


 
total = 0
for l in lines[1:2]:
    conditions, damaged = l.split()
    damaged = list(map(int, damaged.split(',')))
    conditions *= 3
    damaged *= 3
    print(conditions, damaged)
    adepts = place_dots(len(conditions) - sum(damaged), damaged)
    regex = re.sub('\\.', '\\.', conditions)
    regex = re.sub('\\?', '.', regex)
    total += sum(bool(re.fullmatch(regex, a)) for a in adepts)
print(total)
"""


def place_from(g: int, start: int) -> int:
    """Tries placing the group of damaged springs (`g`), starting from `at`"""

    if group_sol_from[g][start] is not None:
        return group_sol_from[g][start]

    solutions = 0
    after = start + groups[g]
    # not enough space
    if after > n:
        pass
    else:
        # wrong characters where group would be placed  OR
        # wrong character after the group
        if (any(conditions[i] == '.' for i in range(start, after)) or
                after < n and conditions[after] == '#'):
            pass
        else:
            if g == len(groups) - 1:
                # check there is no unused '#' left
                if all(conditions[i] != '#' for i in range(after, n)):
                    solutions = 1
            else:
                solutions = place_from(g + 1, after + 1)
        # don't continue when '#' is encountered
        if conditions[start] != '#':
            solutions += place_from(g, start + 1)

    group_sol_from[g][start] = solutions
    return solutions

total_first = 0
total_second = 0
for l in lines:
    conditions, groups = l.split()
    groups = list(map(int, groups.split(',')))

    for first in True, False:
        if not first:
            conditions = '?'.join([conditions] * 5)
            groups *= 5
        # group_sol_from[g][i]: number of solutions when group `g` is placed
        #   at `i` or further
        group_sol_from: list[defaultdict[int]] = \
            [defaultdict(lambda: None) for _ in range(len(groups))]
        n = len(conditions)
        solution = place_from(0, 0)
        if first:
            total_first += solution
        else:
            total_second += solution

print(f'Part 1: {total_first}')
print(f'Part 2: {total_second}')
