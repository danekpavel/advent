import re
import numpy as np


def read_numbers(text: str) -> list[int]:
    """Returns all numbers from a string as a list of integers"""
    return [int(n) for n in re.findall('-?[0-9]+', text)]


with open('input.txt') as file:
    lines = file.readlines()

histories = [read_numbers(l) for l in lines]

total_end = 0
total_start = 0
for h in histories:
    h = np.array(h, dtype=np.int64)
    sign = 1
    while np.any(h):
        total_end += h[-1]
        total_start += sign * h[0]
        h = np.diff(h)
        sign *= -1

print(f'Part 1: {total_end}')
print(f'Part 2: {total_start}')

