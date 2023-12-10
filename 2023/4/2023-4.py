import re


def parse_numbers(line: str) -> tuple[list[int], list[int]]:
    win_my = re.sub('.*:', '', line).split('|')
    return tuple(re.findall('[0-9]+', one) for one in win_my)


def n_winning(win_my: tuple[list[int], list[int]]) -> int:
    return len(set(win_my[0]) & set(win_my[1]))


def points(n_win: int) -> int:
    if n_win:
        return pow(2, n_win - 1)
    return 0


with open('input.txt') as file:
    lines = file.readlines()

cards_win = [n_winning(parse_numbers(line)) for line in lines]
print(f'Part 1: {sum(points(win) for win in cards_win)}')

cards_n = [1] * len(lines)
for i in range(len(cards_n)):
    for j in range(cards_win[i]):
        cards_n[i + j + 1] += cards_n[i]
print(f'Part 2: {sum(cards_n)}')




