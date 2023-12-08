import re

with open('input.txt') as file:
    lines = file.readlines()
# list of boolean lists of whether each character is a symbol
is_symbol = [[c not in list(map(str, range(10))) + ['.'] for c in line.rstrip()]
             for line in lines]
m = len(is_symbol)  # no of rows
n = len(is_symbol[0])  # no of columns

is_star = [[c == '*' for c in line.rstrip()]
           for line in lines]
# dictionary of lists to store part numbers adjacent to stars
star_nums = {i * n + j: []
             for i in range(m)
             for j in range(n)
             if lines[i][j] == '*'}


def update_star_nums(num: int, start: int, end: int, line_i: int) -> None:
    # Adds the part number to all the stars to which it is adjacent
    for i in range(max(0, line_i - 1), min(line_i + 2, m-1)):
        for j in range(max(0, start - 1), min(end + 1, n-1)):
            try:
                star_nums[i * n + j].append(num)
            except KeyError:
                pass


def process_part_numbers(text: str, line_i: int) -> list[int]:
    # Identifies (and returns) part numbers and stores them to their adjacent stars
    matches = re.finditer('[0-9]+', text)
    part_ns = []
    for match in matches:
        if has_symbol(*match.span(), line_i):
            num = int(match.group())
            part_ns.append(num)
            update_star_nums(num, *match.span(), line_i)

    return part_ns


def has_symbol(start: int, end: int, line_i: int) -> bool:
    # Is there a symbol around characters `start`--`end` on line `line_i`?
    #   `end` is after the last character, hence `+ 1` (as opposed
    #   to `+ 2` for lines)
    for i in range(max(0, line_i - 1), min(line_i + 2, m-1)):
        for j in range(max(0, start - 1), min(end + 1, n-1)):
            if is_symbol[i][j]:
                return True
    return False


total = 0
for i, line in enumerate(lines):
    total += sum(process_part_numbers(line, i))
print(f'Part 1: {total}')
print(f'Part 2: {sum(sn[0] * sn[1] for sn in star_nums.values() if len(sn) == 2)}')

