import math
import re
from operator import mul
from functools import reduce


def win_range(t: int, record: int) -> list[int, int]:
    """Returns the range of charging times leading to a win"""
    D = t**2 - 4 * record
    if D <= 0:  # zero or one solution
        return []
    r1, r2 = [(t + sign * math.sqrt(D)) / 2 for sign in [-1, 1]]
    # stretch to whole numbers leaving out exactly whole-numbered roots
    if r1 == round(r1):
        r1 = round(r1) + 1
    else:
        r1 = math.ceil(r1)
    if r2 == round(r2):
        r2 = round(r2) - 1
    else:
        r2 = math.floor(r2)

    # no whole-number solution inside the interval
    if r1 > r2:
        return []

    return [r1, r2]


def win_n(wr: list[int, int]) -> int:
    """Returns the number of winning times inside the range"""
    if not wr:
        return 0
    return wr[1] - wr[0] + 1


def read_numbers(text: str) -> list[int]:
    """Returns all numbers from a string as a list of integers"""
    return [int(n) for n in re.findall('[0-9]+', text)]


with open('input.txt') as file:
    lines = file.readlines()

times, distances = map(read_numbers, lines)
# numbers of possible wins in each race
wins = [win_n(win_range(*t_d)) for t_d in zip(times, distances)]
print(f'Part 1: {reduce(mul, wins)}')

# merge times and distances into one number
t2, d2 = map(lambda lst: int(''.join(str(i) for i in lst)), [times, distances])
print(f'Part 2: {win_n(win_range(t2, d2))}')