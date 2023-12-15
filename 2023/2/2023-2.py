import re
from functools import reduce
from operator import mul

GameType = list[list[int, int, int]]


def color_count(text: str, color: str) -> int:
    """Returns count for the specified color"""
    res = re.search('([0-9]+) ' + color, text)
    if not res:
        return 0
    return int(res.group(1))


def parse_game(text: str) -> GameType:
    # remove game ID
    text = re.sub('^.*: ', '', text)
    # split to sets
    sets = text.split('; ')
    return [[color_count(s, color) for color in ['red', 'green', 'blue']]
            for s in sets]


def game_possible(game: GameType, col_max: tuple[int, int, int] = (12, 13, 14)):
    for col in range(3):
        for s in range(len(game)):
            if game[s][col] > col_max[col]:
                return False
    return True


def game_power(game: GameType) -> int:
    necessary = [max([s[col] for s in game]) for col in range(3)]
    return reduce(mul, necessary)


with open('input.txt', 'r') as file:
    games = file.readlines()
games = [parse_game(g) for g in games]

possible = [game_possible(g) for g in games]
print(f'Part 1: {sum([i for i, pos in enumerate(possible, 1) if pos])}')
print(f'Part 2: {sum([game_power(g) for g in games])}')
