from copy import deepcopy

with open('input.txt') as file:
    layout = file.read().splitlines()
M = len(layout)
N = len(layout[0])


def energize_it(i_start: int, j_start: int, horiz_start: bool, vec_start: -1|1):
    energized = [[False for _ in range(N)] for __ in range(M)]
    # for storing whether a beam of a given direction has been in a tile
    visit_hor_plus = deepcopy(energized)
    visit_hor_minus = deepcopy(energized)
    visit_ver_plus = deepcopy(energized)
    visit_ver_minus = deepcopy(energized)

    i_next = [i_start]
    j_next = [j_start]
    horiz_next = [horiz_start]
    # vec: 1: right/down, -1: left/up
    vec_next = [vec_start]

    while i_next:
        i = i_next.pop()
        j = j_next.pop()
        horiz = horiz_next.pop()
        vec = vec_next.pop()

        energized[i][j] = True

        if horiz:
            if vec == 1:
                if visit_hor_plus[i][j]:
                    continue
                visit_hor_plus[i][j] = True
            else:
                if visit_hor_minus[i][j]:
                    continue
                visit_hor_minus[i][j] = True
        else:
            if vec == 1:
                if visit_ver_plus[i][j]:
                    continue
                visit_ver_plus[i][j] = True
            else:
                if visit_ver_minus[i][j]:
                    continue
                visit_ver_minus[i][j] = True

        i_new = [i]
        j_new = [j]
        vec_new = [vec]

        match layout[i][j]:
            case '.':
                if horiz:
                    j_new = [j + vec]
                else:
                    i_new = [i + vec]
            case '/':
                if horiz:
                    i_new = [i - vec]
                else:
                    j_new = [j - vec]
                vec_new = [-vec]
                horiz = not horiz
            case '\\':
                if horiz:
                    i_new = [i + vec]
                else:
                    j_new = [j + vec]
                vec_new = [vec]
                horiz = not horiz
            case '|':
                if horiz:
                    i_new = [i - 1, i + 1]
                    j_new = [j, j]
                    vec_new = [-1, 1]
                    horiz = False
                else:
                    i_new = [i + vec]
            case '-':
                if horiz:
                    j_new = [j + vec]
                else:
                    i_new = [i, i]
                    j_new = [j - 1, j + 1]
                    vec_new = [-1, 1]
                    horiz = True

        for _i, _j, v in zip(i_new, j_new, vec_new):
            if 0 <= _i < M and 0 <= _j < N:
                i_next.append(_i)
                j_next.append(_j)
                vec_next.append(v)
                horiz_next.append(horiz)

    # print('\n'.join(''.join('#' if r else '.' for r in row) for row in energized))
    return sum(sum(x for x in row) for row in energized)


energ_max = 0

for j in range(N):
    # top row
    ei = energize_it(0, j, False, 1)
    # bottom row
    energ_max = max(energ_max, ei)
    ei = energize_it(M - 1, j, False, -1)
    energ_max = max(energ_max, ei)

for i in range(M):
    # left side
    ei = energize_it(i, 0, True, 1)
    energ_max = max(energ_max, ei)
    # right side
    ei = energize_it(i, N - 1, False, -1)
    energ_max = max(energ_max, ei)

print(energ_max)